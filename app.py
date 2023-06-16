import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from textblob import TextBlob

# Cargar los datos de los registros de WhatsApp
def cargar_datos(archivo):
    datos = pd.read_csv(archivo, sep="]", header=None, names=["Mensaje"])
    # Eliminar el mensaje inicial de privacidad de WhatsApp
    datos = datos[1:]
    # Extraer fecha, hora, remitente y contenido del mensaje utilizando expresiones regulares
    datos[['Fecha', 'Hora', 'Remitente', 'Contenido']] = datos['Mensaje'].str.extract(r'\[(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{1,2}:\d{1,2} [a|p]\.m\.)\] (.+?): (.+)')
    # Eliminar caracteres no deseados en la columna "Contenido"
    datos['Contenido'] = datos['Contenido'].str.replace(r"[^a-zA-Z0-9\s]+", "")
    return datos.drop(columns=['Mensaje'])

# Analizar los datos y generar visualizaciones
def analizar_sentimiento(datos):
    # Convertir la columna "Contenido" a tipo cadena
    datos['Contenido'] = datos['Contenido'].astype(str)
    # Analizar el sentimiento de los mensajes
    datos["Sentimiento"] = datos["Contenido"].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Graficar el sentimiento promedio
    st.subheader("Sentimiento promedio de los mensajes")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=datos.index, y=datos["Sentimiento"])
    plt.xlabel("Mensaje")
    plt.ylabel("Sentimiento")
    plt.xticks(rotation=45)
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
