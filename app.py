import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("DeathEventPrediction.pkl")

st.set_page_config(page_title="Prediksi Kematian Pasien", page_icon="💔", layout="centered")
st.title("💉 Prediksi Kematian Pasien Gagal Jantung")

st.markdown("Aplikasi ini memprediksi apakah pasien dengan gagal jantung berisiko meninggal berdasarkan beberapa parameter medis.")

# Fungsi konversi
def ya_tidak(val):
    return 1 if val == "Ya" else 0

def jenis_kelamin(val):
    return 1 if val == "Laki-laki" else 0

st.markdown("---")
st.header("📝 Input Data Pasien")

# Layout kolom
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Usia (tahun)", min_value=1, max_value=120, help="Usia pasien saat pemeriksaan")
    sex = jenis_kelamin(st.radio("Jenis Kelamin", ["Perempuan", "Laki-laki"]))
    anaemia = ya_tidak(st.radio("Apakah pasien mengalami anaemia?", ["Tidak", "Ya"]))
    diabetes = ya_tidak(st.radio("Apakah pasien memiliki diabetes?", ["Tidak", "Ya"]))
    smoking = ya_tidak(st.radio("Apakah pasien merokok?", ["Tidak", "Ya"]))
    hbp = ya_tidak(st.radio("Tekanan darah tinggi?", ["Tidak", "Ya"]))

with col2:
    cpk = st.number_input("Creatinine Phosphokinase", min_value=0.0, help="Kadar enzim CPK dalam darah")
    ef = st.slider("Ejection Fraction (%)", 0, 100, help="Persentase darah yang dipompa keluar oleh jantung")
    platelets = st.number_input("Jumlah Platelets", min_value=0.0, help="Jumlah trombosit dalam darah")
    sc = st.number_input("Serum Creatinine", min_value=0.0, help="Tingkat kreatinin dalam serum darah")
    ss = st.number_input("Serum Sodium", min_value=0.0, help="Tingkat sodium dalam serum darah")
    time = st.number_input("Waktu pengamatan (hari)", min_value=0, help="Jumlah hari pasien diamati sejak pemeriksaan")

# Tombol prediksi
st.markdown("---")
if st.button("🔍 Prediksi"):
    input_data = np.array([[age, anaemia, cpk, diabetes, ef, hbp, platelets, sc, ss, sex, smoking, time]])
    prediction = model.predict(input_data)[0]
    
    st.markdown("## Hasil Prediksi")
    if prediction == 1:
        st.error("⚠️ Pasien diprediksi **MENINGGAL** dalam periode pengamatan.")
    else:
        st.success("✅ Pasien diprediksi **BERTAHAN HIDUP** dalam periode pengamatan.")
