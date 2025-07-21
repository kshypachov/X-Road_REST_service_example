import configparser
import os
import logging
from dataclasses import dataclass
from typing import Optional

# OpenTelemetry imports are optional; import lazily to avoid hard dependency when disabled
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased, ParentBased
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.pymysql import PyMySQLInstrumentor

# Optional instrumentation targets
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
except ImportError:  # FastAPI may not be installed in all envs
    FastAPIInstrumentor = None

try:
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
except ImportError:
    RequestsInstrumentor = None

try:
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
except ImportError:
    HTTPXClientInstrumentor = None


# Create a logger instance
logger = logging.getLogger(__name__)


# Function to load configuration file
def load_config(file_path: str, defaults: dict = None) -> configparser.ConfigParser:
    config = configparser.ConfigParser(defaults=defaults, interpolation=None)

    # Check USE_ENV_CONFIG; if true, skip loading config file
    if os.getenv("USE_ENV_CONFIG", "false").lower() == "true":
        logger.info("Skipping config file loading, using environment variables only.")
    else:
        # Load config file only if USE_ENV_CONFIG is not true
        if not config.read(file_path):
            logger.error(f"Configuration file {file_path} not found or is empty.")
            raise FileNotFoundError(f"Configuration file {file_path} not found or is empty.")

    return config


# Function to retrieve configuration parameter from file or environment variable
def get_config_param(config: configparser.ConfigParser, section: str, param: str, env_var: str = None, default: str = None) -> str:
    # If only environment variables are used
    if os.getenv("USE_ENV_CONFIG", "false").lower() == "true":
        env_value = os.getenv(env_var)
        if env_var and env_value is not None:
            return env_value
        else:
            return default  # Return default if env variable is not present

    # If using config file
    if config.has_option(section, param):
        return config.get(section, param)
    else:
        return default  # Return default if param not found in config


# Function to construct the database connection URL
def get_database_url(config: configparser.ConfigParser) -> str:
    db_user = get_config_param(config, 'database', 'username', 'DB_USER')
    db_password = get_config_param(config, 'database', 'password', 'DB_PASSWORD')
    db_host = get_config_param(config, 'database', 'host', 'DB_HOST')
    db_name = get_config_param(config, 'database', 'name', 'DB_NAME')

    missing_params = []
    if db_user is None:
        missing_params.append("DB_USER")
    if db_password is None:
        missing_params.append("DB_PASSWORD")
    if db_host is None:
        missing_params.append("DB_HOST")
    if db_name is None:
        missing_params.append("DB_NAME")

    if missing_params:
        missing_params_str = ", ".join(missing_params)
        logger.error(f"The following database connection parameters are missing: {missing_params_str}")
        raise ValueError(f"Missing database connection parameters: {missing_params_str}")

    return f"mysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"


# Function to configure logging
def configure_logging(config: configparser.ConfigParser):
    log_filename = get_config_param(config, 'logging', 'filename', 'LOG_FILENAME', default=None)
    log_filemode = get_config_param(config, 'logging', 'filemode', 'LOG_FILEMODE', default=None)
    log_format = get_config_param(config, 'logging', 'format', 'LOG_FORMAT', default=None)
    log_datefmt = get_config_param(config, 'logging', 'dateformat', 'LOG_DATEFORMAT', default=None)
    log_level = get_config_param(config, 'logging', 'level', 'LOG_LEVEL', default="info").upper()

    # If log_filename is empty, logs will be output to console (stdout)
    if not log_filename:
        log_filename = None

    logging.basicConfig(
        filename=log_filename,  # If None, logs will be written to stdout
        filemode=log_filemode,
        format=log_format,
        datefmt=log_datefmt,
        level=getattr(logging, log_level, logging.DEBUG)
    )

# ---------------------------------------------------------------------------
# OpenTelemetry Support
# ---------------------------------------------------------------------------

@dataclass
class TelemetrySettings:
    enabled: bool
    service_name: str
    endpoint: str
    sample_ratio: float  # 0.0 - 1.0
    insecure: bool = True              # mTLS off -> True
    parent_based: bool = True          # use ParentBased wrapper
    instrument_requests: bool = True   # outgoing http via requests
    instrument_httpx: bool = True      # outgoing http via httpx
    instrument_fastapi: bool = True    # incoming FastAPI routes


def _getbool(v: Optional[str], default: bool = False) -> bool:
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "on")


def _getfloat(v: Optional[str], default: float = 1.0) -> float:
    if v is None:
        return default
    try:
        return float(v)
    except ValueError:
        logger.warning("Invalid float value '%s', falling back to %s.", v, default)
        return default


def load_telemetry_settings(config: configparser.ConfigParser) -> TelemetrySettings:
    """
    Build TelemetrySettings from config/env.
    INI section: [open-telemetry]
      enabled = true|false
      own-service-name = my-service
      endpoint = http://otel-collector:4317
      sample_ratio = 0.1
      insecure = true|false
      parent_based = true|false
      instrument_requests = true|false
      instrument_httpx = false|true
      instrument_fastapi = true|false
    Env overrides (if USE_ENV_CONFIG=true):
      OTEL_ENABLED, OTEL_SERVICE_NAME, OTEL_ENDPOINT, OTEL_SAMPLE_RATIO, OTEL_INSECURE, ...
    """
    enabled_str = get_config_param(config, 'open-telemetry', 'enabled', 'OTEL_ENABLED', default="false")
    svc_name = get_config_param(config, 'open-telemetry', 'own-service-name', 'OTEL_SERVICE_NAME', default="app")
    endpoint = get_config_param(config, 'open-telemetry', 'endpoint', 'OTEL_ENDPOINT', default="http://localhost:4317")
    ratio_str = get_config_param(config, 'open-telemetry', 'sample_ratio', 'OTEL_SAMPLE_RATIO', default="1.0")
    insecure_str = get_config_param(config, 'open-telemetry', 'insecure', 'OTEL_INSECURE', default="true")
    parent_str = get_config_param(config, 'open-telemetry', 'parent_based', 'OTEL_PARENT_BASED', default="true")
    inst_req_str = get_config_param(config, 'open-telemetry', 'instrument_requests', 'OTEL_INSTRUMENT_REQUESTS', default="true")
    inst_httpx_str = get_config_param(config, 'open-telemetry', 'instrument_httpx', 'OTEL_INSTRUMENT_HTTPX', default="false")
    inst_fapi_str = get_config_param(config, 'open-telemetry', 'instrument_fastapi', 'OTEL_INSTRUMENT_FASTAPI', default="true")

    settings = TelemetrySettings(
        enabled=_getbool(enabled_str, False),
        service_name=svc_name,
        endpoint=endpoint,
        sample_ratio=_getfloat(ratio_str, 1.0),
        insecure=_getbool(insecure_str, True),
        parent_based=_getbool(parent_str, True),
        instrument_requests=_getbool(inst_req_str, True),
        instrument_httpx=_getbool(inst_httpx_str, False),
        instrument_fastapi=_getbool(inst_fapi_str, True),
    )
    return settings


def configure_telemetry(settings: TelemetrySettings) -> None:
    """
    Initialize the global tracer provider + exporter + sampler.
    Safe to call multiple times (subsequent calls will log & return).
    """
    if not settings.enabled:
        logger.info("Telemetry disabled; skipping OpenTelemetry initialization.")
        return

    # Detect if already configured (avoid duplicate providers)
    provider = trace.get_tracer_provider()
    if isinstance(provider, TracerProvider):
        # Heuristic: if a TracerProvider is already set and has processors, assume configured
        if getattr(provider, "_active_span_processor", None):
            logger.debug("TracerProvider already configured; skipping re-init.")
            return

    # Build sampler
    base_sampler = TraceIdRatioBased(settings.sample_ratio)
    sampler = ParentBased(base_sampler) if settings.parent_based else base_sampler

    # Create provider with service resource
    provider = TracerProvider(
        sampler=sampler,
        resource=Resource.create({SERVICE_NAME: settings.service_name}),
    )
    trace.set_tracer_provider(provider)

    # Exporter (OTLP gRPC)
    exporter = OTLPSpanExporter(
        endpoint=settings.endpoint,
        insecure=settings.insecure,
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))
    logger.info(
        "OpenTelemetry tracing initialized: service=%s endpoint=%s sample_ratio=%s parent_based=%s",
        settings.service_name,
        settings.endpoint,
        settings.sample_ratio,
        settings.parent_based,
    )


def instrument_app_with_telemetry(app, settings: TelemetrySettings) -> None:
    """
    Instrument FastAPI app + outbound HTTP clients conditionally.
    Call after `configure_telemetry(settings)` and after app object exists.
    """
    if not settings.enabled:
        logger.info("Telemetry disabled in config")
        return
    logger.info("Telemetry enabled in config")

    # Instrument inbound FastAPI routes
    if settings.instrument_fastapi and FastAPIInstrumentor is not None:
        try:
            FastAPIInstrumentor.instrument_app(app)
            logger.info("FastAPI instrumentation enabled.")
        except Exception as e:
            logger.exception("Failed to instrument FastAPI: %s", e)

    # Instrument outbound requests (requests library)
    if settings.instrument_requests and RequestsInstrumentor is not None:
        try:
            RequestsInstrumentor().instrument()
            logger.info("Requests instrumentation enabled.")
        except Exception as e:
            logger.exception("Failed to instrument requests: %s", e)

    # Instrument outbound httpx (more detailed telemetry; optional)
    if settings.instrument_httpx and HTTPXClientInstrumentor is not None:
        try:
            HTTPXClientInstrumentor().instrument()
            logger.info("HTTPX instrumentation enabled.")
        except Exception as e:
            logger.exception("Failed to instrument httpx: %s", e)

    PyMySQLInstrumentor().instrument()