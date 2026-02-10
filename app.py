import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="NovaRetail – Dashboard Marketing",
    layout="wide"
)

# =========================
# TITRE & CONTEXTE
# =========================
st.title("📊 NovaRetail – Dashboard Marketing")

st.markdown("""
Analyse des performances marketing (Emailing, Google Ads, LinkedIn Ads)  
🎯 **Objectif :** évaluer la génération et la qualité des leads.
""")

st.info("Dashboard décisionnel – KPI & visualisations marketing")

# =========================
# CHARGEMENT DES DONNÉES
# =========================
@st.cache_data
def load_data():
    leads = pd.read_csv("leads_novaretail.csv")
    crm = pd.read_csv("crm_novaretail.csv")
    campaigns = pd.read_csv("campaigns_novaretail.csv")
    return leads, crm, campaigns

leads, crm, campaigns = load_data()

# =========================
# PRÉPARATION DES DONNÉES
# =========================
# Merge Leads + CRM
data = leads.merge(crm, on="lead_id", how="left")

# =========================
# KPI TUNNEL CRM
# =========================
total_leads = len(data)
nb_mql = (data["status"] == "MQL").sum()
nb_sql = (data["status"] == "SQL").sum()
nb_clients = (data["status"] == "Client").sum()

pct_mql = nb_mql / total_leads * 100
pct_sql = nb_sql / total_leads * 100
pct_clients = nb_clients / total_leads * 100

# =========================
# KPI MARKETING
# =========================
campaigns["CTR"] = campaigns["clicks"] / campaigns["impressions"]
campaigns["taux_conversion"] = campaigns["conversions"] / campaigns["clicks"]
campaigns["CPL"] = campaigns["cost"] / campaigns["conversions"]

cpl_moyen = campaigns["CPL"].mean()

# =========================
# AFFICHAGE KPI
# =========================
st.subheader("📌 Indicateurs clés")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total leads", total_leads)
col2.metric("% MQL", f"{pct_mql:.0f}%")
col3.metric("% SQL", f"{pct_sql:.0f}%")
col4.metric("% Clients", f"{pct_clients:.0f}%")
col5.metric("CPL moyen (€)", f"{cpl_moyen:.1f}")

# =========================
# VISUALISATION 1 – TUNNEL CRM
# =========================
st.subheader("📊 Répartition des leads par statut")

fig1, ax1 = plt.subplots()
data["status"].value_counts().plot(kind="bar", ax=ax1)
ax1.set_xlabel("Statut")
ax1.set_ylabel("Nombre de leads")
ax1.set_title("Distribution des leads dans le tunnel CRM")
st.pyplot(fig1)

# =========================
# VISUALISATION 2 – CPL PAR CANAL
# =========================
st.subheader("💰 Coût par lead (CPL) par canal")

fig2, ax2 = plt.subplots()
campaigns.groupby("channel")["CPL"].mean().plot(kind="bar", ax=ax2)
ax2.set_xlabel("Canal")
ax2.set_ylabel("CPL (€)")
ax2.set_title("CPL moyen par canal marketing")
st.pyplot(fig2)

# =========================
# VISUALISATION 3 – VOLUME DE LEADS PAR CANAL
# =========================
st.subheader("📈 Volume de leads par canal")

fig3, ax3 = plt.subplots()
leads["channel"].value_counts().plot(kind="bar", ax=ax3)
ax3.set_xlabel("Canal")
ax3.set_ylabel("Nombre de leads")
ax3.set_title("Répartition des leads par canal")
st.pyplot(fig3)

# =========================
# TABLE DE DONNÉES
# =========================
st.subheader("📋 Détails des campagnes marketing")
st.dataframe(campaigns)
