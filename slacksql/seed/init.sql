--Create mock data using the schema below.

CREATE TABLE customers (
    CUSTOMERID VARCHAR(1000) PRIMARY KEY,
    CUSTOMER_NAME VARCHAR(1000),
    CUSTOMEREMAIL VARCHAR(1000),
    CITY VARCHAR(50),
    CUSTOMERCRETEDAT DATE
);

CREATE TABLE products (
    ID VARCHAR(1000) PRIMARY KEY,
    PRODUCT_NAME VARCHAR(1000),
    CATEGORY VARCHAR(500)
);

CREATE TABLE orders (
    ORDERID VARCHAR(1000) PRIMARY KEY,
    CUSTOMERID VARCHAR(1000),
    ORDERDATE DATE,
    STATUS VARCHAR(20),
    REVENUE DECIMAL(10,2)
);

CREATE TABLE order_items (
    ID VARCHAR(1000) PRIMARY KEY,
    ORDERID VARCHAR(1000),
    PRODUCTID VARCHAR(1000),
    QUANTITY INTEGER,
    REVENUE DECIMAL(10,2)
);

COPY customers FROM '/docker-entrypoint-initdb.d/customers.csv' WITH CSV HEADER;
COPY products FROM '/docker-entrypoint-initdb.d/products.csv' WITH CSV HEADER;
COPY orders FROM '/docker-entrypoint-initdb.d/orders.csv' WITH CSV HEADER;
COPY order_items FROM '/docker-entrypoint-initdb.d/order_items.csv' WITH CSV HEADER;