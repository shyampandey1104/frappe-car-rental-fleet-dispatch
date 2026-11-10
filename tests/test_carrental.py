import unittest
from carrental.engine import CarRentalEngine, RentalVehicle


class TestCarRentalEngine(unittest.TestCase):
    def setUp(self):
        self.engine = CarRentalEngine()
        self.engine.add_vehicle(RentalVehicle(
            vehicle_id="CAR-01",
            make_model="Mahindra Thar 4x4",
            registration_no="GA-03-Z-8888",
            daily_tariff=3000.0,
            free_km_per_day=200.0,
            extra_km_rate=15.0,
            security_deposit=5000.0,
            current_odometer_km=15000.0
        ))

    def test_booking_and_return_with_extra_km(self):
        booking = self.engine.create_booking(
            booking_id="BKG-9901",
            customer_name="Rohan Verma",
            dl_no="DL-1420110012345",
            vehicle_id="CAR-01",
            start_date="2026-05-01 10:00",
            end_date="2026-05-03 10:00"
        )
        self.assertFalse(self.engine.fleet["CAR-01"].is_available)

        # 2 Days: allowed free = 400 km. Actual = 550 km (+150 km extra @ 15 = 2250)
        # Base rent = 2 * 3000 = 6000
        settlement = self.engine.process_vehicle_return(
            booking_id="BKG-9901",
            actual_return_date="2026-05-03 09:30",
            return_odometer_km=15550.0,
            damage_repair_charge=500.0
        )
        self.assertEqual(settlement["days_billed"], 2)
        self.assertEqual(settlement["extra_km"], 150.0)
        self.assertEqual(settlement["extra_km_charges"], 2250.0)
        self.assertEqual(settlement["security_deposit_refunded"], 4500.0)  # 5000 - 500 damage
        self.assertTrue(self.engine.fleet["CAR-01"].is_available)


if __name__ == "__main__":
    unittest.main()
