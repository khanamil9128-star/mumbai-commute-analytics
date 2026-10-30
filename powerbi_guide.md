# Power BI Dashboard Setup Guide: Mumbai Commute Analytics

This guide explains step-by-step how to build the **Mumbai Commute Analytics Power BI Dashboard** using `data/commute_data_cleaned.csv`.

---

## 1. Load Data into Power BI Desktop

1. Open **Power BI Desktop**.
2. Click **Get Data** → Select **Text/CSV** → Click **Connect**.
3. Browse and select: `data/commute_data_cleaned.csv`.
4. In the preview window, verify the columns:
   - `Commute_ID` (Text)
   - `Date` (Date)
   - `Starting_Area` (Text)
   - `Destination` (Text)
   - `Transport_Mode` (Text)
   - `Distance_km` (Decimal Number)
   - `Travel_Time_min` (Whole Number)
   - `Waiting_Time_min` (Whole Number)
   - `Cost_INR` (Whole Number)
   - `Peak_Hour` (Text)
   - `Crowd_Level` (Text)
   - `Delay_min` (Whole Number)
   - `Weather` (Text)
   - `Comfort_Rating` (Whole Number)
   - `User_Rating` (Decimal Number)
5. Click **Load**.

---

## 2. Key DAX Measures to Create

Click **New Measure** on the Home ribbon and paste these formulas:

### Measure 1: Total Commutes
```dax
Total Commutes = COUNTROWS('commute_data_cleaned')
```

### Measure 2: Average Travel Time
```dax
Avg Travel Time (min) = ROUND(AVERAGE('commute_data_cleaned'[Travel_Time_min]), 1)
```

### Measure 3: Average Cost
```dax
Avg Commute Cost (INR) = ROUND(AVERAGE('commute_data_cleaned'[Cost_INR]), 0)
```

### Measure 4: Average Distance
```dax
Avg Distance (km) = ROUND(AVERAGE('commute_data_cleaned'[Distance_km]), 1)
```

### Measure 5: Cost per Kilometer
```dax
Cost per KM = DIVIDE([Avg Commute Cost (INR)], [Avg Distance (km)], 0)
```

---

## 3. Visual Layout Configuration

### Top Row: 4 KPI Cards
- **Card 1:** Field = `[Total Commutes]` (Title: Total Trips)
- **Card 2:** Field = `[Avg Travel Time (min)]` (Title: Avg Travel Time)
- **Card 3:** Field = `[Avg Commute Cost (INR)]` (Title: Avg Commute Cost)
- **Card 4:** Field = `[Avg Distance (km)]` (Title: Avg Distance)

---

### Row 2: Visual Comparison Charts
1. **Donut Chart (Mode Share)**:
   - **Legend:** `Transport_Mode`
   - **Values:** `[Total Commutes]`
   - *Colors:* Metro = Green, Local = Blue, Auto = Gold.

2. **Clustered Column Chart (Average Travel Time by Mode)**:
   - **X-Axis:** `Transport_Mode`
   - **Y-Axis:** `[Avg Travel Time (min)]`
   - **Data Labels:** On

3. **Clustered Bar Chart (Average Cost by Mode)**:
   - **Y-Axis:** `Transport_Mode`
   - **X-Axis:** `[Avg Commute Cost (INR)]`
   - **Data Labels:** On

---

### Row 3: In-Depth Operational Analysis
1. **Clustered Column Chart (Peak vs Non-Peak Travel Time)**:
   - **X-Axis:** `Transport_Mode`
   - **Y-Axis:** `Travel_Time_min` (Average)
   - **Legend:** `Peak_Hour` (Yes / No)

2. **100% Stacked Bar Chart (Crowd Level by Transport Mode)**:
   - **Y-Axis:** `Transport_Mode`
   - **X-Axis:** `Commute_ID` (Count)
   - **Legend:** `Crowd_Level` (Low, Medium, High, Extreme)

3. **Scatter Chart (Distance vs Travel Time)**:
   - **X-Axis:** `Distance_km`
   - **Y-Axis:** `Travel_Time_min`
   - **Legend:** `Transport_Mode`

---

## 4. Interactive Slicers Panel (Left or Top Filter Bar)

Add 6 Slicer visuals:
1. **Slicer 1 (Tile / Buttons):** `Transport_Mode` (Metro, Local, Auto)
2. **Slicer 2 (Dropdown):** `Starting_Area`
3. **Slicer 3 (Dropdown):** `Destination`
4. **Slicer 4 (Radio):** `Peak_Hour` (Yes / No)
5. **Slicer 5 (Dropdown):** `Weather` (Clear, Rainy, Humid, Cloudy)
6. **Slicer 6 (Dropdown):** `Crowd_Level` (Low, Medium, High, Extreme)

---

## 5. Viva Explanation for Power BI

When asked in Viva:
> *"What does your Power BI dashboard provide that your Flask website does not?"*

**Answer:**
> *"Power BI provides real-time cross-filtering and slicing for business analysts. Clicking on 'Metro' instantly filters all KPI cards, scatter plots, and area rankings without reloading the web page or writing server-side SQL queries."*

