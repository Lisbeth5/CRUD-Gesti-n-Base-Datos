namespace frontend_blazor.Client.Models
{
    public class UsuarioModel
    {
        public int UsuarioID { get; set; }
        public string? Usuario { get; set; }
        public string? NombreCompleto { get; set; }
        public string? Correo { get; set; }
        public bool Activo { get; set; }
        public DateTime FechaCreacion { get; set; }
        public string? Roles { get; set; }
    }

    public class UsuarioCreateModel
    {
        public string Usuario { get; set; } = "";
        public string Password { get; set; } = "";
        public string NombreCompleto { get; set; } = "";
        public string Correo { get; set; } = "";
        public bool Activo { get; set; } = true;
    }

    public class UsuarioUpdateModel
    {
        public string Usuario { get; set; } = "";
        public string NombreCompleto { get; set; } = "";
        public string Correo { get; set; } = "";
        public bool Activo { get; set; } = true;
    }

    public class ReiniciarPasswordModel
    {
        public int UsuarioID { get; set; }
        public string NuevaPassword { get; set; } = "";
    }

    public class RolModel
    {
        public int RolID { get; set; }
        public string? NombreRol { get; set; }
    }

    public class RolRequestModel
    {
        public string NombreRol { get; set; } = "";
    }

    public class AsignarRolesModel
    {
        public int UsuarioID { get; set; }
        public List<int> RolesID { get; set; } = new();
    }
}
