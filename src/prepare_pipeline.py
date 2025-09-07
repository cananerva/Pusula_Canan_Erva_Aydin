import pandas as pd
import numpy as np
import re
import joblib
import os
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# data/raw/Talent_Academy_Case_DT_2025.csv
# data/processed/cleaned_dataset.csv
# models/preprocessor.joblib
# models/feature_metadata.txt

RAW_DATA_PATH = Path("data/raw/Talent_Academy_Case_DT_2025.csv")
CLEAN_DATA_PATH = Path("data/processed/cleaned_dataset.csv")
PIPELINE_PATH = Path("models/preprocessor.joblib")
FEATURES_PATH = Path("models/feature_metadata.txt")

os.makedirs("models", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv(RAW_DATA_PATH)
df.columns = [str(c).strip() for c in df.columns]

for col in ["Yas", "UygulamaSuresi", "TedaviSuresi"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

def split_tokens(val):
    if pd.isna(val):
        return []
    s = re.sub(r"[;/]", ",", str(val))
    parts = [p.strip().lower() for p in s.split(",")]
    return [p for p in parts if p and p not in {"nan","none","yok","no"}]

multi_cols = ["KronikHastalik", "Alerji", "Tanilar", "UygulamaYerleri"]
for mc in multi_cols:
    if mc in df.columns:
        lists = df[mc].apply(split_tokens)
        df[f"{mc}_Count"] = lists.apply(len)

for c in ["Cinsiyet", "KanGrubu", "Uyruk", "Bolum", "TedaviAdi"]:
    if c in df.columns:
        df[c] = df[c].astype(str).str.strip().replace(
            {"nan": np.nan, "None": np.nan, "": np.nan}
        )

df.to_csv(CLEAN_DATA_PATH, index=False)

target_col = "TedaviSuresi" if "TedaviSuresi" in df.columns else None
numeric_cols = [c for c in df.select_dtypes(include="number").columns if c != target_col]
categorical_cols = [c for c in df.columns if c not in numeric_cols + ([target_col] if target_col else [])]

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_cols),
    ("cat", categorical_transformer, categorical_cols)
])

X = df.drop(columns=[target_col]) if target_col else df.copy()
preprocessor.fit(X)

joblib.dump(preprocessor, PIPELINE_PATH)

with open(FEATURES_PATH, "w", encoding="utf-8") as f:
    f.write("Numeric columns:\n")
    f.write("\n".join(numeric_cols))
    f.write("\n\nCategorical columns:\n")
    f.write("\n".join(categorical_cols))
    if target_col:
        f.write(f"\n\nTarget: {target_col}")

print("Pipeline hazır!")
print(f"- Temiz veri: {CLEAN_DATA_PATH}")
print(f"- Pipeline:   {PIPELINE_PATH}")
print(f"- Metadata:   {FEATURES_PATH}")
