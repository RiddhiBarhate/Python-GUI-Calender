from tkinter import *
import calendar
from datetime import datetime
import json
from tkinter import simpledialog, messagebox

#create the main window
window = Tk()
window.title("GUI Calendar")
window.geometry("400x400")
window.config(bg="#ADD8E6")

#create a label for the calender title
label = Label(window, text="", font=("Arial", 50), pady=50, bg="#ADD8E6")
label.pack()

#create a frame to hold calender grid
frame = Frame(window)
frame.pack()

#get the current month and year
now = datetime.now()
current_day = now.day
current_year = now.year
current_month = now.month

#label to show selected day
selected_day_label = Label(window, text="Selected day : ")
selected_day_label.pack(pady=10)

#load and save event functions
events = {}

#global variables to track
delete_event_button = None
edit_event_button = None
dark_mode_on = False

#function to schedule an event
def schedule_event(day, month, year):
    event_text = simpledialog.askstring("Event", f"{day}-{month}-{year}")
    if event_text:
        event_date = f"{day}-{month}-{year}"
        if event_date in events:
            events[event_date].append(event_text)
        else:
            events[event_date] = [event_text]
        save_events()

#function to edit an event
def edit_event(event_date):
    if event_date in events:
        event_text = simpledialog.askstring("Edit Event", f"Edit event for date {event_date}:")
        if event_text:
            events[event_date] = [event_text]
            save_events()
            messagebox.showinfo("Event Edited", f"Event for {event_date} has been updated.")
            selected_day_label.config(text=f"Events for {event_date}:\n{event_text}")
    else:
        messagebox.showerror("Error", f"No event found for {event_date}.")

#function to delete an event
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

#function to save events to a JSON file
def save_events():
    with open("events.json","w") as f:
        json.dump(events,f)

#fuction to load events from a JSON file
def load_events():
    global events
    try:
        with open("events.json","r") as f:
            events = json.load(f)
    except FileNotFoundError:
        events = {}

#function to toggle dark mode
def toggle_dark_mode():
    global dark_mode_on
    dark_mode_on = not dark_mode_on
    if dark_mode_on:
        window.config(bg="black")
        label.config(bg="black", fg="white")
        
    else:
        window.config(bg="#ADD8E6")
        label.config(bg="#ADD8E6", fg="black")

#function to display current month and year
def display_calendar(month, year):
    global current_day, current_month, current_year

    #winfo.children() return the list of widgets in frame
    for widget in frame.winfo_children():
        widget.destroy()    #clear the frame before adding new widgets

    #update the label with current month and year
    if 1 <= month <= 12:
        label.config(text=f"{calendar.month_name[month]} {year}")
    else:
        label.config(text=f"Error: Invalid Month {month}")

    #get the days of the week and add them to calender grid
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    for idx,day in enumerate(days):
        day_label = Label(frame, text=day, font=("Times New Roman",35,"underline"), padx=10, pady=10)
        day_label.grid(row=0, column=idx)

    #get the month calender as a lis of a week
    cal = calendar.monthcalendar(year, month)

    #add each day in a calender grid
    for r,week in enumerate(cal,1):
        for c,day in enumerate(week):
            if day == 0:    #not in current month
                day_label = Label(frame, text="", font=40, padx=10, pady=10)
            else:
                #Check if today's day
                if day == now.day and month == now.month and year == now.year:
                    day_label = Label(frame, text=day, font=("Arial", 30, "bold"), bg="lightgray", padx=10, pady=10)
                else: 
                    day_label = Label(frame, text=day, font=40, padx=10, pady=10)

            #bind a click event to each day
            day_label.bind("<Button-1>", lambda event, d=day:on_day_click(d))

            day_label.grid(row=r,column=c)

#display the calender
if 1 <= current_month <= 12:
    display_calendar(current_month, current_year)
else:
    print(f"Error: Invalid current month {current_month}")

#function to handle day click events and show events
def on_day_click(day):
    global delete_event_button, edit_event_button

    schedule_event(day, current_month, current_year)

    event_date = f"{day}-{current_month}-{current_year}"
    if event_date in events:
        event_list = "\n".join(events[event_date])
        selected_day_label.config(text=f"Events for {event_date}:\n{event_list}")

         # Remove the old delete button and event button if it exists
        if delete_event_button:
            delete_event_button.destroy()
        if edit_event_button:
            edit_event_button.destroy()
            
        # Add a button to delete events and edit events
        edit_event_button = Button(window, text="Edit Event", command=lambda d=event_date :edit_event(d))
        edit_event_button.pack(pady=10)

        delete_event_button = Button(window, text="Delete Event", command=lambda: delete_event(day, current_month, current_year))
        delete_event_button.pack(pady=10)
    else:
        selected_day_label.config(text=f"No events for {event_date}")

#function to go to button
def go_to_today():
    now = datetime.now()
    display_calendar(now.month, now.year)

#function to add recurring events
def add_recurring_event():
    event_text = simpledialog.askstring("Recurring Event", "Enter recurring event:")
    if event_text:
        for month in range(1,13):
            event_date = f"{current_day}-{month}-{current_year}"
            if event_date in events:
                events[event_date].append(event_text)
            else:
                events[event_date] = [event_text]
        save_events()

#function to change the month and year
def change_month(delta):
    global current_month, current_year

    current_month += delta

    if current_month > 12:
        current_month = 1
        current_year += 1
    elif current_month < 1:
        current_month = 12
        current_year -= 1

    display_calendar(current_month,current_year)

#load the event when starting the program
load_events()

#to change the month and year add buttons
prev_button = Button(window, text="<< Previous", command=lambda: change_month(-1), font=30, bg="lightgray")
prev_button.pack(side=LEFT,padx=20)

next_button = Button(window, text="Next >>", command=lambda: change_month(1), font=30, bg="lightgray")
next_button.pack(side=RIGHT,padx=20)

#button for dark mode
dark_mode_button = Button(window, text="Dark Mode", command=toggle_dark_mode)
dark_mode_button.pack(pady=10)

#button to add recurring events
recurring_button = Button(window, text="Add Recurring Event", command=add_recurring_event)
recurring_button.pack(pady=10)

#to add go to button
go_today_button = Button(window, text="Go to today", command=go_to_today)
go_today_button.pack(pady=10)

window.mainloop()