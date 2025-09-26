# Helpdesk & Ticket Management System

A Django + DRF project implementing a **Helpdesk / Ticket Management** system with:
- User registration & authentication (Django built-in auth).
- Role-based access (User, Agent, Admin).
- Ticket creation, assignment, escalation, and filtering.
- Celery task queue for automatic escalation & email alerts.
- Comment system for tickets.
- Reporting endpoint (admin-only).
- API documentation via Swagger.

---

## ⚙️ Tech Stack
- Python 3.10+
- Django 4.x / 5.x
- Django REST Framework
- Celery
- Redis (or Memurai on Windows / Docker Redis)
- SQLite (default DB)

---

## 🚀 Setup Instructions (Step by Step)

### 1. Clone the repository
```bash
git clone <your-repo-url> helpdesk_project
cd helpdesk_project

2. Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt
