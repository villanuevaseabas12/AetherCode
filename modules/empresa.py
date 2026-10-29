import os
import pandas as pd
import streamlit as st


def mostrar_modulo_empresa(
    ruta_archivo_empresa: str, empresa_id_usuario: int
) -> None:
  """Permite visualizar y actualizar los datos de la empresa vinculada a la sesión."""
  st.subheader("Datos de la Empresa")

  if not os.path.exists(ruta_archivo_empresa):
    st.error("No se encontró el archivo de base de datos de empresas.")
    return

  tabla_empresas = pd.read_csv(ruta_archivo_empresa)

  # Filtro estricto por el ID de la empresa del usuario activo
  registro_empresa = tabla_empresas[
      tabla_empresas["id"].astype(str) == str(empresa_id_usuario)
  ]

  if registro_empresa.empty:
    st.warning(
        f"No se encontró registro para la empresa con ID {empresa_id_usuario}."
    )
    return

  indice_empresa = registro_empresa.index[0]
  datos_actuales = registro_empresa.iloc[0]

  with st.container(border=True):
    st.markdown("#### Configuración de Información Fiscal")

    with st.form("formulario_edicion_empresa"):
      columna_izquierda, columna_derecha = st.columns(2)

      with columna_izquierda:
        nuevo_nombre = st.text_input(
            "Nombre / Razón Social",
            value=str(datos_actuales.get("nombre", "")),
        )
        nuevo_nit = st.text_input(
            "NIT o Documento",
            value=str(datos_actuales.get("nit_cc", "")),
        )

      with columna_derecha:
        nuevo_correo = st.text_input(
            "Correo Electrónico",
            value=str(datos_actuales.get("correo", "")),
        )
        st.text_input(
            "ID Empresa (Asignado)",
            value=str(empresa_id_usuario),
            disabled=True,
        )

      st.markdown("<br>", unsafe_allow_html=True)
      boton_guardar = st.form_submit_button(
          "Guardar Cambios", type="primary", use_container_width=True
      )

      if boton_guardar:
        # Modificación directa de la fila correspondiente
        tabla_empresas.loc[indice_empresa, "nombre"] = nuevo_nombre
        tabla_empresas.loc[indice_empresa, "nit_cc"] = nuevo_nit
        tabla_empresas.loc[indice_empresa, "correo"] = nuevo_correo

        # Sobrescritura en el archivo CSV
        tabla_empresas.to_csv(ruta_archivo_empresa, index=False)
        st.success("Información actualizada exitosamente.")
        st.rerun()