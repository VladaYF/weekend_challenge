--logs
CREATE TABLE logs (
    day_number INTEGER,
    table_name VARCHAR(50),
    rows_count INTEGER,
    load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- raw layer

CREATE TABLE products (
    product_id VARCHAR(50),
    name VARCHAR(100),
    category VARCHAR(50),
    base_price DECIMAL(10,2),
    load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id VARCHAR(50),
    order_date DATE,
    customer_id VARCHAR(50), 
    load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INTEGER, 
    price  DECIMAL(10,2),
    load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customers (
    customer_id VARCHAR(50),
    name VARCHAR(100),
    city VARCHAR(100),
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Data Vault layer
-- Hub
CREATE TABLE customers_hub (
    customer_id VARCHAR(50) PRIMARY KEY,
    load_date TIMESTAMP NOT NULL
);

CREATE TABLE products_hub (
    product_id VARCHAR(50) PRIMARY KEY,
    load_date TIMESTAMP NOT NULL
);

CREATE TABLE orders_hub (
    order_id VARCHAR(50) PRIMARY KEY,
    load_date TIMESTAMP NOT NULL
);

-- Link
CREATE TABLE order_customers_link (
    nk_order_customer VARCHAR(100) PRIMARY KEY,
    order_id VARCHAR(50) REFERENCES orders_hub(order_id),
    customer_id VARCHAR(50) REFERENCES customers_hub(customer_id),
    load_date TIMESTAMP NOT NULL 
);

CREATE TABLE order_products_link (
    nk_order_products VARCHAR(100) PRIMARY KEY,
    order_id VARCHAR(50) REFERENCES orders_hub(order_id),
    product_id VARCHAR(50) REFERENCES products_hub(product_id),
    load_date TIMESTAMP NOT NULL
);

-- Satellite
CREATE TABLE order_sat (
    nk_order_id VARCHAR(50) REFERENCES orders_hub(order_id),
    order_date DATE,
    load_date TIMESTAMP,
    end_date TIMESTAMP,
    hash_diff VARCHAR(100) NOT NULL
);

CREATE TABLE customers_details_sat (
    customer_id VARCHAR(50) REFERENCES customers_hub(customer_id),
    name VARCHAR(100),
    city VARCHAR(100),
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,
    hash_diff VARCHAR(100) NOT NULL
);

CREATE TABLE products_details_sat (
    product_id VARCHAR(50) REFERENCES products_hub(product_id),
    name VARCHAR(100) ,
    category VARCHAR(50),
    quantity INTEGER, 
    base_price DECIMAL(10,2),
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,
    hash_diff VARCHAR(100) NOT NULL
);