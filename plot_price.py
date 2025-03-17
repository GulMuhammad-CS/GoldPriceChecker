import mysql.connector
import matplotlib.pyplot as plt

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",            # Database host (usually localhost)
    user="root",                 # MySQL username (e.g., root)
    password="",                 # Your MySQL password
    database="gold_tracker_db"   # The name of your database
)

cursor = connection.cursor()

# Define the SQL query to fetch data from the table
query = "SELECT timestamp,gold_price  FROM gold_price"

cursor.execute(query)

data = cursor.fetchall()

# Process the data into two lists (x and y values)
x = [row[0] for row in data]
y = [row[1] for row in data]

# Close the cursor and the database connection
cursor.close()
connection.close()

# Plot the data using Matplotlib
plt.plot(x, y, marker='o', linestyle='-', color='b')  # Blue line with circle markers
plt.title("Gold Price plot")
plt.xlabel("X Axis Label")
plt.ylabel("Y Axis Label")
plt.grid(True)

# Display the plot
plt.show()