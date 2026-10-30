-- ====================================================================
-- Mumbai Commute Analytics — MySQL Database Schema & Analysis Queries
-- File: database/database.sql
-- Beginner-friendly B.Sc Data Science College Project
-- ====================================================================

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS mumbai_commute_db;
USE mumbai_commute_db;

-- 2. Create commute_data Table
DROP TABLE IF EXISTS commute_data;

CREATE TABLE commute_data (
    Commute_ID VARCHAR(20) PRIMARY KEY,
    Commute_Date DATE NOT NULL,
    Starting_Area VARCHAR(50) NOT NULL,
    Destination VARCHAR(50) NOT NULL,
    Transport_Mode VARCHAR(20) NOT NULL,
    Distance_km DECIMAL(5, 2) NOT NULL,
    Travel_Time_min INT NOT NULL,
    Waiting_Time_min INT NOT NULL,
    Cost_INR INT NOT NULL,
    Peak_Hour VARCHAR(5) NOT NULL,
    Crowd_Level VARCHAR(20) NOT NULL,
    Delay_min INT NOT NULL,
    Weather VARCHAR(20) NOT NULL,
    Comfort_Rating INT NOT NULL,
    User_Rating DECIMAL(3, 1) NOT NULL
);

-- Note for Students on Loading CSV into MySQL:
-- You can load data via MySQL Workbench (Right-click Table -> Table Data Import Wizard)
-- Or use the SQL command below (ensure secure-file-priv allows local infile):
/*
LOAD DATA LOCAL INFILE 'C:/path/to/data/commute_data_cleaned.csv'
INTO TABLE commute_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Commute_ID, Commute_Date, Starting_Area, Destination, Transport_Mode, Distance_km, Travel_Time_min, Waiting_Time_min, Cost_INR, Peak_Hour, Crowd_Level, Delay_min, Weather, Comfort_Rating, User_Rating);
*/

-- ====================================================================
-- 3. Sample Benchmark Queries for Viva & Project Defense
-- ====================================================================

-- Query 1: Average cost by transport mode
-- Demonstrates which mode is cheapest on average
SELECT 
    Transport_Mode,
    COUNT(*) AS Total_Trips,
    ROUND(AVG(Cost_INR), 2) AS Avg_Cost_INR,
    MIN(Cost_INR) AS Min_Cost,
    MAX(Cost_INR) AS Max_Cost
FROM commute_data
GROUP BY Transport_Mode
ORDER BY Avg_Cost_INR ASC;

-- Query 2: Average travel time and distance by transport mode
-- Demonstrates which mode is fastest and covers what distance
SELECT 
    Transport_Mode,
    ROUND(AVG(Distance_km), 2) AS Avg_Distance_km,
    ROUND(AVG(Travel_Time_min), 2) AS Avg_Travel_Time_min,
    ROUND(AVG(Travel_Time_min / Distance_km), 2) AS Minutes_Per_Km
FROM commute_data
GROUP BY Transport_Mode
ORDER BY Avg_Travel_Time_min ASC;

-- Query 3: Most-used transport mode in the dataset
SELECT 
    Transport_Mode,
    COUNT(*) AS Trip_Count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM commute_data), 2) AS Percentage_Share
FROM commute_data
GROUP BY Transport_Mode
ORDER BY Trip_Count DESC;

-- Query 4: Transport mode with highest average delay
SELECT 
    Transport_Mode,
    ROUND(AVG(Delay_min), 2) AS Avg_Delay_min,
    MAX(Delay_min) AS Max_Delay_min
FROM commute_data
GROUP BY Transport_Mode
ORDER BY Avg_Delay_min DESC;

-- Query 5: Peak-hour vs Non-Peak hour average travel time
SELECT 
    Transport_Mode,
    Peak_Hour,
    ROUND(AVG(Travel_Time_min), 2) AS Avg_Travel_Time,
    ROUND(AVG(Cost_INR), 2) AS Avg_Cost
FROM commute_data
GROUP BY Transport_Mode, Peak_Hour
ORDER BY Transport_Mode, Peak_Hour DESC;

-- Query 6: Top 5 Origin areas with highest average commute time
SELECT 
    Starting_Area,
    COUNT(*) AS Total_Commutes,
    ROUND(AVG(Travel_Time_min), 2) AS Avg_Travel_Time,
    ROUND(AVG(Cost_INR), 2) AS Avg_Cost
FROM commute_data
GROUP BY Starting_Area
ORDER BY Avg_Travel_Time DESC
LIMIT 5;

-- Query 7: User Comfort and Satisfaction score ranking
SELECT 
    Transport_Mode,
    ROUND(AVG(Comfort_Rating), 2) AS Avg_Comfort_Rating_1to5,
    ROUND(AVG(User_Rating), 2) AS Avg_User_Rating_1to5
FROM commute_data
GROUP BY Transport_Mode
ORDER BY Avg_User_Rating_1to5 DESC;

