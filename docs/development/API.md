# API Architecture

Version: 1.0

Status: Living Document

Related Documents

- docs/architecture/Overview.md
- docs/architecture/Backend.md
- docs/architecture/Security.md
- docs/architecture/NamingConventions.md
- docs/product/Requirements.md

---

# Purpose

This document defines the API architecture and standards for CipherForge.

It establishes how APIs are designed, versioned, authenticated, documented, and maintained.

This document defines API conventions rather than individual endpoints.

---

# API Philosophy

The API should be:

- Predictable
- Consistent
- Versioned
- Stateless
- Secure
- Well documented
- Easy to consume

Every endpoint should behave consistently with every other endpoint.

---

# API Style

CipherForge exposes a RESTful HTTP API.

Version 1 intentionally avoids:

- GraphQL
- gRPC
- SOAP

Future versions may introduce additional interfaces without replacing REST.

---

# Base URL

Development

```
http://localhost:8000/api/v1
```

Production

```
https://api.cipherforge.com/api/v1
```

All endpoints belong under:

```
/api/v1
```

---

# Resource Naming

Resources use plural nouns.

Examples

```
/users

/categories

/levels

/challenges

/trophies

/submissions
```

Avoid verbs in resource names.

Good

```
POST /users
```

Avoid

```
POST /createUser
```

---

# HTTP Methods

Use standard HTTP semantics.

| Method | Purpose |
|----------|----------|
| GET | Read |
| POST | Create |
| PUT | Replace |
| PATCH | Partial Update |
| DELETE | Remove |

Methods should be idempotent where defined by the HTTP specification.

---

# HTTP Status Codes

Use standard status codes consistently.

## Success

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 202 | Accepted |
| 204 | No Content |

## Client Errors

| Code | Meaning |
|------|---------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 429 | Too Many Requests |

## Server Errors

| Code | Meaning |
|------|---------|
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

# URL Structure

Pattern

```
/api/v1/{resource}

/api/v1/{resource}/{id}
```

Examples

```
GET /users

GET /users/{id}

PATCH /users/{id}

DELETE /users/{id}
```

Nested resources should be used sparingly.

Example

```
/categories/{categoryId}/levels
```

Avoid deeply nested URLs.

---

# Request Format

Clients send JSON.

Example

```json
{
  "displayName": "Alice",
  "email": "alice@example.com"
}
```

UTF-8 encoding is required.

---

# Response Format

Successful responses follow a consistent envelope.

```json
{
  "success": true,
  "data": {
  },
  "meta": {
  }
}
```

The `meta` object is optional.

---

# Error Format

Errors follow a consistent structure.

```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User not found",
    "details": {}
  }
}
```

Do not expose stack traces or internal implementation details.

---

# Validation Errors

Validation errors return HTTP 422.

Example

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "email": [
        "Email is required"
      ]
    }
  }
}
```

---

# Pagination

Collection endpoints should support pagination.

Query parameters

```
?page=1&pageSize=20
```

Example response

```json
{
  "success": true,
  "data": [],
  "meta": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 245,
    "totalPages": 13
  }
}
```

---

# Filtering

Filtering uses query parameters.

Examples

```
GET /challenges?category=web

GET /users?isActive=true
```

---

# Sorting

Sorting uses:

```
sortBy

sortOrder
```

Example

```
GET /leaderboard?sortBy=score&sortOrder=desc
```

---

# Searching

Search uses:

```
search
```

Example

```
GET /challenges?search=sql
```

---

# Authentication

Authentication uses Bearer JWT tokens.

Example

```
Authorization:

Bearer <access_token>
```

Tokens are never transmitted via query parameters.

---

# Authorization

Authorization is role-based.

Version 1 supports:

- Administrator
- Learner

Authorization decisions belong to backend services.

Clients must never assume permissions.

---

# Idempotency

Idempotent operations should remain safe to retry.

Examples

```
PUT

DELETE
```

For future payment or external operations, idempotency keys may be introduced.

---

# Rate Limiting

Rate limiting protects the platform.

Example policy

- Anonymous users
- Authenticated users
- Administrative endpoints

Exact limits are environment-specific.

Clients should receive HTTP 429 when limits are exceeded.

---

# Caching

GET requests may be cached where appropriate.

Sensitive resources must not be cached.

Cache behavior should be explicitly defined using HTTP cache headers.

---

# Content Types

Supported request type

```
application/json
```

Future support

```
multipart/form-data
```

For file uploads.

---

# Versioning

Major API changes require a new version.

Examples

```
/api/v1

/api/v2
```

Avoid breaking changes inside a major version.

---

# Deprecation

Deprecated endpoints should:

- Remain available during the deprecation window.
- Emit appropriate deprecation headers where supported.
- Be documented in release notes.

Removal requires a new major API version unless an emergency security issue exists.

---

# API Documentation

OpenAPI is the canonical API reference.

FastAPI automatically generates:

- OpenAPI schema
- Swagger UI
- ReDoc

Developers should keep endpoint documentation complete and accurate.

---

# Security Principles

All APIs should:

- Validate input
- Authenticate requests
- Authorize actions
- Prevent injection attacks
- Avoid information leakage
- Enforce HTTPS in production

---

# Long-Running Operations

Operations expected to take significant time should return:

```
202 Accepted
```

The client should poll a status endpoint or use a future asynchronous notification mechanism.

---

# File Uploads

Future uploads should use:

```
multipart/form-data
```

Large files should be streamed where practical.

---

# Time Format

All timestamps use ISO 8601.

Example

```
2026-08-01T14:35:42Z
```

All timestamps are UTC.

---

# API Evolution

Prefer additive changes.

Safe changes

- Add fields
- Add endpoints
- Add optional query parameters

Breaking changes

- Remove fields
- Rename fields
- Change field types
- Change endpoint behavior

Breaking changes require a new API version.

---

# API Checklist

Before adding a new endpoint, confirm:

- Resource follows naming conventions.
- Correct HTTP method is used.
- Input validation is defined.
- Authorization is enforced.
- Success response is documented.
- Error responses are defined.
- OpenAPI documentation is updated.
- Tests are implemented.

---

# Guiding Principle

The API is the public contract between the frontend and the backend.

Once published, it should evolve carefully, remain consistent, and preserve backward compatibility whenever possible.