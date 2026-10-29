import pandas as pd
import streamlit as st


def mostrar_modulo_empresa(tabla_empresa: pd.DataFrame) -> None:
  """Muestra la información general de la empresa emisora."""
  st.subheader("🏢 Información de la Empresa")

  if tabla_empresa.empty:
    st.info("No se encontraron registros en el archivo empresa.csv.")
    return

  datos_empresa = tabla_empresa.iloc[0]

  with st.container(border=True):
    columna_uno, columna_dos = st.columns(2)
    with columna_uno:
      st.write(
          f"**Razón Social:** {datos_empresa.get('nombre', 'Sin definir')}"
      )
      st.write(
          f"**Identificación (NIT/CC):**"
          f" {datos_empresa.get('nit_cc', 'Sin definir')}"
      )
    with columna_dos:
      st.write(
          f"**Correo Electrónico:** {datos_empresa.get('correo', 'Sin definir')}"
      )
      st.write(
          f"**Identificador (ID):** {datos_empresa.get('id', 'Sin definir')}"
      )