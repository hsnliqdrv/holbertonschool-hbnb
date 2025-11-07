-- Create the main table
CREATE TABLE entities (
    id CHAR(36) PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    is_admin INTEGER DEFAULT 0  -- 0 = FALSE, 1 = TRUE
);

CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    title TEXT,
    description TEXT,
    price REAL,
    latitude REAL,
    longitude REAL,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    text TEXT,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    UNIQUE(user_id, place_id)
);

CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    name TEXT UNIQUE
);

CREATE TABLE place_amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$10$mg5jzZslU7q1PyPTm4TLe.UHmvV/7tbSVo8c5hD85sUSQz7Xn2Wze',
    1
);

INSERT INTO amenities (id, name) VALUES ('97f2db25-d1f4-47ee-97ac-cd426e3fb053', 'WiFi');
INSERT INTO amenities (id, name) VALUES ('266c181e-1b25-44d4-b1cf-da4bc23fea11', 'Swimming Pool');
INSERT INTO amenities (id, name) VALUES ('d0cc047d-f7b0-46fc-b3a2-af5c5d4ccc3d', 'Air Conditioning');

