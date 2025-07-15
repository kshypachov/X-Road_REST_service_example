# Service Usage

### **Person Post**

Creates a single database record for a person.

| HTTP Method | Service Code | Base URL                                                               |
| ----------- | ------------ | ---------------------------------------------------------------------- |
| POST        | Person Post  | [http://your-server-ip:8000/person](http://your-server-ip:8000/person) |

#### Request Body:

```json
{
  "name": "Марина",
  "surname": "Петренко",
  "patronym": "Петрівна",
  "dateOfBirth": "2024-10-11",
  "gender": "female",
  "rnokpp": "1111111111",
  "passportNumber": "123456789",
  "unzr": "20241011-12345"
}
```

#### Parameter Description:

| Nesting Level | Parameter Name | Data Type              | Description                                                                                                 | Required |
| ------------- | -------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------- | -------- |
| 1             | name           | String, min=1, max=128 | First name                                                                                                  | Yes      |
| 1             | surname        | String, min=1, max=128 | Last name                                                                                                   | Yes      |
| 1             | patronym       | String, min=0, max=128 | Middle name                                                                                                 | No       |
| 1             | dateOfBirth    | String                 | Date of birth                                                                                               | Yes      |
| 1             | gender         | String                 | Gender                                                                                                      | Yes      |
| 1             | rnokpp         | String                 | RNOKPP, 10 digits                                                                                           | Yes      |
| 1             | passportNumber | String                 | Passport number. **Old format**: 2 Cyrillic letters, space, 6 digits. **New format**: 9 digits              | Yes      |
| 1             | unzr           | String                 | UNZR, 14 characters in format YYYYMMDD-XXXXC, where YYYY is year, MM is month, DD is day, XXXXC is 5 digits | Yes      |

#### Example curl request:

```bash
curl -X 'POST' \
  'http://your-server-ip:8000/person' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"name": "Марина", "surname": "Петренко", "patronym": "Петрівна", "dateOfBirth": "2024-10-11", "gender": "female", "rnokpp": "1111111111", "passportNumber": "123456789", "unzr": "20241011-12345"}'
```

#### Success Response (HTTP Code 200):

```json
{
  "message": {
    "id": 2
  }
}
```

| Nesting Level | Parameter Name | Data Type | Description              | Required |
| ------------- | -------------- | --------- | ------------------------ | -------- |
| 1             | message        | Object    | Result data object       | Yes      |
| 2             | id             | Integer   | ID of the created record | Yes      |

#### Validation Error Response (HTTP Code 422):

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "rnokpp"],
      "msg": "Value error, RNOKPP must be a 10 digit number",
      "input": "11111111312",
      "ctx": {
        "error": {}
      }
    }
  ]
}
```

#### Bad Request Response (HTTP Code 400):

```json
{
  "detail": "Data integrity error"
}
```

---

### **Person Get All**

Returns all records from the database.

| HTTP Method | Service Code   | Base URL                                                               |
| ----------- | -------------- | ---------------------------------------------------------------------- |
| GET         | Person Get All | [http://your-server-ip:8000/person](http://your-server-ip:8000/person) |


#### Example curl request:

```bash
curl -X 'GET' \
  'http://your-server-ip:8000/person' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json'
```

#### Success Response (HTTP Code 200):

```json
{
  "message": [
    {
      "id": 1,
      "name": "Марина",
      "surname": "Петренко",
      "patronym": "Петрівна",
      "dateOfBirth": "2024-10-44",
      "gender": "female",
      "rnokpp": "1111111111",
      "passportNumber": "123456789",
      "unzr": "20241011-12345"
    },
    {
      "id": 2,
      "name": "Карен",
      "surname": "Симоненко",
      "patronym": "Олегович",
      "dateOfBirth": "2017-12-22",
      "gender": "male",
      "rnokpp": "1111111131",
      "passportNumber": "133456789",
      "unzr": "201712022-12445"
    }
  ]
}
```

#### Error Response (HTTP Code 404):

```json
{
  "detail": "Person not found"
}
```

---
Materials created with support from the EU Technical Assistance Project "Bangladesh e-governance (BGD)".