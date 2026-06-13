# CampaignMasta

Mobile-first Django MVP for the CampaignMasta political CRM and campaign operations blueprint.

## Setup (local development)

```bash
cd campaignmasta
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Demo logins after seeding:

```text
Platform / web admin   →  username: admin     password: admin12345
Mobile app (field)     →  username: manager   password: manager12345
```

The web admin (`admin`) is a superuser for the Django admin, the SaaS control
centre at `/saas-admin/`, and the candidate workspace. The `manager` account is a
Campaign Manager `TeamMember` with a mobile login, used to sign in to the Android app.

## Production deployment

`settings.py` is fully environment-driven — copy `.env.example` to `.env` and set
at minimum `DJANGO_DEBUG=false` and a strong `DJANGO_SECRET_KEY`. With `DEBUG` off,
HTTPS redirects, HSTS, and secure cookies are enabled automatically, and static
files are served with WhiteNoise (run `collectstatic`). Postgres is used when the
`DB_*` variables are set; otherwise it falls back to SQLite.

```bash
# Container build & run (migrations + gunicorn + static via WhiteNoise)
docker build -t campaignmasta .
docker run --env-file .env -p 8031:8031 campaignmasta
```

Team members are given mobile-app logins from **Team → Add / Edit** in the web app
(set a Login username + password); this provisions the linked account and API token.

## MVP Coverage

- Multi-tenant candidate workspaces
- Flexible module-based subscriptions with SaaS-controlled pricing
- Discounted bundles and full-platform package entitlements
- District Open vs Provincial candidate rules
- PNG-style geography hierarchy
- Candidate profile and team roles
- Supporter/contact registry with consent tracking
- Influencer CRM with call reminders
- Call checklist and call logging
- Messaging drafts with priority/read/acknowledgement fields
- Campaign tasks, events, issues, promises, polling records
- Mobile-first command centre and field workflows
- Django admin for platform management

## Subscribable Module Design

CampaignMasta is split into SaaS-controlled modules so candidates can subscribe according to budget and campaign stage.

- `SoftwareModule` defines each product module.
- `ModulePrice` stores per-module prices by billing cycle and currency.
- `ModuleBundle` groups modules into discounted packages, including a full-platform package.
- `Subscription` records the candidate tenant billing relationship.
- `TenantModuleSubscription` records the actual modules enabled for a tenant.
- `SubscriptionQuote` can calculate module and bundle selections before a tenant accepts.

Suggested module examples in the demo seed:

- Core Campaign CRM
- Supporter Registry
- Ward Intelligence
- Relationship Calls
- Messaging Platform
- Events and Tasking
- Polling-Day War Room
- AI Assistant
- Constituency Management

## Connector Settings

Each candidate tenant can configure its own external service connectors from the settings page.

Supported connector types in code:

- AI Provider
- WhatsApp Business
- SMS Gateway
- Email
- Maps / GIS
- Payment Gateway
- File Storage
- Webhook

Secrets are entered through password-style fields and existing secrets are preserved when an edit form is saved blank. Connector health checks validate required fields for each connector type and store the latest status/result.

## Prepaid Connector Usage

Paid connector usage is prepaid and metered per tenant.

- `UsageWallet` stores prepaid balances per service, such as AI, WhatsApp, SMS, or email.
- `UsageTopUp` records prepaid payments, for example PGK 20 before using AI.
- `UsageRateCard` stores SaaS admin pricing, provider cost, markup percentage, fixed markup, and minimum charge.
- `UsageEvent` records every allowed, free, blocked, or refunded usage event.
- `FreeAIModel` stores free AI models that tenants can select without consuming paid AI credit.

Paid usage is blocked when the wallet reaches zero or when no active rate card exists. Free AI models and free rate cards do not debit prepaid balances.

Subscription plans and bundles can also include usage quotas. `IncludedUsageQuota` attaches included AI/SMS/WhatsApp/email units to a module or bundle, and `TenantUsageQuota` is provisioned when a quote is accepted. Usage consumes included quota first, then prepaid wallet balance for any overage.
