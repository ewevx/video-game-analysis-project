import streamlit as st
import pandas as pd
import plotly.express as px
import scipy.stats as stats

# -------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------------------------
st.set_page_config(
    page_title="Análise do Mercado de Jogos Digitais",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    
    df = df.dropna(subset=['name', 'genre'])
    
    return df

df = carregar_dados()

# -------------------------------------------------
# SIDEBAR - FILTROS
# -------------------------------------------------
st.sidebar.title("Filtros")

ano_min = int(df['year_of_release'].min())
ano_max = int(df['year_of_release'].max())

intervalo_anos = st.sidebar.slider(
    "Selecione o período:",
    ano_min,
    ano_max,
    (2010, 2016)
)

df_filtrado = df[
    (df['year_of_release'] >= intervalo_anos[0]) &
    (df['year_of_release'] <= intervalo_anos[1])
]

# -------------------------------------------------
# TÍTULO PRINCIPAL
# -------------------------------------------------
st.title("🎮 Análise do Mercado Global de Jogos Digitais")

st.markdown("""
Este projeto apresenta uma análise exploratória do mercado global de jogos digitais,
com foco na evolução temporal, desempenho por plataforma e diferenças estatísticas
entre grupos.
""")

st.divider()

# -------------------------------------------------
# MÉTRICAS PRINCIPAIS
# -------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total de Jogos", len(df_filtrado))
col2.metric("Vendas Totais (milhões)", round(df_filtrado['total_sales'].sum(), 2))
col3.metric("Número de Plataformas", df_filtrado['platform'].nunique())

st.divider()

# -------------------------------------------------
# ABAS
# -------------------------------------------------
aba1, aba2, aba3 = st.tabs([
    "📈 Evolução do Mercado",
    "🎮 Análise por Plataforma",
    "🧪 Testes de Hipótese"
])

# -------------------------------------------------
# ABA 1 - EVOLUÇÃO DO MERCADO
# -------------------------------------------------
with aba1:
    jogos_por_ano = (
        df_filtrado.groupby('year_of_release')['name']
        .count()
        .reset_index()
    )

    fig1 = px.line(
        jogos_por_ano,
        x='year_of_release',
        y='name',
        markers=True,
        title="Quantidade de Jogos Lançados por Ano",
        labels={
            "year_of_release": "Ano de Lançamento",
            "name": "Quantidade de Jogos"
        }
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    **Interpretação:**  
    O gráfico evidencia ciclos de crescimento e retração no mercado,
    possivelmente relacionados ao lançamento de novas gerações de consoles
    e mudanças na demanda dos consumidores.
    """)

# -------------------------------------------------
# ABA 2 - ANÁLISE POR PLATAFORMA
# -------------------------------------------------
with aba2:
    plataforma = st.selectbox(
        "Selecione a plataforma:",
        df_filtrado['platform'].unique()
    )

    df_plataforma = df_filtrado[df_filtrado['platform'] == plataforma]

    col1, col2 = st.columns(2)

    with col1:
        vendas_genero = (
            df_plataforma.groupby('genre')['total_sales']
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig2 = px.bar(
            vendas_genero,
            x='genre',
            y='total_sales',
            title=f"Vendas por Gênero - {plataforma}",
            labels={
                "genre": "Gênero",
                "total_sales": "Vendas Totais (milhões)"
            }
        )

        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        fig3 = px.scatter(
            df_plataforma,
            x="critic_score",
            y="total_sales",
            trendline="ols",
            title="Relação entre Nota da Crítica e Vendas",
            labels={
                "critic_score": "Nota da Crítica",
                "total_sales": "Vendas Totais (milhões)"
            }
        )

        st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------
# ABA 3 - TESTES DE HIPÓTESE
# -------------------------------------------------
with aba3:
    st.subheader("Comparação de Nota dos Usuários: Xbox One vs PC")

    xbox = df_filtrado[df_filtrado['platform'] == 'XOne']['user_score'].dropna()
    pc = df_filtrado[df_filtrado['platform'] == 'PC']['user_score'].dropna()

    t_stat, p_val = stats.ttest_ind(xbox, pc, equal_var=False)

    st.write(f"Estatística t: {round(t_stat, 2)}")
    st.write(f"Valor-p: {round(p_val, 4)}")

    if p_val < 0.05:
        st.success("Existe diferença estatisticamente significativa entre as médias.")
    else:
        st.info("Não há evidência suficiente para afirmar diferença significativa.")

    st.markdown("""
    **Interpretação Estatística:**  
    Considerando um nível de significância de 5%, avaliamos se as médias das
    notas atribuídas pelos usuários diferem entre as plataformas Xbox One e PC.
    """)