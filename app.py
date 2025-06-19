import streamlit as st
import joblib
import numpy as np

# Load model (ensure 'DeathEventPrediction.pkl' is in the same directory)
try:
    model = joblib.load("DeathEventPrediction.pkl")
except FileNotFoundError:
    st.error("Error: Model file 'DeathEventPrediction.pkl' not found. Please ensure it's in the same directory.")
    st.stop() # Stop the app if the model isn't found

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Prediksi Kematian Pasien Gagal Jantung",
    page_icon="❤‍🩹", # Changed to a more relevant icon
    layout="centered",
    initial_sidebar_state="auto"
)

# --- HELPER FUNCTIONS ---
def ya_tidak_to_int(val):
    return 1 if val == "Ya" else 0

def jenis_kelamin_to_int(val):
    return 1 if val == "Laki-laki" else 0

# --- HEADER SECTION ---
st.markdown(
    """
    <style>
    .main-header {
        font-size: 3.5em;
        font-weight: bold;
        color: #FF4B4B; /* A striking red for emphasis */
        text-align: center;
        margin-bottom: 0.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .subheader {
        font-size: 1.5em;
        color: #555;
        text-align: center;
        margin-bottom: 2em;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green for predict button */
        color: white;
        font-size: 1.2em;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.3);
    }
    .stRadio div[data-baseweb="radio"] {
        padding: 5px 0;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Custom styling for success/error messages */
    .stAlert {
        border-radius: 8px;
        font-size: 1.2em;
        padding: 15px;
    }
    .stAlert.success {
        background-color: #e6ffe6;
        color: #006600;
        border-left: 5px solid #00cc00;
    }
    .stAlert.error {
        background-color: #ffe6e6;
        color: #cc0000;
        border-left: 5px solid #ff0000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="main-header">❤‍🩹 Prediksi Risiko Kematian Pasien Gagal Jantung</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Aplikasi ini membantu memprediksi risiko kematian pasien gagal jantung berdasarkan parameter medis penting.</p>', unsafe_allow_html=True)

st.write("---") # Visual separator

# --- INPUT SECTION ---
st.header("📋 Masukkan Data Pasien")
st.markdown("Isi detail pasien di bawah untuk mendapatkan prediksi.")

# Using columns for better organization and less vertical scroll
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Informasi Demografi")
    age = st.number_input(
        "Usia (tahun)",
        min_value=1,
        max_value=120,
        value=50, # Default value
        help="Usia pasien saat pemeriksaan",
        key="age_input"
    )
    sex = jenis_kelamin_to_int(
        st.radio("Jenis Kelamin", ["Perempuan", "Laki-laki"], key="sex_radio")
    )
    anaemia = ya_tidak_to_int(
        st.radio("Anaemia?", ["Tidak", "Ya"], key="anaemia_radio", help="Apakah pasien mengalami anaemia?")
    )

with col2:
    st.subheader("Kondisi Medis")
    diabetes = ya_tidak_to_int(
        st.radio("Diabetes?", ["Tidak", "Ya"], key="diabetes_radio", help="Apakah pasien memiliki riwayat diabetes?")
    )
    smoking = ya_tidak_to_int(
        st.radio("Merokok?", ["Tidak", "Ya"], key="smoking_radio", help="Apakah pasien adalah perokok?")
    )
    hbp = ya_tidak_to_int(
        st.radio("Tekanan Darah Tinggi?", ["Tidak", "Ya"], key="hbp_radio", help="Apakah pasien memiliki tekanan darah tinggi (hipertensi)?")
    )
    
with col3:
    st.subheader("Hasil Tes Laboratorium & Observasi")
    cpk = st.number_input(
        "Creatinine Phosphokinase (CPK)",
        min_value=0.0,
        value=500.0, # Default value
        help="Kadar enzim Creatinine Phosphokinase dalam darah (mcg/L)",
        key="cpk_input"
    )
    ef = st.slider(
        "Ejection Fraction (%)",
        0, 100, 40, # Default value
        help="Persentase darah yang dipompa keluar oleh ventrikel kiri jantung pada setiap detak",
        key="ef_slider"
    )
    platelets = st.number_input(
        "Jumlah Platelets (kiloplatelets/mL)",
        min_value=0.0,
        value=250000.0, # Default value
        help="Jumlah trombosit dalam darah",
        key="platelets_input"
    )
    sc = st.number_input(
        "Serum Creatinine (mg/dL)",
        min_value=0.0,
        value=1.5, # Default value
        help="Tingkat kreatinin dalam serum darah",
        key="sc_input"
    )
    ss = st.number_input(
        "Serum Sodium (mEq/L)",
        min_value=0.0,
        value=137.0, # Default value
        help="Tingkat sodium dalam serum darah",
        key="ss_input"
    )
    time = st.number_input(
        "Waktu Pengamatan (hari)",
        min_value=0,
        value=100, # Default value
        help="Jumlah hari pasien diamati sejak pemeriksaan awal",
        key="time_input"
    )

st.write("---") # Another visual separator

# --- PREDICTION BUTTON & RESULT ---
st.markdown("<h3><br></h3>", unsafe_allow_html=True) # Add some vertical space
if st.button("🚀 Dapatkan Prediksi", use_container_width=True):
    # Prepare input data for the model
    input_data = np.array([[age, anaemia, cpk, diabetes, ef, hbp, platelets, sc, ss, sex, smoking, time]])

    # Make prediction
    prediction = model.predict(input_data)[0]

    st.markdown("---")
    st.subheader("Hasil Prediksi")
    if prediction == 1:
        st.error("⚠ *Pasien diprediksi MENINGGAL* dalam periode pengamatan.", icon="🚨")
        st.markdown("<br>Penting: Hasil ini adalah prediksi dan harus dikonfirmasi oleh tenaga medis profesional.", unsafe_allow_html=True)
    else:
        st.success("✅ *Pasien diprediksi BERTAHAN HIDUP* dalam periode pengamatan.", icon="🎉")
        st.markdown("<br>Penting: Hasil ini adalah prediksi dan harus dikonfirmasi oleh tenaga medis profesional.", unsafe_allow_html=True)

st.markdown("---")
st.info("Aplikasi ini dibuat untuk tujuan edukasi dan demonstrasi. Selalu konsultasikan dengan dokter untuk diagnosis dan penanganan medis.")
