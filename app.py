import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# Configuración de la página
st.set_page_config(page_title="Mi Photomath Local", page_icon="🧮", layout="centered")
st.title("🧮 Mi Propio Photomath")
st.write("Toma una foto de la ecuación para ver el desarrollo paso a paso.")

# Obtener la API key del entorno
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.warning("⚠️ No se ha detectado la variable de entorno GEMINI_API_KEY. Configúrala en tu docker-compose.yml.")
else:
    genai.configure(api_key=API_KEY)
    # Usamos Gemini 1.5 Flash: es multimodal (lee imágenes) y su nivel gratuito es amplísimo
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Opción 1: Cámara (ideal al acceder desde el iPhone)
    foto = st.camera_input("Enfoca tu problema matemático")
    # Opción 2: Subir archivo
    archivo = st.file_uploader("O sube una imagen desde la galería", type=["png", "jpg", "jpeg"])

    imagen_capturada = foto if foto else archivo

    if imagen_capturada is not None:
        imagen = Image.open(imagen_capturada)
        
        if st.button("Resolver paso a paso", type="primary"):
            with st.spinner('Analizando la imagen y calculando...'):
                prompt = """
                Eres un profesor de matemáticas. Extrae la ecuación o problema matemático de esta imagen.
                1. Muestra la ecuación original detectada.
                2. Resuelve el problema paso a paso explicando brevemente cada operación.
                3. Muestra el resultado final claramente.
                Usa formato Markdown. Para las fórmulas matemáticas, envuélvelas siempre en el símbolo de dólar ($) para que se rendericen en LaTeX.
                """
                try:
                    respuesta = model.generate_content([prompt, imagen])
                    st.success("¡Resuelto!")
                    st.markdown(respuesta.text)
                except Exception as e:
                    st.error(f"Hubo un error de conexión: {e}")