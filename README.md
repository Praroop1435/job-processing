# Service Gateway: API & Job Core

A highly optimized, production-scale infrastructure connecting a **FastAPI / SQLAlchemy** asynchronous backend with a dedicated **Next.js (React)** authorization dashboard.

This monolithic repository exposes a complete User Authentication suite layered over strict sliding-window rate-limiting, secure identity-driven credential provisioning, and asynchronous background worker queues.

---

## 🏗 Full-Stack Architecture

### 1. Protective Gateway (FastAPI Backend)
An isolated, pure asynchronous Python microservice routing all network constraints safely into a localized SQLite execution layer.

- **Token Authentication & Security**: Intercepts `POST /auth/register` and `POST /auth/login` to distribute cryptographically secure **JWT Bearer Tokens**. Passwords are encrypted strictly using `bcrypt`.
- **Identity Rate Limiting Layer**: Strictly controls key utilization using a mathematically absolute Sliding-Window tracking mechanism, locking consumers universally at precisely **5 Requests / Minute**.
- **Asynchronous Task Workers**: Utilizes standard `BackgroundTasks` via an explicitly isolated database `sessionmaker`, avoiding thread collisions while executing complex delayed jobs concurrently.

### 2. Administrator Dashboard (Next.js Frontend)
A pristine, lightning-fast React interface rendered using Tailwind CSS to visually interact with the backend API. 

- **State-based Authentication**: A seamless login sequence that injects the securely retrieved **JWT** into an `Authorization: Bearer <token>` Header internally to govern fetch actions across the local network. Only fully authenticated accounts process the identity dashboard.
- **Dynamic Analytic Progression**: Auto-polls the exact consumption threshold allocated from the Python backend securely, updating a visual gauge exactly reflecting the sliding window metrics. 

---

## ⚙️ Deployment & Execution

### Prerequisites
You must have Node.js (`npm`), Python `>=3.11`, and `uv` package manager installed natively.

### Boot Sequence

#### 1. Launch the Backend API
Navigate to the root directory and initiate the `uvicorn` protocol via `uv`:
```bash
# This commands handles hot-reloading naturally
uv run uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
> The API automatically exposes automated **Swagger UI Documentation** instantly at `http://127.0.0.1:8000/docs`.

#### 2. Launch the Next.js Service Gateway
Open an entirely separate split-terminal instance to bind the React DOM onto Node.
```bash
cd frontend
npm run dev
```

### Authorization Workflow
1. Direct your browser specifically to **`http://localhost:3000`** while both terminal nodes are active.
2. The UI naturally restricts access until authenticated. Proceed to **Create Account** using any test email criteria (ex: `admin@gateway.local`) and standard secure password combinations (>6 length). 
3. After registration concludes successfully, cleanly **Sign In** to pierce the interface. You can now execute and provision secure keys mapped absolutely to your provisioned UUID under the SQLite database.
