-- Suppliers
INSERT INTO suppliers (supplier_name, country, lead_time_days, lead_time_std)
VALUES
('Korean Food Trading Co.', 'South Korea', 14, 3),
('Tokyo Import GmbH', 'Japan', 12, 2),
('Thai Spice Export Ltd.', 'Thailand', 18, 4),
('Taiwan Fresh Foods Co.', 'Taiwan', 15, 3),
('Shanghai Supply', 'China', 20, 6);

-- Products
INSERT INTO products (product_name, category, unit_cost, unit_price, shelf_life_days, supplier_id, reorder_qty)
VALUES
('Shin Ramyun Spicy Noodles', 'Noodles', 0.80, 1.59, 365, 1, 200),
('Kimchi 500g', 'Refrigerated', 2.00, 4.9, 30, 1, 80),
('Korean BBQ Sauce', 'Sauces', 1.50, 3.50, 180, 1, 100),

('Sushi Rice 1.5kg', 'Rice', 2.40, 5.29, 365, 2, 150),
('Miso Paste 500g', 'Sauces', 1.50, 3.65, 180, 2, 160),
('Pocky Chocolate', 'Snacks', 0.70, 1.99, 270, 2, 300),

('Thai Jasmine Rice 2kg', 'Rice', 3.0, 6.99, 365, 3, 180),
('Green Curry Paste', 'Sauces', 0.9, 2.49, 180, 3, 150),
('Coconut Milk 400ml', 'Canned', 0.85, 1.89, 365, 3, 200),

('Bubble Milk Tea Powder', 'Beverage', 2.20, 5.49, 365, 4, 150),
('Pineapple Cake Box', 'Snacks', 3.00, 6.99, 120, 4, 80),
('Soy Sauce 600ml', 'Sauces', 1.10, 2.69, 365, 4, 160),

('Chili Oil 250ml', 'Sauces', 0.95, 2.29, 365, 5, 120),
('Hot Pot Soup Base', 'Instant', 1.30, 3.19, 240, 5, 90),
('Frozen Dumplings 1kg', 'Frozen', 2.50, 5.99, 90, 5, 90);
