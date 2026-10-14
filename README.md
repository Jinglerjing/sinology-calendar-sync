# sinology-calendar-sync

# Sinology Calendar to Google Calendar Sync

An automated, maintenance-free Python pipeline that dynamically synchronizes traditional Chinese solar terms (*Jieqi*) and cultural festivals from WordPress to a dedicated Google Calendar.

Designed to power the interactive calendar widget on [Sinology Studio](https://sinologystudio.com/rhythm), this repository runs on GitHub Actions to ensure seamless, evergreen updates.

---

## Key Features

* **Dynamic WordPress Integration**: Pulls live post excerpts directly from the WordPress REST API (`/wp-json/wp/v2/posts`).


* **Automated Solar Term & Festival Calculations**: Uses the `lunar_python` library to calculate accurate astronomical solar term dates and traditional Chinese lunar calendar festival dates across multi-year windows (2026–2030).
* **Smart Upsert Logic**: Computes deterministic Base32 MD5 event IDs (`evt` + MD5 hash) to guarantee zero duplicate entries during automated sync runs.
* **Automatic Legacy Event Cleanup**: Scans the Google Calendar and purges outdated or legacy test events to maintain clean calendar instances.
* **API Backoff & Rate-Limit Protection**: Employs backoff retries and execution delays to prevent Google Calendar API quota limits or temporary server errors.



---

## System Architecture

```
┌─────────────────────────┐
│  WordPress REST API     │
│  (Sinology Studio)      │
└────────────┬────────────┘
             │ (Fetch Excerpts)
             ▼
┌─────────────────────────┐     Calculates Dates     ┌─────────────────────────┐
│  GitHub Actions Workflow│ ────────────────────────►│  Lunar / Solar Engine   │
│  (sync_calendar.py)     │                          │  (lunar_python)         │
└────────────┬────────────┘                          └─────────────────────────┘
             │ (OAuth 2.0 Upsert)
             ▼
┌─────────────────────────┐
│  Google Calendar API    │ ───────────────► [ Sinology Studio Web Embed ]
└─────────────────────────┘

```

---

## Prerequisites & Setup

### 1. Google Cloud Console Setup

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Calendar API**.


3. Configure an **OAuth 2.0 Client ID** and obtain:
* Client ID
* Client Secret
* Refresh Token (with `[https://www.googleapis.com/auth/calendar](https://www.googleapis.com/auth/calendar)` scope)





### 2. GitHub Secrets Configuration

Store the following credentials in your repository under **Settings** $\rightarrow$ **Secrets and variables** $\rightarrow$ **Actions**:

| Secret Name | Description |
| --- | --- |
| `CALENDAR_ID` | The ID of the target Google Calendar (e.g., `c_...@group.calendar.google.com`)

 |
| `GOOGLE_CLIENT_ID` | OAuth 2.0 Client ID

 |
| `GOOGLE_CLIENT_SECRET` | OAuth 2.0 Client Secret

 |
| `GOOGLE_REFRESH_TOKEN` | OAuth 2.0 Refresh Token

 |

---

## Workflow Schedule

The GitHub Action (`.github/workflows/sync.yml`) is configured to run on a scheduled cron job (or manually via `workflow_dispatch`):

```yaml
name: Sync Sinology Calendar to Google

on:
  schedule:
    - cron: '0 0 1 * *' # Runs on the 1st of every month
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |
          pip install requests lunar-python google-api-python-client google-auth-oauthlib

      - name: Execute Calendar Sync
        env:
          CALENDAR_ID: ${{ secrets.CALENDAR_ID }}
          GOOGLE_CLIENT_ID: ${{ secrets.GOOGLE_CLIENT_ID }}
          GOOGLE_CLIENT_SECRET: ${{ secrets.GOOGLE_CLIENT_SECRET }}
          GOOGLE_REFRESH_TOKEN: ${{ secrets.GOOGLE_REFRESH_TOKEN }}
        run: python sync_calendar.py

```

---

## Local Development & Testing

1. Clone the repository:
```bash
git clone https://github.com/Jinglerjing/sinology-calendar-sync.git
cd sinology-calendar-sync

```


2. Install dependencies:
```bash
pip install requests lunar-python google-api-python-client google-auth-oauthlib

```


3. Export environment variables and run locally:
```bash
export CALENDAR_ID="your-calendar-id"
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REFRESH_TOKEN="your-refresh-token"

python sync_calendar.py

```
