# Market Intelligence & Research Management Software

A modular Django full-stack application foundation for market research, market intelligence, projects, surveys, reports, data-source management, AI-assisted research and workspace administration.

## Included working functionality

- Authentication using Django sessions and a private workspace bootstrap.
- Organisation, membership and subscription records.
- Dashboard with live counts and research distribution chart.
- 21 configurable research record modules: industry, market sizing, competitors, products, customers, surveys, market data, geography, pricing, suppliers, trade, trends, procurement, opportunities, feasibility, financial analysis, reports, news, projects, analytics and data sources.
- Create, read, update, delete, search, status filtering and pagination for research records.
- CSV import and export.
- Research project records with budgets and actual costs.
- Survey builder, public survey URL, question management and response capture.
- Research report authoring and print / browser Save-as-PDF.
- Data-source registry for APIs, public datasets and research references.
- Keyword alert registry.
- AI assistant integration through an optional OpenAI-compatible chat-completions API; a local research-planning fallback is provided without a key.
- Workspace profile, membership overview and Django admin console.
- Responsive Bootstrap UI.

## Important delivery scope

This is a runnable application foundation with working CRUD and core workflows. The requested 28 capability areas are represented in the navigation and application architecture, but some advanced capabilities are starter implementations or registries rather than fully automated services. In particular:

- Market sizing, competitor intelligence, customer research, pricing, supplier, trade, tender and financial analysis use a flexible structured research record (including a JSON data field). Add dedicated domain-specific models and calculation workflows as requirements are refined.
- External APIs are registered as data sources but not automatically connected. Each provider requires API credentials, licensing review, mapping and error handling.
- Alerts are configured records; scheduled monitoring and email/SMS delivery need Celery/Redis and provider integrations.
- Forecasting, TAM/SAM/SOM calculators, statistical models, sentiment analysis and predictive scoring need domain logic and validated datasets.
- Subscription plans are stored, but payment gateway, webhook processing and plan enforcement are not enabled.
- Role names and memberships exist; full permission enforcement and secure multi-tenant isolation require a production hardening pass.
- The AI feature requires a configured API provider for generated answers. The no-key fallback is research guidance, not live market intelligence.

Do not treat generated estimates or AI output as verified market facts. Store source URLs, dates, methodology, assumptions and confidence notes for research findings.

## Requirements

- Python 3.10+
- pip
- SQLite for local development; PostgreSQL recommended for production.

## Run on Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Run on Ubuntu / WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Open http://127.0.0.1:8000/ in your browser.

On first dashboard visit, the application creates the signed-in user's workspace, owner membership and free subscription.

## PostgreSQL

Change `.env`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=market_intelligence
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

Install the driver: `pip install psycopg[binary]` and add it to `requirements.txt`.

## AI assistant

Set `AI_API_KEY`, `AI_API_BASE` and `AI_MODEL` in `.env`. The assistant sends the user's prompt and up to 25 workspace research summaries to the provider. Review provider privacy terms before using confidential client information.

## CSV import

Required header: `Title`

Optional headers: `Summary, Status, Category, Geography, Source, Source URL, Unit, Tags`

Export includes Value, Score and Data as well.

## Administration

Visit `/admin/` and sign in with the superuser to manage users, organisations, memberships, research records, projects, surveys, questions, responses, data sources, alerts, notifications, reports, conversations and subscriptions.

## Production hardening checklist

1. Set `DEBUG=False`, a strong secret key and explicit `ALLOWED_HOSTS`.
2. Use PostgreSQL, HTTPS, secure cookies and a secrets manager.
3. Enforce organisation-level access checks for every operation and API.
4. Add role-based permissions, audit logs and tenant isolation tests.
5. Configure email delivery and scheduled background jobs.
6. Integrate licensed data providers and retain source provenance.
7. Add payment gateway webhooks and subscription entitlements.
8. Add upload validation, rate limits, backups, monitoring and disaster recovery.
9. Review privacy, data retention and AI provider handling.
10. Run security and performance testing before commercial deployment.

## Structure

- `config/`: Django settings, ASGI, WSGI and root URLs
- `core/`: models, forms, views, URLs, admin and module registry
- `templates/core/`: application pages
- `static/core/`: responsive stylesheet
