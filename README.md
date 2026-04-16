# Full-Stack Job Processing & API Identity Dashboard

This project is a complete full-stack web application. It features a scalable asynchronous **Python FastAPI backend** and a modern **Next.js React frontend**. 

It is designed to solve three major backend engineering tasks:
1. **User Authentication:** Users can register and log in to the dashboard securely via `bcrypt` hashed passwords and `JWT Bearer tokens`.
2. **API Key Generation & Rate Limiting:** Authenticated users can generate unique secure API keys. The system strictly enforces a **5 request per minute** sliding-window usage limit on these keys, and provides a backend endpoint to track live usage natively.
3. **Background Job Processing:** Users can submit long-running tasks. The backend executes them asynchronously using FastAPI `BackgroundTasks`, updating their status in the SQLite database moving from `pending` -> `in_progress` -> `completed` without freezing the main application.

---

## 🛠 Tech Stack

**Backend:**
* Python (>= 3.11)
* FastAPI + Uvicorn
* SQLite + SQLAlchemy (Async isolation)
* Package Manager: `uv`
* Security: `passlib` (bcrypt), `PyJWT`, CORS Middleware

**Frontend:**
* Node.js
* Next.js (React App Router)
* Tailwind CSS
* Lucide-React (Icons)

---

## 🚀 How to Run the Project Locally

### 1. Start the Backend API (FastAPI)
The backend manages the database, the rate-limiting calculations, and the background asynchronous workers.

1. Open your terminal and navigate to the project directory:
   ```bash
   cd job-processing
   ```
2. Run the server using the `uv` package manager:
   ```bash
   uv run uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```
3. The API will boot up. You can view the Auto-Generated Swagger Interface at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 2. Start the Frontend Dashboard (Next.js)
The frontend is the visual User Interface connecting users seamlessly to the Backend via standard REST fetch requests.

1. Open a **new separate terminal window**.
2. Navigate into the frontend folder:
   ```bash
   cd job-processing/frontend
   ```
3. Install dependencies and start the development server:
   ```bash
   npm install
   npm run dev
   ```
4. Open your browser and navigate to **[http://localhost:3000](http://localhost:3000)**.

---

## 💻 How to Use the Dashboard

Once both servers are running successfully, here is how you interact with the project:

### Step 1: Authentication
- The first screen you see on `localhost:3000` is the Secure Gateway.
- Click **"Need an account? Register"**.
- Enter an email (e.g. `user@test.com`) and a 6-character password to register your account into the SQLite Database.
- Log in to proceed to the Dashboard.

### Step 2: Rate Limiting & Identity
- Once logged in, click **"Generate API Key"**. It will map a new `sk_...` key precisely to your user identity.
- Go to the **Quota Verification** section and select your active key from the credentials dropdown.
- Click **"Execute Secure Fetch"**. 
- Watch the **Usage Tracking gauge** naturally climb (`1/5 Req.. 2/5 Req..`). If you click it faster than 5 times in 60 seconds, it will reject your request with a `429 Too Many Requests` error dynamically!

### Step 3: Background Jobs
- On the right side of the dashboard, you will see the **Asynchronous Job Queue**.
- Type a dummy task name into the input field and click **"Dispatch"**.
- The frontend will auto-poll the backend, automatically updating the UI showing the task naturally transitioning dynamically over a simulated delay period into a `completed` state.

---

## 🔒 Postman Developer Testing
If you would like to test the backend API completely independently of the visual Next.js frontend, this repository includes an explicitly configured Postman file.

Simply import `postman_collection.json` into Postman. It includes automatic Authentication token tracking scripts that dynamically construct your Bearer Headers specifically for testing the Rate-limiter directly!
