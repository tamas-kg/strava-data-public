# Strava Data Platform (WIP)

A self-hosted analytics and data platform for ingesting, transforming, analyzing, and visualizing Strava activity data.

Built for local-first development on Apple Silicon (M5 Mac) and deployed to Raspberry Pi using Docker Compose and GitHub Actions.

---

# Current Architecture

## Infrastructure

* Docker Compose orchestration
* Traefik reverse proxy
* Local HTTPS using mkcert
* GitHub Actions deployment pipeline
* ARM64-native containers for Mac + Raspberry Pi parity

## Services

| Service          | Purpose                                  |
| ---------------- | ---------------------------------------- |
| PostGIS/Postgres | Primary application database             |
| Streamlit        | Analytics dashboard and UI               |
| Jupyter          | Exploration and notebook development     |
| Airflow          | Workflow orchestration and scheduling    |
| ETL              | Strava ingestion and transformation jobs |
| dbt              | SQL modeling and transformations         |
| fastapi          | Backend service                          |

---

# Repository Structure

```text
strava-data/
│
├── docker-compose.yml
├── .env
│
├── db/
├── etl/
│   ├── src/
│   └── tests/
├── dbt/
├── airflow/
├── jupyter/
└── streamlit/
└── fastapi/
```

---

# Current Development Goals

The current focus is local platform development and service architecture.

## Priorities

* Add FastAPI backend service
* Add Redis for caching and background task support
* Move Streamlit to consume APIs instead of querying Postgres directly
* Improve service boundaries and async workflows
* Prepare architecture for eventual k3s migration

## Deferred Until Later

These are intentionally postponed until the application architecture stabilizes:

* Cloudflare DNS + HTTPS for external access
* Authentik authentication and SSO
* Kubernetes/k3s deployment
* cert-manager integration
* production-grade secrets management

---

# Planned Architecture Evolution

## Current

```text
Streamlit --> Postgres
ETL ------> Postgres
Airflow --> ETL
```

## Planned

```text
Streamlit --> FastAPI --> Postgres
                      --> Redis

Airflow --> FastAPI
Workers --> Redis Queue
```

---

# Why FastAPI

FastAPI will become the primary backend application layer.

Responsibilities:

* API endpoints
* Business logic
* Data aggregation
* Authentication integration
* Caching
* Background job orchestration
* Future frontend/mobile support

Benefits:

* Typed APIs with Pydantic
* Async support
* Automatic OpenAPI documentation
* Better separation of concerns
* Easier testing and scaling

---

# Why Redis

Redis will initially be used for:

* API response caching
* Expensive query caching
* Background task queues
* Session/token storage later

Redis is not intended to replace Postgres.

---

# Local Development

## Requirements

* Docker
* Docker Compose
* mkcert
* Traefik external proxy network

## Start Services

```bash
docker compose up -d
```

## Rebuild Services

```bash
docker compose up --build
```

## View Logs

```bash
docker compose logs -f
```

---


# Testing

## ETL Tests

```bash
docker compose --profile test up etl-test
```

## dbt Tests

```bash
docker compose --profile test up dbt-test
```

---

# Deployment

Deployment is handled through GitHub Actions targeting a Raspberry Pi host.

Current deployment model:

* Build ARM64 containers
* Push/update containers remotely
* Docker Compose-based orchestration

Future deployment target:

* k3s
* Helm/Kustomize
* Traefik Ingress
* cert-manager
* GitOps workflows

---

# Roadmap

## Phase 1 — Backend Foundation

* [x] Add FastAPI service
* [ ] Add Redis service
* [x] Move Streamlit to API consumption

## Phase 2 — Async Workloads

* [ ] Add background workers
* [ ] Introduce task queue
* [ ] Cache expensive analytics queries

## Phase 3 — Platform Hardening

* [ ] Add Alembic migrations
* [ ] Centralize configuration management
* [ ] Add structured logging
* [ ] Add monitoring/metrics

## Phase 4 — Kubernetes Migration

* [ ] Deploy k3s
* [ ] Move Traefik to Kubernetes ingress
* [ ] Add cert-manager
* [ ] Add Cloudflare DNS challenge
* [ ] Add Authentik authentication
* [ ] GitOps deployment model

---

# Design Principles

* Local-first development
* ARM-native compatibility
* Infrastructure parity between Mac and Raspberry Pi
* Incremental complexity
* API-first architecture
* Clear service boundaries
* Docker-first workflow before Kubernetes

---