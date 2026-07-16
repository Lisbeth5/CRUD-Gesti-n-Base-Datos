USE AdventureWorks2025;
GO

CREATE OR ALTER PROCEDURE dbo.USP_TerritorioListar
    @territorio_id INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        TerritoryID,
        Name,
        CountryRegionCode,
        [Group],
        SalesYTD,
        SalesLastYear,
        CostYTD,
        CostLastYear
    FROM Sales.SalesTerritory
    WHERE (@territorio_id IS NULL OR TerritoryID = @territorio_id)
    ORDER BY Name;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_TerritorioCrear
    @name NVARCHAR(50),
    @country_region_code NVARCHAR(3),
    @group NVARCHAR(50),
    @sales_ytd DECIMAL(19,4) = 0,
    @sales_last_year DECIMAL(19,4) = 0,
    @cost_ytd DECIMAL(19,4) = 0,
    @cost_last_year DECIMAL(19,4) = 0
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Sales.SalesTerritory
    (
        Name,
        CountryRegionCode,
        [Group],
        SalesYTD,
        SalesLastYear,
        CostYTD,
        CostLastYear
    )
    VALUES
    (
        @name,
        @country_region_code,
        @group,
        @sales_ytd,
        @sales_last_year,
        @cost_ytd,
        @cost_last_year
    );
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_TerritorioActualizar
    @territorio_id INT,
    @name NVARCHAR(50),
    @country_region_code NVARCHAR(3),
    @group NVARCHAR(50),
    @sales_ytd DECIMAL(19,4) = 0,
    @sales_last_year DECIMAL(19,4) = 0,
    @cost_ytd DECIMAL(19,4) = 0,
    @cost_last_year DECIMAL(19,4) = 0
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE Sales.SalesTerritory
    SET
        Name = @name,
        CountryRegionCode = @country_region_code,
        [Group] = @group,
        SalesYTD = @sales_ytd,
        SalesLastYear = @sales_last_year,
        CostYTD = @cost_ytd,
        CostLastYear = @cost_last_year
    WHERE TerritoryID = @territorio_id;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_TerritorioEliminar
    @territorio_id INT
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM Sales.SalesTerritory
    WHERE TerritoryID = @territorio_id;
END;
GO
