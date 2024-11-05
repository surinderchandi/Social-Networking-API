**Social Networking API**

Overview

This is a scalable, secure, and efficient social networking API built with Django Rest Framework (DRF), PostgreSQL, Redis for caching, and JWT for authentication. The API supports user authentication, role-based access control (RBAC), friend request management, user search, activity logging, and more.

Table of Contents
Installation
Project Structure
Environment Variables
API Endpoints
Authentication
Friend Request Management
User Search
Caching & Optimization
Docker Setup
Testing
Contributing
License

**Installation**
Prerequisites
Python 3.9+
PostgreSQL
Redis
Docker (for containerization)


**Project Structure**

social-network-api

│
├── Users                   # Users app for the project

│   ├── migrations/          # Migrations for the app

│   ├── serializers.py       # Users serializers

│   ├── urls.py              # Users routes

│   ├── views.py             # Users view logic

│
├── friendships/             # friendships app for the project

│   ├── migrations/          # Migrations for the app

│   ├── serializers.py       # friendships serializers

│   ├── urls.py              # friendships routes

│   ├── views.py             # friendships view logic

│
├── social_network/          # Main project directory

│   ├── settings.py          # Project settings

│   ├── urls.py              # Project routes

│
├── Dockerfile               # Docker configuration

├── docker-compose.yml       # Docker-compose for multi-container setup

├── README.md                # Project documentation

├── requirements.txt         # Python dependencies

└── manage.py                # Django management


Postman Collection

A Postman collection for all API endpoints is provided for quick evaluation. Download and import the collection here.
https://api.postman.com/collections/38386895-2e734541-fcec-4ff1-92d3-d91f1f8accfe?access_key=PMAT-01J86T0W8R7T0R0CQQ944K640D



