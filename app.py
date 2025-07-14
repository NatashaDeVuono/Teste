import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Dashboard Jurídico", layout="wide")

st.title("📊 Dashboard Jurídico de Contratos")

# Carregar os dados
df = pd.read_csv("contratos.csv")
df["data_assinatura"] = pd.to_datetime(df["data_assinatura"])
df["vencimento"] = df["data_assinatura"] + pd.to_timedelta(df["prazo_dias"], unit="d")
df["vencido"] = df["vencimento"] < datetime.now()

# Filtros
tipo = st.multiselect("Filtrar por tipo de contrato:", df["tipo_contrato"].unique())
status = st.multiselect("Filtrar por status:", df["status"].unique())

df_filtrado = df.copy()
if tipo:
    df_filtrado = df_filtrado[df_filtrado["tipo_contrato"].isin(tipo)]
if status:
    df_filtrado = df_filtrado[df_filtrado["status"].isin(status)]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total de Contratos", len(df_filtrado))
col2.metric("Valor Total (R$)", f"{df_filtrado['valor_total'].sum():,.2f}")
col3.metric("Contratos Vencidos", df_filtrado["vencido"].sum())

# Gráficos
st.subheader("📌 Contratos por Status")
st.bar_chart(df_filtrado["status"].value_counts())

st.subheader("📌 Valor Total por Tipo de Contrato")
valor_tipo = df_filtrado.groupby("tipo_contrato")["valor_total"].sum()
st.bar_chart(valor_tipo)

# Tabela
st.subheader("📄 Visualização Detalhada")
st.dataframe(df_filtrado)
# Botão para baixar os dados filtrados como CSV
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar planilha do dashboard",
    data=csv,
    file_name='relatorio_contratos.csv',
    mime='text/csv'
)
