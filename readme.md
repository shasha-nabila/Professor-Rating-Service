# Professor Rating Service

A RESTful web service for students to rate professors, developed as part of the Web Services and Web Data module at the University of Leeds. The system includes a Django-based backend API and a Python command-line client.

## 🌐 Live Service
Hosted at: [https://sc22snba.pythonanywhere.com](https://sc22snba.pythonanywhere.com)

## 📌 Features

### Backend (Django + Django REST Framework)
- User registration, login, logout (JWT authentication)
- View all modules and their associated professors
- View professor ratings (overall and module-specific)
- Submit ratings for professors in specific module instances
- Robust validation and error handling
- Admin dashboard for managing data

### Client (Python CLI)
- Command-driven interface for interacting with the API
- Secure session-based actions using stored JWT tokens
- Error handling for common failures (network, input, etc.)

## 🗄️ Database Schema

- **Professor**: `identifier`, `name`
- **Module**: `code`, `name`, `year`, `semester`, `professors`
- **Rating**: `user`, `professor`, `module`, `year`, `semester`, `score`

Relationships:
- Professors teach many modules (many-to-many)
- Users can rate professors once per module instance
- Ratings link professors, modules, and users

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/register/` | POST | Register a new user |
| `/api/login/` | POST | Authenticate user and receive JWT |
| `/api/logout/` | POST | Logout current user |
| `/api/modules/` | GET | List all module instances with professors |
| `/api/professors/` | GET | View all professors and their average ratings |
| `/api/average/<professor_id>/<module_code>/` | GET | View average rating of a professor in a module |
| `/api/rate/` | POST | Submit a rating for a professor in a module instance |

## 💻 Client Commands

```bash
register                           # Register a new user
login <URL>                        # Log in (e.g., https://sc22snba.pythonanywhere.com)
logout                             # Log out from session
list                               # List modules and professors
view                               # View professor ratings
average                            # View average rating for a professor in a module
rate                               # Submit a professor rating
exit                               # Exit the client

## 🧪 Usage

This is a command-line application. You must run client.py from the command line or terminal.
