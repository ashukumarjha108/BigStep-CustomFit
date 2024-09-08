import pymysql
import getpass

DB_HOST = 'localhost'
DB_USER = 'root'
DB_NAME = 'BigStep_CustomFit2'

def connect_to_database(password):
    """
    Connect to the database using the provided password.
    """
    try:
        return pymysql.connect(host=DB_HOST, user=DB_USER, password=password, database=DB_NAME)
    except pymysql.Error as e:
        print(f"Database connection error: {e}")
        return None

def setup_database(cursor):
    """
    Set up the database by creating tables, altering the 'Orders' table, creating triggers.
    """
    try:        
        # Check if the 'Size' column exists in the 'Orders' table
        cursor.execute("SHOW COLUMNS FROM Orders LIKE 'Size'")
        if not cursor.fetchone():
            # Alter the 'Orders' table to include 'Size' and 'Color' columns
            cursor.execute("ALTER TABLE Orders ADD COLUMN Size VARCHAR(50)")
            cursor.execute("ALTER TABLE Orders ADD COLUMN Color VARCHAR(50)")
        print("Database setup completed successfully.")

        # Create Inventory table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Inventory (
                ProductID INT AUTO_INCREMENT PRIMARY KEY,
                ProductName VARCHAR(255),
                Quantity INT
            )
        """)
        
    except pymysql.Error as e:
        print(f"Error setting up database: {e}")

def display_customizations(cursor):
    """
    Display available customizations.
    """
    try:
        cursor.execute("SELECT * FROM Customization")
        customizations = cursor.fetchall()
        print("Available Customizations:")
        for customization in customizations:
            print(f"Customization ID: {customization[0]}")
            print(f"Size: {customization[2]}, Color: {customization[3]}, Design: {customization[4]}")
            print()
    except pymysql.Error as e:
        print(f"Error fetching customizations: {e}")

def view_products(cursor):
    """
    View all products.
    """
    try:
        cursor.execute("SELECT * FROM Product")
        products = cursor.fetchall()
        for product in products:
            print(product)
    except pymysql.Error as e:
        print(f"Error fetching products: {e}")

def search_products(cursor, keyword):
    """
    Search for products by keyword.
    """
    try:
        query = "SELECT * FROM Product WHERE Name LIKE %s"
        cursor.execute(query, ('%' + keyword + '%'))
        products = cursor.fetchall()
        if products:
            print("Products found:")
            for product in products:
                print(product)
            return True  # Products found
        else:
            print("No products found matching the search keyword.")
            return False  # No products found
    except pymysql.Error as e:
        print(f"Error fetching products: {e}")
        return False  # Error occurred

def place_order(cursor, user_id):
    """
    Place an order for the user.
    """
    try:
        view_products(cursor)
        product_id = input("Enter product ID to place order: ")
        quantity = int(input("Select quantity to place order: "))  # Convert input to integer
        while quantity >= 5:
            print("You cannot order more than 5 products.")
            quantity = int(input("Select quantity to place order: "))
            return quantity
        
        cursor.execute("SELECT * FROM Product WHERE ProductID = %s", (product_id,))
        product = cursor.fetchone()
        if product:
            size = input("Enter product size: ")
            color = input("Enter product color: ")
            customization_choice = input("Do you want to apply any customizations? (yes/no): ").lower()
            if customization_choice == 'yes':
                display_customizations(cursor)
                customization_id = input("Enter Customization ID to place order: ")
                # Insert order into the 'Orders' table with a reference to the 'CustomizationID'
                cursor.execute("INSERT INTO Orders (UserID, ProductID, Size, Color, OrderDate, DeliveryStatus, Quantity, CustomizationID) VALUES (%s, %s, %s, %s, CURDATE(), 'Pending', %s, %s)", (user_id, product_id, size, color, quantity, customization_id))
                amount = product[2] * quantity  # Calculate the total amount
                print("Total Amount:", amount)
                payment_method = input("Enter payment method (e.g., Credit card, Debit card, COD, Net Banking): ")
                print("Order placed successfully!")
                # Update inventory
                update_inventory(cursor, product_id, quantity)
                add_payment_details(cursor, user_id, amount, payment_method)
            else:
                # Insert order into the 'Orders' table without any customization
                cursor.execute("INSERT INTO Orders (UserID, ProductID, Size, Color, OrderDate, DeliveryStatus, Quantity) VALUES (%s, %s, %s, %s, CURDATE(), 'Pending', %s)", (user_id, product_id, size, color, quantity))
                amount = product[4] * quantity  # Calculate the total amount
                print("Total Amount:", amount)
                payment_method = input("Enter payment method (e.g., Credit card, Debit card, COD, Net Banking): ")
                print("Order placed successfully!")
                # Update inventory
                update_inventory(cursor, product_id, quantity)
                add_payment_details(cursor, user_id, amount, payment_method)
        else:
            print("Product not found or unavailable.")
    except ValueError:
        print("Please enter a valid quantity.")
    except pymysql.Error as e:
        print(f"Error placing order: {e}")
    except IndexError:
        print("Error: Product tuple index out of range. Please check product ID.")



def display_inventory(cursor):
    """
    Display the inventory.
    """
    try:
        cursor.execute("SELECT * FROM Inventory")
        inventory = cursor.fetchall()
        print("Inventory:")
        print("ProductID\tProductName\t\tQuantity")
        print("---------------------------------------------")
        for item in inventory:
            print(f"{item[0]}\t\t{item[1]}\t\t{item[2]}")
    except pymysql.Error as e:
        print(f"Error fetching inventory: {e}")

def update_inventory(cursor, product_id, quantity):
    """
    Update the inventory by subtracting the ordered quantity.
    """
    try:
        cursor.execute("UPDATE Inventory SET Quantity = Quantity - %s WHERE ProductID = %s", (quantity, product_id))
        print("Inventory updated successfully.")
    except pymysql.Error as e:
        print(f"Error updating inventory: {e}")

def user_feedback(cursor, user_id):
    """
    Get user feedback for a specific order.
    """
    try:
        # Fetch orders of the specific user
        cursor.execute("SELECT * FROM Orders WHERE UserID = %s AND DeliveryStatus = 'Delivered'", (user_id,))
        orders = cursor.fetchall()

        if not orders:
            print("No delivered orders found for feedback.")
            return

        print("Select an order to provide feedback:")
        for order in orders:
            print(f"Order ID: {order[0]}, Product ID: {order[2]}, Size: {order[3]}, Color: {order[4]}, Status: {order[5]}")

        order_id = int(input("Enter the Order ID for feedback: "))

        feedback = input("Enter your feedback: ")

        # Insert feedback into the Feedback table
        cursor.execute("INSERT INTO UserFeedback (Name, FeedbackText, FeedbackDate) VALUES (%s, %s, CURDATE())", (user_id, feedback))

        print("Feedback submitted successfully!")
    except pymysql.Error as e:
        print(f"Error submitting feedback: {e}")

def view_orders(cursor, user_id):
    """
    View orders for a specific user or all orders for the admin.
    """
    try:
        if user_id is None:  # Admin view: all orders
            cursor.execute("SELECT * FROM Orders")
        else:  # User view: orders of specific user
            cursor.execute("SELECT * FROM Orders WHERE UserID = %s", (user_id,))
        orders = cursor.fetchall()
        for order in orders:
            print(order)
    except pymysql.Error as e:
        print(f"Error fetching orders: {e}")

def view_Payments(cursor, user_id):
    """
    View Payments for a specific user or all orders for the admin.
    """
    try:
        if user_id is None:  # Admin view: all orders
            cursor.execute("SELECT * FROM Payment ORDER BY UserID")
        else:  # User view: orders of specific user
            cursor.execute("SELECT * FROM Payment WHERE UserID = %s", (user_id,))
        Payment = cursor.fetchall()
        for payment in Payment:
            print(payment)
    except pymysql.Error as e:
        print(f"Error fetching orders: {e}")

def add_product(cursor, name, size, color, price):
    """
    Add a new product.
    """
    try:
        cursor.execute("INSERT INTO Product (Name, Size, Color, Price) VALUES (%s, %s, %s, %s)", (name, size, color, price))
        print("Product added successfully!")
    except pymysql.Error as e:
        print(f"Error adding product: {e}")

def remove_product(cursor, product_id):
    """
    Remove a product by product ID.
    """
    try:
        # Fetch associated customization and orders
        cursor.execute("SELECT * FROM Customization WHERE ProductID = %s", (product_id,))
        customizations = cursor.fetchall()
        if customizations:
            print("This product has associated customizations:")
            for customization in customizations:
                print(customization)
            confirmation = input("Do you want to delete the product along with its customizations? (yes/no): ").lower()
            if confirmation == 'yes':
                # Delete associated customizations first
                cursor.execute("DELETE FROM Customization WHERE ProductID = %s", (product_id,))
                # Then delete associated orders
                cursor.execute("DELETE FROM Orders WHERE ProductID = %s", (product_id,))
                # Finally, delete the product
                cursor.execute("DELETE FROM Product WHERE ProductID = %s", (product_id,))
                print("Product and associated customizations removed successfully!")
            else:
                print("Product removal canceled.")
        else:
            # No associated customizations, proceed with product deletion
            cursor.execute("DELETE FROM Orders WHERE ProductID = %s", (product_id,))
            cursor.execute("DELETE FROM Product WHERE ProductID = %s", (product_id,))
            print("Product removed successfully!")
    except pymysql.Error as e:
        print(f"Error removing product: {e}")

def user_operations(cursor, connection, user_id=None):
    """
    Perform user operations.
    """
    while True:
        print("User Menu:")
        print("1. View Products")
        print("2. Search Products")
        print("3. Place Order")
        print("4. View Orders")
        print("5. Provide Feedback")
        print("6. View Payments")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_products(cursor)
        elif choice == '2':
            keyword = input("Enter keyword to search: ")
            search_products(cursor, keyword)
        elif choice == '3':
            if user_id:
                place_order(cursor, user_id)
            else:
                print("Please sign in or sign up to place an order.")
        elif choice == '4':
            view_orders(cursor, user_id)
        elif choice == '5':
            view_Payments(cursor, user_id)
        elif choice == '6':
            if user_id:
                user_feedback(cursor, user_id)
            else:
                print("Please sign in or sign up to provide feedback.")
        elif choice == '7':
            print("Exiting user operations.")
            return
        else:
            print("Invalid choice. Please enter a valid option.")

def sign_in_user(cursor, connection, name, password):
    """
    Sign in an existing user.
    """
    try:
        cursor.execute("SELECT UserID FROM Users WHERE Name = %s AND Password = %s", (name, password))
        user_id = cursor.fetchone()
        if user_id:
            # Reset failed login attempts if the user is not blocked
            query = f"SELECT is_blocked FROM Users WHERE Name = '{name}'"
            cursor.execute(query)
            is_blocked = cursor.fetchone()
            if is_blocked and is_blocked[0] == 1:
                print("Account blocked. Please contact support.")
                return None  # Return None if the user is blocked
            else:
                print("Logged In Successfully.")
                return user_id[0]  # Return the user_id if credentials are correct
        else:
            # Add code for updating failed login attempts
            query = f"SELECT attempts FROM failedLogin WHERE Name = '{name}'"
            cursor.execute(query)
            attempts = cursor.fetchall()
            attempts = attempts[0][0] if attempts else 0
            attempts += 1
            query = f"UPDATE failedLogin SET attempts = {attempts} WHERE Name = '{name}'"
            cursor.execute(query)
            connection.commit()
            return None # Return None if credentials are incorrect
    except pymysql.Error as e:
        print(f"Error signing in: {e}")
        return None

def sign_up_user(cursor, connection, Name, age, gender, email, address, MobileNumber, Password):
    """
    Sign up a new user.
    """
    try:
        # Check if the user already exists
        cursor.execute("SELECT UserID FROM Users WHERE Name = %s", (Name))
        if cursor.fetchone():
            print("User already exists. Please sign in.")
            return None

        # Insert the new user
        cursor.execute("INSERT INTO Users (Name, age, gender, email, address, MobileNumber, Password) VALUES (%s, %s,%s,%s,%s,%s,%s)", (Name, age, gender, email, address, MobileNumber, Password))
        connection.commit()
        return sign_in_user(cursor, connection, Name, age, gender, email, address, MobileNumber, Password)
    except pymysql.Error as e:
        print(f"Error signing up: {e}")
        return None

def admin_operations(cursor):
    """
    Perform admin operations.
    """
    login_attempts = 0
    max_attempts = 3

    while login_attempts < max_attempts:
        admin_name = input("Enter admin name: ")
        admin_password = getpass.getpass("Enter admin password: ")

        if verify_admin_credentials(cursor, admin_name, admin_password):
            while True:
                print("Admin Menu:")
                print("1. Add Product")
                print("2. Remove Product")
                print("3. View Orders")
                print("4. View User Feedback")
                print("5. View All Payments")
                print("6. View Inventory")
                print("7. Exit")

                admin_choice = input("Enter your choice: ")

                if admin_choice == '1':
                    name = input("Enter product name: ")
                    size = input("Enter product size: ")
                    color = input("Enter product color: ")
                    price = float(input("Enter product price: "))
                    add_product(cursor, name, size, color, price)
                elif admin_choice == '2':
                    view_products(cursor)
                    product_id = input("Enter product ID to remove: ")
                    remove_product(cursor, product_id)
                elif admin_choice == '3':
                    view_orders(cursor, user_id=None)  # View all orders regardless of user ID
                elif admin_choice == '4':
                    view_user_feedback(cursor)
                elif admin_choice == '5':
                    view_Payments(cursor,user_id=None)
                elif admin_choice == '6':
                    display_inventory(cursor)
                elif admin_choice == '7':
                    print("Returning to home screen.")
                    return "home"
                else:
                    print("Invalid choice. Please try again.")
        else:
            login_attempts += 1
            print("Invalid admin credentials. Please try again.")
            if login_attempts == max_attempts:
                print("Maximum login attempts reached. Exiting admin operations.")
                break

def view_user_feedback(cursor):
    """
    View user feedback.
    """
    try:
        cursor.execute("SELECT * FROM UserFeedback")
        feedbacks = cursor.fetchall()
        if feedbacks:
            print("User Feedbacks:")
            for feedback in feedbacks:
                print(f"User ID: {feedback[1]}, Feedback: {feedback[2]}, Feedback Date: {feedback[3]}")
        else:
            print("No user feedbacks found.")
    except pymysql.Error as e:
        print(f"Error fetching user feedbacks: {e}")

def verify_admin_credentials(cursor, admin_name, admin_password):
    """
    Verify admin credentials.
    """
    try:
        cursor.execute("SELECT * FROM Administrator WHERE Username = %s AND Password = %s", (admin_name, admin_password))
        admin = cursor.fetchone()
        if admin:
            return True
        else:
            return False
    except pymysql.Error as e:
        print(f"Error verifying admin credentials: {e}")
        return False

def verify_user_credentials(cursor, connection, name, password):
    """
    Verify user credentials and fetch user_id if the credentials are correct.
    """
    try:
        cursor.execute("SELECT UserID FROM Users WHERE Name = %s AND Password = %s", (name, password))
        user_id = cursor.fetchone()
        if user_id:
            # Reset failed login attempts if the user is not blocked
            query11 = f"SELECT is_blocked FROM users WHERE Name = '{name}'"
            cursor.execute(query11)
            is_blocked = cursor.fetchone()
            if is_blocked and is_blocked[0] == 1:
                return "Blocked"  # Return None if the user is blocked
            else:
                query100 = f"UPDATE failedLogin SET attempts = 0 WHERE Name = '{name}'"
                cursor.execute(query100)
                connection.commit()
                return user_id[0]  # Return the user_id if credentials are correct
        else:
            # Add code for updating failed login attempts
            query0 = f"SELECT attempts FROM failedLogin WHERE Name = '{name}'"
            cursor.execute(query0)
            attempts = cursor.fetchall()
            attempts = attempts[0][0] if attempts else 0
            attempts += 1
            query10 = f"UPDATE failedLogin SET attempts = {attempts} WHERE Name = '{name}'"
            cursor.execute(query10)
            connection.commit()
            return None # Return None if credentials are incorrect
    except pymysql.Error as e:
        print(f"Error verifying user credentials: {e}")
        return None

def add_payment_details(cursor, user_id, amount, payment_method):
    """
    Add payment details for a specific order.
    """
    try:
        # Insert payment details into the Payment table
        cursor.execute("INSERT INTO Payment (UserID, Amount, PaymentDate, PaymentMethod) VALUES (%s, %s, CURDATE(), %s)", (user_id, amount, payment_method))
        print("Payment details added successfully!")
    except pymysql.Error as e:
        print(f"Error adding payment details: {e}")

def main():
    """
    Run the main application.
    """
    # password = getpass.getpass("Enter database password: ")
    password = 'mysql'
    connection = connect_to_database(password)
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        # Set up database by altering the 'Orders' table
        setup_database(cursor)

        while True:
            print("Welcome to BigStep CustomFit2")
            print("Select your role:")
            print("1. User")
            print("2. Admin")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                while True:
                    print("User Menu:")
                    print("1. Sign In")
                    print("2. Sign Up")
                    print("3. Exit")
                    user_choice = input("Enter your choice: ")
                    if user_choice == '1':
                        user_name = input("Enter your User name: ")
                        user_password = input("Enter your password: ")
                        user_id = sign_in_user(cursor, connection, user_name, user_password)
                        if user_id:
                            user_operations(cursor, connection, user_id)
                            break
                        else:
                            print("Sign in failed.")
                    elif user_choice == '2':
                        user_name = input("Enter your name: ")
                        user_password = getpass.getpass("Enter your password: ")
                        MobileNumber = input("Enter your Password: ")
                        age = int(input("Enter your age: "))
                        gender = input("Enter your gender: ")
                        email = input("Enter your email address: ")
                        address = input("Enter your address: ")
                        user_id = sign_up_user(cursor, connection, user_name, age, gender, email, address, MobileNumber, user_password)
                        if user_id:
                            user_operations(cursor, connection, user_id)
                            break
                        else:
                            print("Sign up failed.")
                    elif user_choice == '3':
                        break
                    else:
                        print("Invalid choice. Please enter a valid option.")
            elif choice == '2':
                admin_operations(cursor)
            elif choice == '3':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
