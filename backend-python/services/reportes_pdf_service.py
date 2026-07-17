"""Generacion de los archivos PDF para los reportes de ventas."""

from datetime import date
from decimal import Decimal
from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


_CONFIGURACION_REPORTES: dict[str, dict[str, Any]] = {
    "detalle": {
        "titulo": "Detalle de Ventas",
        "columnas": ["Fecha", "Orden", "Cliente", "Vendedor", "Producto", "Cantidad", "Precio Unitario", "Total Linea"],
        "campos": ["Fecha", "NumeroOrden", "Cliente", "Vendedor", "Producto", "Cantidad", "PrecioUnitario", "TotalLinea"],
        "anchos": [2.0, 2.0, 3.0, 3.0, 4.5, 1.8, 2.6, 2.6],
    },
    "resumen": {
        "titulo": "Resumen de Ventas",
        "columnas": ["Cliente", "Vendedor", "Pedidos", "Total Vendido"],
        "campos": ["Cliente", "Vendedor", "NumeroPedidos", "TotalVendido"],
        "anchos": [6.0, 6.0, 3.0, 4.0],
    },
    "productos": {
        "titulo": "Ventas por Producto",
        "columnas": ["Producto", "Cantidad Vendida", "Total Vendido"],
        "campos": ["Producto", "CantidadVendida", "TotalVendido"],
        "anchos": [9.5, 4.0, 4.5],
    },
    "categorias": {
        "titulo": "Ventas por Categoria",
        "columnas": ["Categoria", "Cantidad Vendida", "Total Vendido"],
        "campos": ["Categoria", "CantidadVendida", "TotalVendido"],
        "anchos": [9.5, 4.0, 4.5],
    },
    "territorios": {
        "titulo": "Ventas por Territorio",
        "columnas": ["Territorio", "Categoria", "Producto", "Cantidad", "Total Vendido"],
        "campos": ["Territorio", "Categoria", "Producto", "Cantidad", "TotalVendido"],
        "anchos": [4.0, 4.0, 6.0, 2.2, 3.3],
    },
}


def generar_reporte_pdf(
    tipo_reporte: str,
    filas: list[Any],
    fecha_inicial: date | None,
    fecha_final: date | None,
    identificadores: dict[str, int | None],
) -> bytes:
    """Crea un PDF con todas las filas consultadas y los filtros aplicados."""
    configuracion = _CONFIGURACION_REPORTES[tipo_reporte]
    buffer = BytesIO()
    documento = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.4 * cm,
    )
    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle("TituloReporte", parent=estilos["Heading1"], textColor=colors.HexColor("#0d6efd"), alignment=TA_CENTER)
    subtitulo = ParagraphStyle("FiltroReporte", parent=estilos["Normal"], textColor=colors.HexColor("#495057"), alignment=TA_CENTER, leading=15)
    celda = ParagraphStyle("CeldaReporte", parent=estilos["BodyText"], fontSize=7.5, leading=9)

    contenido = [
        Paragraph(configuracion["titulo"], titulo),
        Spacer(1, 0.15 * cm),
        Paragraph(_texto_filtros(fecha_inicial, fecha_final, identificadores), subtitulo),
        Spacer(1, 0.45 * cm),
    ]
    datos = [configuracion["columnas"]]
    for fila in filas:
        datos.append([
            Paragraph(_formatear_valor(_obtener_valor(fila, campo)), celda)
            for campo in configuracion["campos"]
        ])

    tabla = Table(datos, colWidths=[ancho * cm for ancho in configuracion["anchos"]], repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#212529")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#ced4da")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    contenido.append(tabla)
    documento.build(contenido, onFirstPage=_pie_pagina, onLaterPages=_pie_pagina)
    return buffer.getvalue()


def _texto_filtros(fecha_inicial: date | None, fecha_final: date | None, identificadores: dict[str, int | None]) -> str:
    filtros: list[str] = []
    if fecha_inicial and fecha_final:
        filtros.append(f"Fecha: {fecha_inicial:%d/%m/%Y} a {fecha_final:%d/%m/%Y}")
    elif fecha_inicial:
        filtros.append(f"Fecha desde: {fecha_inicial:%d/%m/%Y}")
    elif fecha_final:
        filtros.append(f"Fecha hasta: {fecha_final:%d/%m/%Y}")
    for nombre, valor in identificadores.items():
        if valor is not None:
            filtros.append(f"{nombre}: {valor}")
    return "Reporte filtrado por: " + (" | ".join(filtros) if filtros else "Sin filtros aplicados")


def _obtener_valor(fila: Any, campo: str) -> Any:
    return getattr(fila, campo) if hasattr(fila, campo) else fila[campo]


def _formatear_valor(valor: Any) -> str:
    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")
    if isinstance(valor, Decimal):
        return f"${valor:,.2f}"
    return str(valor)


def _pie_pagina(canvas: Any, documento: Any) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6c757d"))
    canvas.drawRightString(28.5 * cm, 0.7 * cm, f"Pagina {documento.page}")
    canvas.restoreState()
