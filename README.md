# Geode

A smart schedule optimizer for university students. Geode takes your required courses and personal preferences, generates every valid schedule, and surfaces the best options — so you can spend less time wrestling with registration and more time on what matters.

---

## What It Does

University registration is stressful. Sections fill up, time slots conflict, and building the "perfect" schedule by hand is tedious. Geode automates that process.

You tell Geode:
- Which courses you need to take
- What your schedule should *feel* like (compact, spacey, grouped by day, spread out, etc.)

Geode handles the rest — finding every conflict-free schedule and ranking them by how well they match your preferences.

---

## Features

- **Schedule Optimizer** — generates all valid, conflict-free schedules from your selected courses and sections
- **Preference-Based Scoring** — rank schedules by compactness, day grouping, breathing room, subject adjacency, and more
- **"Best Effort" Mode** — always returns the best available option even when ideal constraints can't be fully met
- **Course Watchlist** — monitor seat availability and waitlist status for sections you care about
- **Notifications** — get alerted via email, SMS, or in-app when a watched section opens up
- **Dashboard** — view your saved schedules, watchlisted sections, and upcoming registration windows

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, React Query |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy + Alembic |
| Background Jobs | APScheduler |
| Notifications | SendGrid (email), Twilio (SMS) |
| Auth | JWT (access + refresh tokens) |
| Deployment | Vercel (frontend), Render/Railway (backend) |

---

## Project Structure

```
geode/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI route handlers
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── optimizer/    # Schedule generation + scoring engine
│   │   ├── scraper/      # University portal integration
│   │   ├── notifications/# Email, SMS, in-app dispatch
│   │   └── core/         # Config, auth, database setup
│   ├── alembic/          # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── api/          # React Query API calls
│   └── package.json
└── README.md
```

---

## The Optimizer

The core of Geode is a **constraint satisfaction + scoring engine**.

1. **Generate** — uses backtracking to build all conflict-free schedule combinations, pruning invalid branches early
2. **Score** — each valid schedule is scored against the user's preferences (compactness, day balance, adjacency, etc.)
3. **Rank** — the top N schedules are returned, ordered by score

User preferences are treated as **soft constraints** (they affect scoring) while time conflicts are **hard constraints** (they eliminate a schedule entirely). This means Geode always returns a result — the best it can do with what's available.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start the API
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Auto-generated docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/geode

# Auth
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Notifications
SENDGRID_API_KEY=your-sendgrid-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=+1234567890
```

---

## Roadmap

- [ ] Core schedule optimizer engine
- [ ] University portal scraper
- [ ] User auth (register, login, JWT)
- [ ] Course watchlist + seat monitoring
- [ ] Notification dispatch (email, SMS, in-app)
- [ ] Schedule dashboard (React frontend)
- [ ] Preference UI (sliders/ranking for optimizer settings)
- [ ] Multi-university support

---

## Contributing

This project is in early development. If you'd like to contribute, open an issue first to discuss what you'd like to change.

---

## License

MIT