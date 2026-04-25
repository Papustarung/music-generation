# Music Generation App

A Django-based domain layer implementation for a music generation platform. This project models the core domain entities including Creators, Songs, Libraries, and Generation Jobs.

---

## Requirements

- Python 3.10+
- pip

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Papustarung/music-generation.git
cd music_generation
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (for Django Admin access)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 6. Run the development server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

---

## CRUD Operations (For exercise 3 only)

### HTML Interface (Function-Based Views)

Full CRUD is available via plain HTML pages at the following URLs. No login required in development.

| Entity | List | Create | Detail | Edit | Delete |
|---|---|---|---|---|---|
| **Creator** | `/creators/` | `/creators/create/` | `/creators/<id>/` | `/creators/<id>/edit/` | `/creators/<id>/delete/` |
| **Library** | `/libraries/` | `/libraries/create/` | `/libraries/<id>/` | `/libraries/<id>/edit/` | `/libraries/<id>/delete/` |
| **Song** | `/songs/` | `/songs/create/` | `/songs/<id>/` | `/songs/<id>/edit/` | `/songs/<id>/delete/` |
| **Generation Job** | `/jobs/` | `/jobs/create/` | `/jobs/<id>/` | `/jobs/<id>/edit/` | `/jobs/<id>/delete/` |

Visiting `http://127.0.0.1:8000/` redirects to `/creators/`. A navigation bar links to all four entity lists.

**Recommended creation order** (to satisfy foreign-key constraints):
1. Create a **Creator**
2. Create a **Library** — select the Creator created above
3. Create a **Song** — select the Library created above
4. Create a **Generation Job** — select a Creator (and optionally a Song)

[CRUD functionality demo (API)](https://youtu.be/H5vxge5HoOg)

### Django Admin Interface

1. Start the server and navigate to `http://127.0.0.1:8000/admin/`
2. Log in with the superuser credentials created above
3. The following models are available for full Create, Read, Update, and Delete operations:

| Model | Description |
|---|---|
| **Creator** | Platform users with email, display name, and token balance |
| **Library** | Personal song library belonging to each Creator |
| **Song** | Songs stored in a Library, with genre, vocal style, occasion, and visibility |
| **Generation Job** | Music generation requests submitted by a Creator |

[CRUD functionality demo (Admin)](https://youtu.be/h37pt2xlssQ)

---

## Song Generation — Strategy Pattern

Generation is implemented using the **Strategy** design pattern, allowing the AI backend to be swapped without changing the rest of the application.

### Architecture

```
SongGeneratorStrategy (abstract base — base.py)
├── MockSongGeneratorStrategy   (mock_strategy.py)   ← no network, instant result
└── SunoSongGeneratorStrategy   (suno_strategy.py)   ← calls api.sunoapi.org

SongGeneratorFactory (factory.py)  ← reads GENERATOR_STRATEGY from .env
GenerationService   (service.py)   ← orchestrates the full job lifecycle
```

| File | Role |
|---|---|
| `core/generation/strategies/base.py` | `SongGeneratorStrategy` ABC + `GenerationRequest` / `GenerationResult` dataclasses |
| `core/generation/strategies/mock_strategy.py` | Returns a static MP3 instantly — no API key required |
| `core/generation/strategies/suno_strategy.py` | POSTs to Suno API, receives webhook callback, parses clips |
| `core/generation/factory.py` | Reads `GENERATOR_STRATEGY` env var and returns the right strategy |
| `core/generation/service.py` | Runs the full QUEUED → GENERATING → SAVING → COMPLETED lifecycle |

---

### Running in Mock Mode

Mock mode requires no API key and completes instantly.

**1. Set environment variable**

In your `.env` file:
```
GENERATOR_STRATEGY = mock
```

**2. Start the server**
```bash
python manage.py runserver
```

**3. Generate a song**

Go to `http://127.0.0.1:8000/jobs/create/`, fill in the form, and submit.  
The job will complete immediately and the song will appear in your library with a static placeholder audio file.

**Example log output (mock):**
```
INFO Suno webhook: callbackType=... (not called in mock mode)
# Job transitions: QUEUED → GENERATING → SAVING → COMPLETED
```

---

### Running in Suno Mode

**1. Obtain a Suno API key**

Register at [api.sunoapi.org](https://api.sunoapi.org) and copy your API key.

**2. Configure `.env`**

```
GENERATOR_STRATEGY = suno
SUNO_API_KEY = <your-key-here>
SUNO_CALLBACK_URL = https://<your-ngrok-subdomain>.ngrok-free.app/jobs/webhook/suno/
```

> **Never commit your `.env` file.** It is excluded by `.gitignore`.  
> Use `.env.example` as a safe template to share with collaborators.

**3. Expose localhost with ngrok** (required for Suno's callback)

```bash
ngrok http 8000
```

Copy the `https://xxxx.ngrok-free.app` URL into `SUNO_CALLBACK_URL` in `.env`.

**4. Start the server**
```bash
python manage.py runserver
```

**5. Generate a song**

Go to `/jobs/create/`, fill in the form, and submit.  
The job starts asynchronously. Status updates every 5 seconds on the detail page.

**Example log output (Suno):**
```
INFO Suno webhook: callbackType=text job=5
INFO Suno webhook: callbackType=first job=5
INFO Suno webhook: callbackType=complete job=5
INFO Suno webhook: job=5 audio_url=https://tempfile.aiquickdraw.com/r/....mp3
INFO Suno webhook: job 5 completed successfully
```

---

## Domain Model

The domain layer consists of the following entities and enumerations:

### Entities

- **Creator** — `email`, `displayName`, `tokenAmount`
- **Library** — belongs to one Creator (one-to-one)
- **Song** — `title`, `story`, `genre`, `vocalStyle`, `occasion`, `lyrics` (optional), `visibility`, `audioLocation`; belongs to a Library
- **GenerationJob** — `status`, `requestedAt`, `title`, `story`, `genre`, `vocalStyle`, `occasion`, `lyrics` (optional); linked to a Creator and optionally to a Song

### Enumerations

- **Genre**: JAZZ, ROCK, POP, HIPHOP, CLASSICAL, EDM, RNB, FOLK, METAL, OTHER
- **VocalStyle**: MALE, FEMALE, DUET, INSTRUMENTAL, RAP, OTHER
- **Occasion**: BIRTHDAY, WEDDING, STUDY, WORKOUT, PARTY, RELAX, OTHER
- **Visibility**: PRIVATE, SHARED
- **JobStatus**: QUEUED, GENERATING, COMPLETED, FAILED

---

## Project Structure

```
music_generation/
├── manage.py
├── db.sqlite3
├── music_generation/       # Project settings
│   ├── settings.py
│   └── urls.py
└── core/                   # Main application
    ├── admin.py
    ├── forms.py            # ModelForms for each entity
    ├── urls.py
    ├── models/
    │   ├── entities/       # Domain entities
    │   │   ├── creator.py
    │   │   ├── library.py
    │   │   ├── song.py
    │   │   └── generation_job.py
    │   └── enum/           # Domain enumerations
    │       ├── genre.py
    │       ├── vocal_style.py
    │       ├── occasion.py
    │       ├── visibility.py
    │       └── job_status.py
    ├── views/
    │   ├── creator_views.py
    │   ├── library_views.py
    │   ├── song_views.py
    │   └── generation_job_views.py
    ├── templates/
    │   ├── core/
    │   │   └── base.html           # Shared base with navigation
    │   ├── creator/
    │   │   ├── list.html
    │   │   ├── detail.html
    │   │   ├── form.html           # Shared create/update form
    │   │   └── confirm_delete.html
    │   ├── library/                # Same 4 templates
    │   ├── song/                   # Same 4 templates
    │   └── generation_job/         # Same 4 templates
    └── migrations/
        └── 0001_initial.py
```
