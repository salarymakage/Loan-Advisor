# Django Project Setup Guide

This guide will help you set up a **Django** project quickly.

## **Prerequisites**

Before starting, ensure you have:

- Python (>= 3.8) installed
- pip and virtualenv installed
- PostgreSQL/MySQL (optional for production)
- Git (for version control)

---

## **1. Create and Activate a Virtual Environment**

```sh
# Create a virtual environment
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

---

## **2. Install Django**

```sh
pip install django
pip install -r requirements.txt
```

To verify the installation:

```sh
django-admin --version
```

---

## **3. Create a Django Project**

```sh
django-admin startproject myproject
cd myproject
```

---

## **4. Run the Development Server**

```sh
python manage.py runserver
```

Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

---

## **5. Create a Django App**

```sh
python manage.py startapp myapp
```

Then, add `myapp` to the `INSTALLED_APPS` list in `settings.py`.

---

## **6. Apply Migrations**

```sh
python manage.py migrate
```

This initializes the database.

---

## **7. Create a Superuser (Admin Panel Access)**

```sh
python manage.py createsuperuser
```

Follow the prompts to set up an admin user.

---

## **8. Setup ****`.env`**** for Environment Variables**

Install **django-environ**:

```sh
pip install django-environ
```

Create a `.env` file:

```sh
touch .env
```
