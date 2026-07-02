namespace frontend_blazor.Client.Models
{
    public class ClienteModel
    {
        public int CustomerID { get; set; }
        public int? PersonID { get; set; }
        public string? FirstName { get; set; }
        public string? LastName { get; set; }
        public int TerritoryID { get; set; }
        public string? AccountNumber { get; set; }
    }
}