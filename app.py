import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

# Cargar los datos de los registros de WhatsApp
def cargar_datos(archivo):
    datos = pd.read_csv(archivo, sep="\t", header=None, names=["Fecha", "Hora", "Mensaje"])
    return datos

# Analizar los datos y generar visualizaciones
def analizar_sentimiento(datos):
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
    st.title("Análisis de sentimiento de registros de WhatsApp")
    st.write("Esta aplicación analiza el sentimiento de los mensajes de WhatsApp y presenta los resultados en forma gráfica.")

    # Subir el archivo de registros de WhatsApp
    archivo = st.file_uploader("Sube el archivo de registros de WhatsApp (_chat.txt)", type="txt")

    if archivo is not None:
        # Cargar los datos
        datos = cargar_datos(archivo)

        # Analizar el sentimiento de los mensajes
        analizar_sentimiento(datos)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
