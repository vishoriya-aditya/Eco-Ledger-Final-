import tkinter as tk
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt
from datetime import date

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="ecoledger"
)
cursor = db.cursor(buffered=True)

# ---------------- CONSTANTS ----------------
THRESHOLD = 5.0
current_user = None

carbon_factor = {
    "fruit": 0.4,
    "vegetable": 0.3,
    "non_veg": 1.2,
    "tobacco": 1.5,
    "bike": 0.10,
    "car": 0.21,
    "metro": 0.04
}

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("ECOLEDGER")
root.geometry("520x750")
root.configure(bg="#e8f5f2")

TITLE_FONT = ("Segoe UI", 20, "bold")
LABEL_FONT = ("Segoe UI", 11)
BTN_FONT = ("Segoe UI", 12, "bold")

def clear():
    for w in root.winfo_children():
        w.destroy()

# ---------------- ENTRY FRAME ----------------
def entry_frame():
    clear()

    tk.Label(
        root, text="ECOLEDGER",
        font=TITLE_FONT, bg="#e8f5f2", fg="#0d6efd"
    ).pack(pady=25)

    tk.Button(
        root, text="New User",
        font=BTN_FONT, width=22, height=2,
        bg="#198754", fg="white",
        command=signup_frame
    ).pack(pady=10)

    tk.Button(
        root, text="Existing User",
        font=BTN_FONT, width=22, height=2,
        bg="#0d6efd", fg="white",
        command=login_frame
    ).pack(pady=10)

# ---------------- SIGNUP FRAME ----------------
def signup_frame():
    clear()

    tk.Label(root, text="Create Account", font=TITLE_FONT,
             bg="#e8f5f2", fg="#0d6efd").pack(pady=15)

    tk.Label(root, text="Username", font=LABEL_FONT, bg="#e8f5f2").pack()
    u = tk.Entry(root, font=LABEL_FONT, width=30)
    u.pack(pady=5)

    tk.Label(root, text="Email", font=LABEL_FONT, bg="#e8f5f2").pack()
    e = tk.Entry(root, font=LABEL_FONT, width=30)
    e.pack(pady=5)

    tk.Label(root, text="Password", font=LABEL_FONT, bg="#e8f5f2").pack()
    p = tk.Entry(root, show="*", font=LABEL_FONT, width=30)
    p.pack(pady=5)

    def register():
        cursor.execute(
            "INSERT INTO users (username,email,password) VALUES (%s,%s,%s)",
            (u.get(), e.get(), p.get())
        )
        db.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        user_id = cursor.fetchone()[0]

        messagebox.showinfo(
            "Registration Successful",
            f"Account created successfully!\nYour User ID is: {user_id}"
        )
        entry_frame()

    tk.Button(
        root, text="Register",
        font=BTN_FONT, width=20, height=2,
        bg="#198754", fg="white",
        command=register
    ).pack(pady=15)

    tk.Button(
        root, text="Back",
        font=BTN_FONT, width=15,
        command=entry_frame
    ).pack()

# ---------------- LOGIN FRAME ----------------
def login_frame():
    clear()

    tk.Label(root, text="Login", font=TITLE_FONT,
             bg="#e8f5f2", fg="#0d6efd").pack(pady=20)

    tk.Label(root, text="Username", font=LABEL_FONT, bg="#e8f5f2").pack()
    u = tk.Entry(root, font=LABEL_FONT, width=30)
    u.pack(pady=5)

    tk.Label(root, text="Password", font=LABEL_FONT, bg="#e8f5f2").pack()
    p = tk.Entry(root, show="*", font=LABEL_FONT, width=30)
    p.pack(pady=5)

    def login():
        global current_user
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (u.get(), p.get())
        )
        user = cursor.fetchone()
        if user:
            current_user = user
            messagebox.showinfo(
                "Welcome",
                f"Hello {user[1]}!\nYour User ID is {user[0]}"
            )
            expense_frame()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    tk.Button(
        root, text="Login",
        font=BTN_FONT, width=20, height=2,
        bg="#0d6efd", fg="white",
        command=login
    ).pack(pady=15)

    tk.Button(
        root, text="Back",
        font=BTN_FONT, width=15,
        command=entry_frame
    ).pack()

# ---------------- EXPENSE DASHBOARD ----------------
def expense_frame():
    clear()

    tk.Label(root, text="Expense Dashboard", font=TITLE_FONT,
             bg="#e8f5f2", fg="#0d6efd").pack(pady=10)

    entries = {}
    for f in carbon_factor:
        tk.Label(root, text=f.capitalize(), font=LABEL_FONT,
                 bg="#e8f5f2").pack()
        ent = tk.Entry(root, font=LABEL_FONT, width=25)
        ent.pack(pady=2)
        entries[f] = ent

    tk.Label(root, text="Date (YYYY-MM-DD)", font=LABEL_FONT,
             bg="#e8f5f2").pack(pady=5)
    date_entry = tk.Entry(root, font=LABEL_FONT, width=25)
    date_entry.pack()

    info = tk.Label(root, text="", bg="#e8f5f2",
                    font=LABEL_FONT, fg="#198754")
    info.pack(pady=8)

    def submit():
        entered_date = date_entry.get()

        cursor.execute(
            "SELECT COUNT(*) FROM expense WHERE user_id=%s AND date=%s",
            (current_user[0], entered_date)
        )
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "Expense already added for this date")
            return

        values = {k: int(entries[k].get()) for k in entries}

        cursor.execute("""
            INSERT INTO expense
            (user_id, fruit, vegetable, non_veg, tobacco, bike, car, metro, date)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            current_user[0],
            values["fruit"], values["vegetable"],
            values["non_veg"], values["tobacco"],
            values["bike"], values["car"], values["metro"],
            entered_date
        ))
        db.commit()

        carbon = sum((values[k]/100)*carbon_factor[k] for k in carbon_factor)

        cursor.execute("SELECT streak FROM users WHERE user_id=%s",
                       (current_user[0],))
        streak = cursor.fetchone()[0]
        streak = streak + 1 if carbon <= THRESHOLD else 0

        cursor.execute("""
            UPDATE users SET prev_carbon=%s, streak=%s WHERE user_id=%s
        """, (carbon, streak, current_user[0]))
        db.commit()

        info.config(text=f"Carbon: {round(carbon,2)} kg | Streak: {streak} days")

        # -------- INSERT INTO WEEKLY_CARBON --------
        cursor.execute(
            "SELECT COUNT(*) FROM weekly_carbon WHERE user_id=%s",
            (current_user[0],)
        )
        day_count = cursor.fetchone()[0]

        if day_count < 7:
            day_no = day_count + 1
        else:
            cursor.execute(
                "DELETE FROM weekly_carbon WHERE user_id=%s",
                (current_user[0],)
            )
            db.commit()
            day_no = 1

        cursor.execute(
            "INSERT INTO weekly_carbon (user_id, day_no, carbon_value) VALUES (%s,%s,%s)",
            (current_user[0], day_no, carbon)
        )
        db.commit()

    tk.Button(root, text="Submit Expense",
              font=BTN_FONT, width=22, height=2,
              bg="#198754", fg="white",
              command=submit).pack(pady=6)

    tk.Button(root, text="Category Graph",
              font=BTN_FONT, width=22,
              command=show_category_graph).pack(pady=6)

    tk.Button(root, text="Weekly Graph",
              font=BTN_FONT, width=22,
              command=show_weekly_graph).pack(pady=3)

    tk.Button(root, text="View History",
              font=BTN_FONT, width=22,
              command=history_frame).pack(pady=3)

# -------- (category graph, weekly graph, history remain SAME as your logic) --------
# ---------------- WEEKLY GRAPH ----------------
def show_weekly_graph():
    cursor.execute("""
        SELECT day_no, carbon_value
        FROM weekly_carbon
        WHERE user_id=%s
        ORDER BY day_no
    """, (current_user[0],))

    data = cursor.fetchall()
    if not data:
        messagebox.showinfo("Info", "No weekly data available")
        return

    days = [row[0] for row in data]
    carbon = [row[1] for row in data]

    plt.plot(days, carbon, marker="o")
    plt.xticks(days, [f"Day {d}" for d in days])
    plt.xlabel("Day")
    plt.ylabel("Carbon (kg)")
    plt.title("Weekly Carbon Footprint")
    plt.show()

# ---------------- CATEGORY-WISE GRAPH ----------------
def show_category_graph():
    win = tk.Toplevel(root)
    win.title("Category-wise Carbon Graph")
    win.geometry("300x250")

    tk.Label(win, text="Enter User ID").pack()
    uid_entry = tk.Entry(win)
    uid_entry.pack()

    tk.Label(win, text="Enter Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(win)
    date_entry.pack()

    def plot():
        cursor.execute("""
            SELECT fruit, vegetable, non_veg, tobacco, bike, car, metro
            FROM expense
            WHERE user_id=%s AND date=%s
        """, (uid_entry.get(), date_entry.get()))

        row = cursor.fetchone()
        if not row:
            messagebox.showinfo("Info", "No data found for this date")
            return

        categories = list(carbon_factor.keys())
        carbon_values = [
            (row[i] / 100) * carbon_factor[categories[i]]
            for i in range(len(categories))
        ]

        plt.figure()
        plt.bar(categories, carbon_values)
        plt.xlabel("Category")
        plt.ylabel("Carbon Footprint (kg)")
        plt.title("Category-wise Carbon Footprint")
        plt.show()

    tk.Button(win, text="Show Graph", command=plot).pack(pady=10)


# ---------------- HISTORY ----------------
def history_frame():
    clear()

    tk.Label(root, text="View History", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="Enter User ID").pack()
    uid = tk.Entry(root)
    uid.pack()

    tk.Label(root, text="Enter Date (YYYY-MM-DD)").pack()
    d = tk.Entry(root)
    d.pack()

    out = tk.Label(root, text="", justify="left")
    out.pack(pady=10)

    def fetch():
        cursor.execute("""
            SELECT fruit, vegetable, non_veg, tobacco, bike, car, metro
            FROM expense
            WHERE user_id=%s AND date=%s
        """, (uid.get(), d.get()))

        row = cursor.fetchone()
        if not row:
            out.config(text="No data found")
            return

        labels = ["Fruit", "Vegetable", "Non-veg", "Tobacco", "Bike", "Car", "Metro"]
        text = "EXPENSE DETAILS\n----------------------\n"

        for l, v in zip(labels, row):
            text += f"{l}: {v}\n"

        out.config(text=text)

    tk.Button(root, text="Fetch", width=20, height=2,
              command=fetch).pack(pady=5)
    tk.Button(root, text="Back", width=20, height=2,
              command=expense_frame).pack(pady=5)

# ---------------- START APP ----------------
entry_frame()
root.mainloop()
