"""Behave step definitions for movie booking features."""

from behave import given, then, when
from django.contrib.auth.models import User
from django.test import Client

from bookings.models import Booking, Movie, Seat


@given('a user named "{username}" exists')
def create_user(context, username):
    """Create a test user."""
    User.objects.create_user(
        username=username,
        password="password123",
    )


@given('a movie named "{title}" exists')
def create_movie(context, title):
    """Create a test movie."""
    Movie.objects.get_or_create(
        title=title,
        defaults={
            "description": "Test movie description.",
            "release_date": "2014-11-07",
            "duration": 169,
        },
    )


@given('an available seat named "{seat_number}" exists')
def create_seat(context, seat_number):
    """Create an available theater seat."""
    Seat.objects.get_or_create(
        seat_number=seat_number,
        defaults={
            "is_booked": False,
        },
    )


@given('I am logged in as "{username}"')
def login_user(context, username):
    """Log the user into the Django test client."""
    context.client = Client()

    logged_in = context.client.login(
        username=username,
        password="password123",
    )

    assert logged_in


@given(
    '"{username}" has booked seat "{seat_number}" '
    'for "{movie_title}"'
)
def create_existing_booking(
    context,
    username,
    seat_number,
    movie_title,
):
    """Create an existing booking for a user."""
    user = User.objects.get(username=username)
    movie = Movie.objects.get(title=movie_title)
    seat = Seat.objects.get(seat_number=seat_number)

    Booking.objects.create(
        user=user,
        movie=movie,
        seat=seat,
    )

    seat.is_booked = True
    seat.save()


@when("I visit the movie list")
def visit_movie_list(context):
    """Visit the movie listing page."""
    context.client = Client()
    context.response = context.client.get("/")


@when('I book seat "{seat_number}" for "{movie_title}"')
def book_seat(context, seat_number, movie_title):
    """Submit the seat booking form."""
    movie = Movie.objects.get(title=movie_title)
    seat = Seat.objects.get(seat_number=seat_number)

    context.response = context.client.post(
        f"/movies/{movie.id}/book/",
        {
            "seat_id": seat.id,
        },
    )


@when("I visit my booking history")
def visit_history(context):
    """Visit the current user's booking history."""
    context.response = context.client.get("/history/")


@then('I should see "{text}"')
def response_contains(context, text):
    """Verify that text appears in the response."""
    page = context.response.content.decode()

    assert text in page


@then('I should see seat "{seat_number}"')
def response_contains_seat(context, seat_number):
    """Verify that a seat number appears in the response."""
    page = context.response.content.decode()

    assert seat_number in page


@then("the booking should exist")
def booking_exists(context):
    """Verify that a booking exists."""
    assert Booking.objects.exists()


@then('seat "{seat_number}" should be marked booked')
def seat_is_booked(context, seat_number):
    """Verify that the selected seat is booked."""
    seat = Seat.objects.get(
        seat_number=seat_number
    )

    assert seat.is_booked is True