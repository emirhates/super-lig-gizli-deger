import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import unicodedata
from thefuzz import process

st.title("⚽ Süper Lig Gizli Değerli Oyuncular")
st.write("Piyasa değeri düşük ama performansı yüksek oyuncuları keşfet!")

# Veriyi yükle
@st.cache_data
def veri_yukle():
    df = pd.read_csv("birlesik_veri.csv", encoding="utf-8-sig")
    for col in ["Player", "Squad"]:
        try:
            df[col] = df[col].str.encode("latin-1").str.decode("utf-8", errors="replace")
        except:
            pass
    return df

df = veri_yukle()

# Filtreler
st.sidebar.header("Filtreler")
min_mac = st.sidebar.slider("Minimum Maç Sayısı", 5, 30, 15)
max_deger = st.sidebar.slider("Maximum Piyasa Değeri (Milyon €)", 1, 10, 5)
pozisyon = st.sidebar.multiselect("Pozisyon", ["FW", "MF", "DF"], default=["FW", "MF"])

# Piyasa değeri dönüştür
def deger_donustur(deger):
    if deger == "-" or pd.isna(deger):
        return np.nan
    deger = str(deger).replace(" ", "").replace("€", "")
    if "mil." in deger:
        return float(deger.replace("mil.", "")) * 1_000_000
    elif "bin" in deger:
        return float(deger.replace("bin", "")) * 1_000
    return np.nan

df["Deger_Euro"] = df["Piyasa_Degeri"].apply(deger_donustur)
df["Yas"] = df["Age"].str.split("-").str[0].astype(int, errors="ignore")

# Performans skoru
def performans_skoru(row):
    pos = str(row["Pos"])
    if "FW" in pos:
        return (row["Gls.1"] * 0.7) + (row["Ast.1"] * 0.3)
    elif "MF" in pos:
        return (row["Gls.1"] * 0.4) + (row["Ast.1"] * 0.6)
    else:
        return (row["Gls.1"] * 0.3) + (row["Ast.1"] * 0.7)

df["Performans"] = df.apply(performans_skoru, axis=1)

def yas_carpan(yas):
    if yas <= 23: return 1.5
    elif yas <= 26: return 1.2
    elif yas <= 29: return 1.0
    elif yas <= 32: return 0.8
    else: return 0.6

df["Yas_Carpan"] = df["Yas"].apply(yas_carpan)
df["Gizli_Deger"] = (df["Performans"] / (df["Deger_Euro"] / 1_000_000)) * df["Yas_Carpan"]

# Filtrele
df_filtre = df[
    (df["Deger_Euro"].notna()) &
    (df["MP"] >= min_mac) &
    (df["Deger_Euro"] <= max_deger * 1_000_000) &
    (df["Performans"] >= 0.25) &
    (df["Pos"].apply(lambda x: any(p in str(x) for p in pozisyon)))
].copy()

# Grafik
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df_filtre["Deger_Euro"] / 1_000_000,
           df_filtre["Performans"],
           color="lightgray", alpha=0.6, s=60)

top10 = df_filtre.sort_values("Gizli_Deger", ascending=False).head(10)
ax.scatter(top10["Deger_Euro"] / 1_000_000,
           top10["Performans"],
           color="red", s=100)

for _, row in top10.iterrows():
    ax.annotate(row["Player"],
                (row["Deger_Euro"] / 1_000_000, row["Performans"]),
                textcoords="offset points",
                xytext=(8, 4), fontsize=8)

ax.set_xlabel("Piyasa Değeri (Milyon €)")
ax.set_ylabel("Performans Skoru (90 dk başına)")
ax.set_title("Süper Lig Gizli Değerli Oyuncular")
ax.set_xlim(0, max_deger)
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# Tablo
st.subheader("Top 15 Gizli Değerli Oyuncu")
st.dataframe(
    df_filtre[["Player", "Squad", "Pos", "Yas", "MP", "Gls", "Ast", "Piyasa_Degeri", "Gizli_Deger"]]
    .sort_values("Gizli_Deger", ascending=False)
    .head(15)
    .reset_index(drop=True)
)
