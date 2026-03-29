import streamlit as st
import pandas as pd
import plotly.express as px
import scipy.stats as stats

# -------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------------------------
st.set_page_config(
    page_title="Dashboard - Mercado de Jogos",
    layout="wide"
)

# -------------------------------------------------
# ESTILO VISUAL (POWER BI STYLE)
# -------------------------------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e6e6e6;
        box-shadow: 0px 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# CARREGAMENTO DOS DADOS
# -------------------------------------------------
@st.cache_data
def carregar_dados():
    df = pd.read_csv("games.csv")
    df.columns = df.columns.str.lower()

    df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')
    df['critic_score'] = pd.to_numeric(df['critic_score'], errors='coerce')

    df['total_sales'] = (
        df['na_sales'] +
        df['eu_sales'] +
        df['jp_sales'] +
        df['other_sales']
    )

    return df

df = carregar_dados()

# -------------------------------------------------
# SIDEBAR - FILTROS
# -------------------------------------------------
st.sidebar.title("Filtros do Dashboard")

ano_min = int(df['year_of_release'].min())
ano_max = int(df['year_of_release'].max())

intervalo = st.sidebar.slider(
    "Período de análise:",
    ano_min,
    ano_max,
    (2010, 2016)
)

plataformas = st.sidebar.multiselect(
    "Selecione plataformas:",
    df['platform'].unique(),
    default=df['platform'].unique()
)

df_filtrado = df[
    (df['year_of_release'] >= intervalo[0]) &
    (df['year_of_release'] <= intervalo[1]) &
    (df['platform'].isin(plataformas))
]

# -------------------------------------------------
# TÍTULO
# -------------------------------------------------
st.title("🎮 Dashboard Executivo — Mercado Global de Jogos Digitais")
st.caption("Análise estratégica de desempenho de mercado, plataformas e comportamento de vendas.")

st.divider()

# -------------------------------------------------
# KPIs PRINCIPAIS
# -------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de Jogos", f"{len(df_filtrado):,}")
col2.metric("Vendas Totais (Mi)", f"{df_filtrado['total_sales'].sum():,.2f}")
col3.metric("Plataformas Ativas", df_filtrado['platform'].nunique())
col4.metric("Média Nota Usuário", f"{df_filtrado['user_score'].mean():.2f}")

st.divider()

# -------------------------------------------------
# GRÁFICOS PRINCIPAIS
# -------------------------------------------------
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    vendas_ano = (
        df_filtrado.groupby('year_of_release')['total_sales']
        .sum()
        .reset_index()
    )

    fig1 = px.line(
        vendas_ano,
        x="year_of_release",
        y="total_sales",
        markers=True,
        title="Evolução das Vendas Globais",
        labels={
            "year_of_release": "Ano",
            "total_sales": "Vendas Totais (milhões)"
        }
    )

    fig1.update_layout(template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

with col_graf2:
    vendas_plataforma = (
        df_filtrado.groupby('platform')['total_sales']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig2 = px.bar(
        vendas_plataforma,
        x="platform",
        y="total_sales",
        title="Vendas Totais por Plataforma",
        labels={
            "platform": "Plataforma",
            "total_sales": "Vendas Totais (milhões)"
        }
    )

    fig2.update_layout(template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -------------------------------------------------
# ANÁLISE DETALHADA
# -------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    vendas_genero = (
        df_filtrado.groupby('genre')['total_sales']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig3 = px.bar(
        vendas_genero,
        x="genre",
        y="total_sales",
        title="Desempenho por Gênero",
        labels={
            "genre": "Gênero",
            "total_sales": "Vendas Totais (milhões)"
        }
    )

    fig3.update_layout(template="plotly_white")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.scatter(
        df_filtrado,
        x="critic_score",
        y="total_sales",
        trendline="ols",
        title="Relação entre Nota da Crítica e Vendas",
        labels={
            "critic_score": "Nota da Crítica",
            "total_sales": "Vendas Totais (milhões)"
        }
    )

    fig4.update_layout(template="plotly_white")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# -------------------------------------------------
# TESTE DE HIPÓTESE
# -------------------------------------------------
st.subheader("🧪 Teste Estatístico — Xbox One vs PC")

xbox = df_filtrado[df_filtrado['platform'] == 'XOne']['user_score'].dropna()
pc = df_filtrado[df_filtrado['platform'] == 'PC']['user_score'].dropna()

if len(xbox) > 0 and len(pc) > 0:
    t_stat, p_val = stats.ttest_ind(xbox, pc, equal_var=False)

    colA, colB = st.columns(2)

    colA.metric("Estatística t", f"{t_stat:.2f}")
    colB.metric("Valor-p", f"{p_val:.4f}")

    if p_val < 0.05:
        st.success("Há diferença estatisticamente significativa entre as médias.")
    else:
        st.info("Não há evidência suficiente para diferença significativa.")
else:
    st.warning("Dados insuficientes para realizar o teste no período selecionado.")

st.divider()

# -------------------------------------------------
# CONCLUSÃO EXECUTIVA
# -------------------------------------------------
st.markdown("""
### 📌 Conclusão Estratégica

O dashboard permite identificar:

- Tendências de crescimento ou retração do mercado
- Plataformas com maior participação em vendas
- Gêneros mais rentáveis
- Relação entre avaliação crítica e desempenho comercial

Essas informações podem orientar decisões estratégicas de investimento,
lançamento e posicionamento de produtos no mercado de jogos digitais.
""")