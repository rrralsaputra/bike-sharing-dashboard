import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np


st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

st.markdown("""
<style>
.insight-box {
    background: #f8f9fb;
    border-left: 5px solid #4C9BE8;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 10px;
    font-size: 0.95rem; 
    line-height: 1.6;
    color: #1e1e2e;
}
.insight-box.green  { border-color: #6ECB8A; }
.insight-box.orange { border-color: #F4845F; }
.insight-box.yellow { border-color: #F9C846; }
.insight-label {
    font-weight: 700;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

def insight(icon, label, text, color="blue"):
    st.markdown(f"""
    <div class="insight-box {color}">
        <div class="insight-label">{icon} {label}</div>
        {text}
    </div>""", unsafe_allow_html=True)

# Load Data 
@st.cache_data
def load_data():
    day  = pd.read_csv("day.csv",  parse_dates=["dteday"])
    hour = pd.read_csv("hour.csv", parse_dates=["dteday"])
   
    label_maps = {
        "season":     {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"},
        "weathersit": {1: "Cerah", 2: "Berkabut/Berawan", 3: "Hujan/Salju Ringan", 4: "Hujan/Salju Lebat"},
        "yr":         {0: "2011", 1: "2012"},
    }
    
    for df in (day, hour):
        for col, mapping in label_maps.items():
            df[col] = df[col].map(mapping)
        df["month_name"] = df["dteday"].dt.strftime("%b")
        df["month_num"]  = df["dteday"].dt.month
    return day, hour

day_df, hour_df = load_data()

#  Sidebar 
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Left_side_of_Flying_Pigeon.jpg/320px-Left_side_of_Flying_Pigeon.jpg",
    use_container_width=True,
)
st.sidebar.title("🚲 Bike Sharing")
st.sidebar.markdown("---")

year_options   = ["Semua"] + sorted(day_df["yr"].unique().tolist())
season_options = ["Semua"] + sorted(day_df["season"].unique().tolist())

sel_year   = st.sidebar.selectbox("Pilih Tahun", year_options)
sel_season = st.sidebar.selectbox("Pilih Musim", season_options)

date_min   = day_df["dteday"].min().date()
date_max   = day_df["dteday"].max().date()
sel_dates  = st.sidebar.date_input("Rentang Tanggal", value=(date_min, date_max),
                                    min_value=date_min, max_value=date_max)

def apply_filters(df):
    d = df.copy()
    if sel_year   != "Semua": d = d[d["yr"]     == sel_year]
    if sel_season != "Semua": d = d[d["season"] == sel_season]
    if len(sel_dates) == 2:
        d = d[(d["dteday"].dt.date >= sel_dates[0]) & (d["dteday"].dt.date <= sel_dates[1])]
    return d

day_f  = apply_filters(day_df)
hour_f = apply_filters(hour_df)

PAL  = ["#4C9BE8", "#F4845F", "#6ECB8A", "#F9C846", "#8E44AD"]
BLUE = "#4C9BE8"

#  Header 
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Melihat kebiasaan dan tren orang bersepeda setiap hari dan per jam (2011-2012)")
st.markdown("---")

#  KPI Cards 
total_rides  = int(day_f["cnt"].sum())
avg_daily    = int(day_f["cnt"].mean()) if len(day_f) else 0
total_casual = int(day_f["casual"].sum())
total_reg    = int(day_f["registered"].sum())

k1, k2, k3, k4 = st.columns(4)
k1.metric("🚲 Total Disewa", f"{total_rides:,}")
k2.metric("📅 Rata-rata Harian", f"{avg_daily:,}")
k3.metric("🚶 Penyewa Biasa", f"{total_casual:,}")
k4.metric("🎫 Member Langganan", f"{total_reg:,}")
st.markdown("---")

# Tren & Komposisi 
st.subheader("📈 Tren Penyewaan dan Siapa Saja Penggunanya")
c1, c2 = st.columns([2.5, 1])

with c1:
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.fill_between(day_f["dteday"], day_f["cnt"], alpha=0.2, color=BLUE)
    ax.plot(day_f["dteday"], day_f["cnt"], color=BLUE, linewidth=1.6)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Total Sepeda Disewa")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig); plt.close(fig)
    insight("📌", "Poin Penting",
            "Penggunaan sepeda <b>jauh lebih banyak</b> di tahun 2012 dibandingkan 2011. "
            "Orang-orang paling suka bersepeda di pertengahan tahun saat cuaca sedang hangat.")

with c2:
    fig, ax = plt.subplots(figsize=(4, 4))
    wedges, texts, autotexts = ax.pie(
        [total_casual, total_reg], labels=["Penyewa Biasa\n(Casual)", "Member Langganan\n(Registered)"],
        autopct="%1.1f%%", colors=[PAL[1], PAL[0]], startangle=90,
        wedgeprops=dict(edgecolor="white", linewidth=2),
    )
    for at in autotexts: at.set_fontsize(11); at.set_fontweight("bold")
    fig.tight_layout()
    st.pyplot(fig); plt.close(fig)
    insight("📌", "Poin Penting",
            "Sebagian besar (<b>sekitar 80%</b>) yang menyewa sepeda adalah anggota member, "
            "bukan penyewa biasa yang hanya sesekali pakai.", color="green")

st.markdown("---")

# Musim & Cuaca 
st.subheader("🌿 Efek Musim dan Cuaca Terhadap Jumlah Sewa")
c3, c4 = st.columns(2)

with c3:
    if not day_f.empty:
        season_avg = day_f.groupby("season", observed=True)["cnt"].mean().reset_index().sort_values("cnt", ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(season_avg["season"], season_avg["cnt"], color=PAL, edgecolor="white")
        ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=10, fontweight="bold")
        ax.set_xlabel("Musim")
        ax.set_ylabel("Rata-rata Disewa per Hari")
        ax.set_title("Rata-rata Penyewaan Berdasarkan Musim", fontsize=11, fontweight="bold")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig); plt.close(fig)
        
        best_season = season_avg.iloc[0]["season"]
        best_val    = int(season_avg.iloc[0]["cnt"])
        insight("📌", "Poin Penting",
                f"<b>{best_season}</b> adalah waktu favorit untuk bersepeda (rata-rata <b>{best_val:,} kali disewa per hari</b>). "
                f"Cuaca yang sejuk bikin orang lebih suka bersepeda.")

with c4:
    if not day_f.empty:
        weather_avg = day_f.groupby("weathersit", observed=True)["cnt"].mean().reset_index().sort_values("cnt", ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.barh(weather_avg["weathersit"], weather_avg["cnt"], color=PAL[:len(weather_avg)], edgecolor="white")
        ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=10, fontweight="bold")
        ax.set_xlabel("Rata-rata Disewa per Hari")
        ax.set_title("Rata-rata Penyewaan Berdasarkan Cuaca", fontsize=11, fontweight="bold")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax.grid(axis="x", alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig); plt.close(fig)
        
        best_w  = weather_avg.iloc[0]["weathersit"]
        worst_w = weather_avg.iloc[-1]["weathersit"]
        insight("📌", "Poin Penting",
                f"Paling banyak orang menyewa sepeda saat cuacanya <b>{best_w}</b>. "
                f"Begitu cuaca memburuk seperti <b>{worst_w}</b>, jumlah pesepeda langsung anjlok.", color="yellow")

st.markdown("---")

# Clustering Jam 
st.subheader("⏰ Kapan Orang Paling Sering Bersepeda dalam Sehari?")

def bin_hour(h):
    if   0 <= h <  6: return "🌙 Dini Hari\n(00-05)"
    elif 6 <= h <  9: return "🌅 Pagi Sibuk\n(06-08)"
    elif 9 <= h < 12: return "☀️ Pagi\n(09-11)"
    elif 12 <= h < 14: return "🍽️ Siang\n(12-13)"
    elif 14 <= h < 17: return "🌤️ Sore\n(14-16)"
    elif 17 <= h < 20: return "🚗 Sore Sibuk\n(17-19)"
    else:              return "🌆 Malam\n(20-23)"

cluster_order = [
    "🌙 Dini Hari\n(00-05)", "🌅 Pagi Sibuk\n(06-08)", "☀️ Pagi\n(09-11)",
    "🍽️ Siang\n(12-13)", "🌤️ Sore\n(14-16)", "🚗 Sore Sibuk\n(17-19)", "🌆 Malam\n(20-23)"
]
DENSITY_COLOR = {"🟢 Sepi": "#6ECB8A", "🟡 Sedang": "#F9C846", "🔴 Ramai": "#F4845F"}

hour_c = hour_f.copy()
if not hour_c.empty:
    hour_c["jam_cluster"] = hour_c["hr"].apply(bin_hour)
    agg = hour_c.groupby("jam_cluster", observed=True).agg(
        rata_rata=("cnt", "mean"),
        casual_avg=("casual", "mean"),
        registered_avg=("registered", "mean"),
    ).reindex(cluster_order)

    q33 = agg["rata_rata"].quantile(0.33)
    q66 = agg["rata_rata"].quantile(0.66)
    agg["density"] = agg["rata_rata"].apply(
        lambda v: "🟢 Sepi" if v <= q33 else ("🟡 Sedang" if v <= q66 else "🔴 Ramai")
    )
    density_colors = [DENSITY_COLOR[d] for d in agg["density"]]
    total_avg  = agg["casual_avg"] + agg["registered_avg"]
    pct_casual = (agg["casual_avg"] / total_avg * 100).fillna(0).values
    pct_reg    = (agg["registered_avg"] / total_avg * 100).fillna(0).values

    c5, c6 = st.columns(2)

    with c5:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        bars = ax.bar(range(len(cluster_order)), agg["rata_rata"].values,
                      color=density_colors, edgecolor="white", width=0.7)
        ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=10, fontweight="bold")
        ax.set_xticks(range(len(cluster_order)))
        ax.set_xticklabels([c.split("\n")[0] for c in cluster_order], fontsize=9, rotation=25, ha="right")
        ax.set_ylabel("Rata-rata Disewa per Jam")
        ax.set_title("Jumlah Penyewaan per Rentang Waktu", fontsize=11, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        legend_els = [mpatches.Patch(facecolor=DENSITY_COLOR[k], label=k) for k in DENSITY_COLOR]
        ax.legend(handles=legend_els, fontsize=9, loc="upper left")
        fig.tight_layout()
        st.pyplot(fig); plt.close(fig)

    with c6:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        x = list(range(len(cluster_order)))
        ax.barh(x, pct_casual, color=PAL[1], edgecolor="white", height=0.65, label="Penyewa Biasa")
        ax.barh(x, pct_reg, left=pct_casual, color=PAL[0], edgecolor="white", height=0.65, label="Member Terdaftar")
        for i, (pc, pr) in enumerate(zip(pct_casual, pct_reg)):
            if pc > 5:  ax.text(pc/2,     i, f"{pc:.0f}%", va="center", ha="center", fontsize=9, fontweight="bold", color="white")
            if pr > 5:  ax.text(pc+pr/2,  i, f"{pr:.0f}%", va="center", ha="center", fontsize=9, fontweight="bold", color="white")
        ax.set_yticks(x)
        ax.set_yticklabels([c.split("\n")[0] for c in cluster_order], fontsize=10)
        ax.set_xlabel("Porsi Pengguna (%)")
        ax.set_title("Siapa Saja yang Bersepeda di Tiap Jamnya?", fontsize=11, fontweight="bold")
        ax.set_xlim(0, 100)
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=0.3)
        ax.legend(fontsize=9, loc="lower right")
        fig.tight_layout()
        st.pyplot(fig); plt.close(fig)

    peak_seg        = cluster_order[agg["rata_rata"].argmax()].replace("\n", " ")
    quiet_seg       = cluster_order[agg["rata_rata"].argmin()].replace("\n", " ")
    most_casual_seg = cluster_order[pct_casual.argmax()].replace("\n", " ")
    
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        insight("🔴", "Jam Tersibuk",
                f"Jam <b>{peak_seg}</b> sangat padat. Biasanya ini adalah orang-orang kantoran  yang pakai sepeda untuk berangkat atau pulang kerja.", color="orange")
    with ic2:
        insight("🟢", "Jam Paling Sepi",
                f"Di <b>{quiet_seg}</b> jalanan sangat sepi penyewa. Tentu saja, karena mayoritas orang masih tidur/beristirahat.", color="green")
    with ic3:
        insight("🚶", "Favorit Jalan-Jalan",
                f"Jam <b>{most_casual_seg}</b> paling disukai oleh penyewa biasa . Biasanya mereka menyewa untuk jalan-jalan santai.")

st.markdown("---")

# Suhu & Hari Libur 
st.subheader("🌡️ Dampak Suhu Udara & Jadwal Hari Libur")
c7, c8 = st.columns(2)

with c7:
    temp_data = day_f.copy()
    if not temp_data.empty:
        temp_data["temp_c"]    = temp_data["temp"] * 41
        temp_data["month_num"] = temp_data["dteday"].dt.month
        temp_bins   = [0, 10, 20, 25, 32, 42]
        temp_labels = ["❄️ Dingin Sekali\n(0-10°C)", "🌬️ Dingin\n(10-20°C)",
                       "🌤️ Sejuk\n(20-25°C)",        "☀️ Hangat\n(25-32°C)",
                       "🔥 Panas\n(32+°C)"]
        BIN_COLORS = ["#4C9BE8", "#74B8F0", "#6ECB8A", "#F9C846", "#F4845F"]

        temp_data["temp_bin"] = pd.cut(temp_data["temp_c"], bins=temp_bins, labels=temp_labels, right=False)
        bin_avg   = temp_data.groupby("temp_bin", observed=True)["cnt"].mean().reindex(temp_labels).fillna(0)
        
        fig, ax = plt.subplots(figsize=(6, 4.5))
        bars = ax.bar(range(len(temp_labels)), bin_avg.values, color=BIN_COLORS, edgecolor="white", width=0.68)
        ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=10, fontweight="bold")
        ax.set_xticks(range(len(temp_labels)))
        ax.set_xticklabels([l.split("\n")[0] for l in temp_labels], fontsize=9, rotation=15, ha="right")
        ax.set_ylabel("Rata-rata Disewa per Hari")
        ax.set_title("Rata-rata Sewa Berdasarkan Suhu", fontsize=11, fontweight="bold")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig); plt.close(fig)

        peak_bin = bin_avg.idxmax().replace("\n", " ")
        low_bin  = bin_avg.idxmin().replace("\n", " ")
        peak_val = int(bin_avg.max())
        low_val  = int(bin_avg.min())
        insight("📌", "Poin Penting",
                f"Suhu yang pas buat gowes ada di kisaran <b>{peak_bin}</b> (rata-rata <b>{peak_val:,} sewaan/hari</b>). "
                f"Kalau udaranya <b>{low_bin}</b>, penyewaan langsung anjlok jadi <b>{low_val:,}/hari</b>.")

with c8:
    if not day_f.empty:
        wday = day_f.groupby("workingday", observed=True)[["casual", "registered"]].mean()
        if len(wday) == 2:
            wday.index = ["Hari Libur", "Hari Kerja"]
        fig, ax = plt.subplots(figsize=(6, 4.5))
        wday.plot(kind="bar", ax=ax, color=[PAL[1], PAL[0]], edgecolor="white", rot=0)
        for container in ax.containers:
            ax.bar_label(container, fmt="%.0f", padding=3, fontsize=10, fontweight="bold")
        ax.set_ylabel("Rata-rata Disewa per Hari")
        ax.set_title("Beda Pola: Hari Kerja vs Hari Libur", fontsize=11, fontweight="bold")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax.legend(["Penyewa Biasa", "Member Terdaftar"], fontsize=9)
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig); plt.close(fig)

        cas_libur = int(wday.loc["Hari Libur", "casual"]) if "Hari Libur" in wday.index else 0
        cas_kerja = int(wday.loc["Hari Kerja",  "casual"]) if "Hari Kerja" in wday.index else 0
        reg_kerja = int(wday.loc["Hari Kerja",  "registered"]) if "Hari Kerja" in wday.index else 0
        insight("📌", "Poin Penting",
                f"Di <b>Hari Kerja</b>, sepeda penuh dipakai oleh para member (<b>{reg_kerja:,}/hari</b>) buat pergi bekerja. "
                f"Tapi pas <b>Hari Libur</b>, penyewa biasa yang cuma jalan-jalan santai jumlahnya naik drastis (jadi <b>{cas_libur:,} orang/hari</b>).",
                color="orange")

st.markdown("---")

#  Data Tabel Mentah 
with st.expander("📋 Lihat Data Tabel (day.csv)"):
    st.dataframe(day_f.head(200), use_container_width=True)

st.caption("Dashboard Bike Sharing Dataset By: Muhammad Geralldo A.S")