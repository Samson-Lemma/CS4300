"""Unit and integration tests for the movie theater booking app."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Booking, Movie, Seat


class ModelTests(TestCase):
    """Test the application's database models."""

    def setUp(self):
        """Create shared model data."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

        self.movie = Movie.objects.create(
            title="Interstellar",
            description="Space exploration movie.",
            release_date="2014-11-07",
            duration=169,
        )

        self.seat = Seat.objects.create(
            seat_number="A1",
            is_booked=False,
        )

    def test_movie_string(self):
        """Movie string representation should be its title."""
        self.assertEqual(str(self.movie), "Interstellar")

    def test_seat_string(self):
        """Seat string representation should be its seat number."""
        self.assertEqual(str(self.seat), "A1")

    def test_booking_string(self):
        """Booking string should contain user, movie, and seat."""
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user,
        )

        self.assertEqual(
            str(booking),
            "testuser - Interstellar - A1",
        )

    def test_seat_defaults_to_available(self):
        """New seats should be available by default."""
        seat = Seat.objects.create(seat_number="A2")

        self.assertFalse(seat.is_booked)


class MovieAPITests(TestCase):
    """Integration tests for the movie API."""

    def setUp(self):
        """Create API client and movie."""
        self.client = APIClient()

        self.movie = Movie.objects.create(
            title="Interstellar",
            description="Space exploration movie.",
            release_date="2014-11-07",
            duration=169,
        )

    def test_list_movies(self):
        """GET /api/movies/ should return movie data."""
        response = self.client.get("/api/movies/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            "Interstellar",
        )

    def test_create_movie(self):
        """POST /api/movies/ should create a movie."""
        data = {
            "title": "Inception",
            "description": "A dream-based thriller.",
            "release_date": "2010-07-16",
            "duration": 148,
        }

        response = self.client.post(
            "/api/movies/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Movie.objects.filter(title="Inception").exists()
        )

    def test_retrieve_movie(self):
        """A single movie should be retrievable by ID."""
        response = self.client.get(
            f"/api/movies/{self.movie.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Interstellar",
        )


class SeatAPITests(TestCase):
    """Integration tests for the seat API."""

    def setUp(self):
        """Create API client and seat."""
        self.client = APIClient()

        self.seat = Seat.objects.create(
            seat_number="A1",
            is_booked=False,
        )

    def test_list_seats(self):
        """GET /api/seats/ should return available seat data."""
        response = self.client.get("/api/seats/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["seat_number"],
            "A1",
        )

    def test_create_seat(self):
        """POST /api/seats/ should create a seat."""
        data = {
            "seat_number": "A2",
            "is_booked": False,
        }

        response = self.client.post(
            "/api/seats/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Seat.objects.filter(seat_number="A2").exists()
        )


class BookingAPITests(TestCase):
    """Integration tests for booking API behavior."""

    def setUp(self):
        """Create users, movie, seats, and API client."""
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="student1",
            password="password123",
        )

        self.other_user = User.objects.create_user(
            username="student2",
            password="password123",
        )

        self.movie = Movie.objects.create(
            title="Interstellar",
            description="Space exploration movie.",
            release_date="2014-11-07",
            duration=169,
        )

        self.seat = Seat.objects.create(
            seat_number="A1",
            is_booked=False,
        )

        self.second_seat = Seat.objects.create(
            seat_number="A2",
            is_booked=False,
        )

    def test_booking_requires_authentication(self):
        """Unauthenticated users should not access bookings."""
        response = self.client.get("/api/bookings/")

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ],
        )

    def test_authenticated_user_can_create_booking(self):
        """An authenticated user should be able to book a seat."""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/bookings/",
            {
                "movie": self.movie.id,
                "seat": self.seat.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        booking = Booking.objects.get()

        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.movie, self.movie)
        self.assertEqual(booking.seat, self.seat)

        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)

    def test_already_booked_seat_is_rejected(self):
        """A booked seat must not be booked again."""
        self.seat.is_booked = True
        self.seat.save()

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/bookings/",
            {
                "movie": self.movie.id,
                "seat": self.seat.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(Booking.objects.count(), 0)

    def test_user_only_sees_own_bookings(self):
        """Booking history API should only show the current user's bookings."""
        Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user,
        )

        Booking.objects.create(
            movie=self.movie,
            seat=self.second_seat,
            user=self.other_user,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/bookings/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["user"],
            "student1",
        )


class TemplateViewTests(TestCase):
    """Tests for the Bootstrap user interface."""

    def setUp(self):
        """Create reusable UI test data."""
        self.user = User.objects.create_user(
            username="student",
            password="password123",
        )

        self.other_user = User.objects.create_user(
            username="otherstudent",
            password="password123",
        )

        self.movie = Movie.objects.create(
            title="Interstellar",
            description="Space exploration movie.",
            release_date="2014-11-07",
            duration=169,
        )

        self.seat = Seat.objects.create(
            seat_number="A1",
            is_booked=False,
        )

        self.other_seat = Seat.objects.create(
            seat_number="A2",
            is_booked=False,
        )

    def test_movie_list_page(self):
        """Movie listing page should display movies."""
        response = self.client.get(
            reverse("movie_list")
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "Interstellar",
        )

    def test_booking_page_requires_login(self):
        """Anonymous users should be redirected to login."""
        response = self.client.get(
            reverse(
                "book_seat",
                args=[self.movie.id],
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_book_seat(self):
        """Booking form should create a booking and reserve the seat."""
        self.client.login(
            username="student",
            password="password123",
        )

        response = self.client.post(
            reverse(
                "book_seat",
                args=[self.movie.id],
            ),
            {
                "seat_id": self.seat.id,
            },
        )

        self.assertRedirects(
            response,
            reverse("booking_history"),
        )

        self.assertTrue(
            Booking.objects.filter(
                movie=self.movie,
                seat=self.seat,
                user=self.user,
            ).exists()
        )

        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)

    def test_booking_history_only_shows_current_user(self):
        """Users should only see their own booking history."""
        Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user,
        )

        Booking.objects.create(
            movie=self.movie,
            seat=self.other_seat,
            user=self.other_user,
        )

        self.client.login(
            username="student",
            password="password123",
        )

        response = self.client.get(
            reverse("booking_history")
        )

        self.assertEqual(response.status_code, 200)

        bookings = response.context["bookings"]

        self.assertEqual(bookings.count(), 1)
        self.assertEqual(
            bookings.first().user,
            self.user,
        )

    def test_already_booked_seat_not_shown_as_available(self):
        """Booked seats should not appear in the booking form."""
        self.seat.is_booked = True
        self.seat.save()

        self.client.login(
            username="student",
            password="password123",
        )

        response = self.client.get(
            reverse(
                "book_seat",
                args=[self.movie.id],
            )
        )

        seats = response.context["seats"]

        self.assertNotIn(self.seat, seats)
        self.assertIn(self.other_seat, seats)