"""Database models for the movie theater booking application."""

from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    """A movie available for viewing and booking."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(
        help_text="Duration in minutes"
    )

    def __str__(self):
        """Return the movie title."""
        return self.title


class Seat(models.Model):
    """A theater seat that can be available or booked."""

    seat_number = models.CharField(max_length=10, unique=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        """Return the seat number."""
        return self.seat_number


class Booking(models.Model):
    """A booking connecting a user, movie, and seat."""

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable description of the booking."""
        return (
            f"{self.user.username} - "
            f"{self.movie.title} - "
            f"{self.seat.seat_number}"
        )