USE AdventureWorks2025;
GO

IF OBJECT_ID('dbo.AppUsuarioRol', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.AppUsuarioRol
    (
        UsuarioID INT NOT NULL,
        RolID INT NOT NULL,
        CONSTRAINT PK_AppUsuarioRol PRIMARY KEY (UsuarioID, RolID)
    );
END;
GO

IF OBJECT_ID('dbo.AppUsuario', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.AppUsuario
    (
        UsuarioID INT IDENTITY(1,1) NOT NULL,
        Usuario NVARCHAR(50) NOT NULL,
        PasswordHash NVARCHAR(255) NOT NULL,
        NombreCompleto NVARCHAR(120) NOT NULL,
        Correo NVARCHAR(150) NOT NULL,
        Activo BIT NOT NULL CONSTRAINT DF_AppUsuario_Activo DEFAULT (1),
        FechaCreacion DATETIME2(0) NOT NULL CONSTRAINT DF_AppUsuario_FechaCreacion DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT PK_AppUsuario PRIMARY KEY (UsuarioID),
        CONSTRAINT UQ_AppUsuario_Usuario UNIQUE (Usuario),
        CONSTRAINT UQ_AppUsuario_Correo UNIQUE (Correo)
    );
END;
GO

IF OBJECT_ID('dbo.AppRol', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.AppRol
    (
        RolID INT IDENTITY(1,1) NOT NULL,
        NombreRol NVARCHAR(50) NOT NULL,
        CONSTRAINT PK_AppRol PRIMARY KEY (RolID),
        CONSTRAINT UQ_AppRol_NombreRol UNIQUE (NombreRol)
    );
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = 'FK_AppUsuarioRol_AppUsuario'
)
BEGIN
    ALTER TABLE dbo.AppUsuarioRol
    ADD CONSTRAINT FK_AppUsuarioRol_AppUsuario
        FOREIGN KEY (UsuarioID) REFERENCES dbo.AppUsuario (UsuarioID);
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = 'FK_AppUsuarioRol_AppRol'
)
BEGIN
    ALTER TABLE dbo.AppUsuarioRol
    ADD CONSTRAINT FK_AppUsuarioRol_AppRol
        FOREIGN KEY (RolID) REFERENCES dbo.AppRol (RolID);
END;
GO

-- Consulta usuarios, incluyendo sus roles como texto separado por coma.
CREATE OR ALTER PROCEDURE dbo.USP_AppUsuarioListar
    @usuario_id INT = NULL,
    @incluir_inactivos BIT = 0
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        u.UsuarioID,
        u.Usuario,
        u.NombreCompleto,
        u.Correo,
        CAST(u.Activo AS BIT) AS Activo,
        u.FechaCreacion,
        STRING_AGG(r.NombreRol, ', ') WITHIN GROUP (ORDER BY r.NombreRol) AS Roles
    FROM dbo.AppUsuario AS u
    LEFT JOIN dbo.AppUsuarioRol AS ur
        ON u.UsuarioID = ur.UsuarioID
    LEFT JOIN dbo.AppRol AS r
        ON ur.RolID = r.RolID
    WHERE
        (@usuario_id IS NULL OR u.UsuarioID = @usuario_id)
        AND (@incluir_inactivos = 1 OR u.Activo = 1)
    GROUP BY
        u.UsuarioID,
        u.Usuario,
        u.NombreCompleto,
        u.Correo,
        u.Activo,
        u.FechaCreacion
    ORDER BY
        u.NombreCompleto;
END;
GO

-- Registra usuarios con PasswordHash generado por FastAPI.
CREATE OR ALTER PROCEDURE dbo.USP_AppUsuarioCrear
    @usuario NVARCHAR(50),
    @password_hash NVARCHAR(255),
    @nombre_completo NVARCHAR(120),
    @correo NVARCHAR(150),
    @activo BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dbo.AppUsuario
    (
        Usuario,
        PasswordHash,
        NombreCompleto,
        Correo,
        Activo
    )
    VALUES
    (
        @usuario,
        @password_hash,
        @nombre_completo,
        @correo,
        @activo
    );
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_AppUsuarioActualizar
    @usuario_id INT,
    @usuario NVARCHAR(50),
    @nombre_completo NVARCHAR(120),
    @correo NVARCHAR(150),
    @activo BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE dbo.AppUsuario
    SET
        Usuario = @usuario,
        NombreCompleto = @nombre_completo,
        Correo = @correo,
        Activo = @activo
    WHERE UsuarioID = @usuario_id;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_AppUsuarioEliminarLogico
    @usuario_id INT
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE dbo.AppUsuario
    SET Activo = 0
    WHERE UsuarioID = @usuario_id;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_AppUsuarioReiniciarPassword
    @usuario_id INT,
    @password_hash NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE dbo.AppUsuario
    SET PasswordHash = @password_hash
    WHERE UsuarioID = @usuario_id;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_AppRolListar
    @rol_id INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        RolID,
        NombreRol
    FROM dbo.AppRol
    WHERE @rol_id IS NULL OR RolID = @rol_id
    ORDER BY NombreRol;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_AppRolCrear
    @nombre_rol NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dbo.AppRol (NombreRol)
    VALUES (@nombre_rol);
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_AppRolActualizar
    @rol_id INT,
    @nombre_rol NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE dbo.AppRol
    SET NombreRol = @nombre_rol
    WHERE RolID = @rol_id;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_AppRolEliminar
    @rol_id INT
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM dbo.AppUsuarioRol WHERE RolID = @rol_id)
    BEGIN
        THROW 51000, 'No se puede eliminar un rol asignado a usuarios.', 1;
    END;

    DELETE FROM dbo.AppRol
    WHERE RolID = @rol_id;
END;
GO

-- Reemplaza las asignaciones de roles del usuario. @roles_csv acepta valores como '1,2,3'.
CREATE OR ALTER PROCEDURE dbo.USP_AppUsuarioAsignarRoles
    @usuario_id INT,
    @roles_csv NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRANSACTION;

    DELETE FROM dbo.AppUsuarioRol
    WHERE UsuarioID = @usuario_id;

    IF NULLIF(LTRIM(RTRIM(@roles_csv)), '') IS NOT NULL
    BEGIN
        INSERT INTO dbo.AppUsuarioRol (UsuarioID, RolID)
        SELECT
            @usuario_id,
            CAST(value AS INT)
        FROM STRING_SPLIT(@roles_csv, ',')
        WHERE
            TRY_CAST(value AS INT) IS NOT NULL
            AND EXISTS (
                SELECT 1
                FROM dbo.AppRol AS r
                WHERE r.RolID = TRY_CAST(value AS INT)
            );
    END;

    COMMIT TRANSACTION;
END;
GO
