import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

#import streamlit_modal
#from streamlit_modal import Modal
#import streamlit.components.v1 as components


# Función para calcular los pesos a partir de la matriz de comparación
def calcular_pesos(matriz):
    cant = matriz.shape[0]
    productos = np.prod(matriz, axis=1)
    raices = productos ** (1 / cant)
    pesos = raices / raices.sum()
    return pesos

# Función principal de la app de Streamlit
def app():
    
    # HTML para título y subtítulos
    st.markdown("""
                <h1 style='text-align: center; font-size: 36px;'>Analytic Hierarchy Process - AHP</h1>
                <h3 style='text-align: center; font-size: 30px;'>ANÁLISIS MULTIVARIADO <br> Ponderación de Variables</h3>
    """, unsafe_allow_html=True)
    
    #  Logo
    logo = Image.open('img/logo.png')
    st.image(logo)

    # Captura del Nombre del Fenómeno o Aspecto sobre el quiere ponderar las variables
    nombreFenomeno = st.text_input("Nombre del Fenómeno/Aspecto:")
    st.session_state['nombreFenomeno'] = nombreFenomeno

    # Captura número de criterios
    cant = st.number_input("¿CUÁNTOS CRITERIOS DESEA EVALUAR?", min_value=2, max_value=15, step=1)

    # Si se ha establecido un número de criterios, solicitar sus nombres
    if cant > 0:
        criterios = [st.text_input(f"Nombre del criterio {i+1}:", key=f"criterio_{i}") for i in range(cant)]

    if all(criterios):
        # Crear una matriz de comparación
        matriz = np.ones((cant, cant))
        
        with st.form("matriz_comparacion"):
            st.subheader("Matriz de Comparación")
            # Crear campos de entrada para comparaciones
            opciones = [
                ("Igualmente importante", 1),
                ("Ligeramente más importante", 3),
                ("Bastante más importante", 5),
                ("Considerablemente más importante", 7),
                ("Absolutamente más importante", 9),
            ]
            for i in range(cant):
                for j in range(i+1, cant):
                    # Usar un selectbox con texto en lugar de números
                    opcion = st.selectbox(f"Cómo definirías la comparación entre {criterios[i]} y {criterios[j]}:", 
                                          options=[o[0] for o in opciones], 
                                          format_func=lambda x: x,
                                          key=f"select_{i}_{j}")
                    # Encontrar el valor numérico correspondiente a la opción de texto
                    valor = next(val for text, val in opciones if text == opcion)
                    matriz[i, j] = valor
                    matriz[j, i] = 1 / valor
            
            # Botón de envío
            submitted = st.form_submit_button("Calcular pesos")
            if submitted:
                if nombreFenomeno:
                    st.markdown(f"### {nombreFenomeno}")
                else:
                    st.markdown("### Resultados:")
                # Calcular pesos
                pesos = calcular_pesos(matriz)
                # Mostrar pesos en formato de porcentaje
                # st.subheader("Pesos calculados:")
                pesosPorcentaje = pd.Series(pesos * 100, index=criterios)
                st.session_state['pesosPorcentaje'] = pd.Series(calcular_pesos(matriz) * 100, index=criterios)
                #st.dataframe(pesosPorcentaje.to_frame(name="Peso (%)"))
            
                # Crear un gráfico de torta para los pesos
                fig, ax = plt.subplots()
                ax.pie(pesos, labels=criterios, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Igual aspect ratio asegura que se dibuje el pie como un círculo.
                
                # Usar columnas para organizar el contenido
                col1, col2, col3 = st.columns([1,8,1])
                
                
                # Columna para el gráfico
                col2.subheader("Distribución")
                col2.pyplot(fig)
                st.session_state['fig'] = fig

                col1, col2, col3 = st.columns([2,6,1])
                # Columna para la matriz de resultados
                col2.subheader("Matriz de Resultados")
                col2.dataframe(pesosPorcentaje.to_frame(name="Peso (%)"))

                st.session_state['pesosCalculados'] = True

                st.markdown("""
                    <style>
                    .impresion {
                        font-size: 10pt;
                        color: gray;
                        text-align: center;
                        font-style: italic;
                    }
                    </style>
                    <p class="impresion">Para garantizar la reproducibilidad de este modelo de ponderación, es recomendable obtener una copia de este informe. 
                            Para ello utilice la función de impresión de la aplicación haciendo clic en los tres puntos que están en la esquina superior derecha.
                    </p>
                    """, unsafe_allow_html=True)

    

                
if __name__ == "__main__":
    app()


       # Agregar los créditos e la parte inferior
    st.markdown("""
        <style>
        .credits {
            font-size: 10pt;
            color: gray;
            text-align: right;
        }
        </style>
        <p class="credits">Developed by: Julián Darío Giraldo Ocampo | ingenieria@juliangiraldo.co</p>
        """, unsafe_allow_html=True)