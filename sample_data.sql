-- PostGIS Sample Data Setup Script
-- Run this after enabling PostGIS extensions

-- ============================================
-- 1. CITIES TABLE (Point geometries)
-- ============================================
DROP TABLE IF EXISTS cities CASCADE;

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    population INTEGER,
    elevation_m FLOAT,
    founded_year INTEGER,
    timezone VARCHAR(50),
    geom GEOMETRY(POINT, 4326)
);

INSERT INTO cities (name, country, population, elevation_m, founded_year, timezone, geom) VALUES
('New York', 'USA', 8336817, 10, 1624, 'America/New_York', ST_GeomFromText('POINT(-74.0059 40.7128)', 4326)),
('London', 'UK', 8982000, 35, 43, 'Europe/London', ST_GeomFromText('POINT(-0.1276 51.5074)', 4326)),
('Tokyo', 'Japan', 13929286, 40, 1457, 'Asia/Tokyo', ST_GeomFromText('POINT(139.6917 35.6895)', 4326)),
('Paris', 'France', 2165423, 35, 259, 'Europe/Paris', ST_GeomFromText('POINT(2.3522 48.8566)', 4326)),
('Sydney', 'Australia', 5312163, 58, 1788, 'Australia/Sydney', ST_GeomFromText('POINT(151.2093 -33.8688)', 4326)),
('Mumbai', 'India', 12442373, 14, 1507, 'Asia/Kolkata', ST_GeomFromText('POINT(72.8777 19.0760)', 4326)),
('São Paulo', 'Brazil', 12325232, 760, 1554, 'America/Sao_Paulo', ST_GeomFromText('POINT(-46.6333 -23.5505)', 4326)),
('Cairo', 'Egypt', 9120350, 74, -3100, 'Africa/Cairo', ST_GeomFromText('POINT(31.2357 30.0444)', 4326)),
('Lagos', 'Nigeria', 14368332, 41, 1472, 'Africa/Lagos', ST_GeomFromText('POINT(3.3792 6.5244)', 4326)),
('Mexico City', 'Mexico', 9209944, 2240, 1325, 'America/Mexico_City', ST_GeomFromText('POINT(-99.1332 19.4326)', 4326)),
('Seoul', 'South Korea', 9720846, 38, 1394, 'Asia/Seoul', ST_GeomFromText('POINT(126.9780 37.5665)', 4326)),
('Los Angeles', 'USA', 3971883, 87, 1781, 'America/Los_Angeles', ST_GeomFromText('POINT(-118.2437 34.0522)', 4326));

-- ============================================
-- 2. COUNTRIES TABLE (Polygon geometries)
-- ============================================
DROP TABLE IF EXISTS countries CASCADE;

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    iso_code VARCHAR(3),
    area_km2 FLOAT,
    population BIGINT,
    gdp_usd_billions FLOAT,
    capital VARCHAR(100),
    geom GEOMETRY(POLYGON, 4326)
);

INSERT INTO countries (name, iso_code, area_km2, population, gdp_usd_billions, capital, geom) VALUES
('France', 'FRA', 643801, 67390000, 2937.5, 'Paris', ST_GeomFromText('POLYGON((2 51, 8 51, 8 42, 2 42, 2 51))', 4326)),
('Spain', 'ESP', 505992, 47350000, 1397.9, 'Madrid', ST_GeomFromText('POLYGON((-9 44, 3 44, 3 36, -9 36, -9 44))', 4326)),
('Portugal', 'PRT', 92090, 10290000, 237.7, 'Lisbon', ST_GeomFromText('POLYGON((-9 42, -6 42, -6 37, -9 37, -9 42))', 4326)),
('Germany', 'DEU', 357114, 83240000, 4223.1, 'Berlin', ST_GeomFromText('POLYGON((6 55, 15 55, 15 47, 6 47, 6 55))', 4326)),
('Italy', 'ITA', 301340, 59550000, 2107.7, 'Rome', ST_GeomFromText('POLYGON((7 47, 18 47, 18 36, 7 36, 7 47))', 4326));

-- ============================================
-- 3. ROADS TABLE (LineString geometries)
-- ============================================
DROP TABLE IF EXISTS roads CASCADE;

CREATE TABLE roads (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    road_type VARCHAR(50),
    length_km FLOAT,
    surface VARCHAR(50),
    max_speed_kmh INTEGER,
    construction_year INTEGER,
    geom GEOMETRY(LINESTRING, 4326)
);

INSERT INTO roads (name, road_type, length_km, surface, max_speed_kmh, construction_year, geom) VALUES
('Highway 101', 'highway', 150.5, 'asphalt', 120, 1962, ST_GeomFromText('LINESTRING(-122.4194 37.7749, -122.0 38.0, -121.5 38.5, -121.0 39.0)', 4326)),
('Broadway NYC', 'arterial', 25.3, 'asphalt', 50, 1899, ST_GeomFromText('LINESTRING(-74.0059 40.7128, -74.0000 40.7200, -73.9950 40.7300)', 4326)),
('Ocean Drive Miami', 'coastal', 12.8, 'concrete', 60, 1915, ST_GeomFromText('LINESTRING(-80.1300 25.7600, -80.1250 25.7650, -80.1200 25.7700)', 4326)),
('Rocky Mountain Pass', 'mountain', 35.2, 'asphalt', 80, 1976, ST_GeomFromText('LINESTRING(-105.2700 39.7400, -105.2500 39.7600, -105.2300 39.7800, -105.2100 39.8000)', 4326)),
('Pacific Coast Highway', 'scenic', 89.7, 'asphalt', 90, 1934, ST_GeomFromText('LINESTRING(-118.5 34.0, -118.3 34.1, -118.0 34.3, -117.8 34.5)', 4326)),
('Route 66 Segment', 'historic', 45.1, 'asphalt', 80, 1926, ST_GeomFromText('LINESTRING(-104.9847 39.7391, -104.5 39.8, -104.0 39.9)', 4326));

-- ============================================
-- 4. UTILITY INFRASTRUCTURE TABLE (Mixed geometries)
-- ============================================
DROP TABLE IF EXISTS utility_infrastructure CASCADE;

CREATE TABLE utility_infrastructure (
    id SERIAL PRIMARY KEY,
    facility_name VARCHAR(100) NOT NULL,
    facility_type VARCHAR(50),
    capacity FLOAT,
    operational_status VARCHAR(20),
    install_date DATE,
    maintenance_schedule VARCHAR(50),
    operator VARCHAR(100),
    geom GEOMETRY(GEOMETRY, 4326)
);

INSERT INTO utility_infrastructure (facility_name, facility_type, capacity, operational_status, install_date, maintenance_schedule, operator, geom) VALUES
-- Power Plants (Points)
('Golden Gate Power Plant', 'power_plant', 500.0, 'active', '2015-06-15', 'annual', 'Pacific Energy Corp', ST_GeomFromText('POINT(-118.2437 34.0522)', 4326)),
('Bay Area Substation', 'substation', 150.0, 'active', '2018-03-20', 'quarterly', 'Bay Electric Co', ST_GeomFromText('POINT(-122.4194 37.7749)', 4326)),
('Central Water Treatment', 'water_facility', 250.0, 'maintenance', '2012-05-30', 'monthly', 'Metro Water Authority', ST_GeomFromText('POINT(-74.0059 40.7128)', 4326)),
('Solar Farm Alpha', 'solar_farm', 75.5, 'active', '2019-09-12', 'biannual', 'Green Energy Solutions', ST_GeomFromText('POINT(-105.0178 39.7392)', 4326)),

-- Transmission Lines (LineStrings)
('High Voltage Line 1', 'power_line', 220.0, 'active', '2016-09-10', 'annual', 'Pacific Energy Corp', ST_GeomFromText('LINESTRING(-118.2437 34.0522, -118.0000 34.1000, -117.8000 34.1500)', 4326)),
('Gas Pipeline Main', 'gas_pipeline', 300.0, 'active', '2014-11-05', 'monthly', 'NatGas Distribution', ST_GeomFromText('LINESTRING(-122.4194 37.7749, -122.2000 37.8000, -122.0000 37.8500)', 4326)),
('Fiber Optic Backbone', 'telecom_line', 1000.0, 'active', '2020-01-15', 'quarterly', 'TeleConnect Inc', ST_GeomFromText('LINESTRING(-74.0059 40.7128, -73.9000 40.7500, -73.8000 40.8000)', 4326)),

-- Service Areas (Polygons)
('North Service District', 'service_area', 1000.0, 'active', '2010-01-01', 'annual', 'Municipal Services', ST_GeomFromText('POLYGON((-118.3 34.1, -118.1 34.1, -118.1 33.9, -118.3 33.9, -118.3 34.1))', 4326)),
('Downtown Coverage Zone', 'coverage_area', 500.0, 'active', '2017-07-20', 'quarterly', 'Urban Utilities', ST_GeomFromText('POLYGON((-122.5 37.8, -122.3 37.8, -122.3 37.7, -122.5 37.7, -122.5 37.8))', 4326)),
('Industrial Power Grid', 'power_grid', 800.0, 'active', '2013-04-18', 'monthly', 'Industrial Power Co', ST_GeomFromText('POLYGON((-74.1 40.8, -73.9 40.8, -73.9 40.6, -74.1 40.6, -74.1 40.8))', 4326));

-- ============================================
-- 5. WEATHER STATIONS TABLE (Point geometries with time series data)
-- ============================================
DROP TABLE IF EXISTS weather_stations CASCADE;

CREATE TABLE weather_stations (
    id SERIAL PRIMARY KEY,
    station_name VARCHAR(100) NOT NULL,
    station_code VARCHAR(10),
    elevation_m FLOAT,
    install_date DATE,
    last_reading TIMESTAMP,
    temperature_c FLOAT,
    humidity_percent FLOAT,
    pressure_hpa FLOAT,
    wind_speed_kmh FLOAT,
    rainfall_mm FLOAT,
    geom GEOMETRY(POINT, 4326)
);

INSERT INTO weather_stations (station_name, station_code, elevation_m, install_date, last_reading, temperature_c, humidity_percent, pressure_hpa, wind_speed_kmh, rainfall_mm, geom) VALUES
('Golden Gate Weather', 'GGW001', 67, '2018-01-15', '2024-12-20 14:30:00', 18.5, 72, 1013.2, 15.3, 2.4, ST_GeomFromText('POINT(-122.4783 37.8199)', 4326)),
('Central Park Station', 'CPS002', 42, '2015-03-22', '2024-12-20 14:25:00', 12.1, 65, 1018.7, 8.7, 0.0, ST_GeomFromText('POINT(-73.9653 40.7829)', 4326)),
('LAX Airport Weather', 'LAX003', 38, '2019-07-10', '2024-12-20 14:35:00', 22.8, 68, 1015.1, 12.1, 0.0, ST_GeomFromText('POINT(-118.4085 33.9425)', 4326)),
('Miami Beach Monitor', 'MBM004', 3, '2020-02-14', '2024-12-20 14:40:00', 28.3, 85, 1012.8, 22.5, 5.7, ST_GeomFromText('POINT(-80.1330 25.7907)', 4326)),
('Denver Mountain View', 'DMV005', 1609, '2017-09-05', '2024-12-20 14:20:00', 8.2, 45, 1025.3, 18.9, 0.0, ST_GeomFromText('POINT(-104.9903 39.7392)', 4326)),
('Seattle Waterfront', 'SEW006', 17, '2016-11-30', '2024-12-20 14:32:00', 9.7, 78, 1009.4, 25.2, 8.1, ST_GeomFromText('POINT(-122.3301 47.6038)', 4326));

-- ============================================
-- 6. ADMINISTRATIVE BOUNDARIES TABLE (Polygon geometries)
-- ============================================
DROP TABLE IF EXISTS admin_boundaries CASCADE;

CREATE TABLE admin_boundaries (
    id SERIAL PRIMARY KEY,
    boundary_name VARCHAR(100) NOT NULL,
    boundary_type VARCHAR(50),
    admin_level INTEGER,
    population INTEGER,
    area_km2 FLOAT,
    established_date DATE,
    geom GEOMETRY(POLYGON, 4326)
);

INSERT INTO admin_boundaries (boundary_name, boundary_type, admin_level, population, area_km2, established_date, geom) VALUES
('San Francisco County', 'county', 2, 874961, 600.6, '1850-02-18', ST_GeomFromText('POLYGON((-122.5 37.8, -122.3 37.8, -122.3 37.7, -122.5 37.7, -122.5 37.8))', 4326)),
('Manhattan Borough', 'borough', 3, 1628706, 87.5, '1898-01-01', ST_GeomFromText('POLYGON((-74.1 40.8, -73.9 40.8, -73.9 40.7, -74.1 40.7, -74.1 40.8))', 4326)),
('Los Angeles City', 'city', 4, 3971883, 1302.0, '1850-04-04', ST_GeomFromText('POLYGON((-118.7 34.3, -118.1 34.3, -118.1 33.7, -118.7 33.7, -118.7 34.3))', 4326)),
('Miami-Dade County', 'county', 2, 2716940, 6198.0, '1836-02-04', ST_GeomFromText('POLYGON((-80.9 25.9, -80.1 25.9, -80.1 25.2, -80.9 25.2, -80.9 25.9))', 4326)),
('King County WA', 'county', 2, 2269675, 5581.0, '1852-12-22', ST_GeomFromText('POLYGON((-122.8 47.8, -121.1 47.8, -121.1 47.1, -122.8 47.1, -122.8 47.8))', 4326));

-- ============================================
-- CREATE INDEXES FOR BETTER PERFORMANCE
-- ============================================

-- Spatial indexes
CREATE INDEX cities_geom_idx ON cities USING GIST (geom);
CREATE INDEX countries_geom_idx ON countries USING GIST (geom);
CREATE INDEX roads_geom_idx ON roads USING GIST (geom);
CREATE INDEX utility_infrastructure_geom_idx ON utility_infrastructure USING GIST (geom);
CREATE INDEX weather_stations_geom_idx ON weather_stations USING GIST (geom);
CREATE INDEX admin_boundaries_geom_idx ON admin_boundaries USING GIST (geom);

-- Regular indexes
CREATE INDEX cities_country_idx ON cities (country);
CREATE INDEX cities_population_idx ON cities (population);
CREATE INDEX roads_type_idx ON roads (road_type);
CREATE INDEX utility_status_idx ON utility_infrastructure (operational_status);
CREATE INDEX weather_last_reading_idx ON weather_stations (last_reading);

-- ============================================
-- VERIFY DATA AND DISPLAY SUMMARY
-- ============================================

-- Display summary of created tables
SELECT 'SETUP COMPLETE - SUMMARY OF TABLES:' as message;

SELECT 
    'cities' as table_name,
    COUNT(*) as row_count,
    'Point geometries' as geometry_type
FROM cities
UNION ALL
SELECT 
    'countries' as table_name,
    COUNT(*) as row_count,
    'Polygon geometries' as geometry_type
FROM countries
UNION ALL
SELECT 
    'roads' as table_name,
    COUNT(*) as row_count,
    'LineString geometries' as geometry_type
FROM roads
UNION ALL
SELECT 
    'utility_infrastructure' as table_name,
    COUNT(*) as row_count,
    'Mixed geometries' as geometry_type
FROM utility_infrastructure
UNION ALL
SELECT 
    'weather_stations' as table_name,
    COUNT(*) as row_count,
    'Point geometries with sensor data' as geometry_type
FROM weather_stations
UNION ALL
SELECT 
    'admin_boundaries' as table_name,
    COUNT(*) as row_count,
    'Administrative polygons' as geometry_type
FROM admin_boundaries;

-- Verify PostGIS is working
SELECT 'PostGIS Version: ' || PostGIS_Version() as postgis_info;