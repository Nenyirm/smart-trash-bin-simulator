from pathlib import Path
import base64

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

from fuzzy import INPUT, OUTPUT, RULES, trap, infer, status
from simulasi import SKENARIO, jalankan, metrik


# ============================================================
# 1. KONFIGURASI HALAMAN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"

ICON_CANDIDATES = [
    ASSET_DIR / "smart_trash_bin_icon.png",
    ASSET_DIR / "Tempat Sampah Kompos Pintar Bertenaga Surya.png",
]

ICON_PATH = next(
    (path for path in ICON_CANDIDATES if path.exists()),
    None
)

st.set_page_config(
    page_title="Smart Trash Bin | Intelligent Eco System",
    page_icon=str(ICON_PATH) if ICON_PATH else "♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. TEMA VISUAL MODERN ECO-TECH DASHBOARD
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #172D3F;
    --navy-light: #294B5A;
    --teal: #238F88;
    --teal-dark: #176F6A;
    --mint: #B9DCCB;
    --sage: #DCE9DF;
    --lime: #A8D34F;
    --cyan: #9ADDE0;
    --ink: #263844;
    --muted: #73838A;
    --surface: #FFFFFF;
    --line: #E3EBE7;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

.stApp {
    background:
        radial-gradient(circle at 5% 5%, rgba(168,211,79,.18), transparent 25%),
        radial-gradient(circle at 95% 15%, rgba(111,202,199,.20), transparent 28%),
        linear-gradient(135deg, #E8F0E9 0%, #F4F6F1 48%, #E2EFEC 100%);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: rgba(235,242,237,.65);
}

.main .block-container {
    max-width: 1480px;
    padding: 2rem 2.4rem 3rem;
    margin-top: 1rem;
    margin-bottom: 2rem;
    background: rgba(250,252,249,.91);
    border: 1px solid rgba(255,255,255,.9);
    border-radius: 25px;
    box-shadow: 0 18px 55px rgba(28,55,63,.11);
    position: relative;
}

/* Dekorasi background */
.main .block-container::before {
    content: "";
    position: fixed;
    width: 260px;
    height: 260px;
    right: -90px;
    top: 120px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(133,211,194,.20), transparent 70%);
    pointer-events: none;
    z-index: 0;
}

.main .block-container::after {
    content: "";
    position: fixed;
    width: 230px;
    height: 230px;
    left: -100px;
    bottom: 35px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(168,211,79,.13), transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* HEADER */
.brand-header {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 8px 4px 20px;
    position: relative;
    z-index: 1;
}

.brand-icon-wrap {
    width: 96px;
    height: 96px;
    min-width: 96px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border-radius: 22px;
    background: linear-gradient(145deg, #E4F4EC, #D5F0EF);
    border: 1px solid rgba(35,143,136,.18);
    box-shadow: 0 8px 24px rgba(35,105,96,.15);
}

.brand-icon-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 20px;
}

.brand-title {
    margin: 0;
    color: var(--navy);
    font-family: 'Manrope', sans-serif;
    font-size: clamp(1.6rem, 3.2vw, 2.6rem);
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -1px;
}

.brand-subtitle {
    margin-top: 8px;
    color: #40545D;
    font-size: .95rem;
    font-weight: 500;
    line-height: 1.45;
}

.brand-kicker {
    color: var(--teal);
    font-size: .74rem;
    font-weight: 800;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #172D3F 0%, #203E4A 58%, #24545A 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    color: #F4FAF6 !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #C2D7D0 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 9px;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 12px;
    padding: 11px 13px;
    color: #E6F0EB !important;
    transition: all .2s ease;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(148,218,194,.14);
    border-color: rgba(148,218,194,.25);
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, #287F7B, #3B9C8C);
    border-color: rgba(185,230,210,.35);
    box-shadow: 0 5px 14px rgba(0,0,0,.13);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: #F4FAF6 !important;
    font-weight: 650;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,.14) !important;
}

/* HEADING DAN TEKS */
h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--navy) !important;
    letter-spacing: -.45px;
}

h2 {
    font-size: 1.55rem !important;
    font-weight: 800 !important;
}

h3 {
    font-size: 1.15rem !important;
    font-weight: 750 !important;
}

p, li, label, .stMarkdown {
    color: #40545D;
}

[data-testid="stCaptionContainer"] {
    color: #77888C !important;
    font-size: .91rem;
}

hr {
    border-color: #E2EBE6 !important;
}

/* METRIC CARD */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #FFFFFF, #F4FAF7);
    border: 1px solid #DFEBE5;
    border-radius: 17px;
    padding: 17px 19px;
    box-shadow: 0 7px 18px rgba(28,66,67,.055);
    transition: transform .2s ease, box-shadow .2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 11px 22px rgba(28,66,67,.10);
}

div[data-testid="stMetricLabel"] {
    color: #71838A !important;
    font-weight: 700 !important;
}

div[data-testid="stMetricValue"] {
    color: var(--navy) !important;
    font-family: 'Manrope', sans-serif;
    font-weight: 800 !important;
}

/* SLIDER DAN INPUT */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--teal) !important;
    border: 2px solid white !important;
    box-shadow: 0 2px 7px rgba(35,143,136,.35);
}

.stSlider [data-baseweb="slider"] > div > div {
    background: #B8DDD2 !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #FFFFFF;
    border: 1px solid #DCE8E2;
    border-radius: 11px;
}

/* RADIO */
div[role="radiogroup"] {
    gap: 8px;
}

div[role="radiogroup"] label {
    background: #F0F6F2;
    border: 1px solid #DFEAE3;
    padding: 7px 13px;
    border-radius: 10px;
}

/* ALERT */
div[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid #D7E9E1;
    background: #EDF7F1;
    color: #315D52;
}

/* BUTTON */
.stButton > button {
    border-radius: 11px;
    border: 1px solid #CFE3D9;
    background: linear-gradient(135deg, #E8F5EE, #DDF1ED);
    color: var(--navy);
    font-weight: 700;
    transition: all .2s ease;
}

.stButton > button:hover {
    border-color: var(--teal);
    color: var(--teal-dark);
    box-shadow: 0 5px 13px rgba(35,143,136,.13);
    transform: translateY(-1px);
}

/* TABEL */
div[data-testid="stDataFrame"] {
    border: 1px solid #E0EAE4;
    border-radius: 13px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(28,66,67,.04);
}

/* GAMBAR DAN GRAFIK */
[data-testid="stImage"] img {
    border-radius: 16px;
    border: 1px solid rgba(215,230,222,.8);
    box-shadow: 0 7px 20px rgba(28,66,67,.07);
}

[data-testid="stPyplot"] {
    background: #FFFFFF;
    border: 1px solid #E3ECE6;
    border-radius: 15px;
    padding: 8px;
    box-shadow: 0 5px 15px rgba(28,66,67,.04);
}

/* FOOTER */
.footer-note {
    text-align: center;
    color: #81918F;
    font-size: .82rem;
    padding: 22px 0 4px;
    line-height: 1.5;
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1.2rem 1rem 2rem;
        margin-top: .4rem;
        border-radius: 18px;
    }

    .brand-header {
        gap: 14px;
    }

    .brand-icon-wrap {
        width: 72px;
        height: 72px;
        min-width: 72px;
        border-radius: 16px;
    }

    .brand-title {
        font-size: 1.45rem;
        letter-spacing: -.6px;
    }

    .brand-subtitle {
        font-size: .82rem;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        transition-duration: .01ms !important;
        animation-duration: .01ms !important;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. HEADER DAN IKON SMART TRASH BIN
# ============================================================

def image_to_base64(image_path):
    """Mengubah gambar lokal menjadi base64 agar bisa tampil saat deploy."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except (FileNotFoundError, OSError):
        return None


icon_base64 = image_to_base64(ICON_PATH) if ICON_PATH else None

if icon_base64:
    icon_html = (
        f'<img src="data:image/png;base64,{icon_base64}" '
        'alt="Smart Trash Bin Icon">'
    )
    sidebar_icon_html = (
        f'<div style="margin-bottom:12px;">'
        f'<img src="data:image/png;base64,{icon_base64}" '
        f'style="width:70px; height:70px; border-radius:18px; object-fit:cover; box-shadow:0 6px 18px rgba(0,0,0,.28); border:1px solid rgba(255,255,255,.15);" alt="Smart Trash Bin Icon">'
        f'</div>'
    )
else:
    icon_html = '<div style="font-size:42px;">♻️</div>'
    sidebar_icon_html = '<div style="font-size:2rem; margin-bottom:8px;">♻️</div>'

st.markdown(
    f"""
    <div class="brand-header">
        <div class="brand-icon-wrap">
            {icon_html}
        </div>
        <div>
            <div class="brand-kicker">KECERDASAN TIRUAN</div>
            <h1 class="brand-title">Smart Trash Bin</h1>
            <div class="brand-subtitle">
                <strong>Kelompok 4 · Pengendali Logika Fuzzy</strong><br>
                <span>Mengembalikan daun kering ke alam agar kembali memberi manfaat.</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. NAVIGASI SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        f"""
        <div style="padding:10px 4px 18px;">
            {sidebar_icon_html}
            <div style="font-family:Manrope,sans-serif;
                        font-size:1.08rem;
                        font-weight:800;
                        color:#F4FAF6;">
                SMART TRASH BIN
            </div>
            <div style="font-size:.76rem;
                        color:#BBD2C9;
                        margin-top:4px;">
                INTELLIGENT ECO SYSTEM
            </div>
        </div>
        <hr style="border-color:rgba(255,255,255,.15);">
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p style="font-size:.72rem; letter-spacing:1.5px; '
        'font-weight:800; color:#A9C9BD;">MENU UTAMA</p>',
        unsafe_allow_html=True,
    )

    menu = st.radio(
        "Navigasi",
        [
            "Beranda",
            "Visual Simulasi Mesin",
            "Anatomi Mesin",
            "Simulator AI",
            "AI vs Non-AI",
            "Dokumentasi",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("Kelompok 4 · Pengendali Logika Fuzzy")


# ============================================================
# 5. DATA ANATOMI MESIN
# ============================================================

BAGIAN = {
    "Energi & kontrol": (
        "energi",
        "Panel surya di puncak tiang mengisi baterai di belakang. "
        "Listrik lewat tombol stop darurat ke mikrokontroler, yang "
        "mengendalikan pemanas, motor grinder, motor pengaduk, dan "
        "kunci pintu lewat relay/driver, serta membaca sensor.",
    ),

    "Input & keamanan": (
        "input",
        "Celah ±2 cm hanya meloloskan daun, bukan tangan. Corong "
        "mengarahkan daun ke tengah grinder. Tombol stop darurat "
        "memutus daya seketika.",
    ),

    "Ruang pengomposan": (
        "ruang",
        "Pemanas nichrome berinsulasi di dinding kiri-kanan menjaga "
        "suhu, pengaduk bolak-balik memberi udara (aerasi) dan "
        "mendorong kompos matang ke bawah, sensor memantau kondisi.",
    ),

    "Grinder": (
        "grinder",
        "Dua pisau berputar berlawanan arah menarik dan mencacah "
        "daun jadi serpihan kecil, sehingga luas permukaannya besar "
        "dan lebih cepat diurai mikroba.",
    ),

    "Sensor": (
        "sensor",
        "Suhu & kelembapan (DS18B20/DHT22), pH (probe analog, "
        "target 6,5–7,5), dan gas (MQ-135/MQ-4) mengirim data "
        "ke mikrokontroler.",
    ),

    "Pintu kompos & bantalan alas": (
        "output",
        "Pintu terkunci solenoid (interlock) hanya terbuka saat "
        "proses selesai dan aman. Bantalan alas menampung air "
        "lindi, cairan sisa, dan air hujan.",
    ),
}


# ============================================================
# 6. FUNGSI BANTUAN
# ============================================================

def tampilkan_gambar(nama_file, caption=None, width=None):
    """Menampilkan gambar dari folder assets secara aman tanpa error width."""
    path = ASSET_DIR / nama_file

    if path.exists():
        if width:
            st.image(str(path), caption=caption, width=width)
        else:
            st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.warning(
            f"Gambar {nama_file} belum ditemukan di folder assets."
        )


def tampilkan_kartu_info(judul, isi):
    """Menampilkan informasi dalam bentuk kartu modern."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #FFFFFF, #F0F8F3);
            border: 1px solid #DCEAE1;
            border-radius: 15px;
            padding: 18px;
            margin-bottom: 12px;
            box-shadow: 0 5px 15px rgba(28,66,67,.05);
        ">
            <div style="
                color: #238F88;
                font-weight: 800;
                margin-bottom: 8px;
            ">{judul}</div>
            <div style="color: #40545D; line-height: 1.7;">
                {isi}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def buat_grafik_keanggotaan(kategori, konfigurasi, nilai=None):
    """Membuat grafik fungsi keanggotaan fuzzy."""
    batas = konfigurasi["range"]
    x = np.linspace(batas[0], batas[1], 300)

    fig, ax = plt.subplots(figsize=(8, 3.5))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FAFCFA")

    for nama, parameter in konfigurasi["sets"].items():
        y = trap(x, *parameter)
        ax.plot(x, y, linewidth=2, label=nama.capitalize())

    if nilai is not None:
        ax.axvline(
            nilai,
            color="#D97757",
            linestyle="--",
            linewidth=2,
            label=f"Nilai input: {nilai:.1f}",
        )

    ax.set_title(
        konfigurasi["label"],
        fontsize=12,
        fontweight="bold",
        color="#172D3F",
    )
    ax.set_xlabel("Nilai")
    ax.set_ylabel("Derajat Keanggotaan")
    ax.set_ylim(-0.05, 1.08)
    ax.grid(alpha=0.2)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()

    return fig


def buat_grafik_simulasi(df_fuzzy, df_baseline):
    """Membandingkan perubahan suhu dan gas."""
    fig, axes = plt.subplots(2, 1, figsize=(10, 6))
    fig.patch.set_facecolor("#FFFFFF")

    for ax in axes:
        ax.set_facecolor("#FAFCFA")
        ax.grid(alpha=0.2)

    axes[0].plot(
        df_fuzzy["menit"],
        df_fuzzy["suhu"],
        label="Fuzzy (AI)",
        color="#238F88",
        linewidth=2.2,
    )
    axes[0].plot(
        df_baseline["menit"],
        df_baseline["suhu"],
        label="Non-AI (On/Off)",
        color="#D69A4B",
        linewidth=2,
        linestyle="--",
    )
    axes[0].axhspan(40, 60, alpha=0.10, color="#238F88", label="Rentang target (40–60 °C)")
    axes[0].set_ylabel("Suhu (°C)", fontweight="bold", color="#172D3F")
    axes[0].set_title("Perubahan Suhu Selama Simulasi", fontweight="bold", color="#172D3F")
    axes[0].legend()

    axes[1].plot(
        df_fuzzy["menit"],
        df_fuzzy["gas"],
        label="Fuzzy (AI)",
        color="#238F88",
        linewidth=2.2,
    )
    axes[1].plot(
        df_baseline["menit"],
        df_baseline["gas"],
        label="Non-AI (On/Off)",
        color="#D69A4B",
        linewidth=2,
        linestyle="--",
    )
    axes[1].set_xlabel("Waktu (menit)", fontweight="bold", color="#172D3F")
    axes[1].set_ylabel("Indeks Gas", fontweight="bold", color="#172D3F")
    axes[1].set_title("Perubahan Indeks Gas Selama Simulasi", fontweight="bold", color="#172D3F")
    axes[1].legend()

    fig.tight_layout()
    return fig


# ============================================================
# 7. HALAMAN BERANDA
# ============================================================

if menu == "Beranda":

    st.markdown("## Mengenal Smart Trash Bin")

    col_hero_text, col_hero_img = st.columns([1.35, 1.0], gap="large")

    with col_hero_text:
        st.markdown(
            """
            Daun kering sering kali dibakar, tercampur dengan sampah
            plastik, terbawa angin hingga berterbangan, bahkan menumpuk
            dan menyumbat selokan. Padahal, daun-daun tersebut masih
            bisa dimanfaatkan menjadi kompos yang dapat dikembalikan
            ke tanah untuk menyuburkan tanaman.

            Melalui Smart Trash Bin, kami ingin menghadirkan cara yang
            lebih bermanfaat untuk mengolah daun kering. Mesin ini
            dirancang untuk mencacah daun dan mengolahnya menjadi
            kompos di dalam ruang tertutup, dengan memantau suhu,
            kelembapan, pH, dan gas selama proses pengomposan.
            """
        )

        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
                border: 1px solid #86EFAC;
                border-left: 4px solid #16A34A;
                border-radius: 8px;
                padding: 12px 14px;
                margin-top: 14px;
            ">
                <span style="font-weight: 800; color: #166534; font-size: 13px;">✨ Visi Desain Masa Depan</span><br>
                <span style="color: #14532D; font-size: 12.5px; line-height: 1.5;">
                    Di masa depan, Smart Trash Bin diwujudkan sebagai fasilitas publik cerdas ramah lingkungan yang mandiri energi bertenaga surya, memiliki kompartemen tertutup higienis, serta proses pengomposan daun kering otomatis berbasis AI.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_hero_img:
        tampilkan_gambar(
            "smart_trash_bin_future.png",
            caption="Konsep Fisik Masa Depan: Smart Trash Bin Mandiri Energi & Terkendali AI",
        )

    st.markdown("---")

    st.markdown("### Mengapa menggunakan Web Simulator?")

    st.markdown(
        """
        Karena Smart Trash Bin masih dalam tahap perancangan dan
        pengembangan, kami menghadirkan Web Simulator berbasis
        Logika Fuzzy untuk menggambarkan bagaimana sistem ini
        nantinya bekerja secara otomatis.

        Melalui simulator ini, kita bisa melihat bagaimana data
        dari sensor seperti suhu dan kelembapan digunakan untuk
        menentukan daya pemanas dan lama pengadukan yang
        dibutuhkan. Logika fuzzy memungkinkan sistem mengambil
        keputusan dengan cara yang lebih fleksibel, seperti ketika
        kita mengatakan kondisi "agak dingin" atau "cukup basah",
        bukan hanya bergantung pada batas angka yang kaku.
        """
    )

    st.markdown("---")

    # ============================================================
    # FOTO SKETSA MESIN (ALUR KERJA SMART TRASH BIN)
    # ============================================================
    st.markdown("### Alur kerja Smart Trash Bin")
    st.caption("Sketsa rancangan mesin Smart Trash Bin tampak depan dan tampak samping kanan:")

    col_sketsa1, col_sketsa2, col_sketsa3 = st.columns([0.4, 2.4, 0.4])
    with col_sketsa2:
        # Menggunakan sketsa mesin sesuai permintaan pengguna
        tampilkan_gambar(
            "sketsa_mesin.png",
            caption="Sketsa Rancangan Mesin Smart Trash Bin (Tampak Depan & Tampak Samping Kanan)"
        )

    st.markdown("---")

    st.markdown("### Sistem pengendali cerdas")

    col1, col2 = st.columns(2)

    with col1:
        tampilkan_kartu_info(
            "Input sensor",
            "Sistem menerima data suhu, kelembapan, dan indeks gas "
            "sebagai masukan untuk proses pengambilan keputusan."
        )

    with col2:
        tampilkan_kartu_info(
            "Pengendali logika fuzzy",
            "Data sensor diproses menggunakan aturan fuzzy "
            "Mamdani untuk menghasilkan keputusan pengendalian."
        )

    col3, col4 = st.columns(2)

    with col3:
        tampilkan_kartu_info(
            "Output pengendali",
            "Sistem menghasilkan rekomendasi daya pemanas dan "
            "durasi pengadukan."
        )

    with col4:
        tampilkan_kartu_info(
            "Tujuan",
            "Membantu menggambarkan pengendalian ruang pengomposan "
            "secara otomatis dan fleksibel."
        )


# ============================================================
# 8. HALAMAN VISUAL SIMULASI MESIN (DIGITAL TWIN)
# ============================================================

elif menu == "Visual Simulasi Mesin":

    st.markdown("## Visual Simulasi Gerak Mesin (Digital Twin)")
    st.write(
        "Simulasi visual interaktif: Lihat bagaimana daun kering dicacah oleh pisau grinder, "
        "kawat pemanas menyala merah membara saat dingin, pengaduk bergerak untuk membantu proses pengomposan "
        "terutama aerasi, hingga pintu solenoid terbuka otomatis ketika kompos siap digunakan."
    )

    widget_path = BASE_DIR / "simulator_widget.html"
    if widget_path.exists():
        try:
            with open(widget_path, "r", encoding="utf-8") as f:
                html_code = f.read()
            components.html(html_code, height=560)
        except Exception as e:
            st.error(f"Gagal memuat visual simulator: {e}")
    else:
        st.error("File simulator_widget.html belum ditemukan di folder aplikasi.")

    st.markdown("---")
    st.markdown("### Integrasi Fisik Mesin dengan Pengendali AI")

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        tampilkan_kartu_info(
            "Mekanisme Grinder & Keamanan",
            "Celah masukan dibuat sempit (±2 cm) untuk keamanan tangan pejalan kaki. "
            "Dua bilah pisau berputar berlawanan arah mencacah daun menjadi serpihan kecil "
            "(2–3 cm) untuk memperluas permukaan kontak mikroba. Dilengkapi tombol darurat (E-Stop) "
            "yang seketika memutus daya relai.",
        )
    with col_w2:
        tampilkan_kartu_info(
            "Aktuator Terkontrol Logika Fuzzy",
            "Pemanas Nichrome 80/20 diatur dayanya secara halus (0–100%) berdasarkan inferensi Mamdani "
            "agar suhu stabil di fase termofilik. Pengaduk mekanis bolak-balik digerakkan motor DC untuk aerasi oksigen, "
            "dan pintu solenoid (interlock) menjaga keamanan ruang selama proses.",
        )


# ============================================================
# 9. HALAMAN ANATOMI MESIN
# ============================================================

elif menu == "Anatomi Mesin":

    st.markdown("## Anatomi Smart Trash Bin")

    st.write(
        "Kenali bagian-bagian mesin dan fungsi setiap komponen "
        "yang dirancang untuk mendukung proses pengolahan daun kering."
    )

    nama_bagian = st.selectbox(
        "Pilih bagian mesin:",
        list(BAGIAN.keys()),
    )

    kode_gambar, deskripsi = BAGIAN[nama_bagian]

    nama_file = f"{kode_gambar}.png"

    st.markdown("---")

    kolom_gambar, kolom_info = st.columns([1.15, 1])

    with kolom_gambar:
        tampilkan_gambar(nama_file)

    with kolom_info:
        st.markdown(f"### {nama_bagian}")
        st.write(deskripsi)

        st.info(
            "Komponen ini merupakan bagian dari rancangan "
            "Smart Trash Bin dan ditampilkan sebagai ilustrasi "
            "konsep mesin."
        )

    st.markdown("---")

    st.markdown("### Komponen lainnya")

    for nama, (kode, keterangan) in BAGIAN.items():
        with st.expander(nama):
            tampilkan_gambar(f"{kode}.png")
            st.write(keterangan)


# ============================================================
# 10. HALAMAN SIMULATOR AI
# ============================================================

elif menu == "Simulator AI":

    st.markdown("## Simulator Pengendali Logika Fuzzy")

    st.write(
        "Masukkan nilai sensor untuk melihat bagaimana sistem "
        "menghasilkan rekomendasi daya pemanas dan durasi pengadukan."
    )

    st.markdown("---")

    st.markdown("### 1. Input sensor")

    kolom_suhu, kolom_kelembapan, kolom_gas = st.columns(3)

    with kolom_suhu:
        suhu = st.slider(
            "Suhu ruang (°C)",
            min_value=0,
            max_value=80,
            value=45,
            step=1,
        )

    with kolom_kelembapan:
        kelembapan = st.slider(
            "Kelembapan (%)",
            min_value=0,
            max_value=100,
            value=55,
            step=1,
        )

    with kolom_gas:
        gas = st.slider(
            "Indeks gas",
            min_value=0,
            max_value=100,
            value=20,
            step=1,
        )

    ph = st.slider(
        "Nilai pH",
        min_value=0.0,
        max_value=14.0,
        value=7.0,
        step=0.1,
    )

    nilai_input = {
        "suhu": float(suhu),
        "kelembapan": float(kelembapan),
        "gas": float(gas),
    }

    hasil = infer(nilai_input)
    keluaran = hasil["keluaran"]

    st.markdown("---")

    st.markdown("### 2. Hasil pengendalian")

    met1, met2 = st.columns(2)

    with met1:
        st.metric(
            "Daya pemanas",
            f"{keluaran['pemanas']:.1f}%",
        )

    with met2:
        st.metric(
            "Durasi pengadukan",
            f"{keluaran['pengaduk']:.1f} menit/siklus",
        )

    kondisi = status(nilai_input, ph)

    st.markdown("### 3. Status kondisi pengomposan")

    if kondisi == ["Normal, kondisi pengomposan baik"]:
        st.success(kondisi[0])
    else:
        for pesan in kondisi:
            st.warning(pesan)

    st.markdown("---")

    st.markdown("### 4. Grafik fungsi keanggotaan")

    tab_suhu, tab_kelembapan, tab_gas = st.tabs(
        ["Suhu", "Kelembapan", "Gas"]
    )

    with tab_suhu:
        st.pyplot(
            buat_grafik_keanggotaan(
                "suhu",
                INPUT["suhu"],
                suhu,
            )
        )

    with tab_kelembapan:
        st.pyplot(
            buat_grafik_keanggotaan(
                "kelembapan",
                INPUT["kelembapan"],
                kelembapan,
            )
        )

    with tab_gas:
        st.pyplot(
            buat_grafik_keanggotaan(
                "gas",
                INPUT["gas"],
                gas,
            )
        )

    st.markdown("---")

    st.markdown("### 5. Aturan fuzzy yang aktif")

    aturan_aktif = [
        {
            "Aturan": item["no"],
            "Kekuatan": round(item["kekuatan"], 3),
            "Kondisi": ", ".join(
                f"{key} {value}"
                for key, value in item["jika"].items()
            ),
            "Keputusan": ", ".join(
                f"{key} {value}"
                for key, value in item["maka"].items()
            ),
        }
        for item in hasil["aturan"]
        if item["kekuatan"] > 0
    ]

    if aturan_aktif:
        st.dataframe(
            pd.DataFrame(aturan_aktif),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Tidak ada aturan fuzzy yang aktif.")

    st.caption(
        "Catatan: hasil merupakan keluaran simulasi berdasarkan "
        "aturan fuzzy yang didefinisikan pada fuzzy.py."
    )


# ============================================================
# 11. HALAMAN PERBANDINGAN AI VS NON-AI
# ============================================================

elif menu == "AI vs Non-AI":

    st.markdown("## Perbandingan Pengendali AI dan Non-AI")

    st.write(
        "Halaman ini membandingkan pengendali berbasis logika fuzzy "
        "dengan pengendali konvensional On/Off menggunakan model "
        "simulasi ruang pengomposan."
    )

    st.info(
        "Simulasi ini menggunakan model matematis sederhana, "
        "bukan pembacaan sensor dari perangkat fisik."
    )

    skenario_pilihan = st.selectbox(
        "Pilih skenario pengujian:",
        list(SKENARIO.keys()),
    )

    durasi = st.slider(
        "Durasi simulasi (menit)",
        min_value=30,
        max_value=360,
        value=180,
        step=30,
    )

    if st.button("Jalankan simulasi", type="primary"):

        kondisi_awal = SKENARIO[skenario_pilihan]

        df_fuzzy = jalankan(
            kondisi_awal,
            mode="fuzzy",
            menit=durasi,
            seed=1,
        )

        df_baseline = jalankan(
            kondisi_awal,
            mode="baseline",
            menit=durasi,
            seed=1,
        )

        st.session_state["df_fuzzy"] = df_fuzzy
        st.session_state["df_baseline"] = df_baseline
        st.session_state["skenario_aktif"] = skenario_pilihan

    if (
        "df_fuzzy" in st.session_state
        and "df_baseline" in st.session_state
    ):

        df_fuzzy = st.session_state["df_fuzzy"]
        df_baseline = st.session_state["df_baseline"]

        st.markdown("---")
        st.markdown("### Grafik hasil simulasi")

        st.pyplot(
            buat_grafik_simulasi(
                df_fuzzy,
                df_baseline,
            ),
            use_container_width=True,
        )

        st.markdown("---")
        st.markdown("### Perbandingan metrik")

        metrik_fuzzy = metrik(df_fuzzy)
        metrik_baseline = metrik(df_baseline)

        tabel_metrik = pd.DataFrame({
            "Indikator": list(metrik_fuzzy.keys()),
            "Logika Fuzzy (AI)": list(metrik_fuzzy.values()),
            "On/Off (Non-AI)": list(metrik_baseline.values()),
        })

        st.dataframe(
            tabel_metrik,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("---")
        st.markdown("### Data simulasi")

        tab_fuzzy, tab_baseline = st.tabs(
            ["Data Logika Fuzzy", "Data On/Off"]
        )

        with tab_fuzzy:
            st.dataframe(
                df_fuzzy,
                use_container_width=True,
                hide_index=True,
            )

        with tab_baseline:
            st.dataframe(
                df_baseline,
                use_container_width=True,
                hide_index=True,
            )

        csv_fuzzy = df_fuzzy.to_csv(index=False).encode("utf-8")
        csv_baseline = df_baseline.to_csv(index=False).encode("utf-8")

        kolom_unduh1, kolom_unduh2 = st.columns(2)

        with kolom_unduh1:
            st.download_button(
                "Unduh data Fuzzy (CSV)",
                data=csv_fuzzy,
                file_name="hasil_simulasi_fuzzy.csv",
                mime="text/csv",
            )

        with kolom_unduh2:
            st.download_button(
                "Unduh data On/Off (CSV)",
                data=csv_baseline,
                file_name="hasil_simulasi_on_off.csv",
                mime="text/csv",
            )

    else:
        st.info(
            "Pilih skenario, tentukan durasi, lalu tekan "
            "'Jalankan simulasi' untuk melihat hasil perbandingan."
        )


# ============================================================
# 12. HALAMAN DOKUMENTASI
# ============================================================

elif menu == "Dokumentasi":

    st.markdown("## Dokumentasi Sistem")

    st.write(
        "Halaman ini menjelaskan komponen perangkat lunak "
        "yang digunakan dalam Web Simulator Smart Trash Bin."
    )

    st.markdown("### Teknologi yang digunakan")

    data_teknologi = pd.DataFrame({
        "Teknologi": [
            "Python",
            "Streamlit",
            "NumPy",
            "Pandas",
            "Matplotlib",
            "Logika Fuzzy Mamdani",
        ],
        "Fungsi": [
            "Bahasa pemrograman utama.",
            "Membangun antarmuka Web Simulator.",
            "Perhitungan numerik dan fungsi keanggotaan.",
            "Pengolahan data hasil simulasi.",
            "Visualisasi grafik hasil pengujian.",
            "Metode pengambilan keputusan berdasarkan aturan fuzzy.",
        ],
    })

    st.dataframe(
        data_teknologi,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    st.markdown("### Variabel input dan output")

    st.markdown("**Variabel input**")

    input_rows = []

    for nama, konfigurasi in INPUT.items():
        input_rows.append({
            "Variabel": konfigurasi["label"],
            "Rentang": (
                f"{konfigurasi['range'][0]} – "
                f"{konfigurasi['range'][1]}"
            ),
            "Himpunan fuzzy": ", ".join(
                konfigurasi["sets"].keys()
            ),
        })

    st.dataframe(
        pd.DataFrame(input_rows),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("**Variabel output**")

    output_rows = []

    for nama, konfigurasi in OUTPUT.items():
        output_rows.append({
            "Variabel": konfigurasi["label"],
            "Rentang": (
                f"{konfigurasi['range'][0]} – "
                f"{konfigurasi['range'][1]}"
            ),
            "Himpunan fuzzy": ", ".join(
                konfigurasi["sets"].keys()
            ),
        })

    st.dataframe(
        pd.DataFrame(output_rows),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    st.markdown("### Tahapan proses logika fuzzy")

    tahapan = [
        (
            "1. Fuzzifikasi",
            "Mengubah nilai sensor menjadi derajat keanggotaan "
            "pada himpunan fuzzy."
        ),
        (
            "2. Evaluasi aturan",
            "Memproses aturan IF-THEN berdasarkan kondisi input "
            "yang diterima."
        ),
        (
            "3. Agregasi",
            "Menggabungkan keluaran dari aturan fuzzy yang aktif."
        ),
        (
            "4. Defuzzifikasi",
            "Mengubah hasil fuzzy menjadi nilai numerik "
            "untuk daya pemanas dan durasi pengadukan."
        ),
    ]

    for judul, penjelasan in tahapan:
        tampilkan_kartu_info(judul, penjelasan)

    st.markdown("---")

    st.markdown("### Catatan pengembangan")

    st.write(
        """
        Web Simulator ini merupakan representasi perangkat lunak
        dari konsep pengendalian Smart Trash Bin. Nilai input
        sensor diberikan secara manual melalui antarmuka
        simulator. Model simulasi digunakan untuk menggambarkan
        perubahan kondisi ruang pengomposan dan membandingkan
        dua pendekatan pengendalian.

        Sistem ini belum terhubung langsung dengan sensor maupun
        aktuator pada perangkat keras Smart Trash Bin.
        """
    )


# ============================================================
# 13. FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer-note">
        <strong>SMART TRASH BIN</strong><br>
        Kelompok 4 · Pengendali Logika Fuzzy<br>
        Intelligent Eco System
    </div>
    """,
    unsafe_allow_html=True,
)
