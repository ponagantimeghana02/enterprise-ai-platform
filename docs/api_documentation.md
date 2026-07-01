# Enterprise AI Platform API Documentation

**Version:** 1.0.0

**Framework:** FastAPI

**Documentation:** Swagger / OpenAPI

---

# Overview

The Enterprise AI Platform provides REST APIs for authentication, user management, AI chat, Retrieval-Augmented Generation (RAG), AI agents, audit logging, and system settings.

All APIs return JSON responses.

Base URL

```
http://localhost:8000
```

Production Example

```
https://api.company.com
```

---

# Authentication

Most APIs require JWT Authentication.

Include the access token in every request.

```
Authorization: Bearer <access_token>
```

---

# Standard Response Format

## Success

```json
{
    "success": true,
    "message": "Operation successful",
    "data": {}
}
```

## Error

```json
{
    "success": false,
    "message": "Invalid credentials",
    "errors": []
}
```

---

# HTTP Status Codes

| Code | Meaning |
|------|----------|
|200|Success|
|201|Created|
|204|No Content|
|400|Bad Request|
|401|Unauthorized|
|403|Forbidden|
|404|Not Found|
|409|Conflict|
|422|Validation Error|
|500|Internal Server Error|

---

# Authentication APIs

---

## Login

**Endpoint**

```
POST /auth/login
```

### Description

Authenticates the user and returns JWT access and refresh tokens.

### Request

```json
{
    "email":"admin@company.com",
    "password":"Password123"
}
```

### Success Response

```json
{
    "access_token":"jwt_access_token",
    "refresh_token":"jwt_refresh_token",
    "token_type":"Bearer",
    "expires_in":3600
}
```

### Error Response

```json
{
    "detail":"Invalid email or password"
}
```

### Status Codes

|Code|Description|
|----|-----------|
|200|Login Successful|
|400|Validation Error|
|401|Invalid Credentials|
|500|Internal Server Error|

---

## Logout

**Endpoint**

```
POST /auth/logout
```

### Description

Invalidates the current refresh token.

### Request Header

```
Authorization: Bearer JWT_TOKEN
```

### Response

```json
{
    "message":"Logged out successfully"
}
```

### Status Codes

|Code|Description|
|----|-----------|
|200|Logout Successful|
|401|Unauthorized|

---

## Refresh Token

**Endpoint**

```
POST /auth/refresh-token
```

### Description

Generates a new access token using the refresh token.

### Request

```json
{
    "refresh_token":"your_refresh_token"
}
```

### Response

```json
{
    "access_token":"new_access_token",
    "expires_in":3600
}
```

### Status Codes

|Code|Description|
|----|-----------|
|200|Success|
|401|Invalid Refresh Token|

---

# User APIs

---

## Create User

**Endpoint**

```
POST /users
```

### Description

Creates a new user.

### Roles Allowed

- Admin
- HR

### Request

```json
{
    "name":"John Doe",
    "email":"john@company.com",
    "password":"Password123",
    "role":"Employee"
}
```

### Response

```json
{
    "id":15,
    "name":"John Doe",
    "email":"john@company.com",
    "role":"Employee",
    "created_at":"2026-06-30T15:00:00"
}
```

### Error Codes

|Code|Meaning|
|----|--------|
|201|Created|
|400|Invalid Request|
|401|Unauthorized|
|403|Permission Denied|
|409|Email Already Exists|

---

## Get All Users

**Endpoint**

```
GET /users
```

### Description

Returns all registered users.

### Authorization

Admin

HR

### Response

```json
[
    {
        "id":1,
        "name":"Admin",
        "email":"admin@company.com",
        "role":"Admin"
    }
]
```

### Status Codes

|Code|Meaning|
|----|--------|
|200|Success|
|401|Unauthorized|
|403|Forbidden|

---

## Get User By ID

**Endpoint**

```
GET /users/{id}
```

### Description

Returns details of a specific user.

### Response

```json
{
    "id":10,
    "name":"Alice",
    "email":"alice@company.com",
    "role":"Manager"
}
```

### Status Codes

|Code|Meaning|
|----|--------|
|200|Success|
|404|User Not Found|

---

## Update User

**Endpoint**

```
PUT /users/{id}
```

### Request

```json
{
    "name":"Alice Johnson",
    "role":"Manager"
}
```

### Response

```json
{
    "message":"User updated successfully"
}
```

---

## Delete User

**Endpoint**

```
DELETE /users/{id}
```

### Response

```json
{
    "message":"User deleted successfully"
}
```

### Status Codes

|Code|Meaning|
|----|--------|
|200|Deleted|
|404|User Not Found|
|403|Permission Denied|

---

# Swagger / OpenAPI Configuration

FastAPI automatically generates interactive API documentation.

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

OpenAPI JSON

```
http://localhost:8000/openapi.json
```

Example FastAPI Configuration

```python
from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Platform API",
    version="1.0.0",
    description="REST APIs for Enterprise AI Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
```

---

---

# Chat APIs

The Chat module provides conversational AI capabilities using LLMs.

---

## Send Chat Message

**Endpoint**

```
POST /chat
```

### Description

Sends a user prompt to the AI model and returns the generated response.

### Authorization

- Admin
- HR
- Manager
- Employee
- Support

### Request

```json
{
    "message": "Explain JWT Authentication.",
    "conversation_id": "123456"
}
```

### Success Response

```json
{
    "conversation_id": "123456",
    "response": "JWT (JSON Web Token) is an authentication token...",
    "timestamp": "2026-07-01T11:15:00"
}
```

### Error Response

```json
{
    "detail":"Prompt cannot be empty."
}
```

### Status Codes

|Code|Meaning|
|----|--------|
|200|Response Generated|
|400|Invalid Request|
|401|Unauthorized|
|500|Internal Server Error|

---

## Chat History

**Endpoint**

```
GET /chat/history/{conversation_id}
```

### Description

Returns the complete conversation history.

### Response

```json
[
  {
    "role":"user",
    "message":"What is FastAPI?"
  },
  {
    "role":"assistant",
    "message":"FastAPI is a modern Python framework..."
  }
]
```

### Status Codes

|Code|Meaning|
|----|--------|
|200|Success|
|404|Conversation Not Found|

---

## Delete Conversation

**Endpoint**

```
DELETE /chat/history/{conversation_id}
```

### Response

```json
{
    "message":"Conversation deleted successfully."
}
```

---

# RAG APIs (Retrieval-Augmented Generation)

The RAG module allows uploading documents and querying them using AI.

---

## Upload Document

**Endpoint**

```
POST /rag/upload
```

### Description

Uploads a document into the vector database.

### Supported Formats

- PDF
- DOCX
- TXT
- CSV

### Request

Multipart Form Data

```
document=file.pdf
```

### Response

```json
{
    "document_id":"98765",
    "status":"Uploaded Successfully"
}
```

### Status Codes

|Code|Meaning|
|----|--------|
|201|Uploaded|
|400|Unsupported File|
|413|File Too Large|

---

## Ask Question

**Endpoint**

```
POST /rag/query
```

### Description

Searches uploaded documents and generates an AI response.

### Request

```json
{
    "question":"What is RBAC?"
}
```

### Response

```json
{
    "answer":"Role-Based Access Control (RBAC)...",
    "sources":[
        "Employee Handbook.pdf"
    ]
}
```

### Status Codes

|Code|Meaning|
|----|--------|
|200|Success|
|404|No Relevant Documents|

---

## List Uploaded Documents

**Endpoint**

```
GET /rag/documents
```

### Response

```json
[
    {
        "id":"1",
        "filename":"HRPolicy.pdf"
    }
]
```

---

## Delete Document

**Endpoint**

```
DELETE /rag/documents/{id}
```

### Response

```json
{
    "message":"Document deleted."
}
```

---

# AI Agent APIs

---

## Execute Agent

**Endpoint**

```
POST /agents/run
```

### Description

Runs a selected AI Agent.

### Request

```json
{
    "agent":"resume_analyzer",
    "input":"resume.pdf"
}
```

### Response

```json
{
    "status":"Completed",
    "execution_time":"2.5 sec",
    "result":"Resume Score : 89%"
}
```

---

## List Available Agents

**Endpoint**

```
GET /agents
```

### Response

```json
[
    {
        "id":"1",
        "name":"Resume Analyzer"
    },
    {
        "id":"2",
        "name":"Code Reviewer"
    }
]
```

---

## Agent Status

**Endpoint**

```
GET /agents/status/{task_id}
```

### Response

```json
{
    "status":"Completed"
}
```

---

# Audit Log APIs

The Audit module records every important system activity.

---

## Get Audit Logs

**Endpoint**

```
GET /audit/logs
```

### Authorization

Admin Only

### Response

```json
[
    {
        "user":"Admin",
        "action":"Created User",
        "timestamp":"2026-07-01 11:30"
    }
]
```

---

## Filter Audit Logs

**Endpoint**

```
GET /audit/logs?user=admin&date=2026-07-01
```

### Response

```json
[
    {
        "action":"Login"
    }
]
```

---

# Settings APIs

---

## Get Settings

**Endpoint**

```
GET /settings
```

### Response

```json
{
    "theme":"Dark",
    "notifications":true
}
```

---

## Update Settings

**Endpoint**

```
PUT /settings
```

### Request

```json
{
    "theme":"Light",
    "notifications":false
}
```

### Response

```json
{
    "message":"Settings Updated Successfully"
}
```

---

# Common Error Codes

|HTTP Code|Description|
|----------|-----------|
|200|Request completed successfully|
|201|Resource created successfully|
|204|No content|
|400|Bad request|
|401|Authentication failed|
|403|Access denied|
|404|Resource not found|
|405|Method not allowed|
|409|Conflict|
|413|Payload too large|
|415|Unsupported media type|
|422|Validation error|
|429|Too many requests|
|500|Internal server error|
|502|Bad gateway|
|503|Service unavailable|

---

# API Security

The Enterprise AI Platform follows industry-standard security practices:

- JWT Authentication
- Password Hashing using BCrypt
- HTTPS Communication
- Role-Based Access Control (RBAC)
- Audit Logging
- Token Expiration
- Refresh Tokens
- Input Validation
- SQL Injection Protection
- CORS Configuration
- Rate Limiting
- Secure HTTP Headers

---

# OpenAPI Features

The API automatically generates:

- Swagger UI (`/docs`)
- ReDoc (`/redoc`)
- OpenAPI Specification (`/openapi.json`)

Each endpoint includes:

- Summary
- Description
- Request Schema
- Response Schema
- Authentication Requirements
- Status Codes
- Example Requests
- Example Responses

---

**End of API Documentation**