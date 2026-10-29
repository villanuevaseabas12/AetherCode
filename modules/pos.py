import pandas as pd
import streamlit as st


def mostrar_modulo_pos(
    tabla_productos: pd.DataFrame, nombre_empresa: str
) -> None:
  """Función principal del Punto de Venta (POS).

  Permite ingresar los datos del comprador, seleccionar productos y calcular
  totales.
  """
  st.subheader("🛒 Terminal Punto de Venta (POS)")

  # Validación de inventario cargado
  if tabla_productos.empty:
    st.warning("No hay productos cargados en la base de datos para vender.")
    return

  columna_formulario, columna_resumen = st.columns([1.5, 1], gap="large")

  with columna_formulario:
    # 1. Datos del cliente
    with st.container(border=True):
      st.markdown("#### 1. Datos del Cliente")
      sub_columna_nombre, sub_columna_documento, sub_columna_correo = st.columns(3)
      with sub_columna_nombre:
        nombre_cliente = st.text_input(
            "Nombre o Razón Social", value="Consumidor Final"
        )
      with sub_columna_documento:
        documento_cliente = st.text_input("Cédula o NIT", value="222222222222")

      with sub_columna_correo:
        correo_cliente = st.text_input(
            "Correo Electrónico (*)", value="", placeholder="ejemplo@correo.com"
        )

    # 2. Selección de artículo y cálculo individual
    with st.container(border=True):
      st.markdown("#### 2. Selección de Producto")
      lista_nombres_productos = tabla_productos["nombre"].tolist()
      producto_seleccionado = st.selectbox(
          "Seleccione el producto", lista_nombres_productos
      )

      # Búsqueda de información del producto seleccionado
      fila_producto = tabla_productos[
          tabla_productos["nombre"] == producto_seleccionado
      ].iloc[0]
      precio_unitario = float(fila_producto["precio"])
      stock_disponible = int(fila_producto["stock"])

      col_precio, col_stock, col_cantidad = st.columns(3)
      with col_precio:
        st.info(f"Precio Unitario:\n**${precio_unitario:,.0f}**")
      with col_stock:
        st.info(f"Stock Disponible:\n**{stock_disponible} und**")
      with col_cantidad:
        cantidad_seleccionada = st.number_input(
            "Cantidad a vender",
            min_value=1,
            max_value=max(1, stock_disponible),
            value=1,
        )

      aplica_iva = st.checkbox("¿Cobrar IVA (19%)?", value=False)

  with columna_resumen:
    # 3. Resumen y cobro
    with st.container(border=True):
      st.markdown("#### 💳 Total de la Venta")

      subtotal_venta = precio_unitario * cantidad_seleccionada
      monto_iva = (subtotal_venta * 0.19) if aplica_iva else 0.0
      total_factura = subtotal_venta + monto_iva

      st.metric(label="Total a Pagar", value=f"${total_factura:,.0f}")
      st.divider()

      st.write(f"• **Emisor:** {nombre_empresa}")
      st.write(f"• **Cliente:** {nombre_cliente} ({documento_cliente})")
      st.write(
          f"• **Detalle:** {producto_seleccionado} x {cantidad_seleccionada}"
          " unidades"
      )
      st.write(f"• **Subtotal:** ${subtotal_venta:,.0f}")
      st.write(f"• **IVA liquidado:** ${monto_iva:,.0f}")

      st.markdown("<br>", unsafe_allow_html=True)
      boton_generar = st.button(
          "✅ Generar Factura", type="primary", use_container_width=True
      )
      
      if boton_generar:
        # Validación del correo electrónico obligatorio
        if not correo_cliente.strip():
          st.error("⚠️ El campo de Correo Electrónico es obligatorio para generar la factura.")
        else:
          st.success(
              f"Factura emitida exitosamente por un total de"
              f" ${total_factura:,.0f}."
          )
          # Aquí puedes agregar posteriormente la lógica para guardar la factura o limpiar datos