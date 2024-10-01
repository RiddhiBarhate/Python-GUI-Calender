from tkinter import *
import calendar
from datetime import datetime
import json
from tkinter import simpledialog, messagebox

# Create the main window
window = Tk()
window.title("GUI Calendar")
window.geometry("500x600")
window.config(bg="#ADD8E6")

# Create a label for the calendar title
label = Label(window, text="", font=("Arial", 30), pady=20, bg="#ADD8E6")
label.pack()

# Create a frame to hold the calendar grid
frame = Frame(window)
frame.pack()

# Label to show selected day
selected_day_label = Label(window, text="Selected day:", bg="#ADD8E6")
selected_day_label.pack(pady=10)

# Load and save event functions
events = {}

# Global variables
delete_event_button = None
edit_event_button = None
dark_mode_on = False

# Function to schedule an event
def schedule_event(day, month, year):
    event_text = simpledialog.askstring("Event", f"{day}-{month}-{year}")
    if event_text:
        event_date = f"{day}-{month}-{year}"
        if event_date in events:
            events[event_date].append(event_text)
        else:
            events[event_date] = [event_text]
        save_events()

# Function to edit an event
def edit_event(event_date):
    if event_date in events:
        event_text = simpledialog.askstring("Edit Event", f"Edit event for {event_date}:")
        if event_text:
            events[event_date] = [event_text]
            save_events()
            messagebox.showinfo("Event Edited", f"Event for {event_date} has been updated.")
            selected_day_label.config(text=f"Events for {event_date}:\n{event_text}")
    else:
        messagebox.showerror("Error", f"No event found for {event_date}.")

# Function to delete an event
def delete_event(day, month, year):
    event_date = f"{day}-{month}-{year}"
    if event_date in events:
        event_list = events[event_date]
        event_to_delete = simpledialog.askstring("Delete Event", f"Choose an event to delete:\n{', '.join(event_list)}\nType the exact event to delete:")
        if event_to_delete in event_list:
            event_list.remove(event_to_delete)
            if not event_list:  # Remove the date entry if no events left
                del events[event_date]
            save_events()
            selected_day_label.config(text=f"Deleted event from {event_date}.")
        else:
            messagebox.showerror("Error", "Event not found!")
    else:
        messagebox.showinfo("Info", f"No events for {event_date} to delete.")

# Function to save events to a JSON file
def save_events():
    with open("events.json", "w") as f:
        json.dump(events, f)

# Function to load events from a JSON file
def load_events():
    global events
    try:
        with open("events.json", "r") as f:
            events = json.load(f)
    except FileNotFoundError:
        events = {}

# Function to toggle dark mode
def toggle_dark_mode():
    global dark_mode_on
    dark_mode_on = not dark_mode_on
    if dark_mode_on:
        window.config(bg="black")
        label.config(bg="black", fg="white")
    else:
        window.config(bg="#ADD8E6")
        label.config(bg="#ADD8E6", fg="black")

# Function to display the calendar
def display_calendar(month, year):
    global current_day, current_month, current_year
    for widget in frame.winfo_children():
        widget.destroy()  # Clear the frame before adding new widgets

    # Update the label with the current month and year
    label.config(text=f"{calendar.month_name[month]} {year}")

    # Get the days of the week and add them to the calendar grid
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for idx, day in enumerate(days):
        day_label = Label(frame, text=day, font=("Arial", 15, "bold"), padx=10, pady=10)
        day_label.grid(row=0, column=idx)

    # Get the month calendar as a list of weeks
    cal = calendar.monthcalendar(year, month)

    # Add each day to the calendar grid
    for r, week in enumerate(cal, 1):
        for c, day in enumerate(week):
            if day == 0:  # Not a valid day in the current month
                day_label = Label(frame, text="", font=("Arial", 12), padx=10, pady=10)
            else:
                if day == current_day and month == current_month and year == current_year:
                    day_label = Label(frame, text=day, font=("Arial", 12, "bold"), bg="lightgray", padx=10, pady=10)
                else:
                    day_label = Label(frame, text=day, font=("Arial", 12), padx=10, pady=10)

            # Bind a click event to each day
            day_label.bind("<Button-1>", lambda event, d=day: on_day_click(d))

            day_label.grid(row=r, column=c)

# Function to handle day click events
def on_day_click(day):
    global delete_event_button, edit_event_button
    schedule_event(day, current_month, current_year)
    event_date = f"{day}-{current_month}-{current_year}"
    if event_date in events:
        selected_day_label.config(text=f"Events for {event_date}:\n{', '.join(events[event_date])}")

        # Remove old delete button and edit button if they exist
        if delete_event_button:
            delete_event_button.destroy()
        if edit_event_button:
            edit_event_button.destroy()

        # Add a button to delete and edit events
        edit_event_button = Button(window, text="Edit Event", command=lambda d=event_date: edit_event(d))
        edit_event_button.pack(pady=5)

        delete_event_button = Button(window, text="Delete Event", command=lambda: delete_event(day, current_month, current_year))
        delete_event_button.pack(pady=5)
    else:
        selected_day_label.config(text=f"No events for {event_date}")

# Function to add recurring events
def add_recurring_event():
    event_text = simpledialog.askstring("Recurring Event", "Enter a recurring event:")
    if event_text:
        for month in range(1, 13):
            event_date = f"{current_day}-{month}-{current_year}"
            if event_date in events:
                events[event_date].append(event_text)
            else:
                events[event_date] = [event_text]
        save_events()

# Function to go to today's date
def go_to_today():
    global current_day, current_month, current_year
    now = datetime.now()
    current_day, current_month, current_year = now.day, now.month, now.year
    display_calendar(current_month, current_year)

# Function to change the month and year
def change_month(delta):
    global current_month, current_year
    current_month += delta
    if current_month > 12:
        current_month = 1
        current_year += 1
    elif current_month < 1:
        current_month = 12
        current_year -= 1
    display_calendar(current_month, current_year)

# Load the events when starting the program
load_events()

# Get the current date
now = datetime.now()
current_day = now.day
current_year = now.year
current_month = now.month

# Display the calendar
display_calendar(current_month, current_year)

# Buttons to change the month and year
prev_button = Button(window, text="<< Previous", command=lambda: change_month(-1), font=("Arial", 12), bg="lightgray")
prev_button.pack(side=LEFT, padx=20, pady=20)

next_button = Button(window, text="Next >>", command=lambda: change_month(1), font=("Arial", 12), bg="lightgray")
next_button.pack(side=RIGHT, padx=20, pady=20)

# Button for dark mode
dark_mode_button = Button(window, text="Toggle Dark Mode", command=toggle_dark_mode, font=("Arial", 12))
dark_mode_button.pack(pady=10)

# Button to go to today's date
go_today_button = Button(window, text="Go to Today", command=go_to_today, font=("Arial", 12))
go_today_button.pack(pady=10)

# Button to add recurring events
recurring_button = Button(window, text="Add Recurring Event", command=add_recurring_event, font=("Arial", 12))
recurring_button.pack(pady=10)

# Start the Tkinter main loop
window.mainloop()


