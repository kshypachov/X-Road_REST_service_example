# HTTPS Configuration

This section describes how to configure Nginx as a reverse proxy to forward client requests to the REST service.

Nginx will act as an intermediary between the client and the service. To secure the traffic, a self-signed SSL certificate will be used.

## General Prerequisites

Before configuring Nginx, ensure that the following components are installed on the server hosting the web service:

| Software | Version   | Notes                             |
|:---------|:---------:|------------------------------------|
| Nginx    | **1.18+** |                                    |
| OpenSSL  |           | For generating SSL certificates    |

## Installing Nginx

1. Update the package list:
   ```bash
   sudo apt update
   ```

2. Install Nginx:
   ```bash
   sudo apt install nginx
   ```

## Configuring Nginx as a Reverse Proxy

1. Navigate to the configuration directory:
   ```bash
   cd /etc/nginx/sites-available
   ```

2. Create a new configuration file for the REST service, e.g., `rest_service`:
   ```bash
   sudo nano /etc/nginx/sites-available/rest_service
   ```

3. Add the following reverse proxy configuration:
   ```nginx
   server {
       listen 80;
       server_name _;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }

   server {
       listen 443 ssl;
       server_name _;

       ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
       ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. Create a symbolic link to the configuration in the `sites-enabled` directory:
   ```bash
   sudo ln -s /etc/nginx/sites-available/rest_service /etc/nginx/sites-enabled/
   ```

5. Ensure the symbolic link was created correctly:
   ```bash
   ls -l /etc/nginx/sites-enabled/
   ```

6. Remove the default symbolic link from `/etc/nginx/sites-enabled`:
   ```bash
   sudo rm /etc/nginx/sites-enabled/default
   ```

## Generating a Self-Signed SSL Certificate

Generate an SSL certificate and private key using the following command:
```bash
sudo openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -days 3650 -nodes
```

During generation, you will be prompted to enter some information (e.g., country, organization, domain). For testing purposes, you can use arbitrary values.

## Validating the Configuration

To verify that the Nginx configuration is correct, run:

```bash
sudo nginx -t
```

If the configuration is valid, you will see messages like `syntax is ok` and `test is successful`.

## Restarting Nginx

After making changes, restart Nginx:

```bash
sudo systemctl restart nginx
```

---

Materials created with support from the EU Technical Assistance Project "Bangladesh e-governance (BGD)".