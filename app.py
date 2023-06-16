import streamlit as st
import pandas as pd
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

# Analizar los datos y mostrar información
def analizar_datos(datos):
    # Mostrar la cantidad total de mensajes
    st.write("La cantidad total de mensajes es:", len(datos))

    # Calcular el sentimiento promedio
    datos["Sentimiento"] = datos["Contenido"].apply(lambda x: TextBlob(x).sentiment.polarity if isinstance(x, str) else 0)
    sentimiento_promedio = datos["Sentimiento"].mean()
    st.write("El sentimiento promedio de los mensajes es:", sentimiento_promedio)

# Configuración de la aplicación
def main():
    st.title("Análisis de sentimiento de registros de WhatsApp")
    st.write("Esta aplicación analiza el sentimiento de los mensajes de WhatsApp y muestra los resultados.")

    # Subir el archivo de registros de WhatsApp
    archivo = st.file_uploader("Sube el archivo de registros de WhatsApp (_chat.txt)", type="txt")

    if archivo is not None:
        # Cargar los datos
        datos = cargar_datos(archivo)

        # Analizar los datos
        analizar_datos(datos)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
