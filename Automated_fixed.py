from selenium import webdriver
from selenium.webdriver.common.by import By
import mysql.connector
from datetime import datetime
import time

# Fetch the Gold Price
def fetch_gold_price():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)

    url = 'https://goldprice.org/'
    driver.get(url)

    try:
        # Find the gold price per ounce
        gold_price_element = driver.find_element(By.CLASS_NAME, 'gpoticker-price')
        gold_price_ounce = gold_price_element.text
        gold_price_ounce = float(gold_price_ounce.replace(',', ''))  # Convert to float

        # Convert to price per gram
        gold_price_gram = gold_price_ounce / 31.1035
        driver.quit()
        return round(gold_price_gram, 2)  # Return price per gram rounded to 2 decimal places
    except Exception as e:
        driver.quit()
        raise Exception(f"Error fetching gold price: {e}")

# Insert Gold Price into Database
# Insert Gold Price into Database
def insert_gold_price_into_db(gold_price):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host="localhost",  # Change if your database is not on localhost
            user="root",  # Your MySQL username
            password="",  # Your MySQL password
        )

        cursor = connection.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS gold_tracker_db")

        # Connect to the database
        connection.database = "gold_tracker_db"

        # Create table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS gold_price (
            id INT AUTO_INCREMENT PRIMARY KEY,
            gold_price DECIMAL(10, 2) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)

        # Insert data into the table
        insert_query = """
        INSERT INTO gold_price (gold_price)
        VALUES (%s)
        """
        cursor.execute(insert_query, (gold_price,))

        # Commit the transaction
        connection.commit()

        print(f"Gold price {gold_price} successfully inserted into the database.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Main Function
# if __name__ == "__main__":
#
#     try:
#         # Fetch the current gold price
#         gold_price = fetch_gold_price()
#         print(f"Fetched Gold Price per Gram: {gold_price}")
#
#         # Insert the gold price into the database
#         insert_gold_price_into_db(gold_price)
#     except Exception as e:
#         print(f"Error: {e}")
if __name__ == "__main__":
    while True:
        try:
            print("Fetching data...")
            # Fetch the current gold price
            gold_price = fetch_gold_price()
            print(f"Fetched Gold Price per Gram: {gold_price}, fetched at: {datetime.now()}")

            # Insert the fetched gold price into the database
            insert_gold_price_into_db(gold_price)

            print("Data fetched and inserted into database. Waiting for the next interval.")
            time.sleep(3600)  #can change the interval as per requirement
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3600)   #can change the interval as per requirement
