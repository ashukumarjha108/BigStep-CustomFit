drop database BigStep_CustomFit2;
-- Ensure the database exists or create it
CREATE DATABASE IF NOT EXISTS BigStep_CustomFit2;
-- Use the created database
USE BigStep_CustomFit2;

-- Create tables with appropriate constraints and relationships
CREATE TABLE IF NOT EXISTS Administrator (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    ContactInfo VARCHAR(100) NOT NULL,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(50) NOT NULL,
    SecurityInfo VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Age INT NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Address VARCHAR(255) NOT NULL,
    MobileNumber VARCHAR(15) NOT NULL,
    Password VARCHAR(50) NOT NULL,
    Orders INT NOT NULL DEFAULT 0,
    is_blocked boolean default false
);
ALTER TABLE Users ADD INDEX idx_name (Name);

CREATE TABLE IF NOT EXISTS Vendor (
    VendorID INT PRIMARY KEY AUTO_INCREMENT,
    ContactInfo VARCHAR(100) NOT NULL,
    VendorName VARCHAR(100) NOT NULL,
    SupplierInfo VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS UserFeedback (
    FeedbackID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    FeedbackText TEXT NOT NULL,
    FeedbackDate DATE NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE IF NOT EXISTS Product (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Size VARCHAR(20) NOT NULL,
    Color VARCHAR(20) NOT NULL,
    Price DECIMAL(10,2) NOT NULL
    );

CREATE TABLE IF NOT EXISTS Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    ProductID INT,
    Quantity int not null default 1, 
    OrderDate DATE NOT NULL,
    DeliveryStatus ENUM('Pending', 'Processing', 'Delivered') DEFAULT 'Pending',
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE IF NOT EXISTS Customization (
    CustomizationID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID INT,
    Size VARCHAR(20) NOT NULL,
    Color VARCHAR(20) NOT NULL,
    Design VARCHAR(100),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE IF NOT EXISTS PreviousOrders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    ProductID INT,
    OrderDate DATE NOT NULL,
    DeliveryStatus ENUM('Delivered') DEFAULT 'Delivered',
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE IF NOT EXISTS Payment (
    PaymentID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    Amount DECIMAL(10,2) NOT NULL,
    PaymentDate DATE NOT NULL,
    PaymentMethod VARCHAR(50) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE IF NOT EXISTS FailedLogin (
    name VARCHAR(50),
    attempts INT DEFAULT 0,
    FOREIGN KEY (name) REFERENCES Users(Name)
);

CREATE TABLE Inventory (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(255),
    Quantity INT DEFAULT 0  -- Default quantity set to 0
);

INSERT INTO Administrator (ContactInfo, Username, Password, SecurityInfo) VALUES 
    ('neha2005@gmail.com', 'neha', 'neha@123', 'Admin security info'),
    ('rahul_1990@yahoo.com', 'rahul', 'rahul@789', 'Admin security info'),
    ('priya.sharma@gmail.com', 'priya', 'priya123', 'Admin security info');

INSERT INTO Users (UserID,Name, age, gender, email, address, MobileNumber, Password, orders) VALUES
    (1,'Dheeraj', 42, 'Male', 'dheeraj@example.com', '45 Park Avenue, Dubai, UAE', '+971505050505', 'D123', 3),
    (2,'Ashu', 35, 'Male', 'ashu@example.com', '56 Oxford Street, London, UK', '+442078901234', 'A123', 2),
    (3,'Kunal', 34, 'Male', 'kunal@example.com', '2 Chome-3-1 Nishi-Shinjuku, Tokyo, Japan', '+819012345678', 'K123', 6),
    (4,'Luca', 37, 'Male', 'luca.ferrari@example.com', 'Via Garibaldi, Milan, Italy', '+390112223344', 'L123', 9),
    (5,'Ravi', 32, 'Male', 'ravi.patel@example.com', '12 MG Road, Bangalore, India', '+918765432109', 'R123', 10);

INSERT INTO FailedLogin (name) VALUES
    ('Dheeraj'),
    ('Ashu'),
    ('Kunal'),
    ('Ravi'),
    ('Luca');

INSERT INTO Vendor (ContactInfo, VendorName, SupplierInfo) VALUES
    ('123 Main St, Mumbai, India', 'Walkway Footwear', 'Supplier info 1'),
    ('456 Elm St, Bangalore, India', 'StepUp Shoes', 'Supplier info 2'),
    ('789 Oak St, Delhi, India', 'Sole Comfort', 'Supplier info 3'),
    ('101 Pine St, Hyderabad, India', 'FootFashion Hub', 'Supplier info 4'),
    ('222 Maple St, Kolkata, India', 'Stride Right Shoe Store', 'Supplier info 5'),
    ('333 Cedar St, Chennai, India', 'HappyFeet Footwear', 'Supplier info 6'),
    ('444 Birch St, Pune, India', 'ShoeStyle Emporium', 'Supplier info 7'),
    ('555 Walnut St, Goa, India', 'TrendyToes Shoe Boutique', 'Supplier info 8'),
    ('666 Oak St, Jaipur, India', 'SneakerSphere', 'Supplier info 9'),
    ('777 Elm St, Lucknow, India', 'BootBarn', 'Supplier info 10');

INSERT INTO UserFeedback (UserID, FeedbackText, FeedbackDate) VALUES 
    (1, 'Great service!', '2024-01-15'),
    (2, 'Product quality could be better.', '2024-01-20'),
    (3, 'Very satisfied with the customization options.', '2024-01-25'),
    (4, 'Fast delivery!', '2024-01-10'),
    (5, 'Received wrong product, but customer service resolved it quickly.', '2024-01-18');

INSERT INTO Product (ProductID, Name, Size, Color, Price) VALUES 
    (1, 'CustomFit Shoe', '11', 'Black', 49.99),
    (2, 'Sports Shoe', '12', 'White', 39.99),
    (3, 'Formal Shoe', '13', 'Brown', 59.99),
    (4, 'Casual Shoe', '15', 'Blue', 34.99),
    (5, 'Sandals', '11', 'Red', 24.99),
    (6, 'Boots', '15', 'Black', 69.99),
    (7, 'Slippers', '17', 'Brown', 19.99),
    (8, 'Sneakers', '13', 'White', 44.99),
    (9, 'Loafers', '14', 'Blue', 54.99),
    (10, 'Flip Flops', '12', 'Red', 14.99),
    (60, 'Canvas Shoes', 15, 'Navy', 34.99),
    (61, 'Snow Boots', 16, 'Gray', 99.99),
    (62, 'Espadrilles', 17, 'Beige', 39.99),
    (63, 'Work Boots', 18, 'Brown', 79.99),
    (64, 'Leather Sandals', 11, 'Tan', 44.99),
    (65, 'Golf Shoes', 12, 'White', 69.99),
    (110, 'Ankle Boots', 13, 'Black', 74.99),
    (111, 'Moccasins', 14, 'Brown', 49.99),
    (112, 'Platform Sneakers', 15, 'Pink', 59.99),
    (113, 'Wedge Sandals', 16, 'Black', 54.99),
    (114, 'Slip-resistant Shoes', 17, 'Gray', 64.99),
    (115, 'Rain Boots', 18, 'Yellow', 89.99);

INSERT INTO Orders (UserID, ProductID, OrderDate, DeliveryStatus, Quantity) VALUES 
    (1, 1, '2024-01-28', 'Pending', 1),
    (2, 2, '2024-01-25', 'Delivered', 1),
    (3, 3, '2024-01-20', 'Processing', 1),
    (4, 4, '2024-01-18', 'Delivered', 1),
    (5, 5, '2024-01-15', 'Pending', 1);

INSERT INTO Customization (CustomizationID, ProductID, Size, Color, Design) VALUES 
    (1, 1, '15', 'Black', 'Custom design'),
    (2, 2, '17', 'White', 'Logo printed'),
    (3, 3, '11', 'Brown', 'Engraved initials'),
    (4, 4, '15', 'Blue', 'None'),
    (5, 5, '13', 'Red', 'Custom pattern'),
    (6, 6, '16', 'Black', 'Embossed logo'),
    (7, 7, '12', 'Brown', 'Customized strap'),
    (8, 8, '17', 'White', 'Personalized message'),
    (9, 9, '16', 'Blue', 'Custom artwork'),
    (10, 10, '14', 'Red', 'No customization');

INSERT INTO PreviousOrders (UserID, ProductID, OrderDate, DeliveryStatus) VALUES
    (1, 1, '2023-12-01', 'Delivered'),
    (2, 2, '2023-11-15', 'Delivered'),
    (3, 3, '2023-10-20', 'Delivered'),
    (4, 4, '2023-09-05', 'Delivered'),
    (5, 5, '2023-08-10', 'Delivered');

INSERT INTO Payment (UserID, Amount, PaymentDate, PaymentMethod) VALUES 
    (1, 499.99, '2024-01-28', 'Credit Card'),
    (2, 399.99, '2024-01-25', 'UPI'),
    (3, 599.99, '2024-01-20', 'Net Banking'),
    (4, 349.99, '2024-01-18', 'Debit Card'),
    (5, 249.99, '2024-01-15', 'Cash on Delivery');

INSERT INTO Inventory (ProductID, ProductName, Quantity) VALUES 
    (1, 'CustomFit Shoe', 20),
    (2, 'Sports Shoe', 15),
    (3, 'Formal Shoe', 25),
    (4, 'Casual Shoe', 30),
    (5, 'Sandals', 25),
    (6, 'Boots', 10),
    (7, 'Slippers', 20),
    (8, 'Sneakers', 15),
    (9, 'Loafers', 10),
    (10, 'Flip Flops', 20),
    (60, 'Canvas Shoes', 15),
    (61, 'Snow Boots', 10),
    (62, 'Espadrilles', 20),
    (63, 'Work Boots', 10),
    (64, 'Leather Sandals', 15),
    (65, 'Golf Shoes', 5),
    (110, 'Ankle Boots', 10),
    (111, 'Moccasins', 15),
    (112, 'Platform Sneakers', 10),
    (113, 'Wedge Sandals', 15),
    (114, 'Slip-resistant Shoes', 20),
    (115, 'Rain Boots', 5);

-- Trigger 1 
DELIMITER $$
CREATE TRIGGER update_FailedLogins
AFTER UPDATE ON FailedLogin
FOR EACH ROW
BEGIN
    DECLARE att INT;
    SET att = NEW.attempts;

    IF att >= 3 THEN
        UPDATE Users
        SET is_blocked = true
        WHERE Name = NEW.name;
    END IF;
END$$
DELIMITER ;

-- Trigger 2
DELIMITER //
CREATE TRIGGER refill_inventory
AFTER UPDATE ON Inventory
FOR EACH ROW
BEGIN
    IF NEW.Quantity < 5 THEN
        UPDATE Inventory
        SET Quantity = Quantity + 10
        WHERE ProductID = NEW.ProductID;
    END IF;
END;
//
DELIMITER ;