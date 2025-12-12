import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, RocCurveDisplay

st.title("💳 Prédiction de Fraude Bancaire")

API_URL = "http://127.0.0.1:8000/predict"  # ton endpoint FastAPI

st.write("Renseignez les variables du modèle (négatives ou positives).")

st.markdown("---")

# --- Variables à utiliser (excluant V11, V13, V15, V22) ---
variables = ["Time"] + [f"V{i}" for i in range(1,29) if i not in [11,13,15,22]] + ["Amount"]

# --- Mise en page 2 colonnes ---
col1, col2 = st.columns(2)

input_values = {}

# --- Remplissage des colonnes ---
for i, var in enumerate(variables):
    if i % 2 == 0:
        with col1:
            input_values[var] = st.number_input(var, value=0.0, format="%.6f")
    else:
        with col2:
            input_values[var] = st.number_input(var, value=0.0, format="%.6f")

# --- Bouton de prédiction ---
if st.button("Faire une prédiction"):
    try:
        # Appel API
        response = requests.post(API_URL, json=input_values)

        if response.status_code == 200:
            result = response.json()

            # Conversion en float pour éviter les chaînes
            prediction = int(result.get("prediction", 0))
            st.success(f"Résultat prédiction : **{prediction}**")

            if "probability" in result:
                probability = float(result["probability"])
                st.info(f"Probabilité : **{probability:.4f}**")

        else:
            st.error(f"Erreur API : {response.status_code}")
            st.write(response.text)

    except Exception as e:
        st.error("Impossible de joindre l'API")
        st.write(str(e))


st.markdown("---")

st.markdown(
    """
    <div style='text-align:center; font-size: 15px; color: grey;'>
    👩🏽‍💻 Développé par <b>Wilga  MBANI</b> © 2025
    </div>
    """,
    unsafe_allow_html=True
)
