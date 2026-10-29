import pandas as pd
import streamlit as st


def mostrar_modulo_productos(tabla_productos: pd.DataFrame) -> None:
  """Función para consultar el estado del inventario de productos."""
  st.subheader("📦 Inventario de Productos")

  if tabla_productos.empty:
    st.info("No hay productos registrados en el archivo productos.csv.")
    return

  # Indicadores principales
  columna_tipos, columna_total_stock = st.columns(2)
  with columna_tipos:
    conteo_referencias = len(tabla_productos)
    st.metric(
        label="Variedad de Productos", value=f"{conteo_referencias} referencias"
    )

  with columna_total_stock:
    unidades_totales = int(tabla_productos["stock"].sum())
    st.metric(
        label="Unidades Totales en Existencia",
        value=f"{unidades_totales} unidades",
    )

  st.divider()

  # Visualización de la tabla sin la columna de índice numérico por defecto
  st.dataframe(tabla_productos, use_container_width=True, hide_index=True)