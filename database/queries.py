# SQL helpers
CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sku TEXT UNIQUE,
    price REAL NOT NULL DEFAULT 0.0,
    stock INTEGER NOT NULL DEFAULT 0,
    description TEXT
);
"""

CREATE_CART_TABLE = """
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(id)
);
"""

CREATE_REVIEWS_TABLE = """
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    author TEXT NOT NULL,
    rating INTEGER NOT NULL DEFAULT 5,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(id)
);
"""

SEED_PRODUCTS = [
    ("Samsung Galaxy S24 Ultra", "SGS24U-512", 124999.00, 25, "Latest flagship smartphone with 200MP camera and S Pen"),
    ("Apple iPhone 15 Pro Max", "IP15PM-256", 159900.00, 18, "Premium iPhone with titanium design and A17 Pro chip"),
    ("Sony WH-1000XM5 Headphones", "SONY-WH1000XM5", 29990.00, 40, "Industry-leading noise cancelling wireless headphones"),
    ("Dell XPS 15 Laptop", "DELL-XPS15-I7", 189999.00, 12, "15.6 inch laptop with Intel i7, 16GB RAM, 512GB SSD"),
    ("Apple MacBook Air M2", "MBA-M2-256", 114900.00, 15, "Thin and light laptop with M2 chip and 13.6 inch display"),
    ("Samsung 55 4K Smart TV", "SAM-55-4K-QLED", 74999.00, 8, "55 inch QLED 4K Smart TV with HDR support"),
    ("Canon EOS R6 Camera", "CANON-R6-BODY", 219999.00, 6, "Full-frame mirrorless camera with 20MP sensor"),
    ("Apple Watch Series 9", "AW-S9-45MM", 45900.00, 30, "Advanced health and fitness smartwatch"),
    ("Bose SoundLink Speaker", "BOSE-SL-FLEX", 14999.00, 50, "Portable Bluetooth speaker with 12-hour battery"),
    ("Logitech MX Master 3S", "LOG-MXM3S", 8995.00, 60, "Advanced wireless mouse for productivity"),
    ("iPad Pro 12.9 inch", "IPAD-PRO-129-256", 109900.00, 20, "Powerful tablet with M2 chip and Liquid Retina display"),
    ("Sony PlayStation 5", "PS5-DISC-825GB", 54990.00, 10, "Next-gen gaming console with 825GB SSD"),
    ("Nintendo Switch OLED", "NSW-OLED-64GB", 34999.00, 22, "Handheld gaming console with vibrant OLED screen"),
    ("Kindle Paperwhite", "KINDLE-PW-11GEN", 13999.00, 45, "Waterproof e-reader with 6.8 inch display"),
    ("GoPro Hero 12 Black", "GOPRO-H12-BLK", 44999.00, 15, "Action camera with 5.3K video recording"),
]

SEED_REVIEWS = [
    (1, 'Rajesh Kumar', 5, 'Amazing phone! Camera quality is outstanding and battery lasts all day.'),
    (2, 'Priya Sharma', 5, 'Best iPhone yet! The titanium build feels premium and performance is blazing fast.'),
    (3, 'Amit Patel', 4, 'Excellent noise cancellation. Perfect for long flights and commutes.'),
    (4, 'Sneha Reddy', 5, 'Perfect laptop for work and creative tasks. Display is gorgeous!'),
    (5, 'Vikram Singh', 5, 'Lightweight and powerful. M2 chip handles everything smoothly.'),
]

SEED_CUSTOMERS = [
    ('Rajesh Kumar', 'rajesh.kumar@email.com', '+91-9876543210', 'MG Road, Bangalore, Karnataka 560001'),
    ('Priya Sharma', 'priya.sharma@email.com', '+91-9876543211', 'Connaught Place, New Delhi 110001'),
    ('Amit Patel', 'amit.patel@email.com', '+91-9876543212', 'CG Road, Ahmedabad, Gujarat 380009'),
    ('Sneha Reddy', 'sneha.reddy@email.com', '+91-9876543213', 'Banjara Hills, Hyderabad, Telangana 500034'),
    ('Vikram Singh', 'vikram.singh@email.com', '+91-9876543214', 'Park Street, Kolkata, West Bengal 700016'),
    ('Ananya Iyer', 'ananya.iyer@email.com', '+91-9876543215', 'Anna Nagar, Chennai, Tamil Nadu 600040'),
    ('Rohan Mehta', 'rohan.mehta@email.com', '+91-9876543216', 'Koregaon Park, Pune, Maharashtra 411001'),
    ('Kavya Nair', 'kavya.nair@email.com', '+91-9876543217', 'Marine Drive, Kochi, Kerala 682031'),
]

CREATE_WISHLIST_TABLE = """
CREATE TABLE IF NOT EXISTS wishlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(id)
);
"""

CREATE_CUSTOMERS_TABLE = """
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    total_amount REAL NOT NULL DEFAULT 0.0,
    status TEXT DEFAULT 'Pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);
"""

CREATE_ORDER_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);
"""
