# ALX Backend: GraphQL CRM with Scheduled Stock Alerts

This project demonstrates how to build a simple CRM system using Django and GraphQL. It includes features like product inventory management, GraphQL mutations, and scheduled background jobs using `django-crontab`.

---

## 🚀 Features

- 📦 **Product Stock Tracking** via Django ORM
- 🔁 **GraphQL API** using `graphene-django`
- ⚙️ **Scheduled Cron Job** for low-stock restocking
- 📄 **Logging** of restocking activity
- 💬 **Custom GraphQL Mutation** to bulk update products

---

## 🛠 Technology Stack

- Python 3.7
- Django 3.x
- Graphene-Django
- django-crontab
- Redis (used for Celery tasks if extended)
- SQLite (default, can be swapped with PostgreSQL)

---

## 📂 Project Structure

