-- Create the address table
CREATE TABLE address (
    id SERIAL PRIMARY KEY,  -- Auto-incrementing ID for the address
    street VARCHAR(255),    -- Street address
    city VARCHAR(100),      -- City
    state VARCHAR(100),     -- State/Province
    postal_code VARCHAR(20), -- Postal/ZIP code
    country VARCHAR(100)    -- Country
);

-- Create the users table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,  -- Auto-incrementing ID for the user
    username VARCHAR(255) UNIQUE,  -- Username (unique)
    email VARCHAR(255) UNIQUE,     -- Email (unique)
    first_name VARCHAR(100),    -- User's first name
    last_name VARCHAR(100),     -- User's last name
    phone_number VARCHAR(20),   -- User's phone number
    address_id INT,             -- Foreign key referencing address table
    role VARCHAR(50),           -- Role (e.g., 'admin', 'user')
    status VARCHAR(50),         -- Status (e.g., 'active', 'inactive')
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when user was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when user was last updated
    last_login_at TIMESTAMP,    -- Timestamp when user last logged in
    FOREIGN KEY (address_id) REFERENCES address(id) -- Foreign key constraint to address table
);
