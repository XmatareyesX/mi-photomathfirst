import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="Mi Photomath", page_icon="🧮", layout="centered")
st.title("🧮 Mi Propio Photomath")
st.write("Sube o fotografía tu problema matemático para ver el desarrollo paso a paso.")

# Cargar API Key desde los Secrets de Streamlit
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.warning("⚠️ No se ha detectado la GEMINI_API_KEY en los Secrets de Streamlit.")
else:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Usamos file_uploader con soporte de cámara integrado para evitar errores de DOM
    archivo = st.file_uploader(
        "Haz una foto con la cámara o selecciona una imagen", 
        type=["png", "jpg", "jpeg"]
    )

    if archivo is not None:
        imagen = Image.open(archivo)
        st.image(imagen, caption="Imagen cargada", use_column_width=True)
        
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
                    st.error(f"Hubo un error al procesar la IA: {e}")
