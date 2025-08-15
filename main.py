import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

# ----------------------------
# Configuración de página
# ----------------------------
st.set_page_config(page_title="Agente LLaMA3 - Groq", layout="centered")
st.title("🤖 Agente LLaMA3-8B con LangChain y Groq API")

# ----------------------------
# Obtener API key desde secrets
# ----------------------------
groq_api_key = st.secrets["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"]

# ----------------------------
# Inicializar LLM
# ----------------------------
llm = ChatGroq(
    api_key=groq_api_key,
    model="llama3-8b-8192",
    temperature=0.7
)

# ----------------------------
# Entrada del usuario
# ----------------------------
user_input = st.text_area("Escribe tu pregunta o instrucción:", height=150)

if st.button("Enviar"):
    if user_input.strip():
        with st.spinner("Pensando..."):
            # Crear prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Eres un asistente útil y experto."),
                ("human", "{input}")
            ])

            chain = prompt | llm

            # Ejecutar
            respuesta = chain.invoke({"input": user_input})
            st.markdown("### Respuesta:")
            st.write(respuesta.content)
    else:
        st.warning("Por favor escribe algo antes de enviar.")
