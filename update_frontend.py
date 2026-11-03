import re

def update_login():
    with open('login.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the script block
    script_start = content.find('<script>')
    script_end = content.rfind('</script>') + len('</script>')
    
    if script_start == -1 or script_end == -1:
        print("Script tag not found in login.html")
        return

    new_script = """<script>
/* =========================================
   SHOW LOGIN / SHOW REGISTER
========================================= */
function showLogin() {
    document.getElementById("loginSection").classList.remove("hidden");
    document.getElementById("registerSection").classList.add("hidden");
}

function showRegister() {
    document.getElementById("loginSection").classList.add("hidden");
    document.getElementById("registerSection").classList.remove("hidden");
}

window.addEventListener("DOMContentLoaded", function() {
    const saved = localStorage.getItem("smartHostelUser");
    if (saved) {
        try {
            const u = JSON.parse(saved);
            if (u.email && document.getElementById("loginEmail")) {
                document.getElementById("loginEmail").value = u.email;
            }
        } catch(e) {}
    }
});

/* =========================================
   REGISTRATION (CONNECTS TO SQLITE BACKEND)
========================================= */
document.getElementById("registerForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const name = document.getElementById("studentName").value.trim();
    const email = document.getElementById("registerEmail").value.trim();
    const mobile = document.getElementById("mobile").value.trim();
    const room = document.getElementById("room").value.trim();
    const password = document.getElementById("registerPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const message = document.getElementById("registerMessage");

    if (password !== confirmPassword) {
        message.style.color = "red";
        message.innerHTML = "❌ Passwords do not match.";
        return;
    }

    if (!/^[0-9]{10}$/.test(mobile)) {
        message.style.color = "red";
        message.innerHTML = "❌ Enter valid 10-digit mobile number.";
        return;
    }

    message.style.color = "#2563eb";
    message.innerHTML = "⏳ Saving account into SQLite database...";

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, mobile, room, password })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            localStorage.setItem("smartHostelUser", JSON.stringify(data.user));
            message.style.color = "#087f5b";
            message.innerHTML = "✅ " + data.message;
            document.getElementById("registerForm").reset();

            setTimeout(function() {
                showLogin();
                document.getElementById("loginEmail").value = email;
                document.getElementById("loginMessage").style.color = "#087f5b";
                document.getElementById("loginMessage").innerHTML = "Registered in SQLite successfully! Please log in.";
            }, 1000);
        } else {
            message.style.color = "red";
            message.innerHTML = "❌ " + (data.message || "Registration failed.");
        }
    } catch (err) {
        message.style.color = "red";
        message.innerHTML = "❌ Backend connection error. Ensure Flask server is running.";
    }
});

/* =========================================
   LOGIN (CONNECTS TO SQLITE BACKEND)
========================================= */
document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;
    const message = document.getElementById("loginMessage");

    message.style.color = "#2563eb";
    message.innerHTML = "⏳ Verifying with SQLite database...";

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            localStorage.setItem("smartHostelUser", JSON.stringify(data.user));
            message.style.color = "#087f5b";
            message.innerHTML = "✅ " + data.message;

            setTimeout(function() {
                window.location.href = "mess-menu.html";
            }, 800);
        } else {
            message.style.color = "red";
            message.innerHTML = "❌ " + (data.message || "Invalid email or password.");
        }
    } catch (err) {
        message.style.color = "red";
        message.innerHTML = "❌ Backend connection error. Ensure Flask server is running.";
    }
});
</script>"""

    updated_content = content[:script_start] + new_script + content[script_end:]
    with open('login.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Updated login.html")


def update_attendance():
    with open('attendance.html', 'r', encoding='utf-8') as f:
        content = f.read()

    script_start = content.find('<script>')
    script_end = content.rfind('</script>') + len('</script>')
    
    if script_start == -1 or script_end == -1:
        print("Script tag not found in attendance.html")
        return

    new_script = """<script>
/* ================= TODAY'S DATE ================= */
const today = new Date();
const options = {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric"
};
const formattedDateStr = today.toISOString().split('T')[0];
document.getElementById("todayDate").innerHTML = today.toLocaleDateString("en-IN", options);

function getCurrentUser() {
    const saved = localStorage.getItem("smartHostelUser");
    if (saved) {
        try { return JSON.parse(saved); } catch(e) {}
    }
    return null;
}

/* ================= CHECK TODAY'S ATTENDANCE FROM SQLITE ================= */
async function loadTodayAttendance() {
    const user = getCurrentUser();
    const emailParam = user ? `?email=${encodeURIComponent(user.email)}` : '';
    
    try {
        const response = await fetch(`/api/attendance/today${emailParam}`);
        const data = await response.json();
        
        if (data.success && data.attendance) {
            const status = data.attendance.status;
            const message = document.getElementById("attendanceMessage");
            const continueSection = document.getElementById("continueSection");
            
            if (status === "Present") {
                message.style.color = "#087f5b";
                message.innerHTML = `✅ Saved in SQLite: You marked <strong>Present</strong> for lunch today.`;
                continueSection.style.display = "block";
            } else {
                message.style.color = "#dc2626";
                message.innerHTML = `❌ Saved in SQLite: You marked <strong>Absent</strong> for lunch today.`;
                continueSection.style.display = "none";
            }
        }
    } catch(err) {
        console.log("Could not fetch today's attendance:", err);
    }
}

window.addEventListener("DOMContentLoaded", loadTodayAttendance);

/* ================= MARK ATTENDANCE IN SQLITE ================= */
async function markAttendance(status) {
    const message = document.getElementById("attendanceMessage");
    const continueSection = document.getElementById("continueSection");
    const user = getCurrentUser();

    message.style.color = "#2563eb";
    message.innerHTML = "⏳ Saving attendance in SQLite database...";

    try {
        const response = await fetch('/api/attendance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                status: status,
                meal: "Lunch",
                date: formattedDateStr,
                email: user ? user.email : ''
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            if (status === "Present") {
                message.style.color = "#087f5b";
                message.innerHTML = "✅ SQLite Saved: Lunch attendance marked as Present!";
                continueSection.style.display = "block";
            } else {
                message.style.color = "#dc2626";
                message.innerHTML = "❌ SQLite Saved: Lunch attendance marked as Absent.";
                continueSection.style.display = "none";
            }
        } else {
            message.style.color = "red";
            message.innerHTML = "❌ " + (data.message || "Failed to mark attendance.");
        }
    } catch (err) {
        message.style.color = "red";
        message.innerHTML = "❌ Error connecting to database server.";
    }
}
</script>"""

    updated_content = content[:script_start] + new_script + content[script_end:]
    with open('attendance.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Updated attendance.html")


def update_mess_fees():
    with open('mess-fees.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add IDs to fee card elements if not present
    content = content.replace('<p class="month">\n            August 2026\n        </p>', '<p class="month" id="feeMonth">August 2026</p>')
    content = content.replace('<strong>₹3000</strong>', '<strong id="monthlyFee">₹3000</strong>')
    content = content.replace('<strong>₹2000</strong>', '<strong id="paidAmount">₹2000</strong>')
    content = content.replace('<strong>₹1000</strong>', '<strong id="remainingAmount">₹1000</strong>')
    content = content.replace('<div class="payment-status">\n\n            ⚠️ Payment Pending\n\n        </div>', '<div class="payment-status" id="paymentStatus">⚠️ Payment Pending</div>')
    content = content.replace('<div class="payment-status">\n            ⚠️ Payment Pending\n        </div>', '<div class="payment-status" id="paymentStatus">⚠️ Payment Pending</div>')
    content = content.replace('<div class="payment-status">', '<div class="payment-status" id="paymentStatus">')

    script_start = content.find('<script>')
    script_end = content.rfind('</script>') + len('</script>')

    if script_start == -1 or script_end == -1:
        print("Script tag not found in mess-fees.html")
        return

    new_script = """<script>
function getCurrentUser() {
    const saved = localStorage.getItem("smartHostelUser");
    if (saved) {
        try { return JSON.parse(saved); } catch(e) {}
    }
    return null;
}

/* ================= LOAD FEES FROM SQLITE ================= */
async function loadFees() {
    const user = getCurrentUser();
    const emailParam = user ? `?email=${encodeURIComponent(user.email)}` : '';

    try {
        const response = await fetch(`/api/fees${emailParam}`);
        const data = await response.json();

        if (data.success && data.fee) {
            const fee = data.fee;
            if (document.getElementById("feeMonth")) document.getElementById("feeMonth").textContent = fee.month;
            if (document.getElementById("monthlyFee")) document.getElementById("monthlyFee").textContent = "₹" + fee.monthly_fee;
            if (document.getElementById("paidAmount")) document.getElementById("paidAmount").textContent = "₹" + fee.paid_amount;
            if (document.getElementById("remainingAmount")) document.getElementById("remainingAmount").textContent = "₹" + fee.remaining_amount;

            const statusEl = document.getElementById("paymentStatus");
            if (statusEl) {
                if (fee.status === "Paid" || fee.remaining_amount <= 0) {
                    statusEl.textContent = "✅ Payment Completed";
                    statusEl.style.background = "#e6fcf5";
                    statusEl.style.color = "#087f5b";
                    const payBtn = document.querySelector(".pay-btn");
                    if (payBtn) {
                        payBtn.textContent = "✓ Fees Fully Paid";
                        payBtn.disabled = true;
                        payBtn.style.opacity = "0.7";
                        payBtn.style.cursor = "default";
                    }
                } else {
                    statusEl.textContent = "⚠️ Payment Pending";
                    statusEl.style.background = "#fff9db";
                    statusEl.style.color = "#f08c00";
                }
            }
        }
    } catch(err) {
        console.log("Could not load fees from backend:", err);
    }
}

window.addEventListener("DOMContentLoaded", loadFees);

/* ================= PROCESS PAYMENT IN SQLITE ================= */
async function makePayment() {
    const message = document.getElementById("paymentMessage");
    const user = getCurrentUser();

    message.style.color = "#2563eb";
    message.innerHTML = "⏳ Processing fee payment in SQLite database...";

    try {
        const response = await fetch('/api/fees/pay', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: user ? user.email : '' })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            message.style.color = "#087f5b";
            message.innerHTML = `✅ ${data.message}`;

            // Refresh UI with updated fees
            await loadFees();
        } else {
            message.style.color = "red";
            message.innerHTML = "❌ " + (data.message || "Payment could not be processed.");
        }
    } catch(err) {
        message.style.color = "red";
        message.innerHTML = "❌ Error connecting to database server.";
    }
}
</script>"""

    updated_content = content[:script_start] + new_script + content[script_end:]
    with open('mess-fees.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Updated mess-fees.html")


def update_notices():
    with open('notice.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add id to notice-container
    content = content.replace('<section class="notice-container">', '<section class="notice-container" id="noticeContainer">')

    # Add script at bottom before </body>
    script_to_add = """
<!-- ================= JAVASCRIPT: DYNAMIC SQLITE NOTICES ================= -->
<script>
async function loadNoticesFromDB() {
    const container = document.getElementById("noticeContainer");
    if (!container) return;

    try {
        const response = await fetch('/api/notices');
        const data = await response.json();

        if (data.success && data.notices && data.notices.length > 0) {
            container.innerHTML = "";
            data.notices.forEach(notice => {
                const card = document.createElement("div");
                card.className = "notice-card";
                card.innerHTML = `
                    <div class="notice-icon">${notice.icon || '📢'}</div>
                    <div class="notice-content">
                        <h2>${notice.title}</h2>
                        <p class="notice-date">📅 ${notice.date}</p>
                        <p>${notice.content}</p>
                    </div>
                `;
                container.appendChild(card);
            });
        }
    } catch(err) {
        console.log("Using cached/default notices:", err);
    }
}

window.addEventListener("DOMContentLoaded", loadNoticesFromDB);
</script>
"""
    if "loadNoticesFromDB" not in content:
        content = content.replace("</body>", script_to_add + "\n</body>")

    with open('notice.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated notice.html")


def update_nav_logout():
    files = ['mess-menu.html', 'attendance.html', 'mess-fees.html', 'notice.html']
    script_snippet = """
<script>
// Show logged in user name and handle logout
window.addEventListener('DOMContentLoaded', () => {
    const userStr = localStorage.getItem('smartHostelUser');
    if (userStr) {
        try {
            const user = JSON.parse(userStr);
            const logoutBtn = document.querySelector('.logout-btn');
            if (logoutBtn && user.name) {
                const userBadge = document.createElement('span');
                userBadge.style.cssText = 'font-weight:600; color:#087f5b; margin-right:12px; font-size:14px;';
                userBadge.textContent = `👤 ${user.name} (${user.room || ''})`;
                logoutBtn.parentNode.insertBefore(userBadge, logoutBtn);
            }
        } catch(e) {}
    }

    const logoutLinks = document.querySelectorAll('.logout-btn');
    logoutLinks.forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                await fetch('/api/logout', { method: 'POST' });
            } catch(err) {}
            localStorage.removeItem('smartHostelUser');
            window.location.href = 'login.html';
        });
    });
});
</script>
"""
    for fname in files:
        with open(fname, 'r', encoding='utf-8') as f:
            c = f.read()
        if "Show logged in user name and handle logout" not in c:
            c = c.replace("</body>", script_snippet + "\n</body>")
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Added logout handler to {fname}")

if __name__ == "__main__":
    update_login()
    update_attendance()
    update_mess_fees()
    update_notices()
    update_nav_logout()

