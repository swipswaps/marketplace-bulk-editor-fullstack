-- Marketplace Listings Export
-- Generated: 2025-12-19T19:14:47.027213
-- Total listings: 1

CREATE TABLE IF NOT EXISTS marketplace_listings (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    condition VARCHAR(50) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    offer_shipping VARCHAR(3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO marketplace_listings (id, title, price, condition, description, category, offer_shipping) VALUES (
    '5a8c3482-d746-42e4-905c-1c125518b6c3',
    'Solar Panel 300W High Efficiency',
    150.00,
    'New',
    'Brand new 300W solar panel',
    'Electronics',
    'No'
);

