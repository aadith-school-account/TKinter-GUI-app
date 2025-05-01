import tkinter as tk
import ttkbootstrap as tb

#chatgpt did this and idek why
from ttkbootstrap.widgets import DateEntry
from datetime import datetime, date
from tkinter import messagebox

def calculate_age():
    try:
        date_of_birth = date_entry.entry.get().strip() #gets entry for date of birth, strips string


        #error handling
        if not date_of_birth:
            raise ValueError("Date of birth cannot be empty.") #makes sure the string isn't empty

        birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')

        if birth_date > datetime.today():
            raise ValueError("Date of birth cannot be in the future.") #easy fix

        if birth_date.year <= 0:
            raise ValueError("Year must be greater than 0.")


        #checks today's date, calculate's date
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day)) #Subtracts todays year by birth year, checks for month
        age_in_months = (today.year - birth_date.year) * 12 + today.month - birth_date.month
        age_in_days = (today - birth_date).days
        output_text.set(f"You are {age} years, {age_in_months} months\nOr {age_in_days} days old.")

        if show_birthday_countdown.get():
            next_birthday = datetime(today.year, birth_date.month, birth_date.day)
            
            if next_birthday < today:
                    next_birthday = datetime(today.year + 1, birth_date.month, birth_date.day)
                    days_until_birthday = (next_birthday - today).days
                    countdown_text.set(f"Your next birthday is in {days_until_birthday} days.")


    #more error handling??? (CHATGPT)
    except ValueError as ve:
        messagebox.showerror("Invalid date", str(ve))
    except Exception:
        messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format.")

def toggle_birthday_countdown():
    """Toggles the visibility of the birthday countdown."""
    if show_birthday_countdown.get():
        countdown_label.pack(pady=10)  # Show countdown
    else:
        countdown_label.pack_forget()  # Hide countdown



#---------- INIT GUI ----------
# Initialize main window with ttkbootstrap style
style = tb.Style(theme="minty") #Can switch lol, superhero chill
root = style.master
root.title("Age Calculator")
root.geometry("400x300")
root.resizable(True, True)  # Make the window resizable lol

# Title label
title_label = tk.Label(root, text="Age Calculator", font=("Pristina", 30), bg=style.colors.bg, fg=style.colors.fg)
title_label.pack(pady=10) #pack makes it centered

# Date entry (with Calendar)
date_entry = DateEntry(root, bootstyle="info", dateformat="%Y-%m-%d", width=22)
date_entry.pack(pady=10)

# Calculate button
calc_button = tk.Button(root, text="Calculate Age", font=("Helvetica", 12), bg=style.colors.primary, fg="white",
                        command=calculate_age)
calc_button.pack(pady=10)

# Output text
output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, font=("Elephant", 10), bg=style.colors.bg, fg=style.colors.fg)
output_label.pack(pady=10)


# Toggle button for birthday countdown
show_birthday_countdown = tk.BooleanVar(value=False)  # default is False (hide countdown)
toggle_button = tk.Button(root, text="Toggle Birthday Countdown", font=("Helvetica", 10), bg=style.colors.primary, fg="white",
                          command=lambda: toggle_birthday_countdown())
toggle_button.pack(pady=10) 

# Countdown text label
countdown_text = tk.StringVar()
countdown_label = tk.Label(root, textvariable=countdown_text, font=("Helvetica", 12), bg=style.colors.bg, fg=style.colors.fg)


root.mainloop()
