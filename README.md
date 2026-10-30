# Mumbai Commute Analytics — Metro vs Local vs Auto
**A Beginner-Friendly B.Sc Data Science College Project**

---

> ### ⚠️ Academic Simulation Disclaimer
> **"This dataset is created/simulated for academic analysis and does not represent official Mumbai transport statistics."**  
> Operational metrics (fares, travel durations, peak delays, and crowd conditions) are modeled to reflect real-world commuter dynamics for educational and analytical study.

---

## 1. Project Objective

The Mumbai Metropolitan Region relies heavily on multimodal commuting: **Mumbai Local Trains** (the city's lifeline), **Mumbai Metro** (modern air-conditioned transit), and **Auto Rickshaws** (suburban first/last-mile connectivity).

This project uses Python, Pandas, Seaborn, MySQL, Power BI, and Scikit-learn (Decision Tree Classifier) to answer:
1. **Which transport mode is fastest?**
2. **Which is cheapest?**
3. **Which is most suitable for longer distances?**
4. **How do peak hours affect travel duration and delays?**
5. **How does crowd level differ between modes?**
6. **Is higher cost associated with lower travel time?**
7. **Which mode do users prefer in terms of comfort and satisfaction?**
8. **Can Machine Learning predict the most suitable transport mode from commuter requirements?**

---

## 2. Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **Backend:** Python 3, Flask
- **Data Science:** Pandas, NumPy, Matplotlib, Seaborn
- **Machine Learning:** Scikit-learn (Decision Tree Classifier, Random Forest)
- **Database:** MySQL & `mysql-connector-python`
- **Business Intelligence:** Microsoft Power BI & Excel
- **Editor:** Visual Studio Code (VS Code)

---

## 3. Project Directory Structure

```text
mumbai-commute-analytics/
│
├── app.py                     # Flask web server and routing
├── analysis.py                # Exploratory Data Analysis & chart generation
├── data_processing.py         # Data cleaning, missing value imputation, outlier detection
├── generate_dataset.py        # Realistic commuter simulation dataset generator
├── train_model.py             # Decision Tree & Random Forest training & serialization
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation & execution guide
├── powerbi_guide.md           # Step-by-step Power BI dashboard tutorial
│
├── data/
│   ├── commute_data.csv       # Raw simulated dataset (contains intentional dirty data)
│   └── commute_data_cleaned.csv # Cleaned dataset ready for EDA & ML
│
├── model/
│   └── commute_model.pkl      # Saved Decision Tree model & label encoders
│
├── database/
│   └── database.sql           # MySQL schema, table structure, and benchmark queries
│
├── templates/
│   ├── base.html              # Shared layout navbar and footer
│   ├── index.html             # Home page
│   ├── dashboard.html         # Key metrics & Chart.js interactive graphs
│   ├── comparison.html        # Detailed mode trade-off & radar analysis
│   ├── data.html              # Filterable and searchable data table
│   ├── analytics.html         # Seaborn charts and data science findings
│   ├── prediction.html        # ML user input form & suitability prediction
│   └── about.html             # Viva preparation Q&A & project limitations
│
└── static/
    ├── css/
    │   └── style.css          # Custom styling and color themes
    ├── js/
    │   └── script.js          # Interactive table search & tooltips
    └── images/                # Matplotlib & Seaborn saved visual artifacts
        ├── travel_time_and_cost.png
        ├── distance_vs_time.png
        ├── distance_vs_cost.png
        ├── peak_hour_impact.png
        ├── crowd_distribution.png
        ├── ratings_distribution.png
        ├── confusion_matrix.png
        └── feature_importance.png
```

---

## 4. Step-by-Step How to Run in VS Code

### Step 1: Open the Project in VS Code
Open VS Code, press `Ctrl + O` (or `File -> Open Folder...`), and select the `mumbai-commute-analytics` directory.

### Step 2: Open Terminal & Install Dependencies
Press `Ctrl + ~` to open the integrated terminal in VS Code:
```bash
pip install -r requirements.txt
```

### Step 3: Generate the Dataset
Create the academic simulation dataset (1,225 records with realistic Mumbai locations):
```bash
python generate_dataset.py
```

### Step 4: Run Data Cleaning
Clean raw data (removes duplicates, standardizes casing, imputes missing waiting times with median, prunes outliers):
```bash
python data_processing.py
```

### Step 5: Run Exploratory Data Analysis (EDA)
Compute summary metrics and generate charts into `static/images/`:
```bash
python analysis.py
```

### Step 6: Train the Machine Learning Model
Train Decision Tree Classifier, evaluate accuracy, feature importance, and save `model/commute_model.pkl`:
```bash
python train_model.py
```

### Step 7: Launch the Flask Website
Start the web dashboard:
```bash
python app.py
```
Open your browser and visit: **`http://127.0.0.1:5000`**

---

## 5. MySQL Database Setup

1. Open **MySQL Workbench** or run MySQL command line.
2. Open and execute `database/database.sql`.
3. It creates the database `mumbai_commute_db` and table `commute_data`.
4. Run the included analytical SQL queries to answer benchmark viva questions!

---

## 6. Power BI Dashboard

1. Follow the instructions in `powerbi_guide.md`.
2. Connect Power BI Desktop to `data/commute_data_cleaned.csv`.
3. Add the provided DAX measures and build interactive slicers and KPI cards.

---

## 7. Viva Highlights for Examiners

- **Why Decision Tree?** Explainable, rule-based, matches real human transit choices.
- **Why Impute with Median?** Waiting times are right-skewed; median is robust against extreme values.
- **Why Train-Test Split?** Prevents overfitting and evaluates generalization on unseen commutes.
- **Key Empirical Finding:** Local Trains dominate long distance & cost efficiency; Metro offers maximum comfort & punctuality; Auto Rickshaws offer private first-mile convenience but suffer road traffic congestion in peak hours.

