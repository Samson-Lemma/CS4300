"""URL routes for the booking application and REST API."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BookingViewSet,
    MovieViewSet,
    SeatViewSet,
    booking_history,
    movie_list,
    seat_booking,
)


router = DefaultRouter()

router.register(
    "movies",
    MovieViewSet,
    basename="movie",
)

router.register(
    "seats",
    SeatViewSet,
    basename="seat",
)

router.register(
    "bookings",
    BookingViewSet,
    basename="booking",
)


urlpatterns = [
    # Normal Django pages
    path(
        "",
        movie_list,
        name="movie_list",
    ),
    path(
        "movies/<int:movie_id>/book/",
        seat_booking,
        name="book_seat",
    ),
    path(
        "history/",
        booking_history,
        name="booking_history",
    ),

    # REST API
    path(
        "api/",
        include(router.urls),
    ),

    # Django REST Framework login/logout
    path(
        "api-auth/",
        include(
            "rest_framework.urls",
            namespace="rest_framework",
        ),
    ),
]