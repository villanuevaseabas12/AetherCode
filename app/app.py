import os
import sys
import pandas as pd
import streamlit as st

# 1. Configuración de rutas del proyecto
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIRECTORIO_RAIZ = os.path.abspath(os.path.join(DIRECTORIO_ACTUAL, ".."))
CARPETA_IMAGENES = os.path.join(DIRECTORIO_RAIZ, "images")
RUTA_LOGO = os.path.join(CARPETA_IMAGENES, "logo.png")

if DIRECTORIO_RAIZ not in sys.path:
    sys.path.append(DIRECTORIO_RAIZ)

# 2. Configuración de página e ícono de pestaña
st.set_page_config(
    page_title="AetherCode POS",
    page_icon=RUTA_LOGO if os.path.exists(RUTA_LOGO) else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. CSS: Diseño limpio, tipografía corporativa y encapsulamiento estricto
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Fondo general suave */
        .stApp {
            background-color: #f4f6fa;
            color: #0f172a;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Sidebar sobrio y corporativo */
        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0 !important;
            padding-top: 1.5rem !important;
        }

        /* Tarjeta encapsulada del Login */
        .login-box {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 2.5rem 2rem 2rem 2rem;
            box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.03);
            margin-top: 1.5rem;
        }

        /* Forzar fondo blanco y texto oscuro en inputs */
        .stTextInput input {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
            padding: 0.65rem 0.85rem !important;
            font-size: 0.95rem !important;
        }

        .stTextInput input:focus {
            border-color: #4f46e5 !important;
            box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.15) !important;
        }

        .stTextInput label {
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            color: #334155 !important;
            margin-bottom: 0.25rem !important;
        }

        /* Botones de navegación del Sidebar */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            border: 1px solid #e2e8f0 !important;
            background-color: #ffffff !important;
            color: #475569 !important;
            padding: 0.6rem 1rem !important;
            transition: all 0.2s ease !important;
            text-align: left !important;
        }

        .stButton > button:hover {
            border-color: #c7d2fe !important;
            background-color: #f5f3ff !important;
            color: #4f46e5 !important;
        }

        /* Botón de acción principal / Envío de formulario */
        button[kind="primary"], .stFormSubmitButton > button {
            background-color: #4f46e5 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            padding: 0.65rem 1rem !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25) !important;
        }

        button[kind="primary"]:hover, .stFormSubmitButton > button:hover {
            background-color: #4338ca !important;
            box-shadow: 0 4px 14px rgba(67, 56, 202, 0.35) !important;
        }
    </style>
""", unsafe_allow_html=True)

# 4. Importaciones locales de módulos
from modules.pos import mostrar_modulo_pos
from modules.productos import mostrar_modulo_productos
from modules.facturas import mostrar_modulo_empresa

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
if "modulo_actual" not in st.session_state:
    st.session_state.modulo_actual = "pos"


def pantalla_login() -> None:
    """Pantalla de Login con tarjeta unificada sin elementos residuales."""
    col_izq, col_centro, col_der = st.columns([1, 1.15, 1])

    with col_centro:
        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            if os.path.exists(RUTA_LOGO):
                col_sub_izq, col_sub_centro, col_sub_der = st.columns([1, 2.2, 1])
                with col_sub_centro:
                    st.image(RUTA_LOGO, use_container_width=True)
            else:
                st.markdown("<h3 style='text-align: center; color: #4f46e5; margin: 0; font-weight: 700;'>AetherCode</h3>", unsafe_allow_html=True)

            st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.88rem; margin: 0.5rem 0 1.5rem 0;'>Punto de Venta y Facturación</p>", unsafe_allow_html=True)

            if not os.path.exists(ARCHIVO_USUARIOS):
                st.error(f"No se encontró el archivo de usuarios: {ARCHIVO_USUARIOS}")
                return

            with st.form("formulario_inicio_sesion"):
                usuario_ingresado = st.text_input("Usuario", placeholder="Ingresa tu usuario").strip()
                contrasena_ingresada = st.text_input("Contraseña", type="password", placeholder="••••••••")
                st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
                boton_ingreso = st.form_submit_button("Iniciar Sesión", use_container_width=True)

                if boton_ingreso:
                    tabla_usuarios = pd.read_csv(ARCHIVO_USUARIOS)
                    usuario_valido = tabla_usuarios[
                        (tabla_usuarios["user"].astype(str) == str(usuario_ingresado)) &
                        (tabla_usuarios["user_pass"].astype(str) == str(contrasena_ingresada))
                    ]

                    if not usuario_valido.empty:
                        st.session_state.sesion_activa = True
                        st.session_state.usuario_conectado = usuario_ingresado
                        st.session_state.modulo_actual = "pos"
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas.")


def pantalla_principal() -> None:
    """Carga los CSV, presenta el header institucional y despacha el módulo seleccionado."""
    tabla_empresa = pd.read_csv(ARCHIVO_EMPRESA) if os.path.exists(ARCHIVO_EMPRESA) else pd.DataFrame()
    tabla_productos = pd.read_csv(ARCHIVO_PRODUCTOS) if os.path.exists(ARCHIVO_PRODUCTOS) else pd.DataFrame()

    nombre_tienda = (
        tabla_empresa.iloc[0].get("nombre", "AetherCode Store")
        if not tabla_empresa.empty
        else "AetherCode Store"
    )
    nombre_operador = st.session_state.usuario_conectado

    with st.sidebar:
        if os.path.exists(RUTA_LOGO):
            st.image(RUTA_LOGO, use_container_width=True)
        else:
            st.markdown("<h3 style='color: #4f46e5; margin: 0; font-weight: 700;'>AetherCode</h3>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)

        # Navegación con etiquetas limpias
        if st.button("Caja y Facturación", use_container_width=True, type="primary" if st.session_state.modulo_actual == "pos" else "secondary"):
            st.session_state.modulo_actual = "pos"
            st.rerun()

        if st.button("Inventario de Productos", use_container_width=True, type="primary" if st.session_state.modulo_actual == "productos" else "secondary"):
            st.session_state.modulo_actual = "productos"
            st.rerun()

        if st.button("Datos de la Empresa", use_container_width=True, type="primary" if st.session_state.modulo_actual == "empresa" else "secondary"):
            st.session_state.modulo_actual = "empresa"
            st.rerun()

        st.divider()

        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.sesion_activa = False
            st.session_state.usuario_conectado = ""
            st.session_state.modulo_actual = "pos"
            st.rerun()

    # Header superior limpio
    st.markdown(f"""
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
                Operador: <span style="color: #4338ca;">{nombre_operador}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Despacho de la función del módulo
    if st.session_state.modulo_actual == "pos":
        mostrar_modulo_pos(tabla_productos, nombre_tienda)
    elif st.session_state.modulo_actual == "productos":
        mostrar_modulo_productos(tabla_productos)
    elif st.session_state.modulo_actual == "empresa":
        mostrar_modulo_empresa(tabla_empresa)


# Control de flujo principal
if not st.session_state.sesion_activa:
    pantalla_login()
else:
    pantalla_principal()