PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS inventory_snapshots;
DROP TABLE IF EXISTS purchase_orders;
DROP TABLE IF EXISTS purchase_order_items;

-- Master Tables

CREATE TABLE suppliers (
  supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_name TEXT NOT NULL,
  country TEXT,
  lead_time_days INTEGER NOT NULL CHECK (lead_time_days >= 0),
  lead_time_std REAL DEFAULT 0 CHECK (lead_time_std >= 0)
);

CREATE TABLE products (
  product_id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_name TEXT NOT NULL,
  category TEXT NOT NULL,
  unit_cost REAL NOT NULL CHECK (unit_cost >= 0),
  unit_price REAL NOT NULL CHECK (unit_price >= 0),
  shelf_life_days INTEGER CHECK (shelf_life_days IS NULL OR shelf_life_days >= 0),
  supplier_id INTEGER NOT NULL,
  reorder_qty INTEGER DEFAULT 0 CHECK (reorder_qty >= 0),
  is_active INTEGER DEFAULT 1 CHECK (is_active IN (0, 1)),
  FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id)
);

-- Transaction Tables

-- Daily sales transactions (per product per day)
CREATE TABLE sales (
  sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
  sale_date TEXT NOT NULL,
  product_id INTEGER NOT NULL,
  qty_sold INTEGER NOT NULL CHECK (qty_sold >= 0),
  FOREIGN KEY (product_id) REFERENCES products (product_id),
  UNIQUE (sale_date, product_id)
);

-- Daily inventory (at the end of the day)
CREATE TABLE inventory_snapshots (
  snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
  snapshot_date TEXT NOT NULL,
  product_id INTEGER NOT NULL,
  stock_on_hand INTEGER NOT NULL CHECK (stock_on_hand >= 0),
  FOREIGN KEY (product_id) REFERENCES products (product_id),
  UNIQUE (snapshot_date, product_id)
);

-- Purchase Orders
CREATE TABLE purchase_orders (
  po_id INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_id INTEGER NOT NULL,
  order_date TEXT NOT NULL,
  expected_arrival TEXT NOT NULL,
  received_date TEXT,
  status TEXT NOT NULL CHECK (status IN ('placed', 'received', 'cancelled')),
  notes TEXT,
  FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id)
);

-- Purchase order items
CREATE TABLE purchase_order_items (
  po_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  po_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  qty_ordered INTEGER NOT NULL CHECK (qty_ordered > 0),
  qty_received INTEGER DEFAULT 0 CHECK (qty_received >= 0),
  unit_cost REAL NOT NULL CHECK (unit_cost >= 0),
  FOREIGN KEY (po_id) REFERENCES purchase_orders (po_id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products (product_id)
);

-- Indexes

CREATE INDEX idx_sales_date ON sales (sale_date);
CREATE INDEX idx_sales_product ON sales (product_id);

CREATE INDEX idx_inventory_date ON inventory_snapshots (snapshot_date);
CREATE INDEX idx_inventory_product ON inventory_snapshots (product_id);

CREATE INDEX idx_po_supplier ON purchase_orders (supplier_id);
CREATE INDEX idx_po_status ON purchase_orders (status);
