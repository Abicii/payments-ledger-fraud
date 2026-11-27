# Learning Log

---

## PAY-001 · Repo Bootstrap (`pyproject.toml`, Ruff, Pre-commit & README Stub)

### What We Did
- Created `pyproject.toml` at the repository root with project metadata, an empty core `dependencies = []` list (to start), `dev` optional dependencies (`ruff`, `pre-commit`), and `[tool.ruff]` linting/formatting rules.
- Added `.pre-commit-config.yaml` with git hygiene hooks (trailing whitespace, end-of-file fixer, YAML check, large file check) and Ruff hooks.
- Added `.gitignore` to exclude `.venv/`, `__pycache__/`, `.ruff_cache/`, and local secrets.
- Created a `.venv`, installed `ruff`, and verified `ruff check .` passed with zero errors.
- Updated `README.md` with a structured project stub.

### What We Learned
- `pyproject.toml` is the single configuration file for modern Python projects (replacing scattered `setup.py`, `.flake8`, and `isort` configs).
- Dependencies are separated into **runtime** (`dependencies`) and **developer tools** (`[project.optional-dependencies] dev`), so production builds don't ship linters or test frameworks.
- `ruff` checks code quality and formatting, while `pre-commit` enforces those checks automatically before every `git commit`.

### Explain Like I'm 10
Imagine you're building with LEGOs and you have a rulebook and a picky robot helper.
- **`pyproject.toml`** is the box label and rulebook that says what pieces you need and how neat your build has to be.
- **Ruff** is the super-fast robot helper that checks if you left messy pieces lying around or broke any building rules.
- **Pre-commit** is a security guard standing at the door: before you're allowed to save your work into the shared LEGO box (`git commit`), the guard makes the robot inspect it first. If it's messy, you have to clean it up before saving!

### Software Engineer Explanation
- **PEP 518 / PEP 621 Standardization:** `pyproject.toml` centralizes build-system metadata (`setuptools`), package dependencies, and tool configurations under `[tool.*]` namespaces.
- **Static Analysis & Formatting:** Ruff replaces legacy multi-tool pipelines (`flake8` + `isort` + `black` + `pyupgrade`) with a single Rust-backed AST linter/formatter, enabling sub-second feedback loops in both local development and CI.
- **Shift-Left Quality Gates:** `.pre-commit-config.yaml` registers local Git `pre-commit` hooks so style, import ordering, and syntax issues are caught prior to commit, reducing noisy CI failures and PR review churn.

---

## PAY-002 · Dockerfile for `payments-api`

### What We Did
- Structured the service as a self-contained unit under `services/payments-api/` (`app/main.py`, `pyproject.toml`, `Dockerfile`, `.dockerignore`).
- Built a minimal FastAPI app exposing `GET /health` returning `{"status": "ok"}`.
- Implemented a **multi-stage `Dockerfile`**:
  - `builder` stage (`python:3.11-slim`): creates `/app/.venv` and runs `pip install --no-cache-dir .`.
  - `runner` stage (`python:3.11-slim`): creates a non-root user (`appuser`, UID `10001`), copies `/app/.venv` and `app/`, sets ownership, switches to `USER appuser`, and starts `uvicorn`.
- Added `services/payments-api/.dockerignore` to exclude `.venv/`, `__pycache__/`, `.git/`, and caches from the Docker build context.
- Built `payments-api:latest`, ran the container on port `8000`, verified `GET /health`, and checked `docker images payments-api` (**Image ID:** `347b3529d3d0`, **Disk usage:** `365MB`, **Content size:** `84.1MB`).

### What We Learned
- Docker containers and your local machine are completely isolated filesystems: `pip install` inside a `Dockerfile` never touches your local `.venv`.
- Docker reads `services/payments-api/pyproject.toml` to know which runtime libraries (`fastapi`, `uvicorn`) to install, while ignoring root dev-only tools like Ruff.
- `.dockerignore` must sit at the root of the Docker build context (`services/payments-api/`) so unnecessary files aren't sent to the Docker daemon.
- Running as a non-root user (`appuser`) limits blast radius if the application is ever compromised.

### Explain Like I'm 10
Think of Docker like packing a lunchbox for school:
- **`.dockerignore`** is you saying *"Don't pack my messy backpack, old homework, or toys—only pack the ingredients for lunch!"*
- **Stage 1 (`builder`)** is the kitchen where you chop veggies and cook the meal. It gets messy, with pots and peelings everywhere.
- **Stage 2 (`runner`)** is the clean lunchbox: you ONLY put the finished sandwich inside, leaving all the dirty pots behind in the kitchen so the lunchbox is super light to carry.
- **`USER appuser`** is a safety lock on the lunchbox so nobody can accidentally mess with the rest of the school kitchen.
- **`/health`** is like tapping someone on the shoulder and asking *"You awake?"* and they reply *"Yep, I'm ok!"*

### Software Engineer Explanation
- **Multi-Stage Builds & Layer Caching:** Separating `builder` and `runner` stages decouples build-time dependency resolution (`pip`, wheel compilation) from the production runtime image. Installing into an isolated `/app/.venv` lets Stage 2 perform a single deterministic `COPY --from=builder`, minimizing final image footprint and attack surface. Copying `pyproject.toml` before `app/` preserves Docker layer caching across source-only edits.
- **Build Context Hygiene:** `.dockerignore` prevents local virtual environments, `.git` history, and bytecode caches from bloating the daemon context or invalidating cache layers.
- **Container Security (Principle of Least Privilege):** Explicitly creating a non-privileged system user/group (`UID/GID 10001`, `--shell /sbin/nologin`) and switching via `USER appuser` mitigates container breakout and privilege-escalation risks compared to Docker's default `root` (`UID 0`) execution.
- **Runtime Ergonomics & Observability:** Setting `PYTHONUNBUFFERED=1` ensures stdout/stderr logs flush immediately to container log drivers, `PYTHONDONTWRITEBYTECODE=1` avoids unnecessary `.pyc` writes in an immutable filesystem, and `GET /health` provides a lightweight liveness probe for orchestrators and load balancers.
