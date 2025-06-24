# Ra Factory

> **Multi-tenant factory management system for RaWorkshop**  
> Production tracking, logistics, and management analytics through a unified web interface.

## Project Structure

- `backend/` - FastAPI application (Python 3.11)
- `frontend/admin/` - Admin Panel UI
- `frontend/operator/` - Shop Floor Operator UI

## Development Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### Local Development

```bash
# Clone the repository
git clone git@github.com:AlexPetrovBG/ractory.git
cd ractory

# Start development stack
docker compose --profile dev up -d

# API runs on localhost:8000
# Database on localhost:5434
# Admin UI on localhost:5173 (when implemented)
# Operator UI on localhost:5174 (when implemented)
```

## Environments

- **dev** - Live code reload, mounts source for immediate changes
- **prod** - Production environment with TLS, proper DNS, and stability optimizations

## Documentation

See `docs/` directory for detailed documentation:
- [API Guide](docs/api-guide.md)
- [Implementation Plan](docs/implementation-plan.md)
- [Security Checklist](docs/security-checklist.md)

## License

© 2025 Автоматика Делис – Internal Use 