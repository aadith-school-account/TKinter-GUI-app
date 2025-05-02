import tkinter as tk
import ttkbootstrap as tb
import requests
from ttkbootstrap.widgets import DateEntry
from datetime import datetime
from tkinter import messagebox
from database import setup_db, update_score, get_scores  # Corrected function names

setup_db()
# Modify `highlight_winner()` to save scores
def highlight_winner(cells):
    global current_player
    for row, col in cells:
        board[row][col].config(bootstyle="success")

    # Save score in database
    print(f"DEBUG: Calling update_score() for {current_player}")
    update_score(current_player)
    
    messagebox.showinfo("Tic Tac Toe", f"{current_player} wins!")

# Modify `show_scores()` to fetch scores from database
def show_scores():
    scores = get_scores()
    leaderboard = "\n".join([f"{player}: {wins} wins" for player, wins in scores])
    messagebox.showinfo("Leaderboard", leaderboard if scores else "No games played yet.")


# Function to fetch real-time weather data
def get_weather():
    city = city_entry.get().strip()
    
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    api_key = "83fe2b6ef09b46208ef122932250205"  # Replace with your actual API key
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            messagebox.showerror("Error", data["error"]["message"])
        else:
            location = data["location"]["name"]
            temp_c = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            
            weather_output.set(f"🌎 {location}\n⛅ {condition}")
            temp_output.set(f"{temp_c}°C")

    except Exception as e:
        messagebox.showerror("Error", "Could not fetch weather data. Check your internet connection.")

# Function to calculate age
def calculate_age():
    try:
        date_of_birth = date_entry.entry.get().strip()

        if not date_of_birth:
            raise ValueError("Date of birth cannot be empty.")

        birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')

        if birth_date > datetime.today():
            raise ValueError("Date of birth cannot be in the future.")

        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        age_in_months = (today.year - birth_date.year) * 12 + today.month - birth_date.month
        age_in_days = (today - birth_date).days
        output_text.set(f"✨ You are {age} years, {age_in_months} months\nOr {age_in_days} days old!")

    except ValueError as ve:
        messagebox.showerror("Invalid date", str(ve))
    except Exception:
        messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format.")

# Tic Tac Toe Game
def reset_game():
    global board, current_player
    current_player = "X"
    for row in range(3):
        for col in range(3):
            board[row][col].config(text="", bootstyle="secondary-outline", state="normal")

def check_winner():
    for row in range(3):
        if board[row][0]["text"] == board[row][1]["text"] == board[row][2]["text"] and board[row][0]["text"] != "":
            highlight_winner([(row, 0), (row, 1), (row, 2)])
            return True

    for col in range(3):
        if board[0][col]["text"] == board[1][col]["text"] == board[2][col]["text"] and board[0][col]["text"] != "":
            highlight_winner([(0, col), (1, col), (2, col)])
            return True

    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] and board[0][0]["text"] != "":
        highlight_winner([(0, 0), (1, 1), (2, 2)])
        return True

    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] and board[0][2]["text"] != "":
        highlight_winner([(0, 2), (1, 1), (2, 0)])
        return True

    if all(board[row][col]["text"] != "" for row in range(3) for col in range(3)):
        messagebox.showinfo("Tic Tac Toe", "It's a Tie!")
        return True

    return False

def highlight_winner(cells):
    for row, col in cells:
        board[row][col].config(bg="lightgreen")
    messagebox.showinfo("Tic Tac Toe", f"{current_player} wins!")

def on_click(row, col):
    global current_player
    if board[row][col]["text"] == "":
        board[row][col].config(text=current_player)
        if check_winner():
            for r in range(3):
                for c in range(3):
                    board[r][c].config(state="disabled")
        else:
            current_player = "O" if current_player == "X" else "X"

# Initialize main window
style = tb.Style(theme="minty")
root = style.master
root.title("Utility App")
root.geometry("450x400")

# Create notebook for tabs
notebook = tb.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# Age Calculator Tab
age_frame = tb.Frame(notebook)
notebook.add(age_frame, text="📅 Age Calculator")

title_label = tk.Label(age_frame, text="Age Calculator", font=("Pristina", 30, "bold"))
title_label.pack(pady=10)

date_entry = DateEntry(age_frame, bootstyle="info", dateformat="%Y-%m-%d", width=22)
date_entry.pack(pady=10)

calc_button = tb.Button(age_frame, text="Calculate Age", bootstyle="primary-outline", command=calculate_age)
calc_button.pack(pady=10)

output_text = tk.StringVar()
output_label = tk.Label(age_frame, textvariable=output_text, font=("Comic Sans MS", 12, "bold"))
output_label.pack(fill="both", expand=True, pady=10)

# Weather App Tab
weather_frame = tb.Frame(notebook)
notebook.add(weather_frame, text="☀️ Weather App")

weather_label = tk.Label(weather_frame, text="Weather App", font=("Pristina", 30, "bold"))
weather_label.pack(pady=10)

city_entry = tk.Entry(weather_frame, width=30, font=("Helvetica", 12))
city_entry.pack(pady=10)

weather_button = tb.Button(weather_frame, text="Get Weather", bootstyle="success-outline", command=get_weather)
weather_button.pack(pady=10)

weather_output = tk.StringVar()
weather_result_label = tk.Label(weather_frame, textvariable=weather_output, font=("Comic Sans MS", 12, "bold"))
weather_result_label.pack(fill="both", expand=True, pady=5)

temp_output = tk.StringVar()
temp_label = tk.Label(weather_frame, textvariable=temp_output, font=("Elephant", 16, "bold"), fg="red")
temp_label.pack(pady=5)

# Tic Tac Toe Tab
tic_tac_toe_frame = tb.Frame(notebook)
notebook.add(tic_tac_toe_frame, text="🎮 Tic Tac Toe")

board = [[None] * 3 for _ in range(3)]
current_player = "X"

# Tic Tac Toe Grid (Using `.grid()` instead of `.pack()`)
for row in range(3):
    for col in range(3):
        board[row][col] = tb.Button(tic_tac_toe_frame, text="", width=6, bootstyle="secondary-outline",
                                    command=lambda r=row, c=col: on_click(r, c))
        board[row][col].grid(row=row, column=col, padx=5, pady=5)  # Places in correct row/column

reset_button = tb.Button(tic_tac_toe_frame, text="Restart Game", bootstyle="danger", command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3, pady=10)  # Center reset button below board
# Update Winner Highlight Function
def highlight_winner(cells):
    for row, col in cells:
        board[row][col].config(bootstyle="success")  # Uses ttkbootstrap styling instead of `bg`
    messagebox.showinfo("Tic Tac Toe", f"{current_player} wins!")


leaderboard_button = tb.Button(tic_tac_toe_frame, text="Leaderboard", bootstyle="info-outline", command=show_scores)
leaderboard_button.grid(row=4, column=0, columnspan=3, pady=10)


root.mainloop()
