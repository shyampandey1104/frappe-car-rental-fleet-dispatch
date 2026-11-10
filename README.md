# Frappe Car Rental & Fleet Dispatch Engine 🚘🔑

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Frappe](https://img.shields.io/badge/Frappe-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An enterprise self-drive car rental, chauffeur dispatch, and security deposit escrow management app for **Frappe Framework & ERPNext**. Built for vehicle rental businesses, airport cab fleets, and luxury car leasing providers (Zoomcar, Revv model).

---

## 🚀 Key Features

- **Live Fleet Availability Calendar**: Real-time allocation, lock prevention, and customer driving license verification.
- **Odometer & Distance Allowance Tracking**: Enforces daily free kilometer quotas with automated extra kilometer surcharge calculation.
- **Security Deposit Escrow Settlement**: Fast check-out reconciling scratch/dent repair estimates and fuel missing penalties against the refundable deposit.
- **Automated Fleet Ledger**: Syncs maintenance servicing schedules and vehicle asset depreciation in ERPNext.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/frappe-car-rental-fleet-dispatch.git
cd frappe-car-rental-fleet-dispatch
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from carrental.engine import CarRentalEngine, RentalVehicle

engine = CarRentalEngine()
engine.add_vehicle(RentalVehicle(
    vehicle_id="THAR-01",
    make_model="Mahindra Thar",
    registration_no="GA-01-A-1234",
    daily_tariff=3200.0,
    free_km_per_day=200.0,
    extra_km_rate=15.0,
    security_deposit=5000.0,
    current_odometer_km=12000.0
))

# Dispatch booking
bkg = engine.create_booking("B-101", "Kabir Sen", "DL-90218", "THAR-01", "2026-06-01 10:00", "2026-06-03 10:00")

# Settle return
bill = engine.process_vehicle_return("B-101", "2026-06-03 11:00", return_odometer_km=12480.0, damage_repair_charge=300.0)
print(f"Total Rent: ₹{bill['total_rental_charge']} | Deposit Refund: ₹{bill['security_deposit_refunded']}")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
