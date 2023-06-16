import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

# Cargar los datos de los registros de WhatsApp
def cargar_datos():
    datos = pd.read_csv("whatsapp_logs.csv")  # Reemplaza "whatsapp_logs.csv" con el nombre de tu archivo CSV
    return datos

# Analizar los datos y generar visualizaciones
def analizar_datos(datos):
    # Contar la cantidad de mensajes por usuario
    conteo_mensajes = datos["Usuario"].value_counts()

    # Graficar el conteo de mensajes por usuario
    st.subheader("Conteo de mensajes por usuario")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=conteo_mensajes.index, y=conteo_mensajes.values)
    plt.xlabel("Usuario")
    plt.ylabel("Cantidad de mensajes")
    st.pyplot()

    # Analizar el sentimiento de los mensajes
    datos["Sentimiento"] = datos["Mensaje"].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Graficar el sentimiento promedio por usuario
    st.subheader("Sentimiento promedio por usuario")
    sentimiento_promedio = datos.groupby("Usuario")["Sentimiento"].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=sentimiento_promedio.index, y=sentimiento_promedio.values)
    plt.xlabel("Usuario")
    plt.ylabel("Sentimiento promedio")
    st.pyplot()

    # Mostrar la cantidad total de mensajes
    st.write("La cantidad total de mensajes es:", len(datos))

# Configuración de la aplicación
def main():
    st.title("Análisis de registros de WhatsApp")
    st.write("Esta aplicación analiza los registros de WhatsApp y presenta los resultados en forma gráfica.")

    # Cargar los datos
    datos = cargar_datos()

    # Analizar los datos y generar visualizaciones
    analizar_datos(datos)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
