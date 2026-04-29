# 🌙 Dreamscape

> *A space where dreams live — not just a list, but a sky full of possibilities.*

Dreamscape is a personal wishlist and dream-tracking service. Active wishes float like clouds above you, always visible, always within reach. Fulfilled dreams become stars — glowing reminders of everything you've already achieved.

The idea came from a personal need: there was no comfortable place to gather life goals in one spot, something that would actually inspire rather than just remind. Todo lists felt too utilitarian. Dreamscape is built to feel like a space, not a tool.

---

## ✨ Features

- **JWT Authentication** — secure registration and login with token-based auth
- **Wish Management** — create, edit, delete and track your dreams
- **Categories** — organize wishes by type (travel, gift, personal and more)
- **Visibility Control** — keep wishes private, share by link, or make them public
- **Status Tracking** — mark wishes as dreaming, in progress, or done
- **User Profiles** — avatar, bio, and background image support
- **Image Upload** — attach images to wishes
- **Public API** — fully documented REST API ready for any frontend

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django, Django REST Framework |
| Auth | JWT via djangorestframework-simplejwt |
| Database | PostgreSQL |
| Media | Pillow, WhiteNoise |
| Documentation | drf-spectacular (Swagger UI) |
| Testing | pytest, pytest-django |
| Infrastructure | Docker, docker-compose |
| Deploy | Railway |

---

## 🚀 Quick Start

### Requirements
- Python 3.13
- PostgreSQL
- Docker (optional)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/nozilis/dreamscape.git
cd dreamscape

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (see .env.example)
cp .env.example .env

# Apply migrations
python manage.py migrate

# Run the server
python manage.py runserver
```

### Docker Setup

```bash
docker compose up --build
```

---

## 🔑 Environment Variables

Create a `.env` file based on `.env.example`:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=dreamscape_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
SWAGGER_PUBLIC=True
```

---

## 📖 API Documentation

Interactive Swagger UI available at:
```
/api/schema/swagger-ui/
```

---

## 📡 API Examples

### Register
```http
POST /register/
Content-Type: application/json

{
    "username": "dreamer",
    "email": "dreamer@example.com",
    "password": "securepassword",
    "password_confirm": "securepassword"
}
```

**Response `201`:**
```json
{
    "id": 1,
    "username": "dreamer",
    "email": "dreamer@example.com",
    "access": "eyJ...",
    "refresh": "eyJ..."
}
```

---

### Get Token
```http
POST /api/token/
Content-Type: application/json

{
    "username": "dreamer",
    "password": "securepassword"
}
```

**Response `200`:**
```json
{
    "access": "eyJ...",
    "refresh": "eyJ..."
}
```

---

### Create Wish
```http
POST /wishes/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Visit Japan",
    "description": "Tokyo, Kyoto, Osaka",
    "category_id": 1,
    "visibility": "public",
    "status": "dreaming"
}
```

**Response `201`:**
```json
{
    "title": "Visit Japan",
    "description": "Tokyo, Kyoto, Osaka",
    "is_done": false,
    "status": "dreaming",
    "visibility": "public",
    "category": {
        "id": 1,
        "title": "Travel"
    }
}
```

---

### Get Wishes
```http
GET /wishes/?user_id=1
Authorization: Bearer <access_token>
```

Owners see all their wishes. Guests see only `public` and `link` wishes.

---

### Update Profile
```http
PATCH /user_profile/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

bio: "Living to dream, dreaming to live"
avatar: <file>
```

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🌍 Live Demo

API: `dreamscape-production-4f38.up.railway.app`  
Swagger UI: `dreamscape-production-4f38.up.railway.app/api/schema/swagger-ui/`

---

## 📝 Status

Backend — complete. Frontend — in development.

The visual concept: active wishes float as clouds in the daytime sky. Fulfilled dreams become stars at night — glowing proof of everything you've made real.

---

## 👤 Author

**NoZiliS** — [github.com/nozilis](https://github.com/nozilis)