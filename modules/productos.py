import os
import pandas as pd
import streamlit as st

DB_PATH = "database/productos.csv"

def cargar_productos() -> pd.DataFrame:
    """Carga la base de datos de productos desde el archivo CSV."""
    if os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) > 0:
        df = pd.read_csv(DB_PATH)
        # Rellenar valores vacíos o nulos para evitar errores en el SelectboxColumn
        if "tipo_impuesto" in df.columns:
            df["tipo_impuesto"] = df["tipo_impuesto"].fillna("IVA 19%")
        return df
    else:
        df_default = pd.DataFrame(columns=["id", "nombre", "precio", "stock", "tipo_impuesto"])
        df_default.to_csv(DB_PATH, index=False)
        return df_default

def guardar_cambios_productos(df: pd.DataFrame):
    """Guarda el DataFrame actualizado en el archivo CSV."""
    df.to_csv(DB_PATH, index=False)

def mostrar_modulo_productos(tabla_productos: pd.DataFrame = None):
    """Vista de Streamlit para la gestión completa (CRUD) de productos."""
    st.subheader("📦 Gestión de productos")
    st.markdown(
        "Aquí puedes **agregar** nuevos productos, **modificar** información haciendo doble clic, "
        "o **eliminar** registros seleccionando las filas y guardando los cambios."
    )

    if tabla_productos is None:
        df_productos = cargar_productos()
    else:
        df_productos = tabla_productos
        if "tipo_impuesto" in df_productos.columns:
            df_productos["tipo_impuesto"] = df_productos["tipo_impuesto"].fillna("IVA 19%")

    # Usamos st.data_editor permitiendo seleccionar el tipo de impuesto mediante un desplegable
    df_editado = st.data_editor(
        df_productos,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_productos",
        column_config={
            "id": st.column_config.NumberColumn("ID / Código", step=1),
            "nombre": st.column_config.TextColumn("Nombre del Producto", required=True),
            "precio": st.column_config.NumberColumn("Precio Unitario ($)", min_value=0, format="$%d"),
            "stock": st.column_config.NumberColumn("Stock Disponible", min_value=0, step=1),
            "tipo_impuesto": st.column_config.SelectboxColumn(
                "Tipo de Impuesto",
                help="Selecciona la tarifa aplicable para este producto",
                options=["IVA 19%", "IVA 5%", "Excluido (0%)"],
                required=True
            )
        }
    )

    # Botón para persistir los cambios en el archivo CSV
    if st.button("💾 Guardar Cambios en la Base de Datos", type="primary"):
        guardar_cambios_productos(df_editado)
        st.success("¡Inventario actualizado y guardado correctamente en el sistema!")
        st.rerun()