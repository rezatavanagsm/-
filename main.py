# -*- coding: utf-8 -*-
"""
وقت‌یار - نمونه اولیه دسکتاپ با Python و Tkinter
اجرا: python main.py
تمام داده‌ها در فایل data.json کنار برنامه ذخیره می‌شوند.
"""
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, "data.json")

DOCTORS = [
    {"id": 1, "name": "دکتر علی محمدی", "specialty": "قلب و عروق",
     "experience": "۱۵ سال سابقه", "price": 350000, "rating": "۴.۹",
     "bio": "متخصص بیماری‌های قلب و عروق و فشار خون."},
    {"id": 2, "name": "دکتر سارا احمدی", "specialty": "پوست و مو",
     "experience": "۱۰ سال سابقه", "price": 280000, "rating": "۴.۸",
     "bio": "متخصص پوست، مو و بیماری‌های پوستی."},
    {"id": 3, "name": "دکتر رضا کریمی", "specialty": "ارتوپدی",
     "experience": "۱۲ سال سابقه", "price": 320000, "rating": "۴.۷",
     "bio": "متخصص استخوان، مفاصل و آسیب‌های ورزشی."},
    {"id": 4, "name": "دکتر مریم رضایی", "specialty": "کودکان",
     "experience": "۸ سال سابقه", "price": 250000, "rating": "۴.۹",
     "bio": "متخصص بیماری‌های کودکان و مراقبت سلامت کودک."},
]
TIME_SLOTS = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "16:00"]

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {"appointments": [], "user": "کاربر مهمان"}
        except (json.JSONDecodeError, OSError):
            pass
    return {"appointments": [], "user": "کاربر مهمان"}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class VaghtYarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("وقت‌یار | سامانه رزرو نوبت پزشکی")
        self.root.geometry("1050x720")
        self.root.minsize(850, 600)
        self.root.configure(bg="#f4f7fb")
        self.data = load_data()
        self.selected_doctor = None
        self.selected_time = tk.StringVar(value="")
        self.user_name = self.data.get("user", "کاربر مهمان")
        self.setup_style()
        self.build_ui()
        self.refresh_doctors()
        self.refresh_appointments()
        self.refresh_doctor_panel()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#f4f7fb")
        style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1)
        style.configure("TLabel", background="#f4f7fb", foreground="#253247",
                        font=("Tahoma", 10))
        style.configure("Title.TLabel", font=("Tahoma", 20, "bold"),
                        foreground="#155e9a", background="#f4f7fb")
        style.configure("Subtitle.TLabel", font=("Tahoma", 11),
                        foreground="#607286", background="#f4f7fb")
        style.configure("TButton", font=("Tahoma", 10), padding=7)
        style.configure("Primary.TButton", background="#1769aa", foreground="white")
        style.map("Primary.TButton", background=[("active", "#0f548d")])
        style.configure("Treeview", font=("Tahoma", 10), rowheight=32)
        style.configure("Treeview.Heading", font=("Tahoma", 10, "bold"))

    def build_ui(self):
        header = tk.Frame(self.root, bg="#155e9a", padx=20, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="▣ وقت‌یار", bg="#155e9a", fg="white",
                 font=("Tahoma", 22, "bold")).pack(side="right")
        tk.Label(header, text="سامانه آنلاین رزرو نوبت پزشکان",
                 bg="#155e9a", fg="#dceeff", font=("Tahoma", 10)).pack(side="right", padx=18)
        self.user_label = tk.Label(header, text=f"کاربر: {self.user_name}",
                                   bg="#155e9a", fg="white", font=("Tahoma", 10))
        self.user_label.pack(side="left")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=16)
        self.home_tab = ttk.Frame(self.notebook, padding=16)
        self.booking_tab = ttk.Frame(self.notebook, padding=16)
        self.appointments_tab = ttk.Frame(self.notebook, padding=16)
        self.doctor_tab = ttk.Frame(self.notebook, padding=16)
        self.login_tab = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(self.home_tab, text="صفحه اصلی")
        self.notebook.add(self.booking_tab, text="رزرو نوبت")
        self.notebook.add(self.appointments_tab, text="نوبت‌های من")
        self.notebook.add(self.doctor_tab, text="پنل پزشک")
        self.notebook.add(self.login_tab, text="ورود آزمایشی")
        self.build_home()
        self.build_booking()
        self.build_appointments()
        self.build_doctor_panel()
        self.build_login()

    def build_home(self):
        ttk.Label(self.home_tab, text="سلامت شما، اولویت ماست", style="Title.TLabel").pack(anchor="e")
        ttk.Label(self.home_tab, text="پزشک موردنظر را پیدا کنید و زمان مناسب را رزرو کنید.",
                  style="Subtitle.TLabel").pack(anchor="e", pady=(2, 14))
        search_row = ttk.Frame(self.home_tab)
        search_row.pack(fill="x", pady=5)
        ttk.Label(search_row, text="جستجو بر اساس نام یا تخصص:").pack(side="right", padx=6)
        self.search_var = tk.StringVar()
        search = ttk.Entry(search_row, textvariable=self.search_var, width=35, justify="right")
        search.pack(side="right", padx=5)
        search.bind("<KeyRelease>", lambda _e: self.refresh_doctors())
        ttk.Button(search_row, text="پاک کردن", command=lambda: self.search_var.set("")).pack(side="right")
        columns = ("doctor", "specialty", "experience", "rating", "price")
        self.home_tree = ttk.Treeview(self.home_tab, columns=columns, show="headings", height=12)
        headings = {"doctor":"نام پزشک", "specialty":"تخصص", "experience":"سابقه",
                    "rating":"امتیاز", "price":"هزینه ویزیت"}
        widths = {"doctor":190, "specialty":140, "experience":130, "rating":80, "price":150}
        for col in columns:
            self.home_tree.heading(col, text=headings[col], anchor="center")
            self.home_tree.column(col, width=widths[col], anchor="center")
        self.home_tree.pack(fill="both", expand=True, pady=10)
        self.home_tree.bind("<Double-1>", lambda _e: self.choose_doctor())
        actions = ttk.Frame(self.home_tab)
        actions.pack(fill="x")
        ttk.Button(actions, text="مشاهده و رزرو پزشک انتخاب‌شده",
                   style="Primary.TButton", command=self.choose_doctor).pack(side="right")
        ttk.Label(actions, text="برای انتخاب سریع، روی ردیف پزشک دوبار کلیک کنید.",
                  style="Subtitle.TLabel").pack(side="left")

    def build_booking(self):
        ttk.Label(self.booking_tab, text="رزرو نوبت", style="Title.TLabel").pack(anchor="e")
        self.doctor_info = ttk.Label(self.booking_tab, text="ابتدا از صفحه اصلی یک پزشک انتخاب کنید.",
                                     style="Subtitle.TLabel", justify="right")
        self.doctor_info.pack(anchor="e", pady=10)
        date_row = ttk.Frame(self.booking_tab)
        date_row.pack(fill="x", pady=8)
        ttk.Label(date_row, text="تاریخ مراجعه (مثال: 2026-11-25):").pack(side="right", padx=6)
        self.date_var = tk.StringVar(value="2026-11-25")
        ttk.Entry(date_row, textvariable=self.date_var, width=18, justify="center").pack(side="right")
        ttk.Label(self.booking_tab, text="ساعت‌های قابل رزرو:", style="Subtitle.TLabel").pack(anchor="e")
        slots_frame = ttk.Frame(self.booking_tab)
        slots_frame.pack(fill="x", pady=10)
        for i, slot in enumerate(TIME_SLOTS):
            ttk.Radiobutton(slots_frame, text=slot, value=slot,
                            variable=self.selected_time,
                            command=self.update_booking_button).grid(row=i//4, column=i%4, padx=12, pady=8)
        self.booking_status = ttk.Label(self.booking_tab, text="", style="Subtitle.TLabel")
        self.booking_status.pack(anchor="e", pady=5)
        self.book_button = ttk.Button(self.booking_tab, text="تأیید و ثبت نوبت",
                                      style="Primary.TButton", command=self.book)
        self.book_button.pack(anchor="e", pady=8)
        self.book_button.state(["disabled"])
        self.date_var.trace_add("write", lambda *_: self.update_booking_button())

    def build_appointments(self):
        ttk.Label(self.appointments_tab, text="داشبورد بیمار", style="Title.TLabel").pack(anchor="e")
        self.appointment_summary = ttk.Label(self.appointments_tab, text="", style="Subtitle.TLabel")
        self.appointment_summary.pack(anchor="e", pady=8)
        cols = ("doctor", "specialty", "date", "time", "status")
        self.appointment_tree = ttk.Treeview(self.appointments_tab, columns=cols, show="headings", height=12)
        labels = {"doctor":"پزشک", "specialty":"تخصص", "date":"تاریخ", "time":"ساعت", "status":"وضعیت"}
        for c in cols:
            self.appointment_tree.heading(c, text=labels[c], anchor="center")
            self.appointment_tree.column(c, anchor="center", width=150)
        self.appointment_tree.pack(fill="both", expand=True, pady=10)
        ttk.Button(self.appointments_tab, text="لغو نوبت انتخاب‌شده",
                   command=self.cancel_appointment).pack(anchor="e")

    def build_doctor_panel(self):
        ttk.Label(self.doctor_tab, text="پنل پزشک", style="Title.TLabel").pack(anchor="e")
        ttk.Label(self.doctor_tab, text="نمایش تمام رزروهای ثبت‌شده در نسخه آزمایشی",
                  style="Subtitle.TLabel").pack(anchor="e", pady=8)
        cols = ("doctor", "patient", "date", "time", "status")
        self.doctor_tree = ttk.Treeview(self.doctor_tab, columns=cols, show="headings", height=14)
        labels = {"doctor":"پزشک", "patient":"بیمار", "date":"تاریخ", "time":"ساعت", "status":"وضعیت"}
        for c in cols:
            self.doctor_tree.heading(c, text=labels[c], anchor="center")
            self.doctor_tree.column(c, anchor="center", width=160)
        self.doctor_tree.pack(fill="both", expand=True, pady=10)

    def build_login(self):
        ttk.Label(self.login_tab, text="ورود آزمایشی", style="Title.TLabel").pack(anchor="e")
        ttk.Label(self.login_tab, text="این فرم فقط نام کاربر را برای نمایش در نسخه دمو ذخیره می‌کند.",
                  style="Subtitle.TLabel").pack(anchor="e", pady=8)
        form = ttk.Frame(self.login_tab)
        form.pack(anchor="e", pady=15)
        ttk.Label(form, text="نام و نام خانوادگی:").grid(row=0, column=1, padx=8, pady=8, sticky="e")
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var, width=32, justify="right").grid(row=0, column=0, padx=8)
        ttk.Button(self.login_tab, text="ورود به سامانه", style="Primary.TButton",
                   command=self.login).pack(anchor="e")

    def refresh_doctors(self):
        if not hasattr(self, "home_tree"):
            return
        query = self.search_var.get().strip() if hasattr(self, "search_var") else ""
        for item in self.home_tree.get_children():
            self.home_tree.delete(item)
        for d in DOCTORS:
            if query and query not in d["name"] and query not in d["specialty"]:
                continue
            self.home_tree.insert("", "end", iid=str(d["id"]),
                values=(d["name"], d["specialty"], d["experience"], d["rating"], f'{d["price"]:,} تومان'))

    def choose_doctor(self):
        selected = self.home_tree.selection()
        if not selected:
            messagebox.showinfo("انتخاب پزشک", "ابتدا یک پزشک را از فهرست انتخاب کنید.")
            return
        doctor_id = int(selected[0])
        self.selected_doctor = next(d for d in DOCTORS if d["id"] == doctor_id)
        d = self.selected_doctor
        self.doctor_info.config(text=f'{d["name"]} | {d["specialty"]}\n{d["bio"]}\n{d["experience"]} | هزینه ویزیت: {d["price"]:,} تومان')
        self.selected_time.set("")
        self.notebook.select(self.booking_tab)
        self.update_booking_button()

    def update_booking_button(self):
        if not hasattr(self, "book_button"):
            return
        enabled = bool(self.selected_doctor and self.selected_time.get() and self.date_var.get().strip())
        if enabled:
            self.book_button.state(["!disabled"])
        else:
            self.book_button.state(["disabled"])
        self.refresh_slot_status()

    def refresh_slot_status(self):
        if not hasattr(self, "booking_status"):
            return
        if not self.selected_doctor:
            self.booking_status.config(text="برای رزرو، ابتدا پزشک را انتخاب کنید.")
            return
        date = self.date_var.get().strip()
        taken = [a["time"] for a in self.data["appointments"]
                 if a["doctor_id"] == self.selected_doctor["id"] and a["date"] == date
                 and a["status"] == "تأییدشده"]
        self.booking_status.config(text=("زمان‌های رزروشده: " + "، ".join(taken)) if taken
                                   else "در این تاریخ هنوز نوبتی برای این پزشک ثبت نشده است.")

    def book(self):
        if not self.selected_doctor:
            messagebox.showwarning("رزرو نوبت", "ابتدا پزشک را انتخاب کنید.")
            return
        date = self.date_var.get().strip()
        time = self.selected_time.get()
        if not date or len(date) != 10 or date[4] != "-" or date[7] != "-":
            messagebox.showwarning("تاریخ نامعتبر", "تاریخ را با قالب YYYY-MM-DD وارد کنید.")
            return
        for a in self.data["appointments"]:
            if (a["doctor_id"] == self.selected_doctor["id"] and a["date"] == date
                    and a["time"] == time and a["status"] == "تأییدشده"):
                messagebox.showerror("زمان رزروشده", "این زمان قبلاً رزرو شده است.")
                self.refresh_slot_status()
                return
        d = self.selected_doctor
        self.data["appointments"].append({
            "id": max([a.get("id", 0) for a in self.data["appointments"]] + [0]) + 1,
            "doctor_id": d["id"], "doctor": d["name"], "specialty": d["specialty"],
            "date": date, "time": time, "status": "تأییدشده", "patient": self.user_name
        })
        save_data(self.data)
        self.selected_time.set("")
        self.refresh_appointments()
        self.refresh_doctor_panel()
        self.update_booking_button()
        messagebox.showinfo("ثبت موفق", "نوبت با موفقیت ثبت شد.")
        self.notebook.select(self.appointments_tab)

    def refresh_appointments(self):
        if not hasattr(self, "appointment_tree"):
            return
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)
        rows = self.data["appointments"]
        active = sum(a["status"] == "تأییدشده" for a in rows)
        self.appointment_summary.config(text=f"کاربر: {self.user_name}   |   کل نوبت‌ها: {len(rows)}   |   نوبت فعال: {active}")
        for a in rows:
            self.appointment_tree.insert("", "end", iid=str(a["id"]),
                values=(a["doctor"], a["specialty"], a["date"], a["time"], a["status"]))

    def cancel_appointment(self):
        selected = self.appointment_tree.selection()
        if not selected:
            messagebox.showinfo("لغو نوبت", "ابتدا یک نوبت را انتخاب کنید.")
            return
        appointment_id = int(selected[0])
        for a in self.data["appointments"]:
            if a["id"] == appointment_id:
                if a["status"] != "تأییدشده":
                    messagebox.showinfo("لغو نوبت", "این نوبت قبلاً لغو شده است.")
                    return
                if messagebox.askyesno("تأیید لغو", "آیا از لغو این نوبت مطمئن هستید؟"):
                    a["status"] = "لغوشده"
                    save_data(self.data)
                    self.refresh_appointments()
                    self.refresh_doctor_panel()
                    self.refresh_slot_status()
                    messagebox.showinfo("لغو موفق", "نوبت لغو شد.")
                return

    def refresh_doctor_panel(self):
        if not hasattr(self, "doctor_tree"):
            return
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)
        for a in self.data["appointments"]:
            self.doctor_tree.insert("", "end",
                values=(a["doctor"], a.get("patient", "کاربر مهمان"),
                        a["date"], a["time"], a["status"]))

    def login(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("ورود", "لطفاً نام خود را وارد کنید.")
            return
        self.user_name = name
        self.data["user"] = name
        save_data(self.data)
        self.user_label.config(text=f"کاربر: {self.user_name}")
        self.refresh_appointments()
        messagebox.showinfo("ورود آزمایشی", f"خوش آمدید {name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VaghtYarApp(root)
    root.mainloop()
