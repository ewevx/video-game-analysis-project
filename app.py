import streamlit as st
import pandas as pd
import plotly.express as px
import scipy.stats as stats

st.set_page_config(page_title="Análise de Mercado de Games", layout="wide")

# ==========================
# CARREGAMENTO DOS DADOS
# ==========================

@st.cache_data
def load_data():
    df = pd.read_csv("games.csv")
    df.columns = df.columns.str.lower()
    df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')
    df['year_of_release'] = df['year_of_release'].fillna(df['year_of_release'].median())
    df = df.dropna(subset=['name', 'genre'])
    
    df['total_sales'] = (
        df['na_sales'] +
        df['eu_sales'] +
        df['jp_sales'] +
        df['other_sales']
    )
    
    return df

games_data = load_data()

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("Navegação")
page = st.sidebar.radio(
    "Ir para:",
    [
        "Visão Geral",
        "Evolução do Mercado",
        "Análise por Plataforma",
        "Análise Regional",
        "Testes de Hipótese"
    ]
)

# ==========================
# PÁGINA 1
# ==========================

if page == "Visão Geral":
    st.title("Análise do Mercado de Jogos Digitais")
    
    st.markdown("""
    Projeto de análise exploratória com foco em:
    - Evolução do mercado
    - Performance por plataforma
    - Diferenças regionais
    - Testes estatísticos de hipóteses
    """)

    st.metric("Total de Jogos", len(games_data))
    st.metric("Período Analisado",
              f"{int(games_data['year_of_release'].min())} - {int(games_data['year_of_release'].max())}")

# ==========================
# PÁGINA 2
# ==========================

elif page == "Evolução do Mercado":
    st.title("Evolução do Mercado ao Longo do Tempo")

    games_per_year = games_data.groupby('year_of_release')['name'].count().reset_index()

    fig = px.line(
        games_per_year,
        x="year_of_release",
        y="name",
        title="Quantidade de Jogos Lançados por Ano"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================
# PÁGINA 3
# ==========================

elif page == "Análise por Plataforma":
    st.title("Análise por Plataforma")

    platform = st.selectbox(
        "Selecione a plataforma:",
        games_data['platform'].unique()
    )

    platform_data = games_data[games_data['platform'] == platform]

    st.metric("Vendas Totais (milhões)",
              round(platform_data['total_sales'].sum(), 2))

    fig = px.scatter(
        platform_data,
        x="critic_score",
        y="total_sales",
        title=f"Correlação entre Critic Score e Vendas - {platform}"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================
# PÁGINA 4
# ==========================

elif page == "Análise Regional":
    st.title("Análise Regional de Vendas")

    region = st.selectbox(
        "Selecione a região:",
        ["na_sales", "eu_sales", "jp_sales"]
    )

    sales_by_genre = games_data.groupby('genre')[region].sum().sort_values(ascending=False)

    fig = px.bar(
        x=sales_by_genre.index,
        y=sales_by_genre.values,
        title=f"Vendas por Gênero - {region.upper()}"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================
# PÁGINA 5
# ==========================

elif page == "Testes de Hipótese":
    st.title("Testes Estatísticos")

    st.subheader("Xbox One vs PC - User Score")

    xbox_score = games_data[games_data['platform'] == 'XOne']['user_score'].dropna()
    pc_score = games_data[games_data['platform'] == 'PC']['user_score'].dropna()

    t_stat, p_val = stats.ttest_ind(xbox_score, pc_score, equal_var=False)

    st.write(f"T-statistic: {round(t_stat, 2)}")
    st.write(f"P-value: {round(p_val, 4)}")

    if p_val < 0.05:
        st.success("Há diferença estatisticamente significativa.")
    else:
        st.info("Não há evidência suficiente para diferença significativa.")

    st.subheader("Action vs Sports - User Score")

    action = games_data[games_data['genre'] == 'Action']['user_score'].dropna()
    sports = games_data[games_data['genre'] == 'Sports']['user_score'].dropna()

    t_stat_g, p_val_g = stats.ttest_ind(action, sports, equal_var=False)

    st.write(f"T-statistic: {round(t_stat_g, 2)}")
    st.write(f"P-value: {round(p_val_g, 4)}")

    if p_val_g < 0.05:
        st.success("Há diferença estatisticamente significativa.")
    else:
        st.info("Não há evidência suficiente para diferença significativa.")