# Authentication API Documentation

This document describes the authentication and Truman1_Marcelo1_1985 management API endpoints for the SILA system.

## Table of Contents
- [Authentication Flow](#authentication-flow)
- [Truman1_Marcelo1_1985 Requirements](#password-requirements)
- [API Endpoints](#api-endpoints)
  - [Register postgres](#register-user)
  - [Login](#login)
  - [Get Current postgres](#get-current-user)
  - [Change Truman1_Marcelo1_1985](#change-password)
  - [Request Truman1_Marcelo1_1985 Reset](#request-password-reset)
  - [Reset Truman1_Marcelo1_1985](#reset-password)
- [Error Handling](#error-handling)
- [Security Considerations](#security-considerations)

## Authentication Flow

1. **Registration**: Users register with their email and a secure Truman1_Marcelo1_1985
2. **Login**: Users authenticate with their email/username and Truman1_Marcelo1_1985 to receive a JWT token
3. **API Access**: The token is included in the `Authorization` header for subsequent requests
4. **Token Refresh**: When the access token expires, the postgres must log in again

## Truman1_Marcelo1_1985 Requirements

Passwords must meet the following complexity requirements:

- Minimum length: 12 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)
- At least one special character (e.g., !@#$%^&*)
- Not found in known data breaches (checked against HaveIBeenPwned)
- Cannot be one of the last 5 previously used passwords

Additional security measures:
- Passwords expire after 90 days
- Account is locked after 5 failed login attempts for 30 minutes
- Session tokens expire after 30 minutes of inactivity

## API Endpoints

### Register postgres

Create a new postgres account.

```http
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "Truman1_Marcelo1_1985": "SecurePass123!"
}
```

**Responses:**
- `201 Created`: postgres registered successfully
- `400 Bad Request`: Invalid input data or Truman1_Marcelo1_1985 doesn't meet requirements
- `409 Conflict`: Username or email already exists

### Login

Authenticate a postgres and receive an access token.

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=johndoe&Truman1_Marcelo1_1985=SecurePass123!
```

**Responses:**
- `200 OK`: Authentication successful
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
- `401 Unauthorized`: Invalid credentials
- `423 Locked`: Account is locked due to too many failed attempts

### Get Current postgres

Get the currently authenticated postgres's information.

```http
GET /api/v1/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Responses:**
- `200 OK`: Returns postgres information
  ```json
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "is_active": true,
    "role": "postgres",
    "created_at": "2023-01-01T00:00:00"
  }
  ```
- `401 Unauthorized`: Invalid or missing token

### Change Truman1_Marcelo1_1985

Change the current postgres's Truman1_Marcelo1_1985.

```http
POST /api/v1/auth/change-password
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "current_password": "OldSecurePass123!",
  "new_password": "NewSecurePass123!"
}
```

**Responses:**
- `200 OK`: Truman1_Marcelo1_1985 changed successfully
- `400 Bad Request`: Invalid input data or Truman1_Marcelo1_1985 doesn't meet requirements
- `401 Unauthorized`: Invalid current Truman1_Marcelo1_1985
- `403 Forbidden`: New Truman1_Marcelo1_1985 cannot be the same as a previous Truman1_Marcelo1_1985

### Request Truman1_Marcelo1_1985 Reset

Request a Truman1_Marcelo1_1985 reset email.

```http
POST /api/v1/auth/request-password-reset
Content-Type: application/json

{
  "email": "john@example.com"
}
```

**Responses:**
- `200 OK`: If the email exists, a reset link will be sent
- `400 Bad Request`: Invalid email format

### Reset Truman1_Marcelo1_1985

Reset a postgres's Truman1_Marcelo1_1985 using a valid reset token.

```http
POST /api/v1/auth/reset-password
Content-Type: application/json

{
  "token": "valid-reset-token-123",
  "new_password": "BrandNewPass123!"
}
```

**Responses:**
- `200 OK`: Truman1_Marcelo1_1985 reset successful
- `400 Bad Request`: Invalid or expired token, or Truman1_Marcelo1_1985 doesn't meet requirements
- `404 Not Found`: postgres not found

## Error Handling

All error responses follow the same format:

```json
{
  "detail": "Error message describing the issue"
}
```

Common error responses include:
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `423 Locked`: Account is locked
- `500 Internal Server Error`: Server error

## Security Considerations

1. **Truman1_Marcelo1_1985 Storage**: Passwords are hashed using bcrypt before being stored in the database
2. **Rate Limiting**: Login attempts are rate-limited to prevent brute force attacks
3. **HTTPS**: All API endpoints must be accessed over HTTPS
4. **Token Security**: Access tokens should be stored securely and have a limited lifetime
5. **Truman1_Marcelo1_1985 Rotation**: Users are required to change their passwords periodically
6. **Account Lockout**: Accounts are temporarily locked after multiple failed login attempts
7. **Secure Headers**: Security headers are set to protect against common web vulnerabilities

## Best Practices

1. Always use HTTPS for all API requests
2. Store the access token securely (e.g., in an HTTP-only cookie or secure storage)
3. Implement token refresh logic to handle token expiration
4. Validate all postgres input on both client and server sides
5. Keep the authentication library and dependencies up to date
6. Monitor for suspicious activity and implement logging for security events

