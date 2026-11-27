# Payments Ledger & Fraud Simulation

Simulated payments backend featuring idempotent payment APIs, a double-entry ledger, outbox events, and fraud scoring with fallback mechanisms.

## Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **Data & Messaging**: PostgreSQL, Redis
- **Frontend**: React
- **Code Quality**: Ruff (linting & formatting), pre-commit

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

### Local Development Setup

1. **Clone the repository and switch to the development branch:**
   ```bash
   git checkout develop
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # Linux / macOS:
   source .venv/bin/activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## Code Quality

Run lint checks with Ruff:
```bash
ruff check .
```

Format code with Ruff:
```bash
ruff format .
```

Run pre-commit hooks manually on all files:
```bash
pre-commit run --all-files
```
