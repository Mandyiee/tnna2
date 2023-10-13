# The Nigerian News API

## Introduction
This project is a Django-based web application that scrapes the top 10 Nigerian news websites, stores the data in a database, and provides this information through a RESTful API. Additionally, it utilizes Celery and Celery Beat to refresh the API every morning, ensuring that the news data is always up-to-date.

## Features
Scrape the top 10 Nigerian news websites.
Store the scraped data in a database.
Expose the scraped data as a RESTful API using Django REST framework.
Schedule and automate the data refresh process using Celery and Celery Beat.

## Prerequisites
Before you begin, ensure you have the following dependencies installed:

Python
Django
Scrapy
Celery
Celery Beat
Django REST framework


**Clone the Repository:**

```
git clone https://github.com/Mandyiee/tnna2.git
```

**Create a Virtual Environment:**

```
python -m venv venv
```

**Activate the Virtual Environment:**

```
source venv/bin/activate (Linux/OS X)
venv\Scripts\activate (Windows)
```

**Install Dependencies:**

```
pip install -r requirements.txt
```

**Apply Migrations:**

```
python manage.py migrate
```

**Start the Celery Beat Scheduler:**

```
celery -A tnna beat -l info
```

**Start the Celery Worker:**

```
celery -A tnna worker -l info
```

**Run the Development Server:**

```
python manage.py runserver
```

## Automated Data Refresh
- The Celery Beat scheduler is set up to automatically refresh the data every morning.
- You can configure the refresh schedule in the Celery Beat settings (tasks.py).

## Customization
You can customize this project to include additional features or modify the scraping logic as per your requirements. Explore the project's codebase to understand how it works and make necessary changes.
