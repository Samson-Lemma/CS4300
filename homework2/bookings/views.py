"""Views and API viewsets for the movie theater booking application."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions, viewsets

from .models import Booking, Movie, Seat
from .serializers import BookingSerializer, MovieSerializer, SeatSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """Provide CRUD operations for movies through the REST API."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SeatViewSet(viewsets.ModelViewSet):
    """Provide CRUD operations and availability information for seats."""

    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """Allow authenticated users to create and view their bookings."""

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only bookings belonging to the logged-in user."""
        return (
            Booking.objects.filter(user=self.request.user)
            .select_related("movie", "seat", "user")
            .order_by("-booking_date")
        )


def movie_list(request):
    """Display all movies available in the theater."""
    movies = Movie.objects.all().order_by("title")

    return render(
        request,
        "bookings/movie_list.html",
        {"movies": movies},
    )


@login_required
def seat_booking(request, movie_id):
    """Allow an authenticated user to select an available seat."""
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == "POST":
        seat_id = request.POST.get("seat_id")

        if not seat_id:
            messages.error(request, "Please select a seat.")
            return redirect("book_seat", movie_id=movie.id)

        with transaction.atomic():
            seat = get_object_or_404(
                Seat.objects.select_for_update(),
                pk=seat_id,
            )

            if seat.is_booked:
                messages.error(
                    request,
                    "That seat has already been booked.",
                )
                return redirect("book_seat", movie_id=movie.id)

            Booking.objects.create(
                movie=movie,
                seat=seat,
                user=request.user,
            )

            seat.is_booked = True
            seat.save(update_fields=["is_booked"])

        messages.success(
            request,
            f"Seat {seat.seat_number} was booked successfully.",
        )

        return redirect("booking_history")

    available_seats = Seat.objects.filter(
        is_booked=False
    ).order_by("seat_number")

    return render(
        request,
        "bookings/seat_booking.html",
        {
            "movie": movie,
            "seats": available_seats,
        },
    )


@login_required
def booking_history(request):
    """Display booking history for the logged-in user."""
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("movie", "seat")
        .order_by("-booking_date")
    )

    return render(
        request,
        "bookings/booking_history.html",
        {"bookings": bookings},
    )