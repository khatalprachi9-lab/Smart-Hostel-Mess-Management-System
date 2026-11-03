# 🏠 Smart Hostel Mess Management System

A full-stack web application designed for managing hostel mess operations, student registrations, meal attendance, weekly lunch menus, mess fees, payments, and announcements, backed by **Python Flask** and an **SQLite database (`smart_hostel.db`)**.

---

## 🚀 How to Run the Project

### Option 1: Double-Click
Double-click **`start_server.bat`** in the project folder.

### Option 2: Command Line / Terminal
Open your terminal or command prompt inside `C:\Smart-Hostel-Mess` and run:

```bash
python app.py
```

Then open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📸 Mess Menu Visuals
The weekly lunch menu features dedicated photorealistic images for each day of the week:
- **Monday (`monday.jpg`)**: Steamed Rice, Dal Tadka, Chapati, Potato Sabzi, Salad
- **Tuesday (`tuesday.jpg`)**: Jeera Rice, Dal Fry, Chapati, Mixed Veg, Fresh Curd
- **Wednesday (`wednesday.jpg`)**: Basmati Rice, Dal Tadka, Chapati, Spiced Brinjal Sabzi, Salad
- **Thursday (`thursday.jpg`)**: Rice, Homestyle Dal, Chapati, Mixed Veg Sabzi, Chilled Buttermilk
- **Friday (`friday.jpg`)**: Veg Pulao, Dal, Chapati, Aloo Gobi, Cucumber-Tomato Salad
- **Saturday (`saturday.jpg`)**: Rice, Dal, Chapati, Tomato Sabzi, Curd
- **Sunday (`sunday.jpg`)**: Special Sunday Feast - Veg Biryani, Dal Tadka, Chapati, Special Sabzi, Raita

---

## 🗄️ Database Architecture (SQLite: `smart_hostel.db`)

The SQLite database is auto-created on start and includes the following tables:

| Table | Description |
|---|---|
| **`users`** | Member registration details (Name, Email, Mobile, Room, Password) |
| **`attendance`** | Daily lunch attendance records (`Present` / `Absent`) per student |
| **`fees`** | Mess fees, total amount, paid amount, remaining balance, and status |
| **`payments`** | Transaction logs with unique Transaction IDs when fees are paid |
| **`notices`** | Announcements and hostel mess notices |
| **`menu`** | Weekly lunch menu schedule (Monday to Sunday) |

---

## 🔑 Demo Account

You can register your own new account on the Register page, or use the pre-configured demo account:
- **Email:** `student@smarthostel.com`
- **Password:** `student123`

---

## 🌐 Connected Endpoints

- **`POST /api/register`** - Registers new students into the SQLite database.
- **`POST /api/login`** - Authenticates credentials from the SQLite database.
- **`POST /api/logout`** - Clears the session.
- **`GET /api/me`** - Gets profile details for the currently logged-in student.
- **`POST /api/attendance`** - Records meal attendance in SQLite (`Present` / `Absent`).
- **`GET /api/attendance/today`** - Checks if today's attendance has already been marked.
- **`GET /api/fees`** - Fetches real-time mess fee details from SQLite.
- **`POST /api/fees/pay`** - Completes payment and logs transaction in SQLite.
- **`GET /api/notices`** - Dynamically loads hostel notices from SQLite.
- **`GET /api/menu`** - Loads weekly lunch menu.

---

## 🧪 Testing

You can verify the backend and database connection at any time by running:
```bash
python test_backend.py
```
