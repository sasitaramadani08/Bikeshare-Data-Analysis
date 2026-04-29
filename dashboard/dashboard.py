import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# PAGE CONFIG & GLOBAL THEME
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide", page_icon="🚲")

# Custom CSS untuk mempercantik dashboard
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #e8f4f8 0%, #d1e9f5 100%);
    } 
    
    /* Card styling */
    .custom-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(33, 147, 176, 0.2);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    .custom-card:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 4px solid #2193b0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .metric-title {
        color: #6c757d;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        color: #2c3e50;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    h2, h3, h4 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0f9ff 100%);
        border-right: 1px solid rgba(33, 147, 176, 0.2);
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: rgba(33, 147, 176, 0.1);
        border-radius: 12px;
        padding: 0.5rem;
    }
    .stRadio label {
        color: #2c3e50 !important;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px !important;
        border-left: 3px solid #2193b0 !important;
        color: #2c3e50 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(33, 147, 176, 0.2);
        margin: 1.5rem 0;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        color: #2193b0 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6c757d !important;
    }
    
    /* Text umum */
    p, li, span {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# Set seaborn style
sns.set_style("whitegrid")
sns.set_palette("Blues_d")

COLORS = {
    'primary': '#2193b0',
    'secondary': '#6dd5ed',
    'tertiary': '#2c3e50',
    'accent': '#3498db',
    'warning': '#f39c12',
    'success': '#27ae60',
    'light_bg': '#f0f9ff'
}

# LOAD DATA
@st.cache_data
def load_data():
    day_df = pd.read_csv("main_data_day.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    hour_df = pd.read_csv("main_data_hour.csv")
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

day_df, hour_df = load_data()

# SIDEBAR
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <img src="https://www.yellowjersey.co.uk/wp-content/uploads/2023/04/ebike-illustration-462x600.png" width="80" style="margin-bottom: 0.5rem;">
            <h2 style="color: #2193b0; margin: 0;">BikeShare</h2>
            <p style="color: #6c757d; font-size: 0.8rem;">Analytics Dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio(
        label="Navigation",
        options=["📊 Overview", "🔬 Advanced Analytics"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("<p style='color: #6c757d; font-size: 0.75rem; margin-bottom: 0.5rem;'>📅 FILTER YEAR</p>", unsafe_allow_html=True)
    selected_year = st.multiselect(
        label="Select Year",
        options=[2011, 2012],
        default=[2011, 2012],
        label_visibility="collapsed"
    )

# Filter data
main_day_df = day_df[day_df['yr'].isin(selected_year)]
main_hour_df = hour_df[hour_df['yr'].isin(selected_year)]


# OVERVIEW PAGE
if menu == "📊 Overview":
    st.markdown("<h1>Bike Sharing Overview</h1>", unsafe_allow_html=True)
    
    if main_day_df.empty:
        st.warning("⚠️ Please select at least one year from the sidebar.")
    else:
        total_cnt = main_day_df.cnt.sum()
        total_reg = main_day_df.registered.sum()
        total_cas = main_day_df.casual.sum()

        # Metric Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div>
                        <div class="metric-title">Total Rentals</div>
                        <div class="metric-value">{total_cnt:,}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div>
                        <div class="metric-title">Registered Users</div>
                        <div class="metric-value">{total_reg:,}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div>
                        <div class="metric-title">Casual Users</div>
                        <div class="metric-value">{total_cas:,}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Chart 1: Hourly Trend
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top: 0;'>Hourly Rental Pattern</h3>", unsafe_allow_html=True)
        
        hourly_data = main_hour_df.groupby('hr')['cnt'].mean().reset_index()
        
        fig_hr, ax_hr = plt.subplots(figsize=(12, 4))
        
        ax_hr.fill_between(hourly_data['hr'], hourly_data['cnt'], alpha=0.3, color=COLORS['primary'])
        ax_hr.plot(hourly_data['hr'], hourly_data['cnt'], marker='o', color=COLORS['accent'], linewidth=2, markersize=6)
        ax_hr.set_xticks(range(0, 24))
        ax_hr.set_xlabel("Hour of Day", color='#6c757d')
        ax_hr.set_ylabel("Average Rentals", color='#6c757d')
        ax_hr.tick_params(colors='#6c757d')
        ax_hr.set_facecolor('white')
        fig_hr.patch.set_facecolor('white')
        st.pyplot(fig_hr)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("💡 **Insight:** Dua puncak penyewaan terjadi jam 08.00 dan 17.00, mengindikasikan pola khas aktivitas komuter. Permintaan terendah jam 00.00-05.00 (rata-rata hanya 32 penyewa).")

        # Chart 2: Monthly Trend dan Composition
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0;'>Monthly Performance</h3>", unsafe_allow_html=True)
            
            df_monthly = main_day_df.copy()
            df_monthly['month'] = df_monthly['dteday'].dt.strftime('%B')
            
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
           
            monthly_agg = df_monthly.groupby(['month', 'yr'])['cnt'].sum().reset_index()
            monthly_agg['month'] = pd.Categorical(monthly_agg['month'], categories=month_order, ordered=True)
            monthly_agg = monthly_agg.sort_values('month')
            
            fig_mon, ax_mon = plt.subplots(figsize=(10, 5))
            
            for i, yr in enumerate([2011, 2012]):
                data_yr = monthly_agg[monthly_agg['yr'] == yr]
                color = COLORS['primary'] if i == 0 else COLORS['accent']
                ax_mon.plot(data_yr['month'], data_yr['cnt'], marker='o', linewidth=2, label=f'{yr}', markersize=5, color=color)
            
            ax_mon.tick_params(axis='x', rotation=45, colors='#6c757d')
            ax_mon.tick_params(axis='y', colors='#6c757d')
            ax_mon.set_facecolor('white')
            ax_mon.legend(facecolor='white', labelcolor='#2c3e50')
            fig_mon.patch.set_facecolor('white')
            st.pyplot(fig_mon)
            st.markdown("</div>", unsafe_allow_html=True)

            #Insight montly trend
            st.caption("💡 **Insight:** Permintaan tertinggi di bulan Juni-September (musim panas), terendah di Januari-Februari (musim dingin). Terjadi peningkatan signifikan dari tahun 2011 ke 2012.")

        with col_right:
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0;'>User Composition</h3>", unsafe_allow_html=True)
            
            color_reg = '#48CAE4'
            color_cas = '#F72585'

            fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
            
            wedges, texts, autotexts = ax_pie.pie (
                [total_reg, total_cas], 
                labels=['Registered', 'Casual'], 
                autopct='%1.1f%%', 
                colors=[color_reg, color_cas], 
                startangle=140,
                pctdistance=0.85,
                explode=[0.05,0],
                wedgeprops={'edgecolor': 'white', 'linewidth': 3,'antialiased': True}
            )

            centre_circle = plt.Circle((0,0), 0.70, fc='white')
            fig_pie.gca().add_artist(centre_circle)

            plt.setp(autotexts, size=12, weight="bold", color="#555555")
            plt.setp(texts, size=12, weight="bold", color="#333333")

            fig_pie.patch.set_facecolor('none')
            
            st.pyplot(fig_pie)
            st.markdown("</div>", unsafe_allow_html=True)

            #Insight composition
            st.caption("💡 **Insight:** Pengguna registered mendominasi total penyewaan.")

        # Performance Insights
        st.markdown("<br>", unsafe_allow_html=True)
        col_ins1, col_ins2 = st.columns(2)
        
        with col_ins1:
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0;'>Peak Performance</h3>", unsafe_allow_html=True)
            
            peak_h = hourly_data.loc[hourly_data['cnt'].idxmax(), 'hr']
            main_day_df['day_name'] = main_day_df['dteday'].dt.day_name()
            peak_d = main_day_df.groupby('day_name')['cnt'].sum().idxmax()
            df_monthly_peak = main_day_df.copy()
            df_monthly_peak['month_name'] = df_monthly_peak['dteday'].dt.strftime('%B')
            peak_m = df_monthly_peak.groupby('month_name')['cnt'].sum().idxmax()
            user_type = "Registered" if total_reg > total_cas else "Casual"
            
            col_peak1, col_peak2 = st.columns(2)
            with col_peak1:
                st.metric("Peak Hour", f"{peak_h}:00")
                st.metric("Busiest Day", peak_d)
            with col_peak2:
                st.metric("Best Month", peak_m)
                st.metric("Dominant User", user_type)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_ins2:
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0;'>Key Insights</h3>", unsafe_allow_html=True)
            st.markdown(f"""
                <ul style="color: #2c3e50; margin: 0; padding-left: 1.2rem;">
                    <li>Jam sibuk terjadi di pagi jam 08.00 dan sore jam 17.00</li>
                    <li><strong style="color: {COLORS['primary']};">{user_type}</strong> mendominasi platform</li>
                    <li>Performa tertinggi terjadi di <strong style="color: {COLORS['primary']};">{peak_m}</strong></li>
                    <li>Pola penyewaan hari kerja berbeda signifikan dengan akhir pekan</li>
                </ul>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


#ADVANCED ANALYTICS PAGE
elif menu == "🔬 Advanced Analytics":
    st.markdown("<h1>Environmental & Mobility Analysis</h1>", unsafe_allow_html=True)

    # Part 1: Environmental Factors
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>🌍 Environmental Factors</h3>", unsafe_allow_html=True)
    
    col_env1, col_env2 = st.columns(2)

    with col_env1:
        st.markdown("<h4>Seasonal Trends</h4>", unsafe_allow_html=True)
        season_df = main_day_df.groupby('season')['cnt'].mean().sort_values(ascending=False).reset_index()
        
        fig_sea, ax_sea = plt.subplots(figsize=(8, 5))
        
        # Warna berbeda untuk setiap musim
        warna_musim = {
            'Summer': '#FF6B6B',      # Merah terang (panas)
            'Fall': '#FFA500',        # Oranye (gugur)
            'Spring': '#4CAF50',       # Hijau (semi)
            'Winter': '#2193B0'        # Biru dingin (dingin)
        }
        colors_bar = [warna_musim[musim] for musim in season_df['season']]
        
        bars = ax_sea.bar(season_df['season'], season_df['cnt'], color=colors_bar, edgecolor='white', linewidth=1.5)
    
        for bar in bars:
            height = bar.get_height()
            ax_sea.annotate(f'{int(height):,}', 
                        xy=(bar.get_x() + bar.get_width()/2, height),ha='center', va='bottom', color='#2c3e50', fontsize=10, fontweight='bold')
        
        ax_sea.tick_params(colors='#6c757d')
        ax_sea.set_facecolor('white')
        ax_sea.set_ylabel("Rata-rata Penyewaan", color='#6c757d')
        fig_sea.patch.set_facecolor('white')
        st.pyplot(fig_sea)

    with col_env2:
        st.markdown("<h4>Weather Impact</h4>", unsafe_allow_html=True)
    
        weather_df = main_day_df.groupby('weathersit')['cnt'].mean().sort_values(ascending=True).reset_index()
    
        fig_wea, ax_wea = plt.subplots(figsize=(8, 5))
    
        warna_cuaca = {
            'Light Rain': '#FFA07A',
            'Cloudy': '#D3D3D3', 
            'Clear': '#72BCD4'
        }
        colors_bar = [warna_cuaca[cuaca] for cuaca in weather_df['weathersit']]
        
        bars = ax_wea.barh(weather_df['weathersit'], weather_df['cnt'], color=colors_bar, edgecolor=COLORS['primary'])
        
        for bar in bars:
            width = bar.get_width()
            ax_wea.annotate(f'{int(width):,}', xy=(width, bar.get_y() + bar.get_height()/2),ha='left', va='center', color='#2c3e50', fontsize=10)
        
        ax_wea.tick_params(colors='#6c757d')
        ax_wea.set_facecolor('white')
        ax_wea.set_xlabel("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca", color='#6c757d')
        fig_wea.patch.set_facecolor('white')
        st.pyplot(fig_wea)

    # Insight Environmental
    st.info("💡 **Key Insight:** Permintaan tertinggi terjadi di **Musim Panas (Summer)** dan terendah di **Musim Dingin (Winter)**.")  
    st.info("📌 **Strategi:** Alokasikan lebih banyak sepeda saat musim panas. Gunakan musim dingin untuk perawatan armada besar-besaran.")

    # Part 2: Rain Impact Analysis
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>🌧️ Dampak Hujan: Hari Kerja vs Akhir Pekan per Musim</h3>", unsafe_allow_html=True)

    rainy_data = main_day_df[main_day_df['weathersit'] == 'Light Rain'].copy()

    if not rainy_data.empty:
        season_order = ['Winter', 'Spring', 'Summer', 'Fall']
        rainy_data['season'] = pd.Categorical(rainy_data['season'], categories=season_order, ordered=True)
        
        # Barplot
        fig_rain, ax_rain = plt.subplots(figsize=(10, 6))
        x_pos = np.arange(len(season_order))
        width_bar = 0.35
        
        weekend_data = rainy_data[rainy_data['workingday'] == 'Weekend'].groupby('season')['cnt'].mean()
        working_data = rainy_data[rainy_data['workingday'] == 'Working day'].groupby('season')['cnt'].mean()
        
        ax_rain.bar(x_pos - width_bar/2, weekend_data.reindex(season_order).values, width_bar, label='Weekend', color='#FFA07A')
        ax_rain.bar(x_pos + width_bar/2, working_data.reindex(season_order).values, width_bar, label='Working day', color=COLORS['primary'])
        
        ax_rain.set_xticks(x_pos)
        ax_rain.set_xticklabels(season_order)
        ax_rain.set_ylabel("Rata-rata Penyewaan Sepeda Saat Light Rain Per Musim", color='#6c757d')
        ax_rain.set_xlabel("Musim", color='#6c757d')
        ax_rain.legend()
        ax_rain.set_facecolor('white')
        fig_rain.patch.set_facecolor('white')
        st.pyplot(fig_rain)
        
        #Insight Rain impact
        tahun_terpilih = ", ".join([str(t) for t in selected_year]) if selected_year else "Semua Tahun"
        
        avg_weekend_rain = weekend_data.mean()
        avg_working_rain = working_data.mean()
        
        gap_dict = {}
        for season in season_order:
            wd_val = weekend_data.get(season, 0)
            wk_val = working_data.get(season, 0)
            gap_dict[season] = abs(wd_val - wk_val) if not np.isnan(wd_val) and not np.isnan(wk_val) else 0
        
        most_extreme_season = max(gap_dict, key=gap_dict.get) if gap_dict else "Fall"
        weekend_extreme = int(weekend_data.get(most_extreme_season, 0))
        working_extreme = int(working_data.get(most_extreme_season, 0))
        
        if weekend_extreme > working_extreme:
            higher_type = "Akhir pekan"
            higher_val = weekend_extreme
            lower_val = working_extreme
        else:
            higher_type = "Hari kerja"
            higher_val = working_extreme
            lower_val = weekend_extreme
        
        st.info(f"""
        💡 **Insight untuk tahun {tahun_terpilih}:** Saat hujan ringan, pola permintaan sangat bervariasi per musim.
        
        📊 **Rata-rata saat hujan:**
        - **Akhir pekan:** {int(avg_weekend_rain):,} penyewa/hari
        - **Hari kerja:** {int(avg_working_rain):,} penyewa/hari
        
        🔍 **Musim dengan perbedaan terbesar:** **{most_extreme_season}**
        - {higher_type}: {higher_val:,} penyewa/hari
        - {'Akhir pekan' if higher_type == 'Hari kerja' else 'Hari kerja'}: {lower_val:,} penyewa/hari
        - Perbedaan: **{abs(weekend_extreme - working_extreme):,} penyewa**
        
        → **Strategi:** 
        - Di **{most_extreme_season}**, fokus distribusi ke area yang sesuai dengan tipe hari yang lebih tinggi.
        - Gunakan promosi untuk menstabilkan permintaan di musim dengan gap besar.
        """)
    else:
        st.warning("No data available for \"Light Rain\" condition with selected filters.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Part 3: Mobility Pattern Analysis
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>🚶 Mobility Pattern Analysis</h3>", unsafe_allow_html=True)
    
    def mobility_segment(hr):
        if 7 <= hr <= 9:
            return '🌅 Morning Rush'
        elif 16 <= hr <= 19:
            return '🌆 Evening Rush'
        elif 10 <= hr <= 15:
            return '💼 Business Hours'
        elif 20 <= hr <= 23:
            return '🌙 Night Leisure'
        else:
            return '😴 Deep Rest'
    
    main_hour_df['mobility_type'] = main_hour_df['hr'].apply(mobility_segment)
    segment_order = ['😴 Deep Rest', '🌅 Morning Rush', '💼 Business Hours', '🌆 Evening Rush', '🌙 Night Leisure']
    
    if not main_hour_df.empty:
        mobility_avg = main_hour_df.groupby('mobility_type', as_index=False)['cnt'].mean()
        mobility_avg['mobility_type'] = pd.Categorical(mobility_avg['mobility_type'], categories=segment_order, ordered=True)
        mobility_avg = mobility_avg.sort_values('mobility_type')
        
        fig_mob, ax_mob = plt.subplots(figsize=(10, 5))
        
        colors_bar = [
             '#A8D8EA',
             '#4A90E2',
             '#2193B0',
             '#0D6B7C',
             '#FF8C42' 
        ]
        
        bars = ax_mob.barh(mobility_avg['mobility_type'], mobility_avg['cnt'], color=colors_bar)
        for bar, val in zip(bars, mobility_avg['cnt']):
            ax_mob.annotate(f'{int(val):,}', xy=(val, bar.get_y() + bar.get_height()/2),ha='left', va='center', color='#2c3e50', fontsize=11)
        
        ax_mob.tick_params(colors='#6c757d')
        ax_mob.set_xlabel("Average Rentals", color='#6c757d')
        ax_mob.set_facecolor('white')
        fig_mob.patch.set_facecolor('white')
        st.pyplot(fig_mob)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Insight Mobility pettern
    st.info("""
    💡 **Insight:** Segmen **Evening Rush (jam 16-19)** memiliki permintaan tertinggi, sedangkan **Deep Rest (jam 00-06)** adalah waktu terendah penyewaan.
    """)

    st.success("""
    📌 **Strategi:** 
               
    • **Sebelum jam 16.00:** Pindahkan sepeda ke area perkantoran untuk mengantisipasi lonjakan Evening Rush.
               
    • **Jam Deep Rest (00-06):** Lakukan perawatan armada & redistribusi sepeda tanpa mengganggu pengguna.
               
    • **Morning Rush (07-09):** Pastikan area pemukiman terisi penuh sebelum jam 07.00.
    """)    
    
    # Part 4: Working Day vs Weekend Pattern
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>📈 Working Day vs Weekend Pattern</h3>", unsafe_allow_html=True)
    
    # Definisi warna baru yang lebih kontras
    COLOR_WORKING = '#2E86C1' 
    COLOR_WEEKEND = '#E67E22' 
    COLOR_EVENING = '#FDE66D'
    COLOR_MORNING = '#FF92BB'

    hourly_weekday = main_hour_df[main_hour_df['workingday'] == 'Working day'].groupby('hr')['cnt'].mean()
    hourly_weekend = main_hour_df[main_hour_df['workingday'] == 'Weekend'].groupby('hr')['cnt'].mean()

    fig_compare, ax_compare = plt.subplots(figsize=(14, 5))
    ax_compare.fill_between(hourly_weekday.index, hourly_weekday.values, alpha=0.2, color=COLOR_WORKING)
    ax_compare.fill_between(hourly_weekend.index, hourly_weekend.values, alpha=0.2, color=COLOR_WEEKEND)
    
    ax_compare.plot(hourly_weekday.index, hourly_weekday.values, marker='o', linewidth=2, 
                    label='Working Day', color=COLOR_WORKING, markersize=5)
    ax_compare.plot(hourly_weekend.index, hourly_weekend.values, marker='s', linewidth=2, 
                    label='Weekend', color=COLOR_WEEKEND, markersize=5)
    
    ax_compare.axvspan(7, 9, alpha=0.15, color=COLOR_MORNING, label='Morning Rush')
    ax_compare.axvspan(16, 19, alpha=0.15, color=COLOR_EVENING, label='Evening Rush')
    
    ax_compare.set_xlabel("Hour (0-23)", color='#6c757d', fontsize=12)
    ax_compare.set_ylabel("Average Rentals", color='#6c757d', fontsize=12)
    ax_compare.set_xticks(range(0, 24))
    ax_compare.tick_params(colors='#6c757d')
    ax_compare.set_facecolor('white')
    
    ax_compare.legend(facecolor='white', labelcolor='#2c3e50', loc='upper right')
    fig_compare.patch.set_facecolor('white')
    st.pyplot(fig_compare)
    
    st.markdown("</div>", unsafe_allow_html=True)

    #Insight Perbandingan working day vs weekend 
    st.info("""
    💡 **Insight:** 
    • **Hari kerja:** Membentuk **dua puncak tajam** di jam 08.00 (pagi) dan jam 17.00 (sore), ini mengindikasikan bahwa aktivitas komuter mendominasi.
    
    • **Akhir pekan:** Membentuk **satu puncak landai** di siang hari (jam 12.00-15.00), ini mengindikasikan aktivitas rekreasi mendominasi.
    """)

    st.success("""
    📌 **Strategi Redistribusi:** 

    • **Sebelum jam 07.00 (hari kerja):** Pindahkan sepeda ke area pemukiman.
    
    • **Sebelum jam 16.00 (hari kerja):** Pindahkan sepeda ke area perkantoran.
    
    • **Akhir pekan (pagi hari):** Pindahkan armada ke area wisata/taman.
    """)
    
    # Part 5: Casual vs Registered Hourly Pattern
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>👥 Casual vs Registered Hourly Pattern</h3>", unsafe_allow_html=True)

    hourly_user = main_hour_df.groupby('hr').agg({
        'casual': 'mean',
        'registered': 'mean'
    }).reset_index()

    fig_user, ax_user = plt.subplots(figsize=(14, 6))
    x = np.arange(len(hourly_user['hr']))
    width = 0.35

    ax_user.bar(x - width/2, hourly_user['registered'], width, label='Registered', color=COLORS['primary'], alpha=0.8)
    ax_user.bar(x + width/2, hourly_user['casual'], width, label='Casual', color='#FFA07A', alpha=0.8)

    ax_user.set_xlabel("Hour of Day", color='#6c757d')
    ax_user.set_ylabel("Average Rentals", color='#6c757d')
    ax_user.set_xticks(x)
    ax_user.set_xticklabels(hourly_user['hr'])
    ax_user.tick_params(colors='#6c757d')
    ax_user.legend(loc='upper right')
    ax_user.set_facecolor('white')
    fig_user.patch.set_facecolor('white')
    st.pyplot(fig_user)

    st.markdown("</div>", unsafe_allow_html=True)

    #Insight Casual vs Registered pettern
    st.info("""
    💡 **Insight:** Pengguna **registered** mendominasi jam sibuk pagi (08.00) dan sore (17.00). Sedangkan pengguna **casual** paling aktif pada siang hari (14.00), terutama di akhir pekan.
    """)

    st.success("""
    📌 **Strategi:** 

    • **Registered (Hari kerja):** Program loyalitas & pastikan stasiun perkantoran terisi sebelum jam sibuk.
    
    • **Casual (Akhir pekan):** Alihkan armada ke area wisata & berikan promosi untuk pengguna baru.
    
    • **Jam non-sibuk:** Manfaatkan untuk maintenance ringan & redistribusi stok.
    """)

    # Part 6: Rekomendasi Strategi
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>💡 Rekomendasi Strategi</h3>", unsafe_allow_html=True)

    col_rec1, col_rec2 = st.columns(2)

    with col_rec1:
        st.markdown("""
            <h4>🌤️ Berdasarkan Musim & Cuaca</h4>
            <ul style='color: #2c3e50;'>
                <li><strong>Musim Panas:</strong> Tingkatkan stok sepeda 2x lipat, ini waktu paling menguntungkan</li>
                <li><strong>Musim Dingin:</strong> Alihkan fokus ke perawatan armada, kurangi operasional</li>
                <li><strong>Saat hujan di hari kerja:</strong> Jaga stasiun perkantoran agar pengguna registered tetap menyewa</li>
                <li><strong>Saat hujan di akhir pekan:</strong> Berikan promo/diskon untuk menarik pengguna casual</li>
            </ul>
        """, unsafe_allow_html=True)

    with col_rec2:
        st.markdown("""
            <h4>⏰ Berdasarkan Waktu</h4>
            <ul style='color: #2c3e50;'>
                <li><strong>Hari Kerja:</strong> Fokus pada jam 07.00-09.00 & 16.00-19.00 karena ini merupakan puncak permintaan</li>
                <li><strong>Sebelum jam 07.00:</strong> Pindahkan stok ke area pemukiman</li>
                <li><strong>Sebelum jam 16.00:</strong> Pindahkan stok ke area perkantoran</li>
                <li><strong>Akhir Pekan:</strong> Pindahkan armada ke area wisata siang hari (jam 12-15)</li>
                <li><strong>Jam 00-06 (Deep Rest):</strong> Waktu terbaik untuk perawatan & redistribusi</li>
            </ul>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


#FOOTER
st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-top: 2rem;">
        <p style="color: #6c757d; font-size: 0.7rem;">Bike Sharing Data Science Project | Dicoding 2026</p>
    </div>
""", unsafe_allow_html=True)