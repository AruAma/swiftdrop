# SwiftDrop 🚀

**SwiftDrop** is a fast and secure anonymous file-sharing service built with Django and Tailwind CSS.  
Perfect for sending personal files without registration or tracking.

## 🔐 Features

- Anonymous user registration and login
- File upload and download functionality
- Clean, responsive UI (Tailwind-based)
- Simple token-based authentication
- REST API support with `TokenAuthentication`

## 🚀 Getting Started

```bash
git clone git@github.com:AruAma/swiftdrop.git
cd swiftdrop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

📦 Dependencies
	•	Django 5.2
	•	Django REST Framework
	•	Tailwind CSS (via CDN)
	•	SQLite (default)

📁 Project Structure
templates/
├── base.html
├── login.html
├── register.html
├── messages.html
├── files.html
