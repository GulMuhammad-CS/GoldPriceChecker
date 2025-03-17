# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Button
# import numpy as np
#
# # Force interactive backend
# matplotlib.use('TkAgg')  # Replace with 'Qt5Agg' or 'MacOSX' if needed TkAgg
# print(f"Using backend: {matplotlib.get_backend()}")
#
# # Sample data
# x_daily = np.arange(1, 31)  # Days 1 to 30
# y_daily = np.random.randint(50, 100, size=30)
#
# x_monthly = np.array([1, 15, 30])  # Monthly points
# y_monthly = np.array([1200, 1400, 1100])
#
# # Create a figure and axis
# fig, ax = plt.subplots()
# plt.subplots_adjust(bottom=0.2)
#
# # Plot daily and monthly data
# daily_plot, = ax.plot(x_daily, y_daily, label="Daily Data", color="blue")
# monthly_plot, = ax.plot(x_monthly, y_monthly, label="Monthly Data", color="orange")
# monthly_plot.set_visible(False)
#
# ax.set_title("Toggle Button Example: Daily Data")
# ax.set_xlabel("Days")
# ax.set_ylabel("Values")
# ax.legend()
#
# # Toggle function
# def toggle_data(event):
#     print("Button clicked")  # Debug message
#     if daily_plot.get_visible():
#         print("Switching to Monthly Data")
#         daily_plot.set_visible(False)
#         monthly_plot.set_visible(True)
#         ax.set_title("Monthly Data")
#     else:
#         print("Switching to Daily Data")
#         daily_plot.set_visible(True)
#         monthly_plot.set_visible(False)
#         ax.set_title("Daily Data")
#     plt.draw()
#
# # Create a button
# button_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
# button = Button(button_ax, "Toggle Data")
# button.on_clicked(toggle_data)
#
# plt.show()
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import mysql.connector

# Force interactive backend
matplotlib.use('TkAgg')  # Replace with 'Qt5Agg' or 'MacOSX' if needed
print(f"Using backend: {matplotlib.get_backend()}")

# Fetch data from database
def fetch_data():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Your MySQL username
            password="",  # Your MySQL password
            database="gold_tracker_db"
        )
        cursor = connection.cursor()

        # Query for daily data (assuming daily data is stored with a timestamp)
        cursor.execute("SELECT DATE(timestamp) AS date, AVG(gold_price) AS daily_avg FROM gold_price GROUP BY DATE(timestamp)")
        daily_data = cursor.fetchall()

        # Query for monthly data
        cursor.execute("SELECT MONTH(timestamp) AS month, YEAR(timestamp) AS year, AVG(gold_price) AS monthly_avg FROM gold_price GROUP BY YEAR(timestamp), MONTH(timestamp)")
        monthly_data = cursor.fetchall()

        return daily_data, monthly_data
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return [], []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Data from database
daily_data, monthly_data = fetch_data()

# Prepare daily data
x_daily = [row[0].day for row in daily_data]  # Extract day from date
y_daily = [row[1] for row in daily_data]     # Extract average gold price

# Prepare monthly data
x_monthly = [f"{row[1]}-{row[0]}" for row in monthly_data]  # Combine year and month
y_monthly = [row[2] for row in monthly_data]               # Extract average gold price

# Create a figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

# Plot daily and monthly data
daily_plot, = ax.plot(x_daily, y_daily, label="Daily Data", color="blue")
monthly_plot, = ax.plot(range(len(x_monthly)), y_monthly, label="Monthly Data", color="orange")
monthly_plot.set_visible(False)

ax.set_title("Toggle Button Example: Daily Data")
ax.set_xlabel("Days")
ax.set_ylabel("Gold Price (per gram)")
ax.legend()

# Toggle function
def toggle_data(event):
    if daily_plot.get_visible():
        print("Switching to Monthly Data")
        daily_plot.set_visible(False)
        monthly_plot.set_visible(True)
        ax.set_title("Monthly Data")
        ax.set_xticks(range(len(x_monthly)))  # Set x-ticks for months
        ax.set_xticklabels(x_monthly, rotation=45)  # Show month labels
    else:
        print("Switching to Daily Data")
        daily_plot.set_visible(True)
        monthly_plot.set_visible(False)
        ax.set_title("Daily Data")
        ax.set_xticks(x_daily)  # Set x-ticks for days
        ax.set_xticklabels(x_daily)
    plt.draw()

# Create a button
button_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
button = Button(button_ax, "Toggle Data")
button.on_clicked(toggle_data)

plt.show()
