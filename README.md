# Risk Registry App

IT risk management app

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/alex-dembele/risk-registry-app/actions)

## Table of Contents
- [Risk Registry App](#risk-registry-app)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Architecture](#architecture)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Contribution](#contribution)
  - [License](#license)

## Description
Professional tool for managing an IT risk registry, with automations, dynamic visualizations, and cybersecurity integrations. Designed for a perfect UX: responsive, accessible, with dark/light themes.

## Features
- Interactive dashboard with charts.
- Risk register with automatic scoring.
- API integrations (Nessus, etc.).
- PDF/Excel notifications and reports.
- RBAC security + encryption.

## Architecture
- **Frontend**: React.js + TailwindCSS + Recharts/D3.js.
- **Backend**: FastAPI (Python) + SQLAlchemy + Celery.
- **DB**: PostgreSQL.
- **Deployment**: Docker + Kubernetes.

## Setup
### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL
- Docker (optional for dev)

### Installation
1. Clone the repo: `git clone https://github.com/alex-dembele/risk-registry-app.git`
2. Backend: `cd backend && poetry install`
3. Frontend: `cd frontend && npm install`
4. Copy `.env.example` to `.env` and configure (DB_URL, etc.)
5. Run: `docker-compose up --build`
6. Access the frontend at http://localhost:3000 and the backend at http://localhost:8000

## Contribution
Forks and PRs welcome! Follow the commit plan.

## License
MIT