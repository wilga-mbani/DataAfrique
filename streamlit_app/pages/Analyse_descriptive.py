import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Analyse descriptive des données")

file = st.file_uploader("Importer un fichier CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    # Structure
    st.subheader("Structure des données")
    st.write("Dimensions :", df.shape)
    st.dataframe(df.head())
    st.dataframe(df.dtypes.astype(str))

    # Statistiques
    st.subheader("Statistiques descriptives")
    st.dataframe(df.describe(include="all").T)

    # Univariée
    st.subheader("Analyse univariée")
    col = st.selectbox("Choisir une variable", df.columns)

    fig, ax = plt.subplots()
    if df[col].dtype in ["int64", "float64"]:
        sns.histplot(df[col], kde=True, ax=ax)
    else:
        df[col].value_counts().plot(kind="bar", ax=ax)

    st.pyplot(fig)

    # Bivariée
    st.subheader("Analyse bivariée")

    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

# Création de deux colonnes
    col_left, col_right = st.columns(2)

# ─────────────────────────────
#  Scatterplot (colonne gauche)
    with col_left:
        st.markdown("###  Scatterplot")

        if len(num_cols) >= 2:
            x_var = st.selectbox(
                "Variable numérique X",
                num_cols,
                key="scatter_x"
            )

            y_var = st.selectbox(
                "Variable numérique Y",
                [c for c in num_cols if c != x_var],
                key="scatter_y"
            )

            fig1, ax1 = plt.subplots()
            sns.scatterplot(data=df, x=x_var, y=y_var, ax=ax1)
            ax1.set_title(f"{x_var} vs {y_var}")
            st.pyplot(fig1)

        else:
            st.warning("Pas assez de variables numériques pour le scatterplot.")

# ─────────────────────────────
    #  Boxplot (colonne droite)
    with col_right:
        st.markdown("###  Boxplot (Class vs variable)")

        if "Class" in df.columns:
            num_box = [c for c in num_cols if c != "Class"]

            if num_box:
                var_box = st.selectbox(
                "Variable numérique",
                    num_box,
                    key="box_var"
                )

                fig2, ax2 = plt.subplots()
                sns.boxplot(
                    data=df,
                    x="Class",
                    y=var_box,
                    ax=ax2,
                    hue= "Class",
                    showfliers=False
                )
                ax2.set_title(f"{var_box} selon la classe")
                st.pyplot(fig2)

            else:
                st.warning("Aucune variable numérique valide pour le boxplot.")
        else:
            st.error("La variable cible 'Class' est absente du dataset.")

