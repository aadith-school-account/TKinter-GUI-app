import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.widgets import DateEntry
from datetime import datetime, date
from tkinter import messagebox
import threading
import time

dateformat="%Y-%m-%d"

def fade_in_label(label):
    for i in range(0, 101, 10):
        label.configure(foreground=f"#{i:02x}{i:02x}{i:02x}")
        label.update()
        time.sleep(0.01)

def calculate_age():
    try:
        raw_date = date_entry.entry.get().strip()
        print(f"DEBUG: Raw date from entry = {raw_date}")  # debug output

        # Try parsing it as YYYY-MM-DD (your intended format)
        try:
            birth_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format. Please use the calendar or type it like 2005-04-01.")

        today = date.today()
        if birth_date > today:
            raise ValueError("Date of birth cannot be in the future.")

        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        age_months = (today.year - birth_date.year) * 12 + today.month - birth_date.month
        age_days = (today - birth_date).days
        age_weeks = age_days // 7

        output_text.set(f"You are {age_years} years\n({age_months} months, {age_weeks} weeks, {age_days} days) old.")

        if show_birthday_countdown.get():
            next_birthday = date(today.year, birth_date.month, birth_date.day)
            if next_birthday < today:
                next_birthday = date(today.year + 1, birth_date.month, birth_date.day)
            days_until = (next_birthday - today).days
            countdown_text.set(f"🎉 Next birthday in {days_until} days!")
            countdown_label.pack(pady=10)
        else:
            countdown_label.pack_forget()

    except ValueError as ve:
        messagebox.showerror("Invalid Input", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")

def show_popup(years, months, days, weeks):
    popup = tk.Toplevel(root)
    popup.title("🎂 Age Breakdown")
    popup.geometry("300x200")
    popup.config(bg=style.colors.bg)

    tk.Label(popup, text="Detailed Age", font=("Arial Rounded MT Bold", 14), bg=style.colors.bg, fg=style.colors.fg).pack(pady=10)
    tk.Label(popup, text=f"{years} years", font=("Helvetica", 12), bg=style.colors.bg).pack()
    tk.Label(popup, text=f"{months} months", font=("Helvetica", 12), bg=style.colors.bg).pack()
    tk.Label(popup, text=f"{weeks} weeks", font=("Helvetica", 12), bg=style.colors.bg).pack()
    tk.Label(popup, text=f"{days} days", font=("Helvetica", 12), bg=style.colors.bg).pack()
    tk.Button(popup, text="Close", command=popup.destroy, bootstyle="danger-outline").pack(pady=10)

def on_calculate_click():
    threading.Thread(target=calculate_age, daemon=True).start()

def toggle_birthday_countdown():
    show_birthday_countdown.set(not show_birthday_countdown.get())
    if show_birthday_countdown.get():
        toggle_button.config(text="Hide Birthday Countdown")
    else:
        countdown_label.pack_forget()
        countdown_text.set("")
        toggle_button.config(text="Show Birthday Countdown")

# ------------- GUI INIT -------------
style = tb.Style(theme="flatly")
root = style.master
root.title("🎈 Age Calculator")
root.geometry("450x400")
root.resizable(False, False)

# Frame-based layout
frame = tb.Frame(root, padding=20)
frame.pack(fill='both', expand=True)

tk.Label(frame, text="Enter your birth date:", font=("Segoe UI", 12)).pack(pady=(10, 5))
date_entry = DateEntry(root, dateformat="%Y-%m-%d", width=22)
date_entry.pack(pady=200)

calc_button = tb.Button(frame, text="Calculate Age", bootstyle="success", command=on_calculate_click)
calc_button.pack(pady=10)

output_text = tk.StringVar()
output_label = tk.Label(frame, textvariable=output_text, font=("Helvetica", 11), bg=style.colors.bg)
output_label.pack(pady=10)

show_birthday_countdown = tk.BooleanVar(value=False)
toggle_button = tb.Button(frame, text="Show Birthday Countdown", bootstyle="primary-outline", command=toggle_birthday_countdown)
toggle_button.pack()

countdown_text = tk.StringVar()
countdown_label = tk.Label(frame, textvariable=countdown_text, font=("Segoe UI", 11), bg=style.colors.bg)

root.mainloop()
