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
git clone <your-repository-url>
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
pip install django
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

## CRUD Operations

CRUD functionality is provided through the **Django Admin interface**.

1. Start the server and navigate to `http://127.0.0.1:8000/admin/`
2. Log in with the superuser credentials created above
3. The following models are available for full Create, Read, Update, and Delete operations:

| Model | Description |
|---|---|
| **Creator** | Platform users with email, display name, and token balance |
| **Library** | Personal song library belonging to each Creator |
| **Song** | Songs stored in a Library, with genre, vocal style, occasion, and visibility |
| **Generation Job** | Music generation requests submitted by a Creator |

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
    └── migrations/
        └── 0001_initial.py
```
