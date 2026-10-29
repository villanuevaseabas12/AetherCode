import os
import sys
import pandas as pd
import streamlit as st

# 1. Configuración de rutas
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIRECTORIO_RAIZ = os.path.abspath(os.path.join(DIRECTORIO_ACTUAL, ".."))
CARPETA_IMAGENES = os.path.join(DIRECTORIO_RAIZ, "images")
RUTA_LOGO = os.path.join(CARPETA_IMAGENES, "logo.png")

if DIRECTORIO_RAIZ not in sys.path:
  sys.path.append(DIRECTORIO_RAIZ)

# 2. Configuración de página
st.set_page_config(
    page_title="AetherCode POS",
    page_icon=RUTA_LOGO if os.path.exists(RUTA_LOGO) else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# 3. CSS Corporativo
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp {
            background-color: #f4f6fa;
            color: #0f172a;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0 !important;
            padding-top: 1.5rem !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 14px !important;
            padding: 1.5rem !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03) !important;
        }

        .stTextInput input {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
            padding: 0.65rem 0.85rem !important;
        }

        .stTextInput input:focus {
            border-color: #4f46e5 !important;
            box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.15) !important;
        }

        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            border: 1px solid #e2e8f0 !important;
            background-color: #ffffff !important;
            color: #475569 !important;
            padding: 0.6rem 1rem !important;
        }

        .stButton > button:hover {
            border-color: #c7d2fe !important;
            background-color: #f5f3ff !important;
            color: #4f46e5 !important;
        }

        button[kind="primary"], .stFormSubmitButton > button {
            background-color: #4f46e5 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25) !important;
        }

        button[kind="primary"]:hover, .stFormSubmitButton > button:hover {
            background-color: #4338ca !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# 4. Importaciones locales
from modules.empresa import mostrar_modulo_empresa
from modules.pos import mostrar_modulo_pos
from modules.productos import mostrar_modulo_productos

# 5. Rutas a archivos CSV en database/
CARPETA_DATABASE = os.path.join(DIRECTORIO_RAIZ, "database")
ARCHIVO_USUARIOS = os.path.join(CARPETA_DATABASE, "usuarios.csv")
ARCHIVO_EMPRESA = os.path.join(CARPETA_DATABASE, "empresa.csv")
ARCHIVO_PRODUCTOS = os.path.join(CARPETA_DATABASE, "productos.csv")

# 6. Variables de control de estado
if "sesion_activa" not in st.session_state:
  st.session_state.sesion_activa = False
if "usuario_conectado" not in st.session_state:
  st.session_state.usuario_conectado = ""
if "empresa_id_conectada" not in st.session_state:
  st.session_state.empresa_id_conectada = None
if "modulo_actual" not in st.session_state:
  st.session_state.modulo_actual = "pos"


def pantalla_login() -> None:
  col_izq, col_centro, col_der = st.columns([1, 1.15, 1])

  with col_centro:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
      if os.path.exists(RUTA_LOGO):
        c1, c2, c3 = st.columns([1, 2.2, 1])
        with c2:
          st.image(RUTA_LOGO, use_container_width=True)
      else:
        st.markdown(
            "<h3 style='text-align: center; color: #4f46e5;'>AetherCode</h3>",
            unsafe_allow_html=True,
        )

      st.markdown(
          "<p style='text-align: center; color: #64748b; font-size: 0.88rem;"
          " margin-bottom: 1.5rem;'>Punto de Venta & Facturación</p>",
          unsafe_allow_html=True,
      )

      if not os.path.exists(ARCHIVO_USUARIOS):
        st.error(f"No se encontró el archivo: {ARCHIVO_USUARIOS}")
        return

      with st.form("formulario_inicio_sesion"):
        usuario_ingresado = st.text_input(
            "Usuario", placeholder="Ingresa tu usuario"
        )
        contrasena_ingresada = st.text_input(
            "Contraseña", type="password", placeholder="••••••••"
        )
        st.markdown(
            "<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True
        )
        boton_ingreso = st.form_submit_button(
            "Iniciar Sesión", use_container_width=True
        )

        if boton_ingreso:
          tabla_usuarios = pd.read_csv(ARCHIVO_USUARIOS)
          coincidencia = tabla_usuarios[
              (tabla_usuarios["user"].astype(str) == str(usuario_ingresado))
              & (
                  tabla_usuarios["user_pass"].astype(str)
                  == str(contrasena_ingresada)
              )
          ]

          if not coincidencia.empty:
            fila_usuario = coincidencia.iloc[0]
            st.session_state.sesion_activa = True
            st.session_state.usuario_conectado = usuario_ingresado
            st.session_state.empresa_id_conectada = int(
                fila_usuario.get("empresa_id", 1)
            )
            st.session_state.modulo_actual = "pos"
            st.rerun()
          else:
            st.error("Credenciales incorrectas.")


def pantalla_principal() -> None:
  empresa_id_actual = st.session_state.empresa_id_conectada

  # 1. Cargar empresa y filtrar por id
  tabla_empresa_completa = (
      pd.read_csv(ARCHIVO_EMPRESA)
      if os.path.exists(ARCHIVO_EMPRESA)
      else pd.DataFrame()
  )
  empresa_filtrada = pd.DataFrame()

  if not tabla_empresa_completa.empty:
    empresa_filtrada = tabla_empresa_completa[
        tabla_empresa_completa["id"].astype(str) == str(empresa_id_actual)
    ]

  nombre_tienda = (
      empresa_filtrada.iloc[0].get("nombre", "AetherCode Store")
      if not empresa_filtrada.empty
      else "AetherCode Store"
  )

  # 2. Cargar y filtrar productos exclusivamente de esta empresa
  tabla_productos_completa = (
      pd.read_csv(ARCHIVO_PRODUCTOS)
      if os.path.exists(ARCHIVO_PRODUCTOS)
      else pd.DataFrame()
  )
  productos_empresa = pd.DataFrame()

  if not tabla_productos_completa.empty:
    productos_empresa = tabla_productos_completa[
        tabla_productos_completa["empresa_id"].astype(str)
        == str(empresa_id_actual)
    ]

  # 3. Sidebar de navegación
  with st.sidebar:
    if os.path.exists(RUTA_LOGO):
      st.image(RUTA_LOGO, use_container_width=True)
    else:
      st.markdown(
          "<h3 style='color: #4f46e5; font-weight: 700;'>AetherCode</h3>",
          unsafe_allow_html=True,
      )

    st.markdown(
        "<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True
    )

    if st.button(
        "Caja y Facturación",
        use_container_width=True,
        type=(
            "primary" if st.session_state.modulo_actual == "pos" else "secondary"
        ),
    ):
      st.session_state.modulo_actual = "pos"
      st.rerun()

    if st.button(
        "Inventario de Productos",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.modulo_actual == "productos"
            else "secondary"
        ),
    ):
      st.session_state.modulo_actual = "productos"
      st.rerun()

    if st.button(
        "Datos de la Empresa",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.modulo_actual == "empresa"
            else "secondary"
        ),
    ):
      st.session_state.modulo_actual = "empresa"
      st.rerun()

    st.divider()

    if st.button("Cerrar Sesión", use_container_width=True):
      st.session_state.sesion_activa = False
      st.session_state.usuario_conectado = ""
      st.session_state.empresa_id_conectada = None
      st.session_state.modulo_actual = "pos"
      st.rerun()

  # 4. Header superior con los datos de la empresa autenticada
  st.markdown(
      f"""
        <div style="
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 0.85rem 1.5rem;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        ">
            <div>
                <span style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; font-weight: 700;">Empresa Emisora</span>
                <h4 style="margin: 0; color: #0f172a; font-weight: 700;">{nombre_tienda}</h4>
            </div>
            <div style="
                background-color: #f5f3ff;
                border: 1px solid #ddd6fe;
                padding: 0.35rem 0.9rem;
                border-radius: 20px;
                color: #4f46e5;
                font-weight: 600;
                font-size: 0.85rem;
            ">
                Operador: <span style="color: #4338ca;">{st.session_state.usuario_conectado}</span>
            </div>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # 5. Ejecución del módulo activo
  if st.session_state.modulo_actual == "pos":
    mostrar_modulo_pos(productos_empresa, nombre_tienda)
  elif st.session_state.modulo_actual == "productos":
    mostrar_modulo_productos(productos_empresa)
  elif st.session_state.modulo_actual == "empresa":
    mostrar_modulo_empresa(ARCHIVO_EMPRESA, empresa_id_actual)


if not st.session_state.sesion_activa:
  pantalla_login()
else:
  pantalla_principal()