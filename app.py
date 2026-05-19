import streamlit as st
import pandas as pd
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Trade System",
    layout="wide"
)

# =========================================================
# CLEAN CSS
# =========================================================

st.markdown("""
<style>

/* Fundo geral */

.stApp {
    background-color: #f5f7fb;
}

/* Container */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 95%;
}

/* Títulos */

h1 {
    font-size: 42px !important;
    font-weight: 700 !important;
    color: #111827 !important;
    margin-bottom: 5px;
}

h2, h3 {
    color: #111827 !important;
    font-weight: 600 !important;
}

/* Subtitulo */

.stCaption {
    color: #6b7280 !important;
    font-size: 14px !important;
}

/* Cards */

div[data-testid="metric-container"] {

    background: white;

    border: 1px solid #e5e7eb;

    padding: 20px;

    border-radius: 14px;

    box-shadow:
        0 1px 3px rgba(0,0,0,0.04);

}

/* Label cards */

div[data-testid="metric-container"] label {

    color: #6b7280 !important;

    font-size: 13px !important;

    font-weight: 500 !important;

}

/* Valores cards */

div[data-testid="metric-container"] div {

    color: #111827 !important;

    font-size: 30px !important;

    font-weight: 700 !important;

}

/* Form */

[data-testid="stForm"] {

    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 14px;

    padding: 24px;

}

/* Inputs */

.stNumberInput input,
.stTextInput input {

    border-radius: 10px !important;

    border: 1px solid #d1d5db !important;

}

/* Select */

.stSelectbox div[data-baseweb="select"] {

    border-radius: 10px !important;

    border: 1px solid #d1d5db;

}

/* Botões */

.stButton button,
.stForm button {

    background: #111827 !important;

    color: white !important;

    border: none !important;

    border-radius: 10px !important;

    height: 44px;

    font-weight: 600 !important;

}

/* Tabela */

[data-testid="stDataFrame"] {

    border-radius: 14px;

    overflow: hidden;

    border: 1px solid #e5e7eb;

}

/* Sidebar */

section[data-testid="stSidebar"] {

    background: white;

}

/* Divider */

hr {

    border-color: #e5e7eb;

    margin-top: 2rem;

    margin-bottom: 2rem;

}

</style>
""", unsafe_allow_html=True)

# =========================================================
# CSV
# =========================================================

CSV_FILE = "operacoes.csv"

DEFAULT_COLUMNS = [
    "ativo",
    "estrategia",
    "direcao",
    "cluster",
    "dte",
    "custo_montagem",
    "valor_atual",
    "alvo",
]

if not Path(CSV_FILE).exists():
    pd.DataFrame(columns=DEFAULT_COLUMNS).to_csv(
        CSV_FILE,
        index=False
    )

try:
    df = pd.read_csv(CSV_FILE)
except:
    df = pd.DataFrame(columns=DEFAULT_COLUMNS)

# =========================================================
# HEADER
# =========================================================

st.title("Painel Operacional — Trade System")

st.caption(
    "Mesa operacional de opções • Gestão estrutural • Controle de risco"
)

st.divider()

# =========================================================
# MÉTRICAS
# =========================================================

capital_operacional = 20000

if not df.empty:

    exposicao = df["custo_montagem"].sum()

    pl_aberto = (
        df["valor_atual"] -
        df["custo_montagem"]
    ).sum()

    operacoes = len(df)

else:

    exposicao = 0
    pl_aberto = 0
    operacoes = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Capital Operacional",
    f"R$ {capital_operacional:,.0f}"
)

col2.metric(
    "Exposição Atual",
    f"R$ {exposicao:,.0f}"
)

col3.metric(
    "P/L Aberto",
    f"R$ {pl_aberto:,.0f}"
)

col4.metric(
    "Operações",
    operacoes
)

# =========================================================
# NOVA OPERAÇÃO
# =========================================================

st.divider()

st.markdown("## Nova Operação")

ativos = [
    "PETR4",
    "VALE3",
    "BOVA11",
    "ITUB4",
    "BBAS3",
    "BBDC4",
    "B3SA3",
    "RENT3",
    "SUZB3",
    "SMAL11",
]

estrategias = [
    "BOI CALL",
    "BOI PUT",
    "Trava Alta",
    "Trava Baixa",
    "Financiamento",
]

clusters = [
    "Commodities",
    "Financeiro",
    "Índice",
    "Crescimento",
]

with st.form("nova_operacao"):

    c1, c2, c3, c4 = st.columns(4)

    ativo = c1.selectbox(
        "Ativo",
        ativos
    )

    estrategia = c2.selectbox(
        "Estratégia",
        estrategias
    )

    direcao = c3.selectbox(
        "Direção",
        ["Alta", "Baixa"]
    )

    cluster = c4.selectbox(
        "Cluster",
        clusters
    )

    c5, c6, c7, c8 = st.columns(4)

    dte = c5.number_input(
        "DTE",
        value=20
    )

    custo = c6.number_input(
        "Custo Montagem",
        value=0.0
    )

    atual = c7.number_input(
        "Valor Atual",
        value=0.0
    )

    alvo = c8.number_input(
        "Alvo",
        value=2000.0
    )

    submitted = st.form_submit_button(
        "Adicionar Operação"
    )

    if submitted:

        new_row = pd.DataFrame([{
            "ativo": ativo,
            "estrategia": estrategia,
            "direcao": direcao,
            "cluster": cluster,
            "dte": dte,
            "custo_montagem": custo,
            "valor_atual": atual,
            "alvo": alvo,
        }])

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        df.to_csv(
            CSV_FILE,
            index=False
        )

        st.success("Operação adicionada.")

        st.rerun()

# =========================================================
# MESA
# =========================================================

st.divider()

st.markdown("## Mesa Operacional")

if not df.empty:

    df["pl_rs"] = (
        df["valor_atual"] -
        df["custo_montagem"]
    )

    df["pl_percentual"] = (
        (
            df["valor_atual"] /
            df["custo_montagem"].replace(0, 1)
        ) - 1
    ) * 100

    def status(row):

        if row["pl_percentual"] >= 100:
            return "Explosão"

        if (
            row["pl_percentual"] <= -50
            or row["dte"] < 10
        ):
            return "Morta"

        if (
            row["pl_percentual"] <= -20
            or row["dte"] < 15
        ):
            return "Atenção"

        return "Válida"

    df["status"] = df.apply(
        status,
        axis=1
    )

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,

        column_config={

            "pl_rs": st.column_config.NumberColumn(
                "P/L R$",
                format="R$ %.2f"
            ),

            "pl_percentual": st.column_config.NumberColumn(
                "P/L %",
                format="%.2f%%"
            ),

        }
    )

    edited_df.to_csv(
        CSV_FILE,
        index=False
    )

    df = edited_df

    # =====================================================
    # CLUSTERS
    # =====================================================

    st.divider()

    st.markdown("## Exposição por Cluster")

    cluster_view = (
        df.groupby(
            ["cluster", "direcao"]
        )
        .size()
        .unstack(fill_value=0)
    )

    st.dataframe(
        cluster_view,
        use_container_width=True
    )

    # =====================================================
    # MÉTRICAS
    # =====================================================

    st.divider()

    st.markdown("## Métricas")

    gains = df[df["pl_rs"] > 0]

    losses = df[df["pl_rs"] < 0]

    gain_medio = (
        gains["pl_rs"].mean()
        if not gains.empty
        else 0
    )

    loss_medio = (
        losses["pl_rs"].mean()
        if not losses.empty
        else 0
    )

    taxa_acerto = (
        len(gains) / len(df) * 100
    ) if len(df) > 0 else 0

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "Taxa de Acerto",
        f"{taxa_acerto:.1f}%"
    )

    m2.metric(
        "Gain Médio",
        f"R$ {gain_medio:,.2f}"
    )

    m3.metric(
        "Loss Médio",
        f"R$ {loss_medio:,.2f}"
    )

else:

    st.info(
        "Nenhuma operação cadastrada."
    )
