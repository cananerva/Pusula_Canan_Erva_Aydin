import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Genel ayarlar
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

# Veri yükle
df = pd.read_csv("data/raw/Talent_Academy_Case_DT_2025.csv")
print("Shape:", df.shape)
print(df.head())

# Çıktı klasörü
os.makedirs("outputs/figures", exist_ok=True)

# Info & Describe
print("\n--- Info ---")
print(df.info())
print("\n--- Describe ---")
print(df.describe(include="all"))

# Eksik değerler
missing = df.isna().sum().sort_values(ascending=False)
print("\n--- Missing Values ---\n", missing)

plt.figure(figsize=(10, 6))
sns.heatmap(df.isna(), cbar=False)
plt.title("Missing Values Heatmap")
plt.savefig("outputs/figures/missing_heatmap.png")
plt.close()

# Sayısal değişkenler
num_cols = df.select_dtypes(include="number").columns
if len(num_cols) > 0:
    df[num_cols].hist(figsize=(12, 8), bins=30)
    plt.tight_layout()
    plt.savefig("outputs/figures/numerical_distributions.png")
    plt.close()

# Kategorik değişkenler
cat_cols = df.select_dtypes(include="object").columns
if len(cat_cols) > 0:
    for col in cat_cols:
        plt.figure(figsize=(8, 4))
        order = df[col].value_counts().index[:20]  # en sık 20 kategori
        sns.countplot(y=col, data=df, order=order)
        plt.title(f"Distribution of {col}")
        plt.savefig(f"outputs/figures/{col}_distribution.png")
        plt.close()

# Hedef değişken (varsa)
if "TedaviSuresi" in df.columns:
    plt.figure(figsize=(8, 4))
    sns.histplot(df["TedaviSuresi"], kde=True, bins=20)
    plt.title("Distribution of TedaviSuresi")
    plt.savefig("outputs/figures/TedaviSuresi_distribution.png")
    plt.close()

# Korelasyon matrisi
if len(num_cols) > 1:
    plt.figure(figsize=(10, 6))
    sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.savefig("outputs/figures/correlation_matrix.png")
    plt.close()
