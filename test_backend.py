import json
import sqlite3
from app import app
from database import DB_NAME

client = app.test_client()

def test_full_flow():
    print("--- 1. Testing Database Tables ---")
    conn = sqlite3.connect(DB_NAME)
    tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    print("Tables in SQLite DB:", tables)
    assert 'users' in tables
    assert 'attendance' in tables
    assert 'fees' in tables
    assert 'payments' in tables
    assert 'notices' in tables
    assert 'menu' in tables
    conn.close()

    print("\n--- 2. Testing Register API ---")
    reg_data = {
        "name": "Amit Sharma",
        "email": "amit@test.com",
        "mobile": "9876543211",
        "room": "B-204",
        "password": "mypassword123"
    }
    res = client.post('/api/register', json=reg_data)
    print("Register Status:", res.status_code, res.get_json())
    assert res.status_code in [201, 409] # 201 or 409 if already exists

    print("\n--- 3. Testing Login API ---")
    login_data = {
        "email": "amit@test.com",
        "password": "mypassword123"
    }
    res = client.post('/api/login', json=login_data)
    print("Login Status:", res.status_code, res.get_json())
    assert res.status_code == 200
    assert res.get_json()['success'] is True

    print("\n--- 4. Testing Attendance API ---")
    att_data = {
        "email": "amit@test.com",
        "meal": "Lunch",
        "date": "2026-11-03",
        "status": "Present"
    }
    res = client.post('/api/attendance', json=att_data)
    print("Mark Attendance Status:", res.status_code, res.get_json())
    assert res.status_code == 200

    res = client.get('/api/attendance/today?email=amit@test.com&date=2026-11-03')
    print("Fetch Attendance Status:", res.status_code, res.get_json())
    assert res.status_code == 200
    assert res.get_json()['attendance']['status'] == "Present"

    print("\n--- 5. Testing Mess Fees & Pay API ---")
    res = client.get('/api/fees?email=amit@test.com')
    fee_json = res.get_json()
    print("Fees Before Payment:", fee_json)
    assert res.status_code == 200

    res = client.post('/api/fees/pay', json={"email": "amit@test.com"})
    print("Fees After Payment:", res.status_code, res.get_json())
    assert res.status_code == 200
    assert res.get_json()['fee']['remaining_amount'] == 0
    assert res.get_json()['fee']['status'] == "Paid"

    print("\n--- 6. Testing Notices API ---")
    res = client.get('/api/notices')
    print("Notices count:", len(res.get_json().get('notices', [])))
    assert res.status_code == 200
    assert len(res.get_json()['notices']) >= 5

    print("\n--- 7. Testing Menu API ---")
    res = client.get('/api/menu')
    print("Menu days count:", len(res.get_json().get('menu', [])))
    assert res.status_code == 200
    assert len(res.get_json()['menu']) == 7

    print("\n=======================================================")
    print(" ALL BACKEND & SQLITE DATABASE TESTS PASSED WITH 100%! ")
    print("=======================================================")

if __name__ == "__main__":
    test_full_flow()

