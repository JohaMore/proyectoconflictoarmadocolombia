import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import geopandas as gpd
from streamlit_folium import st_folium
import unidecode
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Lista de departamentos en formato correcto, incluyendo acentos
correct_departments = [
    "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar", "Boyacá", "Caldas", "Caquetá",
    "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía", "Guaviare",
    "Huila", "La Guajira", "Magdalena", "Meta", "Nariño", "Norte de Santander", "Putumayo",
    "Quindío", "Risaralda", "San Andrés, Providencia y Santa Catalina", "Santander", "Sucre",
    "Tolima", "Valle del Cauca", "Vaupés", "Vichada"
]

# Crear un diccionario de corrección mapeando nombres sin acento a los nombres correctos con acento
correction_dict = {unidecode.unidecode(dep).upper(): dep for dep in correct_departments}

# Función para limpiar los datos
def clean_data(df):
    df.columns = df.columns.str.title()
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip().str.title()

    if "Departamento" in df.columns:
        df["Departamento"] = df["Departamento"].str.upper().str.strip()
        df["Departamento"] = df["Departamento"].map(lambda x: correction_dict.get(unidecode.unidecode(x), x))

        unmapped_departments = df[~df["Departamento"].isin(correct_departments)]["Departamento"].unique()
        if len(unmapped_departments) > 0:
            print("Departamentos no mapeados correctamente:")
            print(unmapped_departments)

        df["Departamento"] = df["Departamento"].where(df["Departamento"].isin(correct_departments), "Sin Identificar")

    if "Año" in df.columns:
        df["Año"] = df["Año"].replace(0, 1946)

    return df

st.set_page_config(layout="wide")

st.markdown(
    """
    <h1 style='text-align: center; font-size: 3em; margin-bottom: 0;'>El conflicto armado en Colombia</h1>
    """,
    unsafe_allow_html=True
)

st.write("Sube los datasets de casos y víctimas, explora un gráfico por departamento y visualiza un mapa interactivo con datos.")

cases_file = st.file_uploader("Sube el archivo de Casos de Masacres", type=["xlsx"], key="cases_file")
victims_file = st.file_uploader("Sube el archivo de Víctimas de Masacres", type=["xlsx"], key="victims_file")
secuestros_file = st.file_uploader("Sube el archivo de Casos de Secuestros", type=["xlsx"], key="secuestros_file")
victimas_secuestros_file = st.file_uploader("Sube el archivo de Víctimas de Secuestros", type=["xlsx"], key="victimas_secuestros_file")
presidentes_file = st.file_uploader("Sube el archivo de Presidentes", type=["xlsx"], key="presidentes_file")

if cases_file and victims_file and secuestros_file and victimas_secuestros_file:
    try:
        cases_df = pd.read_excel(cases_file, sheet_name=0)
        victims_df = pd.read_excel(victims_file, sheet_name=0)
        secuestros_df = pd.read_excel(secuestros_file, sheet_name=0)
        victimas_secuestros_df = pd.read_excel(victimas_secuestros_file, sheet_name=0)

        @st.cache_data
        def load_shapefile():
            return gpd.read_file("gadm41_COL_shp/gadm41_COL_1.shp")

        colombia_shp = load_shapefile()

        cases_cleaned = clean_data(cases_df)
        victims_cleaned = clean_data(victims_df)
        secuestros_cleaned = clean_data(secuestros_df)
        victimas_secuestros_cleaned = clean_data(victimas_secuestros_df)

        years_cases = cases_cleaned["Año"].dropna().unique() if "Año" in cases_cleaned.columns else []
        years_victims = victims_cleaned["Año"].dropna().unique() if "Año" in victims_cleaned.columns else []
        unique_years = sorted(set(years_cases).union(years_victims))
        unique_years.insert(0, "Todos los años")

        selected_year = st.selectbox("Selecciona un año para filtrar", unique_years)

        if selected_year != "Todos los años":
            cases_filtered = cases_cleaned[cases_cleaned["Año"] == selected_year]
            victims_filtered = victims_cleaned[victims_cleaned["Año"] == selected_year]
            secuestros_filtered = secuestros_cleaned[secuestros_cleaned["Año"] == selected_year]
            victimas_secuestros_filtered = victimas_secuestros_cleaned[victimas_secuestros_cleaned["Año"] == selected_year]
        else:
            cases_filtered = cases_cleaned
            victims_filtered = victims_cleaned
            secuestros_filtered = secuestros_cleaned
            victimas_secuestros_filtered = victimas_secuestros_cleaned

        total_cases = len(cases_filtered)
        total_victims = len(victims_filtered)
        total_secuestros = len(secuestros_filtered)
        total_victimas_secuestros = len(victimas_secuestros_filtered)

        st.markdown(
            f"""
            <div style='display: flex; justify-content: center; gap: 30px; margin: 20px 0;'>
                <div style='background-color: #4CAF50; padding: 20px 40px; border-radius: 10px; text-align: center; color: white;'>
                    <h2 style='margin: 0;'>Total Casos Masacres</h2>
                    <h1 style='margin: 0;'>{total_cases:,}</h1>
                </div>
                <div style='background-color: #FF5722; padding: 20px 40px; border-radius: 10px; text-align: center; color: white;'>
                    <h2 style='margin: 0;'>Total Víctimas Masacres</h2>
                    <h1 style='margin: 0;'>{total_victims:,}</h1>
                </div>
                <div style='background-color: #3F51B5; padding: 20px 40px; border-radius: 10px; text-align: center; color: white;'>
                    <h2 style='margin: 0;'>Total Casos de Secuestros</h2>
                    <h1 style='margin: 0;'>{total_secuestros:,}</h1>
                </div>
                <div style='background-color: #009688; padding: 20px 40px; border-radius: 10px; text-align: center; color: white;'>
                    <h2 style='margin: 0;'>Total Víctimas de Secuestros</h2>
                    <h1 style='margin: 0;'>{total_victimas_secuestros:,}</h1>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        department_cases = cases_filtered["Departamento"].value_counts()
        department_victims = victims_filtered.groupby("Departamento")["Id Persona"].count()

        chart_data = pd.DataFrame({
            "Departamento": department_cases.index.union(department_victims.index),
            "Casos": department_cases.reindex(department_cases.index.union(department_victims.index), fill_value=0).values,
            "Víctimas": department_victims.reindex(department_cases.index.union(department_victims.index), fill_value=0).values
        }).sort_values(by="Departamento")

        colombia_mapa = colombia_shp.merge(chart_data, left_on="NAME_1", right_on="Departamento", how="left")
        colombia_mapa["Casos"] = colombia_mapa["Casos"].fillna(0)
        colombia_mapa["Víctimas"] = colombia_mapa["Víctimas"].fillna(0)

        m = folium.Map(location=[4.570868, -74.297333], zoom_start=6)
        folium.Choropleth(
            geo_data=colombia_mapa.to_json(),
            data=colombia_mapa,
            columns=["NAME_1", "Víctimas"],
            key_on="feature.properties.NAME_1",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Número de Víctimas"
        ).add_to(m)

        for _, row in colombia_mapa.iterrows():
            folium.GeoJson(
                row["geometry"],
                tooltip=folium.Tooltip(
                    f"{row['NAME_1']}:\nVíctimas: {int(row['Víctimas'])}\nCasos: {int(row['Casos'])}"
                )
            ).add_to(m)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Mapa de Víctimas y Casos de Masacres  - Departamento")
            st_folium(m, width=700, height=500)

        with col2:
            st.subheader("Distribución de Género - Masacres")
            if "Sexo" in victims_filtered.columns:
                victim_gender_count = victims_filtered["Sexo"].value_counts()
                fig_victims = px.pie(
                    names=victim_gender_count.index,
                    values=victim_gender_count.values,
                    title="Distribución por Sexo (Víctimas Masacres)",
                    hole=0.5,
                    labels={"values": "Número de Víctimas"},
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_victims.update_traces(textinfo="percent+label")
                st.plotly_chart(fig_victims, use_container_width=True)

        st.subheader("Casos y Víctimas de Masacres por Departamento")
        chart_data_melted = chart_data.melt(id_vars="Departamento", 
                                            value_vars=["Casos", "Víctimas"], 
                                            var_name="Tipo", 
                                            value_name="Cantidad")

        fig = px.bar(
            chart_data_melted,
            x="Departamento",
            y="Cantidad",
            color="Tipo",
            barmode="stack",
            title="Casos y Víctimas por Departamento",
            labels={"Cantidad": "Número", "Departamento": "Departamento"},
            text="Cantidad"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Casos por Modalidad de Masacres")
        if "Modalidad" in cases_cleaned.columns and "Año" in cases_cleaned.columns:
            modalidad_trends = cases_cleaned.groupby(["Año", "Modalidad"]).size().reset_index(name="Cantidad")
            fig_line = px.line(
                modalidad_trends,
                x="Año",
                y="Cantidad",
                color="Modalidad",
                title="Tendencias de Casos por Modalidad",
                labels={"Cantidad": "Número de Casos", "Año": "Año"}
            )
            st.plotly_chart(fig_line, use_container_width=True)

        st.subheader("Presuntos Responsables Masacres")
        if "Presunto Responsable" in cases_cleaned.columns:
            responsable_counts = cases_cleaned["Presunto Responsable"].value_counts().reset_index()
            responsable_counts.columns = ["Presunto Responsable", "Cantidad"]
            fig_horizontal_bar = px.bar(
                responsable_counts,
                x="Cantidad",
                y="Presunto Responsable",
                orientation="h",
                title="Distribución por Presunto Responsable",
                labels={"Cantidad": "Número de Casos", "Presunto Responsable": "Responsable"},
                text="Cantidad"
            )
            fig_horizontal_bar.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_horizontal_bar, use_container_width=True)

        st.subheader("Presunto Responsable de Masacres por Año")
        if "Presunto Responsable" in cases_cleaned.columns and "Año" in cases_cleaned.columns:
            responsable_yearly = cases_cleaned.groupby(["Año", "Presunto Responsable"]).size().reset_index(name="Cantidad")
            fig_scatter = px.scatter(
                responsable_yearly,
                x="Año",
                y="Cantidad",
                color="Presunto Responsable",
                size="Cantidad",
                title="Clusters de Casos por Presunto Responsable y Año",
                labels={"Cantidad": "Número de Casos", "Año": "Año"},
                hover_name="Presunto Responsable"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.subheader("Ocupación de Víctimas Masacradas")
        if "Ocupación" in victims_cleaned.columns:
            occupations = victims_cleaned["Ocupación"].dropna().str.upper()
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(' '.join(occupations))

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

        st.subheader("Timeline de Casos y Víctimas de Secuestros")
        secuestros_timeline = secuestros_cleaned.groupby("Año").size().reset_index(name="Casos de Secuestros")
        victimas_secuestros_timeline = victimas_secuestros_cleaned.groupby("Año").size().reset_index(name="Víctimas de Secuestros")

        timeline_data = pd.merge(
            secuestros_timeline, 
            victimas_secuestros_timeline, 
            on="Año", 
            how="outer"
        ).fillna(0).sort_values(by="Año")

        fig_timeline = px.line(
            timeline_data, 
            x="Año", 
            y=["Casos de Secuestros", "Víctimas de Secuestros"], 
            title="Evolución de Casos y Víctimas de Secuestros por Año",
            labels={"value": "Cantidad", "variable": "Tipo"},
            markers=True
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

        st.subheader("Presuntos Responsables de Secuestros por Año")
        if "Presunto Responsable" in secuestros_cleaned.columns and "Año" in secuestros_cleaned.columns:
            responsables_timeline = secuestros_cleaned.groupby(["Año", "Presunto Responsable"]).size().reset_index(name="Cantidad")
            fig_responsables = px.bar(
                responsables_timeline,
                x="Año",
                y="Cantidad",
                color="Presunto Responsable",
                title="Presuntos Responsables de Secuestros por Año",
                labels={"Cantidad": "Número de Casos", "Año": "Año"},
                text="Cantidad",
                
            )
            fig_responsables.update_layout(barmode="stack")
            st.plotly_chart(fig_responsables, use_container_width=True)

        if presidentes_file:
            presidentes_df = pd.read_excel(presidentes_file, sheet_name=0)

            presidentes_cleaned = presidentes_df.rename(columns={"Año": "Año", "Presidente": "Presidente"})

            secuestros_por_presidente = secuestros_cleaned.groupby("Año").size().reset_index(name="Cantidad Secuestros")
            masacres_por_presidente = cases_cleaned.groupby("Año").size().reset_index(name="Cantidad Masacres")

            # Merge con presidentes
            datos_presidentes = presidentes_cleaned.merge(secuestros_por_presidente, on="Año", how="left")
            datos_presidentes = datos_presidentes.merge(masacres_por_presidente, on="Año", how="left")
            datos_presidentes = datos_presidentes.fillna(0)

            # Gráfico
            st.subheader("Secuestros y Masacres en Colombia: Contexto Histórico y Político")
            fig_presidentes = px.bar(
                datos_presidentes.melt(
                    id_vars=["Año", "Presidente"], 
                    value_vars=["Cantidad Secuestros", "Cantidad Masacres"], 
                    var_name="Tipo", 
                    value_name="Cantidad"
                     ),
                x="Año",
                y="Cantidad",
                color="Tipo",
                hover_data={"Presidente": True},
                barmode="group",
                title="Número de Secuestros y Masacres por Presidente",
                labels={"Cantidad": "Número de Casos", "Año": "Año"},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_presidentes.add_shape(
            type="line",
            x0=1998, x1=1998, y0=0, y1=fig_presidentes.data[0]['y'].max(),  # Línea para Andrés Pastrana
            line=dict(color="red", dash="dash"),
            xref="x", yref="y"
            )
            fig_presidentes.add_shape(
            type="line",
            x0=2002, x1=2002, y0=0, y1=fig_presidentes.data[0]['y'].max(),  # Línea para Álvaro Uribe
            line=dict(color="blue", dash="dash"),
            xref="x", yref="y"
            )

            fig_presidentes.add_shape(
            type="line",
            x0=2010, x1=2010, y0=0, y1=fig_presidentes.data[0]['y'].max(),  # Línea para Juan Manuel Santos
            line=dict(color="green", dash="dash"),
            xref="x", yref="y"
            )

            # Añadir anotaciones para los períodos presidenciales
            fig_presidentes.add_annotation(
            x=1999, y=fig_presidentes.data[0]['y'].max() * 0.95,
            text="Andrés Pastrana",
            showarrow=False,
            font=dict(color="red")
            )
            fig_presidentes.add_annotation(
            x=2005, y=fig_presidentes.data[0]['y'].max() * 0.95,
            text="       Álvaro Uribe",
            showarrow=False,
            font=dict(color="blue")
            )
            fig_presidentes.add_annotation(
            x=2014, y=fig_presidentes.data[0]['y'].max() * 0.95,
            text="  Juan Manuel Santos",
            showarrow=False,
            font=dict(color="green")
            )

            st.plotly_chart(fig_presidentes, use_container_width=True)

    except Exception as e:
        st.error(f"Error procesando los archivos: {e}")





















































