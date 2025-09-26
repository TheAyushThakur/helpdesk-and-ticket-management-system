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

4. Database setup
Run migrations and create superuser:

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

5. Run Django server
python manage.py runserver

API Root → http://127.0.0.1:8000/api/
Swagger docs → http://127.0.0.1:8000/swagger/
Admin site → http://127.0.0.1:8000/admin/

6. Celery & Redis Setup
Celery requires Redis, folllowing commands to start the server
redis-server
redis-cli ping   # should print PONG (just for testing)

7. Start Celery Worker
Open a new terminal, activate venv, then run:
# Windows (must use solo)
celery -A config worker -l info -P solo
# Linux/macOS
celery -A config worker -l info
```
## Testing Escalation & Email Alerts

Create a ticket (status=open, priority=high) via API or admin.
Backdate its created_at (e.g. 2h ago for high priority).

from helpdesk.models import Ticket
from django.utils import timezone
from datetime import timedelta

t = Ticket.objects.get(id=1)
t.created_at = timezone.now() - timedelta(hours=2)
t.save()


Run task manually:

python manage.py shell
from helpdesk.tasks import check_ticket_escalations
check_ticket_escalations.delay()

Celery worker should process the task:

Ticket status → escalated
Console shows email output (since we use console.EmailBackend)

## API Endpoints
### Authentication

POST /api/register/ → Register new user
POST /api/login/ → Login (Session cookie)
POST /api/logout/ → Logout

### Tickets

GET /api/tickets/ → List tickets (role-based filtering)
POST /api/tickets/ → Create ticket
PUT /api/tickets/{id}/ → Update ticket
DELETE /api/tickets/{id}/ → Delete ticket
Filters: ?status=...&priority=...&assigned_to=ID&title=...

### Comments

GET /api/comments/ → List comments
POST /api/comments/ → Add comment
Example:
{ "ticket": 1, "text": "This needs urgent fix" }

### Reporting

GET /api/report/ → Admin only
Returns stats for last 7 days:

{
  "tickets_opened_last_7_days": x,
  "tickets_resolved_last_7_days": y,
  "tickets_escalated_last_7_days": z
}

### Docs
Swagger → /swagger/.
Admin → /admin/.
