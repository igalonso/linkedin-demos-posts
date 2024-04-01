CREATE or REPLACE TABLE autofill_form.products_sold (
    ProductName STRING,
    Description STRING,
    Category STRING,
    Brand STRING,
    Model STRING,
    Year INT64,
    Condition STRING,
    Color STRING,
    ReasonForSelling STRING,
    Price NUMERIC,
    Negotiable STRING,
    Delivery STRING
);

INSERT INTO autofill_form.products_sold (ProductName, Description, Category, Brand, Model, Year, Condition, Color, ReasonForSelling, Price, Negotiable, Delivery)
VALUES 
('iPhone 12', 'Used iPhone 12 in good condition', 'Electronics', 'Apple', 'iPhone 12', 2020, 'Used', 'Black', 'Upgraded to a new model', 700.00, 'Yes', 'No'),
('Samsung TV', 'Brand new 50 inch Samsung TV', 'Electronics', 'Samsung', 'UN50NU6900', 2021, 'New', 'Black', 'Won in a raffle', 400.00, 'No', 'Yes'),
('Leather Sofa', 'Leather sofa in excellent condition', 'Furniture', 'Ashley', 'Bladen', 2019, 'Used', 'Brown', 'Moving to a new place', 300.00, 'Yes', 'No'),
('Nike Shoes', 'New Nike running shoes', 'Clothing', 'Nike', 'Revolution 5', 2022, 'New', 'White', 'Wrong size', 50.00, 'No', 'Yes'),
('Dell Laptop', 'Dell laptop with 8GB RAM and 256GB SSD', 'Electronics', 'Dell', 'Inspiron 15', 2018, 'Used', 'Silver', 'Bought a new laptop', 350.00, 'Yes', 'No'),
('Wooden Dining Table', 'Wooden dining table with 4 chairs', 'Furniture', 'IKEA', 'Lerhamn', 2017, 'Used', 'Light antique stain', 'Moving out', 100.00, 'Yes', 'Yes'),
('Bicycle', 'Mountain bike in good condition', 'Sports', 'Trek', 'Marlin 5', 2020, 'Used', 'Blue', 'Bought a new bike', 200.00, 'Yes', 'No'),
('Levi Jeans', 'Levi\'s 501 original fit jeans', 'Clothing', 'Levi\'s', '501', 2021, 'Used', 'Dark blue', 'Does not fit anymore', 30.00, 'No', 'Yes'),
('Electric Guitar', 'Used electric guitar in good condition', 'Musical Instruments', 'Fender', 'Stratocaster', 2018, 'Used', 'Red', 'No longer playing', 500.00, 'Yes', 'No'),
('Skateboard', 'Street skateboard, lightly used', 'Sports', 'Element', 'Section', 2020, 'Used', 'Black', 'Upgraded to a new skateboard', 60.00, 'Yes', 'Yes'),
('Longboard', 'Longboard for cruising and carving', 'Sports', 'Sector 9', 'Aperture Sidewinder', 2021, 'Used', 'Blue', 'Bought a new longboard', 100.00, 'Yes', 'No'),
('Freestyle Skateboard', 'Freestyle skateboard for tricks', 'Sports', 'Powell Peralta', 'Golden Dragon', 2022, 'Used', 'Red', 'Switched to longboarding', 75.00, 'No', 'Yes'),
('Canon Camera', 'Canon DSLR camera with 18-55mm lens', 'Electronics', 'Canon', 'EOS Rebel T7', 2019, 'Used', 'Black', 'Upgraded to a new camera', 300.00, 'Yes', 'No'),
('Yamaha Keyboard', 'Used Yamaha keyboard in good condition', 'Musical Instruments', 'Yamaha', 'PSR-F51', 2019, 'Used', 'Black', 'Bought a new keyboard', 80.00, 'Yes', 'No'),
('Basketball Hoop', 'Portable basketball hoop', 'Sports', 'Lifetime', '1221 Pro Court', 2020, 'Used', 'Red', 'Moving to a new place', 100.00, 'Yes', 'Yes'),
('Office Chair', 'Ergonomic office chair', 'Furniture', 'Herman Miller', 'Aeron', 2018, 'Used', 'Black', 'Got a new chair', 400.00, 'Yes', 'No'),
('PlayStation 4', 'PlayStation 4 with two controllers', 'Electronics', 'Sony', 'PlayStation 4', 2017, 'Used', 'Black', 'Upgraded to PlayStation 5', 200.00, 'No', 'Yes'),
('Mountain Bike', 'Mountain bike with 21 speeds', 'Sports', 'Giant', 'Talon', 2021, 'Used', 'Blue', 'Bought a new bike', 500.00, 'Yes', 'No');