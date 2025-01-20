# 📚 Python Backend Dependencies Overview

This document outlines the dependencies used in the Python backend project, their purposes, and hosting details. These dependencies ensure smooth development and execution of the backend services.

## 🔨 Dependencies

### Core Framework

- **`Flask==3.1.0`**: A lightweight WSGI web application framework for building backend services and APIs.

### CORS and Security

- **`Flask-Cors==5.0.0`**: Enables Cross-Origin Resource Sharing (CORS) for handling requests from different origins.
- **`Flask-JWT-Extended==4.6.0`**: Adds JSON Web Token (JWT) support for securing API endpoints.

### API Documentation and Marshaling

- **`flask-smorest==0.45.0`**: Simplifies API documentation and validation with OpenAPI (Swagger) support.
- **`marshmallow==3.23.1`**: Handles object serialization and deserialization with schemas.

### Database Management

- **`Flask-SQLAlchemy==3.1.1`**: Simplifies interaction with SQL databases using the SQLAlchemy ORM.
- **`mysql-connector-python==9.1.0`**: Provides connectivity to MySQL databases.
- **`mysqlclient==2.2.6`**: Another MySQL database interface for Python.
- **`SQLAlchemy==2.0.36`**: A powerful ORM for managing database models and queries.

### Security Utilities

- **`itsdangerous==2.2.0`**: Provides cryptographic signing utilities for secure token generation.
- **`passlib==1.7.4`**: A password hashing library to secure user credentials.

### Environment Configuration

- **`python-dotenv==1.0.1`**: Loads environment variables from a `.env` file for secure configuration management.

### Other Utilities

- **`packaging==24.2`**: Handles versioning and package requirements.
- **`pillow==11.0.0`**: Supports image processing tasks.
- **`PyJWT==2.10.0`**: Creates and validates JSON Web Tokens (JWT).

## 🏠 Hosting Details

### 🌐 API Hosting

The backend is hosted on **Railway**, a platform offering seamless deployment for web applications.

### 📅 Database Hosting

The MySQL database is hosted on **Aiven**, providing secure and managed database services to ensure data integrity and protection.


## 🌟 Key Features

- **Secure API**: JWT authentication ensures endpoint security.
- **Flexible Deployment**: Easily scalable deployment on Railway.
- **Managed Database**: Aiven ensures high availability and data security.
- **Comprehensive Validation**: Marshmallow and flask-smorest streamline API validation and documentation.

#
#
## 📸 API Documentation

Below is a snapshot of the Swagger API documentation showcasing the available endpoints and their details:

![screencapture-ibm-backend-final-project-production-up-railway-app-swagger-2024-12-31-17_35_37](https://github.com/user-attachments/assets/88a482e7-3e98-498b-8097-051c1c7260ee)

Feel free to contribute to this project and enhance its capabilities! 🚀