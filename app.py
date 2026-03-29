import streamlit as st
import pandas as pd
import plotly.express as px
import scipy.stats as stats

# ------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ------------------------------------------------
st.set_page_config(
    page_title="Game Market Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# CARREGAMENTO DOS DADOS
# ------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("games.csv")
    df.columns = df.columns.str.lower()
    df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')
    df['total_sales'] = (
        df['na_sales'] +
        df['eu_sales'] +
        df['jp_sales'] +
        df['other_sales']
    )
    return df

df = load_data()

# ------------------------------------------------
# SIDEBAR - FILTROS GLOBAIS
# ------------------------------------------------
st.sidebar.title("Filtros")

year_range = st.sidebar.slider(
    "Selecione o período:",
    int(df['year_of_release'].min()),
    int(df['year_of_release'].max()),
    (2010, 2016)
)

filtered_df = df[
    (df['year_of_release'] >= year_range[0]) &
    (df['year_of_release'] <= year_range[1])
]

# ------------------------------------------------
# HEADER
# ------------------------------------------------
st.title("🎮 Video Game Market Analysis")
st.markdown(
    """
    Análise exploratória do mercado global de jogos digitais.
    O objetivo é identificar tendências, desempenho por plataforma
    e diferenças regionais.
    """
)

st.divider()

# ------------------------------------------------
# MÉTRICAS PRINCIPAIS
# ------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Games", len(filtered_df))
col2.metric("Total Sales (M)", round(filtered_df['total_sales'].sum(), 2))
col3.metric("Platforms", filtered_df['platform'].nunique())

st.divider()

# ------------------------------------------------
# TABS DE ANÁLISE
# ------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📈 Market Evolution",
    "🎮 Platform Analysis",
    "🧪 Hypothesis Testing"
])

# ------------------------------------------------
# TAB 1
# ------------------------------------------------
with tab1:
    games_per_year = (
        filtered_df.groupby('year_of_release')['name']
        .count()
        .reset_index()
    )

    fig = px.line(
        games_per_year,
        x='year_of_release',
        y='name',
        markers=True,
        title="Games Released per Year"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insight:**  
    Observe periods of growth and decline in game releases.
    This may reflect console cycles and market saturation.
    """)

# ------------------------------------------------
# TAB 2
# ------------------------------------------------
with tab2:
    platform = st.selectbox(
        "Select platform:",
        filtered_df['platform'].unique()
    )

    platform_df = filtered_df[filtered_df['platform'] == platform]

    col1, col2 = st.columns(2)

    with col1:
        fig_sales = px.bar(
            platform_df.groupby('genre')['total_sales']
            .sum()
            .sort_values(ascending=False),
            title=f"{platform} Sales by Genre"
        )
        st.plotly_chart(fig_sales, use_container_width=True)

    with col2:
        fig_corr = px.scatter(
            platform_df,
            x="critic_score",
            y="total_sales",
            title="Critic Score vs Sales",
            trendline="ols"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

# ------------------------------------------------
# TAB 3
# ------------------------------------------------
with tab3:
    st.subheader("Xbox One vs PC - User Score")

    xbox = filtered_df[filtered_df['platform'] == 'XOne']['user_score'].dropna()
    pc = filtered_df[filtered_df['platform'] == 'PC']['user_score'].dropna()

    t_stat, p_val = stats.ttest_ind(xbox, pc, equal_var=False)

    st.write(f"T-statistic: {round(t_stat, 2)}")
    st.write(f"P-value: {round(p_val, 4)}")

    if p_val < 0.05:
        st.success("Statistically significant difference detected.")
    else:
        st.info("No statistically significant difference detected.")

    st.markdown("""
    **Interpretation:**  
    The result indicates whether user perception differs significantly
    between platforms.
    """)