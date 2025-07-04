CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

INSERT INTO locations (name, latitude, longitude) VALUES
('Marina Beach', 13.0500, 80.2824),
('Chennai Central', 13.0827, 80.2707),
('Guindy National Park', 13.0108, 80.2295);
