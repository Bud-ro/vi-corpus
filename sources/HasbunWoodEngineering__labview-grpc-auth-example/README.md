# labview-grpc-auth-example

https://github.com/user-attachments/assets/052af6c9-db67-4a4f-b65e-4ec2aab541eb

Reference implementation of a browser-based authentication flow for
LabVIEW applications using Django, gRPC, and access tokens (JWT).

-   Django handles users, MFA (TOTP), and token issuance
-   Clients (e.g. LabVIEW) never handle credentials
-   Authentication is performed via browser → access token is delivered
    via gRPC

> ⚠️ This project is a reference implementation focused on integration and architecture. 
> It is not a production‑ready security solution and has not been reviewed or hardened for real‑world deployment.

## 🧠 Concept

This project demonstrates an architectural pattern for integrating
authentication into non-web clients:

-   Login happens exclusively in a browser
-   Access tokens are issued by Django (implemented as JWT)
-   Clients interact via gRPC only

👉 Result: no direct handling of user credentials in LabVIEW or other
native clients

## 🏗️ Architecture

    python/
      auth_service/   # Django app: users, MFA, tokens, device-link sessions
      grpc_auth/      # gRPC server + proto
      templates/      # login / completion pages

    labview/          # LabVIEW client implementation

### What is `grpc_auth`?

`grpc_auth` is a thin gRPC layer that exposes authentication
functionality from Django.

It allows clients to: 
- start login sessions 
- wait for login completion 
- receive access tokens 
- validate identity and permissions 
- refresh or revoke tokens

## 🔄 Authentication Flow

### Browser-based login

1.  Client calls `StartLogin()`
2.  Receives:
    -   `session_id`
    -   `login_url`
3.  Client opens `login_url` in a browser (or embedded web interface)
4.  Client starts `SubscribeLogin(session_id)` and waits for updates
5.  User logs in via the web UI (including MFA if enabled)
6.  Browser redirects to `/app/complete/<session_id>/`
7.  Client receives:

    -   `READY` + access token → success
    -   `PENDING` → still waiting for login completion
    -   or `EXPIRED` / `USED` / `INVALID`

8.  Client terminates the subscription after receiving a final state

### Permissions via group membership

1.  Client calls `ValidateToken(access_token)`
2.  Server returns:
    -   user identity
    -   associated groups
3.  Client evaluates permissions based on group membership

### Token lifecycle

-   Tokens are stateful and tracked server-side
-   Access tokens expire after `JWT_ACCESS_TTL_SECONDS`
-   The client can request a new access token via
    `RefreshToken(access_token)` before expiration
-   A refreshed token replaces the previous one
-   The previous token is immediately invalidated server-side
    
Note: Access tokens are JWTs, but they are still tracked server-side and
validated against server state, so a token can be revoked immediately.


## 🔌 gRPC API

| RPC | Purpose | Returns |
|-----|--------|--------|
| `StartLogin()` | Start login session | `ok`, `error`, `session_id`, `login_url`, `expires_at` |
| `SubscribeLogin()` | Wait for login result | `ok`, `error`, `status`, optional `access_token` (only when `READY`), `access_expires_at`, `username` |
| `RefreshToken()` | Refresh access token | `ok`, `error`, `access_token`, `access_expires_at` |
| `Logout()` | Revoke token | `ok`, `error` |
| `ValidateToken()` | Resolve identity | `valid`, `error`, `user_id`, `groups` |

Note: For full request/response fields, refer to
[`python/grpc_auth/auth.proto`](python/grpc_auth/auth.proto).

## ⚙️ Requirements

-   Docker
-   Docker Compose
-   LabVIEW 20.0.1f1 or newer with WebVIEW2 and gRPC Support installed (see [LabVIEW Dependencies](#labview-dependencies))

## 🚀 Quick Start

Run the following commands from `python/`.

### 1. Setup

``` bash
cp .env.example .env
```

Set: 
- `DJANGO_SECRET_KEY` 
- `JWT_SECRET_KEY`

### 2. Build & Initialize

``` bash
docker compose build
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser
```

You will be requested to type in a username and password for the
superuser.

### 3. Run

``` bash
docker compose up
```

## 🌐 Django Access

- Admin: http://localhost:8000/admin/
- Login: http://localhost:8000/accounts/login/

Log in to the admin interface using the superuser credentials.

Create groups:
- `Operator`
- `Developer`

Create and assign users accordingly.

Users can log in via the web interface to change their password and manage 2-factor authentication.

## 🧪 LabVIEW Usage

Open:

    labview/App with Authentication.lvproj

Run `Main.vi` to see the full client flow: login/logout, token refresh on expiry, and group‑based permissions. Refer to the code for further information.

## 🧹 Cleanup

Remove expired sessions and tokens:

``` bash
docker compose run --rm web python manage.py cleanup_device_links
```

Preview only:

``` bash
docker compose run --rm web python manage.py cleanup_device_links --dry-run
```

Custom retention:

``` bash
docker compose run --rm web python manage.py cleanup_device_links --keep-days 30
```

## ⚠️ Notes

-   Email is disabled in this minimal setup
-   Tokens are stored server-side and can be revoked immediately
-   This project is intentionally simplified for demonstration purposes

## 🎯 Scope

This repository is a **reference implementation**, not a drop-in
solution.

It is intended to demonstrate: 
- architecture 
- integration pattern 
- LabVIEW ↔ gRPC interaction

For production systems, adapt security, deployment, and scaling
accordingly. Additional measures typically include:

- secure secret management (e.g. environment isolation, vault solutions)
- transport security (TLS, reverse proxy setup)
- hardened token handling (scopes, lifetimes, rotation policies)
- secure deployment and access control
- monitoring, logging, and auditing

The exact requirements depend on the target system and threat model.

## License

This project is published under the MIT license. See [LICENSE](LICENSE) for details.

## Third-Party Dependencies

This project is provided as source code and build configuration and does not bundle any third-party libraries directly, except where explicitly noted.

All dependencies are installed during the Docker build process or via external package managers (e.g. pip, VIPM) and are obtained from their original sources.

By building and running this project, users install these third-party components and accept their respective license terms.

### Bundled components

- JetBrains Mono (SIL Open Font License 1.1)  
  Included in this repository. See [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES) for the full license text.

### Python Dependencies

The Python components are based on the following primary frameworks (see [requirements.txt](python/requirements.txt)):

- Django (BSD 3-Clause License)  
  https://github.com/django/django

- django-allauth (MIT License)  
  https://github.com/pennersr/django-allauth

- psycopg (LGPL-3.0)  
  https://github.com/psycopg/psycopg

- gunicorn (MIT License)  
  https://github.com/benoitc/gunicorn

- grpcio (Apache License 2.0)  
  https://github.com/grpc/grpc

- grpcio-tools (Apache License 2.0)  
  https://github.com/grpc/grpc/tree/master/tools/distrib/python/grpcio_tools

- PyJWT (MIT License)  
  https://github.com/jpadilla/pyjwt

- cryptography (Apache License 2.0 / BSD-3 License)  
  https://github.com/pyca/cryptography

- uvicorn (BSD 3-Clause License)  
  https://github.com/Kludex/uvicorn

- whitenoise (MIT License)  
  https://github.com/evansd/whitenoise

Additional Python packages may be installed as transitive dependencies.
Their respective licenses apply.

### LabVIEW Dependencies

The LabVIEW components depend on the following packages:

- WebVIEW2 2.1.1.2 (BSD 3-Clause License)  
  https://www.vipm.io/package/sklein_lib_webview2/

- LabVIEW gRPC Servicer 1.6.1.1 (MIT License)  
  https://github.com/ni/grpc-labview/releases/tag/v1.6.1.1

- LabVIEW gRPC Library 1.6.1.1 (MIT License)  
  https://github.com/ni/grpc-labview/releases/tag/v1.6.1.1

- gRPC Server and Client Template 1.6.1.1 (MIT License)  
  https://github.com/ni/grpc-labview/releases/tag/v1.6.1.1

These components are installed separately and obtained from their original sources.
Their respective licenses apply.

### Notes

Some dependencies (e.g. those licensed under Apache License 2.0) may include additional requirements such as NOTICE files.
Refer to the respective project repositories for full license details.

## Disclaimer

LabVIEW™ is a trademark of National Instruments Corporation.

This project is an independent, open-source tool and is not affiliated with, endorsed by, or sponsored by National Instruments Corporation.
