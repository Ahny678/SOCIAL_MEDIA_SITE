# 🗣️NOW! 🗣️ 

## A TikTok-Inspired Social Media Platform Built with Django

---

### Introduction

**NOW!** is a minimal, TikTok-like social media application built using **Django** with **vanilla HTML/CSS** on the frontend. It features short video sharing, user profiles, likes/dislikes, and real-time commenting. This project is ideal for developers exploring **Django**, **pagination-based video feeds**, and **basic social interactions** in web apps.

This project showcases how to build a lightweight social media platform from scratch, with core features like:

* Infinite-scroll-like feed (via pagination)
* Like/dislike functionality for posts and comments
* User registration, login, and profile management
* Commenting and follower system
* Notifications for interactions

---

## 🏗️ Architecture Overview

```
NOW! Application Architecture
┌─────────────────────┐
│     Django App      │
│  (views, models)    │
└─────────────────────┘
       ▲       ▲
       │       │
       │       │
┌──────┴───┐ ┌──┴──────────┐
│  User    │ │ Video Posts │
│ Profile  │ │ + Comments  │
└──────┬───┘ └────┬────────┘
       │          │
       ▼          ▼
 ┌──────────────────────┐
 │   Notifications App  │
 └──────────────────────┘

Frontend:
- HTML templates (no JS framework)
- Pagination controls for navigating videos
- Static files: vanilla CSS
```

---

## 💻 Installation for Users

These steps will help users who just want to run the platform:

```bash
# Clone the repository
git clone https://github.com/your-username/NOW.git
cd NOW

# Create virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser (admin access)
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## 🧑‍💻 Installation for Developers (Contributors)

If you're looking to contribute or modify the application:

1. **Fork this repository**
2. Clone your fork and set up a virtual environment
3. Install dependencies using:

   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:

   ```bash
   python manage.py migrate
   ```
5. Run development server:

   ```bash
   python manage.py runserver
   ```

> Optional: Set up `.env` for any environment-specific configurations.

---

## 🤝 Contributor Guidelines

We welcome contributions! Here’s what we expect:

* **Code Quality**: Keep your code modular and follow Django best practices.
* **Commits**: Use clear, meaningful commit messages.
* **Issues**: Before starting work on a new feature or bug, create or comment on an issue to avoid duplication.
* **Pull Requests**:

  * One feature/fix per PR.
  * Include tests if relevant.
  * Add brief description of changes in PR body.

---

## 🐞 Known Issues & Limitations

1. **UI/UX**: The frontend is basic and lacks modern JS interactivity (no infinite scrolling or video autoplay).
2. **Reloads**: Navigating between video posts triggers full page reloads.
3. **No Video Processing**: There's no video compression, duration limits, or playback optimization.
4. **Security**: Basic auth protection exists, but further hardening (e.g., CSRF audits, input sanitization) is recommended.
5. **Notifications**: Implemented but not real-time (no WebSockets or polling).

---

## 📌 Future Improvements (TODOs)

* Migrate to Django REST Framework + React/Vue frontend
* Add real-time notifications using Django Channels
* Implement video preloading/infinite scroll
* UI/UX overhaul with Tailwind or Bootstrap
* Enhance mobile responsiveness

 
