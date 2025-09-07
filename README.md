# 🧭 Talent Academy Case Study – Canan Erva Aydın

## 🎯 Objective
This project focuses on analyzing and preprocessing a **physical therapy & rehabilitation** dataset in order to:

- 📊 Perform **Exploratory Data Analysis (EDA)**  
- 🛠️ Build a **data preprocessing pipeline**  
- ✅ Prepare the dataset in a **model-ready** format  

> Note: The target variable **`TedaviSuresi`** is completely missing, therefore model training was not performed.  
> The case study requirements emphasize **EDA and preprocessing**, not modeling.

---

## 📂 Project Structure
Pusula_Canan_Erva_Aydin/
│
├── data/
│ ├── raw/ # Raw dataset
│ │ └── Talent_Academy_Case_DT_2025.csv
│ └── processed/ # Cleaned dataset
│ └── cleaned_dataset.csv
│
├── docs/
│ └── summary.md # EDA summary report
│
├── models/
│ ├── preprocessor.joblib # Preprocessing pipeline (sklearn)
│ └── feature_metadata.txt # Feature list
│
├── outputs/
│ └── figures/ # EDA visualizations
│
├── src/
│ ├── eda.py # EDA script
│ └── prepare_pipeline.py # Preprocessing pipeline script
│
├── .gitignore
├── README.md
└── requirements.txt


