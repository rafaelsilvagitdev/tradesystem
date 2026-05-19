import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Trade System",
    layout="wide"
)

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
    pd.DataFrame(columns=DEFAULT_COLUMNS).to_csv(CSV_FILE, index=False)

df = pd.read_csv(CSV_FILE)

st.title("Painel Operacional — Trade System")

st.subheader("Dashboard")

capital_operacional = 20000

exposicao = df["custo_montagem"].sum() if not df.empty else 0
pl_aberto = (df["valor_atual"] - df["custo_montagem"]).sum() if not df.empty else 0
operacoes = len(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Capital Operacional", f"R$ {capital_operacional:,.2f}")
col2.metric("Exposição Atual", f"R$ {exposicao:,.2f}")
col3.metric("P/L Aberto", f"R$ {pl_aberto:,.2f}")
col4.metric("Operações Abertas", operacoes)

st.divider()

st.subheader("Operações")

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

    ativo = c1.selectbox("Ativo", ativos)
    estrategia = c2.selectbox("Estratégia", estrategias)
    direcao = c3.selectbox("Direção", ["Alta", "Baixa"])
    cluster = c4.selectbox("Cluster", clusters)

    c5, c6, c7, c8 = st.columns(4)

    dte = c5.number_input("DTE", value=20)
    custo = c6.number_input("Custo Montagem", value=0.0)
    atual = c7.number_input("Valor Atual", value=0.0)
    alvo = c8.number_input("Alvo", value=2000.0)

    submitted = st.form_submit_button("Adicionar Operação")

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

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success("Operação adicionada.")
        st.rerun()

if not df.empty:
    df["pl_rs"] = df["valor_atual"] - df["custo_montagem"]

    df["pl_percentual"] = (
        (df["valor_atual"] / df["custo_montagem"]) - 1
    ) * 100

    def status(row):
        if row["pl_percentual"] >= 100:
            return "Explosão"

        if row["pl_percentual"] <= -50 or row["dte"] < 10:
            return "Morta"

        if row["pl_percentual"] <= -20 or row["dte"] < 15:
            return "Atenção"

        return "Válida"

    df["status"] = df.apply(status, axis=1)

    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("Clusters")

    cluster_view = (
        df.groupby(["cluster", "direcao"])
        .size()
        .unstack(fill_value=0)
    )

    st.dataframe(cluster_view, use_container_width=True)

    st.divider()

    st.subheader("Métricas")

    gains = df[df["pl_rs"] > 0]
    losses = df[df["pl_rs"] < 0]

    gain_medio = gains["pl_rs"].mean() if not gains.empty else 0
    loss_medio = losses["pl_rs"].mean() if not losses.empty else 0

    taxa_acerto = (
        len(gains) / len(df) * 100
    ) if len(df) > 0 else 0

    m1, m2, m3 = st.columns(3)

    m1.metric("Taxa de Acerto", f"{taxa_acerto:.1f}%")
    m2.metric("Gain Médio", f"R$ {gain_medio:,.2f}")
    m3.metric("Loss Médio", f"R$ {loss_medio:,.2f}")

    st.divider()

    st.subheader("Excluir Operação")

    index_remove = st.number_input(
        "Índice da operação para remover",
        min_value=0,
        max_value=len(df)-1,
        value=0
    )

    if st.button("Remover"):
        df = df.drop(index=index_remove).reset_index(drop=True)
        df.to_csv(CSV_FILE, index=False)
        st.success("Operação removida.")
        st.rerun()
