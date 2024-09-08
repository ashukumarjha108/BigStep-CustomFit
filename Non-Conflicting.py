import mysql.connector

# Function to connect to MySQL
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="BigStep_CustomFit2"
    )

# Function for transaction 1: Add a new user and place an order
def transaction_1(conn):
    try:
        cursor = conn.cursor()

        # Start transaction
        cursor.execute("START TRANSACTION")

        # Inserting a new user
        cursor.execute("""
            INSERT INTO Users (Name, age, gender, email, address, MobileNumber, Password, orders)
            VALUES ('Raj', 28, 'Female', 'raj@example.com', '123 Park Avenue, New York, USA', '+1234567890', 'P456', 1)
        """)

        # Placing an order
        cursor.execute("""
            INSERT INTO Orders (UserID, ProductID, OrderDate, DeliveryStatus, Quantity)
            VALUES (LAST_INSERT_ID(), 3, '2024-04-20', 'Pending', 1)
        """)

        # Commit transaction
        conn.commit()

    except mysql.connector.Error as error:
        print("Error in Transaction 1:", error)
        conn.rollback()

    finally:
        cursor.close()

# Function for transaction 2: Update failed login attempts
def transaction_2(conn):
    try:
        cursor = conn.cursor()

        # Start transaction
        cursor.execute("START TRANSACTION")

        # Update failed login attempts
        cursor.execute("""
            UPDATE failedLogin SET attempts = 5 WHERE name = 'Dheeraj'
        """)

        # Commit transaction
        conn.commit()

    except mysql.connector.Error as error:
        print("Error in Transaction 2:", error)
        conn.rollback()

    finally:
        cursor.close()

# Function for transaction 3: Add feedback and update inventory
def transaction_3(conn):
    try:
        cursor = conn.cursor()

        # Start transaction
        cursor.execute("START TRANSACTION")

        # Add feedback
        cursor.execute("""
            INSERT INTO UserFeedback (UserID, FeedbackText, FeedbackDate)
            VALUES (6, 'Great experience!', '2024-04-20')
        """)

        # Update inventory
        cursor.execute("""
            UPDATE Inventory SET Quantity = Quantity - 2 WHERE ProductID = 3
        """)

        # Commit transaction
        conn.commit()

    except mysql.connector.Error as error:
        print("Error in Transaction 3:", error)
        conn.rollback()

    finally:
        cursor.close()

# Function for transaction 4: Update user information and process payment
def transaction_4(conn):
    try:
        cursor = conn.cursor()

        # Start transaction
        cursor.execute("START TRANSACTION")

        # Update user information
        cursor.execute("""
            UPDATE Users SET Address = '456 Elm St, New York, USA' WHERE Name = 'Ashu'
        """)

        # Process payment
        cursor.execute("""
            INSERT INTO Payment (UserID, Amount, PaymentDate, PaymentMethod)
            VALUES (2, 399.99, '2024-04-20', 'Credit Card')
        """)

        # Commit transaction
        conn.commit()

    except mysql.connector.Error as error:
        print("Error in Transaction 4:", error)
        conn.rollback()

    finally:
        cursor.close()

# Main function to execute all transactions
def execute_transactions():
    try:
        # Connect to MySQL
        conn = connect_to_mysql()

        # Execute transactions
        transaction_1(conn)
        transaction_2(conn)
        transaction_3(conn)
        transaction_4(conn)

    except mysql.connector.Error as error:
        print("Error:", error)

    finally:
        if conn.is_connected():
            conn.close()

# Call the main function to execute transactions
execute_transactions()
