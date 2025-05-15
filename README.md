# Focus Buddy

**Focus Buddy** is a modern, gamified productivity companion that helps you build—and sustain—healthy study and work habits. Built with Vue 3 and FastAPI (Beanie + MongoDB), it combines task-driven “study sessions” with progress tracking, streaks, challenges, and even a little in-app economy to keep you motivated.

---

## 🚀 Key Features

- **Custom Study Sessions**  
  Build a session by breaking your work into timed “tasks” (e.g. 15 min reading, 30 min coding), then start/pause/resume with a live countdown and visual progress ring.

- **Real-Time Heartbeat & Pause Tracking**  
  The frontend pings the backend every 10 seconds to keep your session alive, and tracks total paused time so you never lose focus metrics.

- **Automatic Stats & Streaks**  
  Every session feeds into your daily/weekly/monthly focus totals and study-day streaks; streak-based multipliers and rewards keep you coming back.

- **Challenges & Milestones**  
  Tackle community or custom challenges (e.g. “Focus 5 hours this week”) and unlock milestone tiers—earn coins for every accomplishment.

- **In-App Shop & Economy**  
  Spend coins in the Shop on fun “rewards” (stickers, themes, mini-games) to celebrate progress or unlock premium features.

- **Website Blocking & Phone Lock**  
  Block distracting websites and optionally trigger a guided phone-lock mode to enforce deep focus.

- **Containerized Deployments**  
  Fully Dockerized frontend and backend services, with environment configuration via `.env`—ready for AWS, Azure, or local development.

---

## 🛠️ Tech Stack

- **Frontend**: Vue 3 ‣ Pinia for state management ‣ Vue Router ‣ Tailwind CSS  
- **Backend**: FastAPI ‣ Beanie ODM (MongoDB) ‣ Pydantic models  
- **Auth & Security**: OAuth2 / JWT  
- **DevOps**: Docker Compose, CI/CD ready, linting & type-checking  

---

## 🔧 Getting Started

1. **Clone & configure**  
   ```bash
   git clone https://github.com/yourorg/focus-buddy.git
   cd focus-buddy
   cp .env.example .env
   # fill in your MongoDB URI, JWT_SECRET, etc.
