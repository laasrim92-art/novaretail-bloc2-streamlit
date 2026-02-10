import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="NovaRetail – Dashboard Marketing",
    layout="wide"
)

st.title("📊 NovaRetail – Dashboard Marketing")
st.markdown("""
Analyse des performances marketing (Emailing, Google Ads, LinkedIn Ads)  
Objectif : évaluer la génération et la qualité des leads.
""")

st.info("Dashboard en cours de construction – visualisations et KPI marketing")
st.subheader("📌 Indicateurs clés")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total leads", total_leads)
col2.metric("% MQL", f"{pct_mql:.0f}%")
col3.metric("% SQL", f"{pct_sql:.0f}%")
col4.metric("% Clients", f"{pct_clients:.0f}%")
col5.metric("CPL moyen (€)", f"{campaigns['CPL'].mean():.1f}")
st.info(...)
st.subheader(...)
col1, col2, col3, col4, col5 = st.columns(5)
...
# -----------------------------
# Chargement des données
# -----------------------------
@st.cache_data
def load_data():
    leads = pd.read_csv("leads_novaretail.csv")
    crm = pd.read_csv("crm_novaretail.csv")
    campaigns = pd.read_csv("campaigns_novaretail.csv")
    return leads, crm, campaigns

leads, crm, campaigns = load_data()

# Merge leads + CRM (comme dans ton notebook)
data = leads.merge(crm, on="lead_id", how="left")

# -----------------------------
# KPI tunnel CRM
# -----------------------------
total_leads = len(data)
nb_mql = (data["status"] == "MQL").sum()
nb_sql = (data["status"] == "SQL").sum()
nb_clients = (data["status"] == "Client").sum()

pct_mql = nb_mql / total_leads * 100
pct_sql = nb_sql / total_leads * 100
pct_clients = nb_clients / total_leads * 100

# -----------------------------
# KPI marketing (CPL)
# -----------------------------
campaigns["CTR"] = campaigns["clicks"] / campaigns["impressions"]
campaigns["taux_conversion"] = campaigns["conversions"] / campaigns["clicks"]
campaigns["CPL"] = campaigns["cost"] / campaigns["conversions"]
col2.metric("% MQL", f"{pct_mql:.0f}%")
col5.metric("CPL moyen (€)", f"{campaigns['CPL'].mean():.1f}")
st.subheader("📊 Répartition des leads par statut")

fig, ax = plt.subplots()
data["status"].value_counts().plot(kind="bar", ax=ax)
ax.set_xlabel("Statut")
ax.set_ylabel("Nombre de leads")
ax.set_title("Distribution des leads dans le tunnel CRM")

st.pyplot(fig)
