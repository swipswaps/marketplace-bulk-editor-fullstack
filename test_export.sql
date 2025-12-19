-- Marketplace Listings Export
-- Generated: 2025-12-19T17:00:45.744103
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
    'f4a85aa5-fdc2-474b-bff0-3b4dcd60edd7',
    'Solar Panel 300W High Efficiency',
    150.00,
    'New',
    'Brand new 300W solar panel with high efficiency rating',
    'Electronics',
    'Yes'
);

