"""Car Rental Booking, Deposit Escrow, Odometer Tracking & Return Damage Settlement Engine."""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class RentalVehicle(BaseModel):
    vehicle_id: str
    make_model: str  # e.g., Hyundai Creta 2024, Mahindra Thar, Maruti Swift
    registration_no: str
    daily_tariff: float
    free_km_per_day: float = 250.0
    extra_km_rate: float = 14.0
    security_deposit: float = 5000.0
    current_odometer_km: float
    is_available: bool = True


class RentalBooking(BaseModel):
    booking_id: str
    customer_name: str
    driving_license_no: str
    vehicle_id: str
    start_date: str  # YYYY-MM-DD HH:MM
    end_date: str    # YYYY-MM-DD HH:MM
    start_odometer_km: float
    security_deposit_paid: float
    is_active: bool = True


class CarRentalEngine:
    """Manages self-drive vehicle dispatches, security deposits, and checkout reconciliations."""

    def __init__(self):
        self.fleet: Dict[str, RentalVehicle] = {}
        self.bookings: Dict[str, RentalBooking] = {}

    def add_vehicle(self, v: RentalVehicle) -> RentalVehicle:
        self.fleet[v.vehicle_id] = v
        return v

    def create_booking(
        self,
        booking_id: str,
        customer_name: str,
        dl_no: str,
        vehicle_id: str,
        start_date: str,
        end_date: str
    ) -> RentalBooking:
        vehicle = self.fleet.get(vehicle_id)
        if not vehicle:
            raise ValueError(f"Vehicle {vehicle_id} not found.")
        if not vehicle.is_available:
            raise ValueError(f"Vehicle {vehicle.make_model} is currently rented out.")

        vehicle.is_available = False
        booking = RentalBooking(
            booking_id=booking_id,
            customer_name=customer_name,
            driving_license_no=dl_no,
            vehicle_id=vehicle_id,
            start_date=start_date,
            end_date=end_date,
            start_odometer_km=vehicle.current_odometer_km,
            security_deposit_paid=vehicle.security_deposit,
            is_active=True
        )
        self.bookings[booking_id] = booking
        return booking

    def process_vehicle_return(
        self,
        booking_id: str,
        actual_return_date: str,
        return_odometer_km: float,
        damage_repair_charge: float = 0.0,
        fuel_penalty_charge: float = 0.0
    ) -> Dict[str, Any]:
        """Calculates final billing, extra KM surcharge, damage deductions, and refundable deposit."""
        booking = self.bookings.get(booking_id)
        if not booking or not booking.is_active:
            raise ValueError("Active booking not found.")

        vehicle = self.fleet[booking.vehicle_id]
        if return_odometer_km < booking.start_odometer_km:
            raise ValueError("Return odometer cannot be less than start odometer.")

        # Calculate rental duration in days
        fmt = "%Y-%m-%d %H:%M"
        t1 = datetime.strptime(booking.start_date, fmt)
        t2 = datetime.strptime(actual_return_date, fmt)
        hours = max(1.0, (t2 - t1).total_seconds() / 3600.0)
        days = max(1, int((hours + 23) // 24))  # round up to full day

        base_rental_fee = days * vehicle.daily_tariff

        # Distance calculation
        distance_travelled = return_odometer_km - booking.start_odometer_km
        allowed_free_km = days * vehicle.free_km_per_day
        extra_km = max(0.0, distance_travelled - allowed_free_km)
        extra_km_fee = extra_km * vehicle.extra_km_rate

        total_gross_bill = base_rental_fee + extra_km_fee + damage_repair_charge + fuel_penalty_charge
        
        # Settle against security deposit
        net_refundable_deposit = max(0.0, booking.security_deposit_paid - (damage_repair_charge + fuel_penalty_charge))
        deposit_deduction = booking.security_deposit_paid - net_refundable_deposit

        # Mark vehicle available again
        vehicle.is_available = True
        vehicle.current_odometer_km = return_odometer_km
        booking.is_active = False

        return {
            "booking_id": booking.booking_id,
            "vehicle": vehicle.make_model,
            "days_billed": days,
            "distance_km": round(distance_travelled, 1),
            "extra_km": round(extra_km, 1),
            "base_rent": round(base_rental_fee, 2),
            "extra_km_charges": round(extra_km_fee, 2),
            "damage_deduction": round(damage_repair_charge, 2),
            "fuel_penalty": round(fuel_penalty_charge, 2),
            "total_rental_charge": round(total_gross_bill, 2),
            "security_deposit_refunded": round(net_refundable_deposit, 2)
        }
