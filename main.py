from tkinter import *
import calendar
from datetime import datetime

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

#function to handle day click events
def on_day_click(day):
    selected_day_label.config(text=f"Selected day {day}")

#function to go to button
def go_to_today():
    now = datetime.now()
    display_calendar(now.month, now.year)

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

#to change the month and year add buttons
prev_button = Button(window, text="<< Previous", command=lambda: change_month(-1), font=30, bg="lightgray")
prev_button.pack(side=LEFT,padx=20)

next_button = Button(window, text="Next >>", command=lambda: change_month(1), font=30, bg="lightgray")
next_button.pack(side=RIGHT,padx=20)

#to add go to button
go_today_button = Button(window, text="Go to today", command=go_to_today)
go_today_button.pack(pady=10)

window.mainloop()