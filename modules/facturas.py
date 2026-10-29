import pandas as pd
import streamlit as st


def mostrar_modulo_empresa(tabla_empresa: pd.DataFrame) -> None:
  """Función para mostrar los datos de la empresa guardados en empresa.csv."""
  st.subheader("🏢 Información de la Empresa")

  if tabla_empresa.empty:
    st.info("No se encontró información en el archivo empresa.csv.")
    return

  datos_empresa = tabla_empresa.iloc[0]

  with st.container(border=True):
    columna_izquierda, columna_derecha = st.columns(2)

    with columna_izquierda:
      st.write(
          f"**Razón Social / Nombre:**"
          f" {datos_empresa.get('nombre', 'No definido')}"
      )
      st.write(
          f"**Identificación (NIT/CC):**"
          f" {datos_empresa.get('nit_cc', 'No definido')}"
      )

    with columna_derecha:
      st.write(
          f"**Correo Electrónico:**"
          f" {datos_empresa.get('correo', 'No definido')}"
      )
      st.write(
          f"**ID de Empresa:** {datos_empresa.get('id', 'No definido')}"
      )