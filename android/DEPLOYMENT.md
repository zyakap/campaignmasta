# CampaignMasta Android — Deployment Guide

This document covers everything needed to build, run, and ship the CampaignMasta
Android app that connects to the Django REST API backend.

---

## 1. Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Android Studio | Hedgehog (2023.1.1) or newer | Download from developer.android.com |
| JDK | 17 (bundled with Android Studio) | Set in File → Project Structure |
| Python | 3.11+ | For Django backend |
| pip / Pipenv | latest | For Python dependencies |
| Android device or emulator | API 26+ (Android 8.0+) | `minSdk = 26` |

---

## 2. Django API Setup

### 2.1 Install Django REST Framework

```bash
cd /path/to/campaignmasta
pip install djangorestframework   # or add to Pipfile
```

Or with Pipenv:
```bash
pipenv install djangorestframework
```

### 2.2 Apply Migrations

The DRF Token model needs a migration:

```bash
python manage.py migrate
```

This creates the `authtoken_token` table.

### 2.3 Create a Superuser (for Django admin)

```bash
python manage.py createsuperuser
```

### 2.4 Create a TeamMember for Your Test User

The API resolves the tenant from `TeamMember.user`. The easiest path:

1. Log in to the web app and open **Team → Add** (or **Edit**)
2. Fill in the team member, set a **Login username** and **Login password**
   — this creates the linked account and API token automatically
3. The team member can now log in via the Android app with those credentials

Alternatively, from `/admin/`: create a `Candidate` (Province, District, etc.),
then a `TeamMember` linked to a `User` with a valid Role.

### 2.5 Configure ALLOWED_HOSTS

In `campaignmasta/settings.py`, add your server's IP:

```python
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "192.168.1.x", "yourdomain.com"]
```

Replace `192.168.1.x` with your LAN IP.

### 2.6 Run the Dev Server Accessible on LAN

```bash
python manage.py runserver 0.0.0.0:8000
```

This makes the API reachable at `http://<your-lan-ip>:8000/` from any device on the same WiFi network.

---

## 3. Android Project Setup

### 3.1 Open the Project

1. Open Android Studio
2. **File → Open** → select the `android/` folder inside the `campaignmasta` project root
3. Wait for Gradle sync to complete (first run downloads ~500 MB of dependencies)

### 3.2 Configure BASE_URL

The app reads `BASE_URL` from `local.properties` in the `android/` root.

Create or edit `android/local.properties`:

```properties
sdk.dir=/Users/<you>/Library/Android/sdk
BASE_URL=http://192.168.1.x:8000/
```

Replace `192.168.1.x` with your server's LAN IP.

If `local.properties` does not set `BASE_URL`, the app defaults to
`http://10.0.2.2:8000/` which is the Android Emulator's alias for `localhost`.

### 3.3 Run on Emulator

1. Create an AVD: **Device Manager → Create Virtual Device** → Pixel 6 → API 34
2. Press the green Run button or `Shift+F10`

### 3.4 Run on Physical Device

1. Enable Developer Options on your Android device:
   Settings → About Phone → tap Build Number 7 times
2. Enable USB Debugging
3. Connect via USB, trust the computer prompt
4. Select your device in Android Studio and press Run

---

## 4. Signing the APK for Production

### 4.1 Generate a Keystore (one time only)

```bash
keytool -genkey -v -keystore campaignmasta-release.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias campaignmasta
```

Store the `.jks` file **outside** the project directory. Never commit it to git.

### 4.2 Configure Signing in app/build.gradle.kts

Add to `android { signingConfigs { ... } }`:

```kotlin
signingConfigs {
    create("release") {
        storeFile = file(project.findProperty("KEYSTORE_PATH") as String)
        storePassword = project.findProperty("KEYSTORE_PASSWORD") as String
        keyAlias = project.findProperty("KEY_ALIAS") as String
        keyPassword = project.findProperty("KEY_PASSWORD") as String
    }
}
buildTypes {
    release {
        signingConfig = signingConfigs.getByName("release")
        // ...
    }
}
```

Add to `android/local.properties` (never commit this file):

```properties
KEYSTORE_PATH=/path/to/campaignmasta-release.jks
KEYSTORE_PASSWORD=your_store_password
KEY_ALIAS=campaignmasta
KEY_PASSWORD=your_key_password
```

### 4.3 Build the Release APK

```bash
cd android
./gradlew assembleRelease
```

Output: `app/build/outputs/apk/release/app-release.apk`

Or build an AAB for Google Play:

```bash
./gradlew bundleRelease
```

---

## 5. Network Setup for Digicel / bmobile Deployment in PNG

PNG campaign field operations often run on Digicel or bmobile 4G data.
The app is designed to work **offline-first** so data entry is never blocked.

### 5.1 LAN / WiFi Hotspot Setup (recommended for election day)

1. Set up a laptop/server running Django at a fixed IP on a portable WiFi hotspot
2. Configure `BASE_URL=http://192.168.x.x:8000/` in `local.properties`
3. All team member phones connect to the same hotspot
4. Sync happens automatically when phones are on the hotspot network

### 5.2 Internet Deployment (campaign HQ server)

1. Deploy Django to a VPS or cloud server (AWS Lightsail, DigitalOcean recommended)
2. Configure a domain or static IP
3. Set `BASE_URL=https://yourdomain.com/` in `local.properties`
4. Use HTTPS (SSL certificate via Let's Encrypt)
5. In `settings.py`, add your server domain to `ALLOWED_HOSTS`
6. Disable `DEBUG` and set `SECURE_SSL_REDIRECT = True`

### 5.3 Reducing Data Usage

The sync uses incremental pull (`?updated_after=<iso_ts>`) so only changed
records are downloaded. On Digicel/bmobile, the default 15-minute periodic
sync keeps data usage minimal (typically <100 KB per cycle after initial sync).

---

## 6. How the Sync Works

### Architecture

```
Android Device                          Django Server
─────────────────────────────────────   ────────────────────────────
UI → ViewModel → Repository             /api/sync/push/
         ↓                              /api/supporters/
      Room DB (local)                   /api/messages/
         ↓                              /api/ward-profiles/
    SyncQueue table                     ... etc
         ↓
    SyncWorker (WorkManager)
         ↓
    Retrofit → API calls
```

### Offline-First Flow

1. **User creates a supporter** → saved to Room immediately with `syncStatus = PENDING`
2. A `SyncQueueEntity` row is inserted with the JSON payload
3. UI updates instantly from Room (user never waits for network)
4. When network reconnects, `NetworkMonitor.NetworkCallback` fires
5. `SyncWorker.enqueueImmediateSync()` is called — WorkManager schedules a one-time job
6. `SyncWorker.doWork()` runs:
   a. **Push phase**: reads all `PENDING` SyncQueue items, sends them to `/api/sync/push/`
   b. Server returns `{results: [{local_id, server_id, status}]}`
   c. Room entities are updated with `serverId` from server; `syncStatus = SYNCED`
   d. **Pull phase**: incremental GET requests with `?updated_after=<last_sync_ts>`
   e. `last_sync_ts` per entity stored in DataStore Preferences

### Conflict Resolution

- **Server wins on pull**: incoming server data always overwrites local data of the same `serverId`
- **Local wins on push**: if a push fails (e.g. validation error), the item retries up to 5 times
- After 5 failures, `status = FAILED` — the item stays in the queue and is visible in logs

### WorkManager Schedule

- **Periodic sync**: every 15 minutes when network is connected (`NETWORK_CONNECTED` constraint)
- **Immediate sync**: triggered by `NetworkCallback.onAvailable()` when network comes back
- **Backoff**: exponential, starting at 30 seconds, capped at 5 retries

### SyncQueue Status Flow

```
PENDING → IN_FLIGHT → DONE (success)
                   └→ FAILED (retry count incremented)
```

---

## 7. Environment Variables / Secrets Management

### Android

Store all secrets in `local.properties` (never committed to git):

| Key | Description |
|-----|-------------|
| `sdk.dir` | Android SDK path (auto-generated) |
| `BASE_URL` | Django API base URL |
| `KEYSTORE_PATH` | Path to release keystore |
| `KEYSTORE_PASSWORD` | Keystore password |
| `KEY_ALIAS` | Key alias in keystore |
| `KEY_PASSWORD` | Key password |

`local.properties` is listed in `.gitignore` by default.

### Django

`settings.py` reads everything from environment variables (no extra dependency).
Copy `.env.example` to `.env` and set:

```bash
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=your-production-secret-key          # required when DEBUG is off
DJANGO_ALLOWED_HOSTS=campaign.webmasta.com.pg,www.campaign.webmasta.com.pg
DJANGO_CSRF_TRUSTED_ORIGINS=https://campaign.webmasta.com.pg

# Postgres (omit all DB_* to fall back to the bundled SQLite database)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=campaignmasta
DB_USER=campaignmasta
DB_PASSWORD=...
DB_HOST=localhost
DB_PORT=5432
```

The provided `Dockerfile` + `entrypoint.sh` run migrations and serve via gunicorn
with WhiteNoise-served static files. When `DJANGO_DEBUG=false`, the security
headers (HSTS, secure cookies, SSL redirect) are enabled automatically.

---

## 8. Production Deployment Checklist

### Django Server

- [ ] `DEBUG = False` in settings
- [ ] `SECRET_KEY` changed from dev default
- [ ] `ALLOWED_HOSTS` set to production domain(s)
- [ ] Database: PostgreSQL recommended (not SQLite)
- [ ] `python manage.py collectstatic` run
- [ ] HTTPS configured (nginx + certbot)
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] Gunicorn or uWSGI as WSGI server
- [ ] Systemd service configured for auto-restart
- [ ] Backups configured for database

### Android App

- [ ] `BASE_URL` points to production HTTPS endpoint
- [ ] Release signing configured with a secure keystore
- [ ] `isMinifyEnabled = true` in release build type
- [ ] ProGuard rules tested — DTOs and Room entities kept
- [ ] App installed on all field team devices before election day
- [ ] Test offline mode: airplane mode + add supporter + reconnect = auto-sync
- [ ] Test background sync: lock phone for 15 min + check server for new data
- [ ] Verify auth token persists across app restart (DataStore)
- [ ] Confirm no unencrypted HTTP traffic in release build (android:usesCleartextTraffic)

### Pre-Election Day

- [ ] Full sync run on all devices before going to field
- [ ] All polling locations loaded in app
- [ ] All scrutineer accounts created in Django admin
- [ ] All scrutineers have logged in at least once (token saved)
- [ ] Hotspot setup tested if using local network deployment
- [ ] Battery packs and charging cables distributed with devices
