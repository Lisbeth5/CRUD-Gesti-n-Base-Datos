namespace frontend_blazor.Client.Models
{
    public class DetalleVentaModel
    {
        public DateTime Fecha { get; set; }
        public string? NumeroOrden { get; set; }
        public string? Cliente { get; set; }
        public string? Vendedor { get; set; }
        public string? Producto { get; set; }
        public int Cantidad { get; set; }
        public decimal PrecioUnitario { get; set; }
        public decimal TotalLinea { get; set; }
    }

    public class ResumenVentaModel
    {
        public string? Cliente { get; set; }
        public string? Vendedor { get; set; }
        public int NumeroPedidos { get; set; }
        public decimal TotalVendido { get; set; }
    }

    public class VentaProductoModel
    {
        public string? Producto { get; set; }
        public int CantidadVendida { get; set; }
        public decimal TotalVendido { get; set; }
    }

    public class VentaCategoriaModel
    {
        public string? Categoria { get; set; }
        public int CantidadVendida { get; set; }
        public decimal TotalVendido { get; set; }
    }

    public class VentaTerritorioModel
    {
        public string? Territorio { get; set; }
        public string? Categoria { get; set; }
        public string? Producto { get; set; }
        public int Cantidad { get; set; }
        public decimal TotalVendido { get; set; }
    }
}
