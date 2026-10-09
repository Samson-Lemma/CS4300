# CS4300 Homework 2 - Movie Theater Booking

This project is a Django and Django REST Framework application for viewing movies, booking seats, and viewing booking history.

## Features

- View available movies
- View and manage seats
- Book available seats
- View personal booking history
- REST API for movies, seats, and bookings
- Bootstrap-based user interface
- Authentication for booking functionality
- Unit and integration tests
- Behavior-driven tests using Behave

## Project Structure

```text
homework2/
├── bookings/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── features/
│   ├── steps/
│   ├── environment.py
│   └── movie_booking.feature
├── movie_theater_booking/
├── manage.py
├── requirements.txt
└── README.md
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv homework2_env --system-site-packages
source homework2_env/bin/activate
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run migrations:

```bash
python3 manage.py migrate
```

Create a superuser:

```bash
python3 manage.py createsuperuser
```

## Running the Application

Start the development server:

```bash
python3 manage.py runserver 0.0.0.0:3000
```

## Web Interface

- `/` - Movie listings
- `/history/` - Booking history
- `/movies/<id>/book/` - Seat booking

## REST API

- `/api/movies/`
- `/api/seats/`
- `/api/bookings/`

## Testing

Run Django unit and integration tests:

```bash
python3 manage.py test bookings -v 2
```

Run Behave BDD tests:

```bash
behave
```

Run coverage:

```bash
coverage erase
coverage run --source=bookings manage.py test bookings
coverage report -m
```

Current test coverage is approximately 98%.

## Deployment

Render URL:

https://cs4300-movie-theater.onrender.com

## AI Usage

AI was used to help clarify the assignment requirements, explain Django concepts, troubleshoot errors, and provide guidance when I was unsure how to structure or test parts of the application. I reviewed and tested the work before including it in the final project.