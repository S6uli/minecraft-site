from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "💎 یه رمز مخفی برای مدیریت سشن‌ها"

# 📦 دیتابیس ساده
users_db = {}
reports = []
rank_requests = []
top_players = [
    {"rank": 1, "name": "AliCraft", "score": 983},
    {"rank": 2, "name": "Shadow_Pro", "score": 917},
    {"rank": 3, "name": "EnderSlayer", "score": 899}
]

# 📱 تشخیص موبایل
def is_mobile():
    ua = request.headers.get('User-Agent')
    return "Mobile" in ua or "Android" in ua or "iPhone" in ua

# ✅ صفحه تأیید گزارش
@app.route("/report_success")
def report_success():
    template = "report_success_mobile.html" if is_mobile() else "report_success.html"
    return render_template(template)

# 🏠 صفحه اصلی
@app.route("/", methods=["GET", "POST"])
def index():
    template = "mobile_index.html" if is_mobile() else "index.html"
    if "username" not in session:
        return render_template(template, error="not_registered")
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            print(f"✅ ثبت‌نام ساده برای: {username}")
            return redirect(url_for("success", username=username))
    return render_template(template)

# 📝 ثبت‌نام
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    ip_address = request.remote_addr

    users_db[username] = {
        "email": email, "password": password,
        "age": age, "ip": ip_address
    }
    print(f"🔔 ثبت‌نام کامل برای {username}")
    session["username"] = username
    return redirect(url_for("success", username=username))

# 🔑 ورود
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users_db and users_db[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="نام کاربری یا رمز اشتباه است")
    return render_template("login.html")

# 🟢 داشبورد
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        template = "mobile_dashboard.html" if is_mobile() else "dashboard.html"
        return render_template(template, username=session["username"])
    return redirect(url_for("login"))

# 🎉 موفقیت
@app.route("/success")
def success():
    username = request.args.get("username", "کاربر")
    template = "mobile_success.html" if is_mobile() else "success.html"
    return render_template(template, username=username)

# 🚪 خروج
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

# 🎮 بازی
@app.route("/play")
def play():
    template = "play_mobile.html" if is_mobile() else "play.html"
    return render_template(template)

# ⚠️ گزارش بازیکن
@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        report_data = {
            "player_name": request.form.get("player_name"),
            "type": request.form.get("type"),
            "details": request.form.get("details"),
            "reporter": session.get("username", "مهمان")
        }
        reports.append(report_data)
        print(f"🚨 گزارش ثبت شد: {report_data}")
        return redirect(url_for("report_success"))
    template = "report_mobile.html" if is_mobile() else "report_player.html"
    return render_template(template)

# 🛒 خرید رنک
@app.route("/rank")
def rank():
    template = "buy_rank_mobile.html" if is_mobile() else "buy_rank.html"
    return render_template(template)

# 📤 ارسال درخواست رنک
@app.route("/submit_rank", methods=["POST"])
def submit_rank():
    data = {
        "username": request.form.get("username"),
        "rank": request.form.get("rank"),
        "message": request.form.get("message"),
        "submitted_by": session.get("username", "مهمان")
    }
    rank_requests.append(data)
    print(f"🛒 درخواست رنک ثبت شد: {data}")
    return redirect(url_for("dashboard"))

# 🏅 برترین بازیکن‌ها
@app.route("/top")
def top():
    template = "top_mobile.html" if is_mobile() else "top_players.html"
    return render_template(template, players=top_players)

# 🚀 اجرای سرور
if __name__ == "__main__":
    app.run(host="192.168.1.101", port=5000, debug=True)