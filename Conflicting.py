import mysql.connector

# Function to connect to MySQL
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="BigStep_CustomFit2"
    )

# Function for transaction 1: User A updates their address, while User B places an order
def transaction_1(conn):
    try:
        cursor = conn.cursor()

        # Start transaction
        cursor.execute("START TRANSACTION")

        # User A updates their address
        cursor.execute("""
            UPDATE Users SET Address = 'New Address for User A' WHERE Name = 'User A'
        """)

        # User B places an order
        cursor.execute("""
            INSERT INTO Orders (UserID, ProductID, OrderDate, DeliveryStatus, Quantity)
            VALUES (2, 3, '2024-04-20', 'Pending', 1)
        """)

        # Commit transaction
        conn.commit()

    except mysql.connector.Error as error:
        print("Error in Transaction 1:", error)
        conn.rollback()

    finally:
        cursor.close()

# Function for transaction 2: User A and User B both try to update their address
def transaction_2(conn):
    try:
        cursor = conn.cursor()

        # Start transaction
        cursor.execute("START TRANSACTION")

        # User A tries to update their address
        cursor.execute("""
            UPDATE Users SET Address = 'New Address for User A' WHERE Name = 'User A'
        """)

        # User B tries to update their address
        cursor.execute("""
            UPDATE Users SET Address = 'New Address for User B' WHERE Name = 'User B'
        """)

        # Commit transaction
        conn.commit()

    except mysql.connector.Error as error:
        print("Error in Transaction 2:", error)
        conn.rollback()

    finally:
        cursor.close()

# Function for transaction 3: User A and User B both try to place an order for the same product
def transaction_3(conn):
    try:
        cursor = conn.cursor()

        # Start transaction
        cursor.execute("START TRANSACTION")

        # User A tries to place an order
        cursor.execute("""
            INSERT INTO Orders (UserID, ProductID, OrderDate, DeliveryStatus, Quantity)
            VALUES (1, 3, '2024-04-20', 'Pending', 1)
        """)

        # User B tries to place an order
        cursor.execute("""
            INSERT INTO Orders (UserID, ProductID, OrderDate, DeliveryStatus, Quantity)
            VALUES (2, 3, '2024-04-20', 'Pending', 1)
        """)

        # Commit transaction
        conn.commit()

    except mysql.connector.Error as error:
        print("Error in Transaction 3:", error)
        conn.rollback()

    finally:
        cursor.close()

# Function for transaction 4: User A updates their address, while User B places an order
def transaction_4(conn):
    try:
        cursor = conn.cursor()

        # Start transaction
        cursor.execute("START TRANSACTION")

        # User A tries to update their address
        cursor.execute("""
            UPDATE Users SET Address = 'New Address for User A' WHERE Name = 'User A'
        """)

        # User B tries to place an order
        cursor.execute("""
            INSERT INTO Orders (UserID, ProductID, OrderDate, DeliveryStatus, Quantity)
            VALUES (2, 3, '2024-04-20', 'Pending', 1)
        """)

        # User A updates their address again
        cursor.execute("""
            UPDATE Users SET Address = 'Another New Address for User A' WHERE Name = 'User A'
        """)

        # User B places an order again
        cursor.execute("""
            INSERT INTO Orders (UserID, ProductID, OrderDate, DeliveryStatus, Quantity)
            VALUES (2, 3, '2024-04-20', 'Pending', 1)
        """)

        # Commit transaction
        conn.commit()

    except mysql.connector.Error as error:
        print("Error in Transaction 4:", error)
        conn.rollback()

    finally:
        cursor.close()

# Main function to execute all conflicting transactions
def execute_conflicting_transactions():
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

# Call the main function to execute conflicting transactions
execute_conflicting_transactions()
