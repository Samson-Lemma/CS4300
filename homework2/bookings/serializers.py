"""Serializers for the movie theater booking API."""

from rest_framework import serializers

from .models import Booking, Movie, Seat


class MovieSerializer(serializers.ModelSerializer):
    """Serialize Movie objects."""

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "description",
            "release_date",
            "duration",
        ]


class SeatSerializer(serializers.ModelSerializer):
    """Serialize Seat objects."""

    class Meta:
        model = Seat
        fields = [
            "id",
            "seat_number",
            "is_booked",
        ]


class BookingSerializer(serializers.ModelSerializer):
    """Serialize Booking objects."""

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "movie",
            "seat",
            "user",
            "booking_date",
        ]
        read_only_fields = [
            "user",
            "booking_date",
        ]

    def validate_seat(self, seat):
        """Prevent users from booking a seat that is already booked."""
        if seat.is_booked:
            raise serializers.ValidationError(
                "This seat is already booked."
            )

        return seat

    def create(self, validated_data):
        """Create a booking and mark the selected seat as booked."""
        request = self.context.get("request")

        booking = Booking.objects.create(
            user=request.user,
            **validated_data,
        )

        booking.seat.is_booked = True
        booking.seat.save()

        return booking