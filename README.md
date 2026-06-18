# NALCO Internal Email Intelligence System

An enterprise-ready, full-stack, AI-powered internal email intelligence system developed for **NALCO (National Aluminium Company Limited)**, a Navratna PSU under the Ministry of Mines, Government of India. 

The system automates email triage by securely connecting to the Gmail API, cleaning email payloads, and running them through an offline AI pipeline using a locally hosted **Gemma 3 (1B)** Large Language Model via Ollama. It classifies emails into NALCO's 10 core administrative divisions, scores their operational urgency, extracts actionable 2-3 line summaries, and exposes analytics via an interactive React dashboard.

---

## 🛠 System Architecture

The project is designed using a decoupled, full-stack architecture with a local Generative AI engine to preserve NALCO's data privacy constraints:

```mermaid
graph TD
    subgraph Frontend (React Dashboard)
        UI[React App] -->|JWT Secure Request| API[FastAPI Backend]
        UI -->|Displays Visuals| Charts[Recharts Analytics]
    end

    subgraph Backend (FastAPI Engine)
        API -->|Authentication| Auth[JWT & SHA-256 Auth]
        API -->|Periodic Polling| Scheduler[APScheduler / 30 mins]
        Scheduler -->|Fetches Payload| GmailAPI[Gmail API / Read-Only]
        API -->|Object Mapping| ORM[SQLAlchemy ORM]
        ORM -->|Dynamic Queries| DB[(SQLite / PostgreSQL)]
    end

    subgraph local_ai [Offline Inference Engine]
        API -->|Prompt & Context| LLM[Gemma 3:1b via Ollama]
        LLM -->|Classify & Summarize| API
    end
```

---

## ✨ Key Features

1. **Gmail OAuth 2.0 Integration**: Secure Google authentication with read-only scopes. Parses plain text and HTML emails, sanitizing them for the LLM.
2. **Local AI Inference (Data Privacy)**: Performs email analysis entirely offline using Ollama and Google's Gemma 3:1b model. No internal email data is exposed to public APIs (e.g., OpenAI).
3. **Multi-Class AI Categorization**: Employs Few-Shot Prompting to categorize emails into 10 target departments:
   * *Finance, HR, Systems/IT, Procurement, Operations, Legal/Vigilance, Administration, Safety/Environment, Friends/Family, Others*
4. **Urgency Detection & Actionable Summaries**: Flag urgent operations and write concise 2-3 line executive summaries.
5. **Database-Agnostic Storage**: Implements SQLAlchemy ORM, supporting local **SQLite** for development and serverless **PostgreSQL** in production with zero code modification.
6. **JWT Role-Based Access Control (RBAC)**: Secure endpoints with token-based authorization supporting `Admin` and `Employee` roles.
7. **Visual Analytics**: Dynamic dashboard with category distribution bar charts and urgency breakdowns.

---

## 🚀 Tech Stack

* **Frontend**: React.js, Recharts, Axios, HTML5/CSS3
* **Backend**: FastAPI, Uvicorn, SQLAlchemy, APScheduler, python-jose (JWT)
* **AI Model**: Gemma 3:1b running via Ollama
* **Database**: SQLite (Local development) / PostgreSQL (Production)
* **API Scopes**: Google Gmail API (`gmail.readonly`)

---

## 💻 Local Setup Instructions

### Prerequisites
* Python 3.10+ installed.
* Node.js and npm installed.
* [Ollama](https://ollama.com) installed and running.
* Gemma model pulled locally: `ollama pull gemma3:1b`.

### 1. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your Gmail credentials configuration file:
   * Save your OAuth client credentials from the Google Cloud Console inside `backend/credentials.json`.
4. Initialize the database schema:
   ```bash
   py database.py
   ```
5. Start the FastAPI backend:
   ```bash
   py -m uvicorn main:app --reload
   ```
   *The backend will run on `http://127.0.0.1:8000`.*

### 2. Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install package dependencies:
   ```bash
   npm install
   ```
3. Launch the development server:
   ```bash
   npm start
   ```
   *The dashboard will launch on `http://localhost:3000`.*

### 3. Logins
* **Admin Login**: Username: `Kutu` | Password: `Kutus@3437`
* **Employee Login**: Username: `employee` | Password: `emp123`

---

## ☁️ Cloud Deployment (Railway)

This codebase is configured to be deployed instantly on **Railway** using the provided environment variables:

1. Create a **PostgreSQL** database service on Railway.
2. Link your GitHub repository.
3. Configure the following Environment Variables in the backend container:
   * `DATABASE_URL`: (Railway automatically populates this when linked to a Postgres service).
   * `SECRET_KEY`: A secure key used for JWT signing.
4. Deploy! The backend uses the `Dockerfile` to configure, boot, and run the service.
