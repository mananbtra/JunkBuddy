-- Create Database
CREATE DATABASE IF NOT EXISTS WasteManagement;
USE WasteManagement;

-- Plastics Table
CREATE TABLE IF NOT EXISTS Plastics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    img_label VARCHAR(255) NOT NULL UNIQUE,
    dispose TEXT NOT NULL,
    recycle TEXT NOT NULL,
    invalid BOOLEAN DEFAULT FALSE
);

-- Electronics Table
CREATE TABLE IF NOT EXISTS Electronics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    img_label VARCHAR(255) NOT NULL UNIQUE,
    dispose TEXT NOT NULL,
    recycle TEXT NOT NULL,
    invalid BOOLEAN DEFAULT FALSE
);

-- E_Waste Table
CREATE TABLE IF NOT EXISTS E_Waste (
    id INT AUTO_INCREMENT PRIMARY KEY,
    img_label VARCHAR(255) NOT NULL UNIQUE,
    dispose TEXT NOT NULL,
    recycle TEXT NOT NULL,
    invalid BOOLEAN DEFAULT FALSE
);

-- Textiles Table
CREATE TABLE IF NOT EXISTS Textiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    img_label VARCHAR(255) NOT NULL UNIQUE,
    dispose TEXT NOT NULL,
    recycle TEXT NOT NULL,
    invalid BOOLEAN DEFAULT FALSE
);

-- Other_Waste Table
CREATE TABLE IF NOT EXISTS Other_Waste (
    id INT AUTO_INCREMENT PRIMARY KEY,
    img_label VARCHAR(255) NOT NULL UNIQUE,
    dispose TEXT NOT NULL,
    recycle TEXT NOT NULL,
    invalid BOOLEAN DEFAULT FALSE
);

-- Batteries Table
CREATE TABLE IF NOT EXISTS Batteries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    img_label VARCHAR(255) NOT NULL UNIQUE,
    dispose TEXT NOT NULL,
    recycle TEXT NOT NULL,
    invalid BOOLEAN DEFAULT FALSE
);

-- Insert Sample Data for Plastics
INSERT INTO Plastics (img_label, dispose, recycle, invalid) VALUES
('Plastic Bottles', 
'1. Properly throw away in recycling bin, 2. Use municipal recycling centers, 3. Participate in bottle drives, 4. Donate to local recycling programs, 5. Crush and store for bulk collection', 
'1. Clean and reuse as planters, 2. Recycle through local facilities, 3. Use as bird feeders, 4. Create self-watering planters, 5. Make wind chimes', 
FALSE),
('Plastic Bags', 
'1. Properly throw away in black bin, 2. Use designated bag collection centers, 3. Participate in bag recycling programs, 4. Donate to local reuse initiatives, 5. Compost if biodegradable', 
'1. Reuse as drop cloths, 2. Upcycle into reusable bags, 3. Use in craft projects, 4. Create rope from strips, 5. Make a quilt from plastic bag strips', 
FALSE);

-- Insert Sample Data for Electronics
INSERT INTO Electronics (img_label, dispose, recycle, invalid) VALUES
('Smartphones', 
'1. E-waste centers, 2. Manufacturer take-back, 3. Municipal collection, 4. Certified recyclers, 5. Retail drop-off', 
'1. Component recovery, 2. Metal extraction, 3. Donate for refurbishment, 4. Art projects, 5. DIY repairs', 
FALSE),
('Laptops', 
'1. Authorized e-waste centers, 2. Manufacturer recycling, 3. Corporate e-waste drives, 4. Certified dismantlers, 5. School donation programs', 
'1. Precious metal recovery, 2. Plastic recycling, 3. Battery reuse, 4. Educational kits, 5. Server farm donations', 
FALSE);

-- Insert Sample Data for E_Waste
INSERT INTO E_Waste (img_label, dispose, recycle, invalid) VALUES
('Circuit Boards', 
'1. Specialized e-waste centers, 2. Manufacturer take-back, 3. Certified recyclers, 4. University programs, 5. Tech company initiatives', 
'1. Gold recovery, 2. Copper extraction, 3. Component reuse, 4. Art installations, 5. Research materials', 
FALSE),
('Motherboards', 
'1. E-waste collection drives, 2. Manufacturer recycling, 3. Component salvage, 4. Local collection points, 5. Retail drop-off', 
'1. Precious metal recovery, 2. Plastic recycling, 3. Vintage computer restoration, 4. Educational kits, 5. DIY projects', 
FALSE);

-- Insert Sample Data for Textiles
INSERT INTO Textiles (img_label, dispose, recycle, invalid) VALUES
('Cotton Fabrics', 
'1. Clothing banks, 2. Municipal collection, 3. Animal shelter donations, 4. Industrial rags, 5. Community swaps', 
'1. Upcycled clothing, 2. Paper production, 3. Insulation material, 4. Composting, 5. Quilt making', 
FALSE),
('Denim', 
'1. Specialty recyclers, 2. Brand take-back, 3. Building insulation, 4. Furniture stuffing, 5. Art projects', 
'1. Denim insulation, 2. Recycled jeans, 3. Bags and accessories, 4. Home decor, 5. Industrial abrasives', 
FALSE);

-- Insert Sample Data for Other_Waste
INSERT INTO Other_Waste (img_label, dispose, recycle, invalid) VALUES
('Cardboard', 
'1. Municipal recycling, 2. Local collection points, 3. School programs, 4. Composting, 5. Retail drop-off', 
'1. Pulp recycling, 2. DIY crafts, 3. Packaging material, 4. Mulching, 5. Animal bedding', 
FALSE),
('Glass Bottles', 
'1. Bottle banks, 2. Cullet processors, 3. Municipal collection, 4. Art studios, 5. Community centers', 
'1. New glass production, 2. Decorative items, 3. Construction aggregate, 4. Mosaic art, 5. Water filtration', 
FALSE);

-- Insert Sample Data for Batteries
INSERT INTO Batteries (img_label, dispose, recycle, invalid) VALUES
('Batteries', 
'1. Retail drop-off, 2. Hazardous waste centers, 3. Municipal collection, 4. Battery banks, 5. Authorized dealers', 
'1. Metal recovery, 2. Component reuse, 3. Energy storage, 4. Art projects, 5. Emergency kits', 
FALSE);
