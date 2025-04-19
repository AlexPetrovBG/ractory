# Ra Factory (RaConnect)

A multi-tenant SaaS platform providing cloud-based, real-time factory production tracking, logistics management, and analytics for window/door manufacturers using RaWorkshop.

## Project Overview

This platform extends the capabilities of RaWorkshop by:

* Ingesting project, component, and piece data.
* Enabling shop-floor operators to log production progress via QR code scans.
* Tracking component logistics using trolleys.
* Providing management dashboards and configuration tools for administrators.

It ensures strict data isolation between different companies using PostgreSQL Row-Level Security.

## Technology Stack

* **Backend:** Python 3.11, FastAPI, SQLAlchemy 2, Pydantic v2
* **Database:** PostgreSQL 15 (with Row-Level Security)
* **Frontend:** Vite, Vanilla JS (ES6), Tailwind CSS, HTMX
* **Authentication:** PyJWT, Passlib (bcrypt), QR Code + PIN
* **Infrastructure:** Docker, Docker Compose, Nginx, Let's Encrypt
* **CI/CD:** GitHub Actions
* **Monitoring:** Netdata, Uptime Kuma
