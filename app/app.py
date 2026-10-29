import os
import sys
import pandas as pd
import streamlit as st

# 1. Configuración de rutas para que reconozca 'modules' y 'database' desde la carpeta app/
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIRECTORIO_RAIZ = os.path.abspath(os.path.join(DIRECTORIO_ACTUAL, ".."))
if DIRECTORIO_RAIZ not in sys.path:
  sys.path.append(DIRECTORIO_RAIZ)

# 2. Importación de las funciones de cada módulo según tus archivos existentes
from modules.facturas import mostrar_modulo_empresa
from modules.pos import mostrar_modulo_pos
from modules.productos import mostrar_modulo_productos

# 3. Definición de rutas a la carpeta database
CARPETA_DATABASE = os.path.join(DIRECTORIO_RAIZ, "database")
ARCHIVO_USUARIOS = os.path.join(CARPETA_DATABASE, "usuarios.csv")
ARCHIVO_EMPRESA = os.path.join(CARPETA_DATABASE, "empresa.csv")
ARCHIVO_PRODUCTOS = os.path.join(CARPETA_DATABASE, "productos.csv")

# 4. Configuración visual general de Streamlit
st.set_page_config(
    page_title="AetherCode POS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# 5. Variables de estado de sesión
if "sesion_activa" not in st.session_state:
  st.session_state.sesion_activa = False
if "usuario_conectado" not in st.session_state:
  st.session_state.usuario_conectado = ""


def pantalla_login() -> None:
  """Muestra el formulario de inicio de sesión y valida contra usuarios.csv."""
  espacio_izquierdo, columna_central, espacio_derecho = st.columns([1, 1.2, 1])

  with columna_central:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container(border=True):
      st.title("⚡ AetherCode POS")
      st.caption("Punto de Venta Local")

      if not os.path.exists(ARCHIVO_USUARIOS):
        st.error(f"No se encontró el archivo de usuarios en: {ARCHIVO_USUARIOS}")
        return

      with st.form("formulario_inicio_sesion"):
        usuario_ingresado = st.text_input("Usuario")
        contrasena_ingresada = st.text_input("Contraseña", type="password")
        boton_ingreso = st.form_submit_button(
            "Iniciar Sesión", use_container_width=True
        )

        if boton_ingreso:
          tabla_usuarios = pd.read_csv(ARCHIVO_USUARIOS)
          usuario_valido = tabla_usuarios[
              (tabla_usuarios["user"].astype(str) == str(usuario_ingresado))
              & (
                  tabla_usuarios["user_pass"].astype(str)
                  == str(contrasena_ingresada)
              )
          ]

          if not usuario_valido.empty:
            st.session_state.sesion_activa = True
            st.session_state.usuario_conectado = usuario_ingresado
            st.rerun()
          else:
            st.error("Usuario o contraseña incorrectos.")


def pantalla_principal() -> None:
  """Carga los CSV y despacha la vista seleccionada."""
  tabla_empresa = (
      pd.read_csv(ARCHIVO_EMPRESA)
      if os.path.exists(ARCHIVO_EMPRESA)
      else pd.DataFrame()
  )
  tabla_productos = (
      pd.read_csv(ARCHIVO_PRODUCTOS)
      if os.path.exists(ARCHIVO_PRODUCTOS)
      else pd.DataFrame()
  )

  nombre_comercio = (
    tabla_empresa.iloc[0].get("nombre", "Empresa Local")
    if not tabla_empresa.empty
    else "AetherCode"
  )

  with st.sidebar:
    st.title("⚡ AetherCode")
    st.caption(f"🏢 {nombre_comercio}")
    st.divider()
    st.write(f"👤 **Cajero:** `{st.session_state.usuario_conectado}`")

    opcion_menu = st.radio(
        "Menú de Operación",
        ["🛒 Caja / Facturación", "📦 Inventario", "🏢 Datos de la Empresa"],
    )

    st.divider()
    if st.button("Cerrar Sesión", use_container_width=True):
      st.session_state.sesion_activa = False
      st.session_state.usuario_conectado = ""
      st.rerun()

  # Ejecución de la función según el módulo seleccionado
  if opcion_menu == "🛒 Caja / Facturación":
    mostrar_modulo_pos(tabla_productos, nombre_comercio)
  elif opcion_menu == "📦 Inventario":
    mostrar_modulo_productos(tabla_productos)
  elif opcion_menu == "🏢 Datos de la Empresa":
    mostrar_modulo_empresa(tabla_empresa)


# 6. Control de flujo
if not st.session_state.sesion_activa:
  pantalla_login()
else:
  pantalla_principal()