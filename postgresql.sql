-- PostgreSQL conversion from MySQL
-- Database: transport_routes
-- Converted from MySQL/MariaDB to PostgreSQL

-- Create database (run this separately as superuser if needed)
-- CREATE DATABASE transport_routes WITH ENCODING 'UTF8';
-- \c transport_routes;

-- Create ENUM types first
CREATE TYPE route_type_enum AS ENUM ('bus', 'trufi', 'micro');

-- --------------------------------------------------------
-- Table structure for table "routes"
-- --------------------------------------------------------

CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT DEFAULT NULL,
    route_type route_type_enum DEFAULT 'bus',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create function to update updated_at automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for automatic updated_at
CREATE TRIGGER update_routes_updated_at 
    BEFORE UPDATE ON routes 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- --------------------------------------------------------
-- Table structure for table "route_coordinates"
-- --------------------------------------------------------

CREATE TABLE route_coordinates (
    id SERIAL PRIMARY KEY,
    route_id INTEGER NOT NULL,
    latitude DECIMAL(10,6) NOT NULL,
    longitude DECIMAL(10,6) NOT NULL,
    sequence_order INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_route_coordinates_route_id 
        FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_route_sequence ON route_coordinates(route_id, sequence_order);

-- --------------------------------------------------------
-- Insert data for table "routes"
-- --------------------------------------------------------

INSERT INTO routes (id, name, description, route_type, is_active, created_at, updated_at) VALUES
(1, 'ruta_2_ida', 'Ruta 1 dirección ida', 'bus', TRUE, '2025-09-02 13:01:59', '2025-09-02 17:48:50'),
(9, 'Trufi C', 'Trufi Americano, Bandera Amarila', 'trufi', TRUE, '2025-09-02 17:46:39', '2025-09-02 17:46:39');

-- --------------------------------------------------------
-- Insert data for table "route_coordinates"
-- --------------------------------------------------------

INSERT INTO route_coordinates (id, route_id, latitude, longitude, sequence_order, created_at) VALUES
(1, 1, -21.993376, -63.683664, 1, '2025-09-02 13:01:59'),
(2, 1, -21.992982, -63.686455, 2, '2025-09-02 13:01:59'),
(3, 1, -21.994234, -63.686592, 3, '2025-09-02 13:01:59'),
(4, 1, -21.994431, -63.685530, 4, '2025-09-02 13:01:59'),
(5, 1, -21.994895, -63.681964, 5, '2025-09-02 13:01:59'),
(6, 1, -21.995092, -63.680098, 6, '2025-09-02 13:01:59'),
(7, 1, -21.990956, -63.679445, 7, '2025-09-02 13:01:59'),
(8, 1, -21.991195, -63.677685, 8, '2025-09-02 13:01:59'),
(9, 1, -21.994099, -63.678148, 9, '2025-09-02 13:01:59'),
(10, 1, -21.994408, -63.676360, 10, '2025-09-02 13:01:59'),
(11, 1, -21.994780, -63.673713, 11, '2025-09-02 13:01:59'),
(12, 1, -21.994975, -63.673623, 12, '2025-09-02 13:01:59'),
(13, 1, -21.995017, -63.673413, 13, '2025-09-02 13:01:59'),
(14, 1, -21.994910, -63.673260, 14, '2025-09-02 13:01:59'),
(15, 1, -21.995159, -63.671205, 15, '2025-09-02 13:01:59'),
(16, 1, -21.995656, -63.671403, 16, '2025-09-02 13:01:59'),
(17, 1, -21.996336, -63.671741, 17, '2025-09-02 13:01:59'),
(18, 1, -21.997513, -63.672328, 18, '2025-09-02 13:01:59'),
(19, 1, -22.000055, -63.673518, 19, '2025-09-02 13:01:59'),
(20, 1, -22.000250, -63.672502, 20, '2025-09-02 13:01:59'),
(21, 1, -22.000567, -63.671716, 21, '2025-09-02 13:01:59'),
(22, 1, -22.002872, -63.672900, 22, '2025-09-02 13:01:59'),
(23, 1, -22.003772, -63.673370, 23, '2025-09-02 13:01:59'),
(24, 1, -22.003493, -63.673962, 24, '2025-09-02 13:01:59'),
(25, 1, -22.003340, -63.673954, 25, '2025-09-02 13:01:59'),
(26, 1, -22.002840, -63.674992, 26, '2025-09-02 13:01:59'),
(27, 1, -22.002367, -63.676034, 27, '2025-09-02 13:01:59'),
(28, 1, -22.002078, -63.676767, 28, '2025-09-02 13:01:59'),
(29, 1, -22.001981, -63.677162, 29, '2025-09-02 13:01:59'),
(30, 1, -22.003453, -63.677929, 30, '2025-09-02 13:01:59'),
(31, 1, -22.008543, -63.680440, 31, '2025-09-02 13:01:59'),
(32, 1, -22.009437, -63.678410, 32, '2025-09-02 13:01:59'),
(33, 1, -22.010232, -63.676602, 33, '2025-09-02 13:01:59'),
(34, 1, -22.013105, -63.678057, 34, '2025-09-02 13:01:59'),
(35, 1, -22.016432, -63.679729, 35, '2025-09-02 13:01:59'),
(36, 1, -22.016403, -63.683118, 36, '2025-09-02 13:01:59'),
(37, 1, -22.018456, -63.684270, 37, '2025-09-02 13:01:59'),
(38, 1, -22.018371, -63.684528, 38, '2025-09-02 13:01:59'),
(39, 1, -22.022118, -63.686419, 39, '2025-09-02 13:01:59'),
(40, 1, -22.022960, -63.684575, 40, '2025-09-02 13:01:59'),
(41, 1, -22.022864, -63.684001, 41, '2025-09-02 13:01:59'),
(42, 1, -22.023074, -63.683382, 42, '2025-09-02 13:01:59'),
(43, 1, -22.023497, -63.683168, 43, '2025-09-02 13:01:59'),
(44, 1, -22.023583, -63.682924, 44, '2025-09-02 13:01:59'),
(45, 1, -22.023810, -63.681996, 45, '2025-09-02 13:01:59'),
(46, 1, -22.024072, -63.680893, 46, '2025-09-02 13:01:59'),
(47, 1, -22.024379, -63.679712, 47, '2025-09-02 13:01:59'),
(48, 9, -21.994837, -63.673129, 1, '2025-09-02 17:46:39'),
(49, 9, -21.995473, -63.669029, 2, '2025-09-02 17:46:39'),
(50, 9, -22.001104, -63.671862, 3, '2025-09-02 17:46:39'),
(51, 9, -22.002397, -63.669072, 4, '2025-09-02 17:46:39'),
(52, 9, -22.007115, -63.670951, 5, '2025-09-02 17:46:39'),
(53, 9, -22.004927, -63.675909, 6, '2025-09-02 17:46:39'),
(54, 9, -22.005802, -63.676339, 7, '2025-09-02 17:46:39'),
(55, 9, -22.006479, -63.674825, 8, '2025-09-02 17:46:39'),
(56, 9, -22.010318, -63.676618, 9, '2025-09-02 17:46:39'),
(57, 9, -22.011094, -63.674686, 10, '2025-09-02 17:46:39'),
(58, 9, -22.013690, -63.675888, 11, '2025-09-02 17:46:39'),
(59, 9, -22.011750, -63.681962, 12, '2025-09-02 17:46:39'),
(60, 9, -22.001207, -63.676693, 13, '2025-09-02 17:46:39'),
(61, 9, -22.002609, -63.673506, 14, '2025-09-02 17:46:39'),
(62, 9, -21.998488, -63.671656, 15, '2025-09-02 17:46:39'),
(63, 9, -21.997665, -63.673947, 16, '2025-09-02 17:46:39'),
(64, 9, -21.996509, -63.673329, 17, '2025-09-02 17:46:39'),
(65, 9, -21.996230, -63.674016, 18, '2025-09-02 17:46:39'),
(66, 9, -21.994862, -63.673152, 19, '2025-09-02 17:46:39');

-- --------------------------------------------------------
-- Update sequences to match the current max IDs
-- --------------------------------------------------------

SELECT setval('routes_id_seq', (SELECT MAX(id) FROM routes));
SELECT setval('route_coordinates_id_seq', (SELECT MAX(id) FROM route_coordinates));

-- --------------------------------------------------------
-- Create view "route_details" (equivalent to MySQL view)
-- --------------------------------------------------------


CREATE OR REPLACE VIEW route_details AS
SELECT 
    r.id,
    r.name,
    r.description,
    r.route_type,
    r.is_active,
    COALESCE(
        JSON_AGG(
            JSON_BUILD_OBJECT(
                'lat', rc.latitude,
                'lng', rc.longitude,
                'order', rc.sequence_order
            ) ORDER BY rc.sequence_order
        ),
        '[]'
    ) AS coordinates
FROM routes r
LEFT JOIN route_coordinates rc ON r.id = rc.route_id
WHERE r.is_active = TRUE
GROUP BY r.id, r.name, r.description, r.route_type, r.is_active;



-- --------------------------------------------------------
-- Optional: Create some useful indexes for better performance
-- --------------------------------------------------------

CREATE INDEX idx_routes_active ON routes(is_active);
CREATE INDEX idx_routes_type ON routes(route_type);
CREATE INDEX idx_coordinates_route_id ON route_coordinates(route_id);