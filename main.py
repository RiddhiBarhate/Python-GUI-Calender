from tkinter import *
import calendar
from datetime import datetime

#create the main window
window = Tk()
window.title("GUI Calender")
window.geometry("400x400")

#create a label for the calender title
label = Label(window, text="", font=("Arial", 16), pady=10)
label.pack()

#create a frame to hold calender grid
frame = Frame(window)
frame.pack()

#function to display current month and year
def display_calendar(month, year):
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
        day_label = Label(frame, text=day, padx=10, pady=10)
        day_label.grid(row=0, column=idx)

    #get the month calender as a lis of a week
    cal = calendar.monthcalendar(year, month)

    #add each day in a calender grid
    for r,week in enumerate(cal,1):
        for c,day in enumerate(week):
            if day == 0:    #not in current month
                day_label = Label(frame, text="", padx=10, pady=10)
            else:
                day_label = Label(frame, text=day, padx=10, pady=10)
            day_label.grid(row=r,column=c)


#get the current month and year
now = datetime.now()
current_year = now.year
current_month = now.month

#display the calender
if 1 <= current_month <= 12:
    display_calendar(current_month, current_year)
else:
    print(f"Error: Invalid current month {current_month}")

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
prev_button = Button(window, text="<< Previous", command=lambda: change_month(-1))
prev_button.pack(side=LEFT,padx=20)

next_button = Button(window, text="Next >>", command=lambda: change_month(1))
next_button.pack(side=RIGHT,padx=20)

window.mainloop()