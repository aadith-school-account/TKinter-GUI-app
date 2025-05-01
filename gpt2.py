import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.widgets import DateEntry
from datetime import datetime, date
from tkinter import messagebox
import threading

def calculate_age():
    """Calculate the age and possibly the birthday countdown."""
    try:
        date_of_birth = date_entry.entry.get().strip()  # gets entry for date of birth, strips string

        # error handling
        if not date_of_birth:
            raise ValueError("Date of birth cannot be empty.")  # makes sure the string isn't empty

        birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')

        if birth_date > datetime.today():
            raise ValueError("Date of birth cannot be in the future.")  # easy fix

        if birth_date.year <= 0:
            raise ValueError("Year must be greater than 0.")

        # checks today's date, calculates date
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))  # Subtracts today's year by birth year, checks for month
        age_in_months = (today.year - birth_date.year) * 12 + today.month - birth_date.month
        age_in_days = (today - birth_date).days

        # Calculate the weekday the user was born on
        weekday = birth_date.strftime("%A")  # %A gives the full weekday name

        # Safely update the UI from a separate thread
        root.after(0, output_text.set, f"You are {age} years, {age_in_months} months\nOr {age_in_days} days old.\nYou were born on a {weekday}.")

        # Show birthday countdown if selected
        if show_birthday_countdown.get():
            next_birthday = datetime(today.year, birth_date.month, birth_date.day)
            
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, birth_date.month, birth_date.day)
            days_until_birthday = (next_birthday - today).days
            root.after(0, countdown_text.set, f"Your next birthday is in {days_until_birthday} days.")

    except ValueError as ve:
        messagebox.showerror("Invalid date", str(ve))
    except Exception:
        messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format.")

def toggle_birthday_countdown():
    """Toggles the visibility of the birthday countdown."""
    print(f"Toggling birthday countdown. Current state: {show_birthday_countdown.get()}")  # Debugging

    # Toggling the BooleanVar
    show_birthday_countdown.set(not show_birthday_countdown.get())

    # Safely update the UI from a separate thread
    root.after(0, update_countdown_label)

def update_countdown_label():
    """Updates the countdown label visibility."""
    if show_birthday_countdown.get():
        countdown_label.pack(pady=10)  # Show countdown with clean appearance
        animate_countdown_label(countdown_label)  # Animate it into view
        print("Countdown label displayed.")  # Debugging
    else:
        countdown_label.pack_forget()  # Hide countdown
        print("Countdown label hidden.")  # Debugging

def animate_countdown_label(label):
    """Animate the countdown label appearing with a fade-in effect."""
    label.place(relx=0.5, rely=1, anchor='center')  # Start off-screen, below
    fade_in(label)  # Animate fade-in

def fade_in(label, alpha=0):
    """Helper function to create a fade-in effect."""
    if alpha < 1:
        label.after(50, fade_in, label, alpha + 0.05)  # Increase alpha
        label.config(fg=rgba_to_hex(0, 0, 0, alpha))  # Change label color opacity

def rgba_to_hex(r, g, b, a):
    """Converts RGBA to Hex for color transparency (alpha blending)."""
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}{int(a * 255):02x}"

def on_calculate_button_click():
    """Runs the calculate_age function in a separate thread."""
    threading.Thread(target=calculate_age, daemon=True).start()

def on_toggle_button_click():
    """Runs the toggle_birthday_countdown function in a separate thread."""
    threading.Thread(target=toggle_birthday_countdown, daemon=True).start()

#---------- INIT GUI ----------
# Initialize main window with ttkbootstrap style
style = tb.Style(theme="minty")  # Can switch lol, superhero chill
root = style.master
root.title("Age Calculator")
root.geometry("400x350")
root.resizable(True, True)  # Make the window resizable lol

# Title label
title_label = tk.Label(root, text="Age Calculator", font=("Pristina", 30), bg=style.colors.bg, fg=style.colors.fg)
title_label.pack(pady=10)  # keep using pack() for layout

# Date entry (with Calendar)
date_entry = DateEntry(root, bootstyle="info", dateformat="%Y-%m-%d", width=22)
date_entry.pack(pady=10)  # keep using pack() for layout

# Calculate button with hover effect
calc_button = tk.Button(root, text="Calculate Age", font=("Helvetica", 12), bg=style.colors.primary, fg="white",
                        command=on_calculate_button_click)  # Use threaded function for calculate age
calc_button.pack(pady=10)  # keep using pack() for layout

# Output text
output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, font=("Elephant", 10), bg=style.colors.bg, fg=style.colors.fg)
output_label.pack(pady=10)  # keep using pack() for layout

# Toggle button for birthday countdown with hover effect
show_birthday_countdown = tk.BooleanVar(value=False)  # default is False (hide countdown)
toggle_button = tk.Button(root, text="Toggle Birthday Countdown", font=("Helvetica", 10), bg=style.colors.primary, fg="white",
                          command=on_toggle_button_click)  # Use threaded function for toggle birthday countdown
toggle_button.pack(pady=10)  # keep using pack() for layout

# Countdown text label
countdown_text = tk.StringVar()
countdown_label = tk.Label(root, textvariable=countdown_text, font=("Helvetica", 12), bg=style.colors.bg, fg=style.colors.fg)

# The countdown label will initially be hidden, so no need to pack it yet

root.mainloop()
