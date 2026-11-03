import os
import re

# 1. NEW COMPREHENSIVE STYLE.CSS
NEW_STYLE_CSS = """/* =====================================================
   SMART HOSTEL MESS MANAGEMENT SYSTEM - STYLE.CSS
   Clean, Modern, Responsive & Neatly Aligned
===================================================== */

/* ================= RESET ================= */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: #f8fafc;
    color: #1e293b;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
}

/* ================= NAVBAR ================= */
.navbar {
    height: 72px;
    width: 100%;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 6%;
    box-shadow: 0 2px 14px rgba(0, 0, 0, 0.06);
    position: sticky;
    top: 0;
    z-index: 100;
}

.logo {
    font-size: 20px;
    font-weight: 800;
    color: #087f5b;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 10px;
    letter-spacing: -0.3px;
    white-space: nowrap;
}

.logo:hover {
    color: #066b4d;
}

/* Navigation Links */
.navbar nav,
.nav-buttons {
    display: flex;
    align-items: center;
    gap: 10px;
}

.navbar nav a,
.nav-buttons .nav-btn {
    text-decoration: none;
    color: #475569;
    font-size: 14px;
    font-weight: 600;
    padding: 8px 16px;
    border-radius: 8px;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.navbar nav a:hover,
.nav-buttons .nav-btn:hover {
    color: #087f5b;
    background: #e6fcf5;
}

.nav-buttons .nav-btn.active {
    background: #087f5b;
    color: #ffffff !important;
}

.user-badge {
    background: #e6fcf5;
    color: #087f5b;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    border: 1px solid #b2f2bb;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
}

.logout-btn {
    text-decoration: none;
    background: #fee2e2;
    color: #dc2626 !important;
    padding: 8px 18px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 700;
    transition: 0.2s;
    border: 1px solid #fecaca;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.logout-btn:hover {
    background: #dc2626;
    color: #ffffff !important;
}

/* ================= PAGE HEADINGS ================= */
.page-heading,
.attendance-heading,
.fees-heading,
.notice-heading {
    text-align: center;
    margin: 40px auto 28px;
    max-width: 680px;
    padding: 0 20px;
}

.heading-icon {
    font-size: 44px;
    margin-bottom: 8px;
    display: inline-block;
}

.page-heading h1,
.attendance-heading h1,
.fees-heading h1,
.notice-heading h1 {
    font-size: 32px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
}

.page-heading p,
.attendance-heading p,
.fees-heading p,
.notice-heading p {
    font-size: 16px;
    color: #64748b;
    font-weight: 500;
}

/* =====================================================
   LOGIN & REGISTRATION PAGE
===================================================== */
.login-page {
    min-height: calc(100vh - 72px);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px 20px;
}

.login-table {
    width: 1000px;
    max-width: 100%;
    background: #ffffff;
    border-radius: 20px;
    display: flex;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    border: 1px solid #e2e8f0;
}

/* Welcome Sidebar */
.welcome-column {
    flex: 1;
    background: linear-gradient(135deg, #087f5b 0%, #065e43 100%);
    color: white;
    padding: 48px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.home-icon {
    font-size: 48px;
    margin-bottom: 16px;
}

.welcome-column h1 {
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 12px;
    line-height: 1.25;
}

.welcome-column > p {
    font-size: 15px;
    color: #d3f9d8;
    line-height: 1.6;
    margin-bottom: 28px;
}

.features-list p {
    font-size: 15px;
    color: #ffffff;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 500;
}

/* Form Column */
.login-column {
    flex: 1.15;
    padding: 48px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: #ffffff;
}

.login-column h2 {
    font-size: 26px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 6px;
}

.subtitle {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 24px;
}

.hidden {
    display: none;
}

.login-column form label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: #334155;
    margin-bottom: 6px;
}

.login-column input[type="text"],
.login-column input[type="email"],
.login-column input[type="tel"],
.login-column input[type="password"] {
    width: 100%;
    padding: 12px 14px;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    font-size: 15px;
    margin-bottom: 16px;
    transition: all 0.2s ease;
    background: #f8fafc;
}

.login-column input:focus {
    border-color: #087f5b;
    background: #ffffff;
    outline: none;
    box-shadow: 0 0 0 3px rgba(8, 127, 91, 0.12);
}

.options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
    margin-bottom: 20px;
}

.remember {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #475569;
    cursor: pointer;
}

.options a {
    color: #087f5b;
    text-decoration: none;
    font-weight: 600;
}

.login-btn {
    width: 100%;
    background: #087f5b;
    color: white;
    border: none;
    padding: 13px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
    box-shadow: 0 4px 12px rgba(8, 127, 91, 0.25);
}

.login-btn:hover {
    background: #066b4d;
    transform: translateY(-1px);
}

.message {
    min-height: 24px;
    margin-top: 14px;
    font-size: 14px;
    font-weight: 600;
    text-align: center;
}

.register {
    text-align: center;
    margin-top: 22px;
    font-size: 14px;
    color: #64748b;
}

.register a {
    color: #087f5b;
    font-weight: 700;
    text-decoration: none;
    margin-left: 6px;
}

/* =====================================================
   MESS MENU PAGE
===================================================== */
.menu-page {
    padding-bottom: 60px;
}

.menu-container {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(330px, 1fr));
    gap: 28px;
}

.menu-card {
    background: #ffffff;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    border: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.menu-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(8, 127, 91, 0.12);
}

.food-image {
    width: 100%;
    height: 210px;
    object-fit: cover;
    display: block;
    background: #e2e8f0;
}

.menu-content {
    padding: 22px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.menu-content h2 {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 6px;
}

.menu-content .instruction {
    font-size: 12px;
    font-weight: 700;
    color: #087f5b;
    background: #e6fcf5;
    padding: 4px 10px;
    border-radius: 6px;
    display: inline-block;
    align-self: flex-start;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 16px;
}

.menu-content p:not(.instruction) {
    font-size: 15px;
    color: #334155;
    padding: 7px 0;
    border-bottom: 1px dashed #f1f5f9;
    font-weight: 500;
}

.menu-content p:last-child {
    border-bottom: none;
}

/* Sunday Card Special Highlight */
.menu-card.sunday {
    border: 2px solid #f59e0b;
    box-shadow: 0 6px 24px rgba(245, 158, 11, 0.12);
}

.menu-card.sunday .instruction {
    background: #fef3c7;
    color: #b45309;
}

.menu-next {
    text-align: center;
    margin: 40px auto 20px;
}

.next-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #087f5b;
    color: white;
    padding: 14px 32px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 700;
    text-decoration: none;
    box-shadow: 0 4px 14px rgba(8, 127, 91, 0.28);
    transition: 0.25s;
}

.next-btn:hover {
    background: #066b4d;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(8, 127, 91, 0.38);
}

/* =====================================================
   MEAL ATTENDANCE PAGE
===================================================== */
.attendance-page {
    padding-bottom: 60px;
}

.attendance-card {
    max-width: 580px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 18px;
    padding: 36px;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.06);
    border: 1px solid #e2e8f0;
    text-align: center;
}

.attendance-card h2 {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
}

.attendance-card .date {
    font-size: 15px;
    color: #64748b;
    font-weight: 500;
    margin-bottom: 24px;
}

.meal-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 26px;
}

.meal-box h3 {
    font-size: 18px;
    color: #087f5b;
    margin-bottom: 6px;
}

.meal-box p {
    font-size: 15px;
    color: #475569;
    font-weight: 500;
}

.attendance-options {
    display: flex;
    gap: 16px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 20px;
}

.present-btn {
    flex: 1;
    min-width: 190px;
    background: #087f5b;
    color: white;
    border: none;
    padding: 13px 20px;
    border-radius: 9px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
    box-shadow: 0 4px 12px rgba(8, 127, 91, 0.22);
}

.present-btn:hover {
    background: #066b4d;
    transform: translateY(-2px);
}

.absent-btn {
    flex: 1;
    min-width: 190px;
    background: #ffffff;
    color: #dc2626;
    border: 2px solid #ef4444;
    padding: 13px 20px;
    border-radius: 9px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
}

.absent-btn:hover {
    background: #fee2e2;
    transform: translateY(-2px);
}

.attendance-message {
    min-height: 28px;
    margin: 16px 0;
    font-size: 15px;
    font-weight: 600;
}

.continue-btn {
    display: inline-block;
    background: #087f5b;
    color: white;
    padding: 12px 28px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 700;
    text-decoration: none;
    transition: 0.2s;
}

.continue-btn:hover {
    background: #066b4d;
}

/* =====================================================
   MESS FEES PAGE
===================================================== */
.fees-page {
    padding-bottom: 60px;
}

.fees-card {
    max-width: 580px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 18px;
    padding: 36px;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.06);
    border: 1px solid #e2e8f0;
}

.fees-card h2 {
    text-align: center;
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
}

.fees-card .month {
    text-align: center;
    font-size: 15px;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 24px;
}

.fee-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 0;
    border-bottom: 1px solid #f1f5f9;
    font-size: 15px;
    color: #475569;
}

.fee-row strong {
    color: #0f172a;
    font-size: 17px;
}

.fee-row.remaining {
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 16px;
    font-weight: 700;
}

.fee-row.remaining strong {
    color: #dc2626;
    font-size: 20px;
}

.payment-status {
    margin: 24px 0;
    padding: 12px;
    border-radius: 9px;
    text-align: center;
    font-weight: 700;
    font-size: 15px;
    background: #fff9db;
    color: #f08c00;
}

.pay-btn {
    width: 100%;
    background: #087f5b;
    color: white;
    border: none;
    padding: 14px;
    border-radius: 9px;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
    box-shadow: 0 4px 12px rgba(8, 127, 91, 0.25);
}

.pay-btn:hover {
    background: #066b4d;
    transform: translateY(-1px);
}

.payment-message {
    min-height: 24px;
    margin-top: 14px;
    font-size: 14px;
    font-weight: 600;
    text-align: center;
}

.notice-btn {
    display: block;
    text-align: center;
    margin-top: 20px;
    color: #087f5b;
    text-decoration: none;
    font-weight: 700;
    font-size: 15px;
}

.notice-btn:hover {
    text-decoration: underline;
}

/* =====================================================
   MESS NOTICES PAGE
===================================================== */
.notice-page {
    padding-bottom: 60px;
}

.notice-container {
    max-width: 820px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.notice-card {
    display: flex;
    gap: 20px;
    align-items: flex-start;
    background: #ffffff;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.05);
    border: 1px solid #e2e8f0;
    border-left: 5px solid #087f5b;
    transition: transform 0.2s ease;
}

.notice-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.notice-icon {
    width: 50px;
    height: 50px;
    border-radius: 12px;
    background: #e6fcf5;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    flex-shrink: 0;
}

.notice-content {
    flex-grow: 1;
}

.notice-content h2 {
    font-size: 19px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
}

.notice-date {
    font-size: 13px;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 10px;
}

.notice-content p:last-child {
    font-size: 15px;
    color: #334155;
    line-height: 1.6;
}

/* ================= FOOTER ================= */
footer {
    text-align: center;
    padding: 30px 20px;
    color: #64748b;
    font-size: 14px;
    font-weight: 500;
    border-top: 1px solid #e2e8f0;
    margin-top: 40px;
    background: #ffffff;
}

/* ================= RESPONSIVE ================= */
@media (max-width: 860px) {
    .navbar {
        padding: 0 4%;
        height: auto;
        padding-top: 12px;
        padding-bottom: 12px;
        flex-direction: column;
        gap: 12px;
    }

    .navbar nav,
    .nav-buttons {
        flex-wrap: wrap;
        justify-content: center;
    }

    .login-table {
        flex-direction: column;
    }

    .welcome-column {
        padding: 36px 24px;
    }

    .login-column {
        padding: 36px 24px;
    }
}
"""

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(NEW_STYLE_CSS)
print("Updated style.css")


# 2. UPDATE LOGIN.HTML
with open('login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace titles, branding, and text
c = re.sub(r'<title>.*?</title>', '<title>Smart Hostel Mess Management System - Login</title>', c)
c = c.replace('🏠 SmartHostel', '🏠 Smart Hostel Mess Management System')
c = c.replace('🏠 Smart Hostel', '🏠 Smart Hostel Mess Management System')
c = c.replace('SmartHostel\n                student dashboard.', 'Smart Hostel Mess Management System dashboard.')
c = c.replace('SmartHostel student dashboard.', 'Smart Hostel Mess Management System dashboard.')
c = c.replace('<h2>\n                    Student Login\n                </h2>', '<h2>\n                    Mess Management Login\n                </h2>')
c = c.replace('<h2>Student Login</h2>', '<h2>Mess Management Login</h2>')
c = c.replace('<h2>\n                    Student Registration\n                </h2>', '<h2>\n                    Student Registration\n                </h2>')
c = c.replace('Create your SmartHostel account', 'Create your Smart Hostel Mess account')
c = c.replace('SmartHostel - Login', 'Smart Hostel Mess Management System - Login')
c = c.replace('SmartHostel', 'Smart Hostel Mess Management System')

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated login.html")


# 3. UPDATE MESS-MENU.HTML
with open('mess-menu.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'<title>.*?</title>', '<title>Smart Hostel Mess Management System - Menu</title>', c)

# Complete unified navbar
navbar_replacement = """<header class="navbar">
    <div class="logo">
        🏠 Smart Hostel Mess Management System
    </div>
    <div class="nav-buttons">
        <a href="mess-menu.html" class="nav-btn active">🍛 Mess Menu</a>
        <a href="attendance.html" class="nav-btn">🍽️ Attendance</a>
        <a href="mess-fees.html" class="nav-btn">💰 Mess Fees</a>
        <a href="notice.html" class="nav-btn">📢 Notices</a>
        <a href="login.html" class="logout-btn">Logout</a>
    </div>
</header>"""

c = re.sub(r'<header class="navbar">.*?</header>', navbar_replacement, c, flags=re.DOTALL)
c = c.replace('© 2026 SmartHostel | Hostel Mess Management', '© 2026 Smart Hostel Mess Management System | All Rights Reserved')
c = c.replace('© 2026 SmartHostel', '© 2026 Smart Hostel Mess Management System')

with open('mess-menu.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated mess-menu.html")


# 4. UPDATE ATTENDANCE.HTML
with open('attendance.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'<title>.*?</title>', '<title>Smart Hostel Mess Management System - Attendance</title>', c)

navbar_att = """<header class="navbar">
    <div class="logo">
        🏠 Smart Hostel Mess Management System
    </div>
    <div class="nav-buttons">
        <a href="mess-menu.html" class="nav-btn">🍛 Mess Menu</a>
        <a href="attendance.html" class="nav-btn active">🍽️ Attendance</a>
        <a href="mess-fees.html" class="nav-btn">💰 Mess Fees</a>
        <a href="notice.html" class="nav-btn">📢 Notices</a>
        <a href="login.html" class="logout-btn">Logout</a>
    </div>
</header>"""

c = re.sub(r'<header class="navbar">.*?</header>', navbar_att, c, flags=re.DOTALL)
c = c.replace('© 2026 SmartHostel | Hostel Mess Management', '© 2026 Smart Hostel Mess Management System | All Rights Reserved')
c = c.replace('© 2026 SmartHostel', '© 2026 Smart Hostel Mess Management System')

with open('attendance.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated attendance.html")


# 5. UPDATE MESS-FEES.HTML
with open('mess-fees.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'<title>.*?</title>', '<title>Smart Hostel Mess Management System - Fees</title>', c)

navbar_fees = """<header class="navbar">
    <div class="logo">
        🏠 Smart Hostel Mess Management System
    </div>
    <div class="nav-buttons">
        <a href="mess-menu.html" class="nav-btn">🍛 Mess Menu</a>
        <a href="attendance.html" class="nav-btn">🍽️ Attendance</a>
        <a href="mess-fees.html" class="nav-btn active">💰 Mess Fees</a>
        <a href="notice.html" class="nav-btn">📢 Notices</a>
        <a href="login.html" class="logout-btn">Logout</a>
    </div>
</header>"""

c = re.sub(r'<header class="navbar">.*?</header>', navbar_fees, c, flags=re.DOTALL)
c = c.replace('© 2026 SmartHostel | Hostel Mess Management', '© 2026 Smart Hostel Mess Management System | All Rights Reserved')
c = c.replace('© 2026 SmartHostel', '© 2026 Smart Hostel Mess Management System')

with open('mess-fees.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated mess-fees.html")


# 6. UPDATE NOTICE.HTML
with open('notice.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'<title>.*?</title>', '<title>Smart Hostel Mess Management System - Notices</title>', c)

navbar_notice = """<header class="navbar">
    <div class="logo">
        🏠 Smart Hostel Mess Management System
    </div>
    <div class="nav-buttons">
        <a href="mess-menu.html" class="nav-btn">🍛 Mess Menu</a>
        <a href="attendance.html" class="nav-btn">🍽️ Attendance</a>
        <a href="mess-fees.html" class="nav-btn">💰 Mess Fees</a>
        <a href="notice.html" class="nav-btn active">📢 Notices</a>
        <a href="login.html" class="logout-btn">Logout</a>
    </div>
</header>"""

c = re.sub(r'<header class="navbar">.*?</header>', navbar_notice, c, flags=re.DOTALL)
c = c.replace('© 2026 SmartHostel | Hostel Mess Management', '© 2026 Smart Hostel Mess Management System | All Rights Reserved')
c = c.replace('© 2026 SmartHostel', '© 2026 Smart Hostel Mess Management System')

with open('notice.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated notice.html")

