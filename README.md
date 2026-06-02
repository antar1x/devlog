## Database Schema

```mermaid
erDiagram
    USER ||--|| PROFILE : has
    USER ||--o{ TOPIC : owns
    USER ||--o{ LOG_SESSION : writes
    USER ||--o{ GOAL : sets

    TOPIC ||--o{ LOG_SESSION : used_in
    TOPIC ||--o{ GOAL : targets

    USER {
        int id PK
        string username
        string email
        string password
    }

    PROFILE {
        int id PK
        int user_id FK
        text bio
        bool is_public
        string avatar
    }

    TOPIC {
        int id PK
        int user_id FK
        string name
    }

    LOG_SESSION {
        int id PK
        int user_id FK
        int topic_id FK
        date date
        int duration_minutes
        text notes
        int difficulty
    }

    GOAL {
        int id PK
        int user_id FK
        int topic_id FK
        string title
        int target_hours
        date deadline
        bool is_completed
    }
```


# DevLog

DevLog is a Django web application for tracking developer learning progress.

Users can create topics, log study sessions, set learning goals, and view progress statistics on a dashboard. The app also includes public developer profiles, so users can share their learning activity, goals, and recent sessions as a portfolio signal.

## Features

- User registration, login, logout, and profile settings
- Study topics management
- Study session CRUD
- Learning goals with progress tracking
- Dashboard with total sessions, minutes, hours, and topic statistics
- Public profile page with learning stats
- Responsive dark UI
- Avatar upload support

## Tech Stack

- Python
- Django
- SQLite
- HTML / CSS