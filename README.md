# Admission Bazaar — Backend (Portal)

Django REST API + Jazzmin admin portal for Admission Bazaar.

## Stack

- Django 4.2
- Django REST Framework + JWT
- MySQL (PyMySQL)
- Jazzmin admin

## Local setup

1. Create and activate a virtualenv
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill values
4. Create MySQL database/user matching `App/settings.py`
5. `python manage.py migrate`
6. `python manage.py createsuperuser`
7. `python manage.py runserver`

## Useful URLs

- Admin: `/admin/`
- API docs: `/api/`
- Schema: `/schema/`
