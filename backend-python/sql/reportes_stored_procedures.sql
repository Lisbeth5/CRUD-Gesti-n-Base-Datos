USE AdventureWorks2025;
GO

-- Reporte 1: detalle transaccional de ventas con filtros opcionales.
CREATE OR ALTER PROCEDURE Sales.USP_ReporteDetalleVentas
    @fecha_inicial DATE = NULL,
    @fecha_final DATE = NULL,
    @cliente_id INT = NULL,
    @vendedor_id INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        CAST(soh.OrderDate AS DATE) AS Fecha,
        soh.SalesOrderNumber AS NumeroOrden,
        COALESCE(CONCAT(pc.FirstName, ' ', pc.LastName), s.Name, c.AccountNumber) AS Cliente,
        COALESCE(CONCAT(pv.FirstName, ' ', pv.LastName), 'Sin vendedor') AS Vendedor,
        p.Name AS Producto,
        sod.OrderQty AS Cantidad,
        CAST(sod.UnitPrice AS DECIMAL(18, 2)) AS PrecioUnitario,
        CAST(sod.LineTotal AS DECIMAL(18, 2)) AS TotalLinea
    FROM Sales.SalesOrderHeader AS soh
    INNER JOIN Sales.SalesOrderDetail AS sod
        ON soh.SalesOrderID = sod.SalesOrderID
    INNER JOIN Production.Product AS p
        ON sod.ProductID = p.ProductID
    INNER JOIN Sales.Customer AS c
        ON soh.CustomerID = c.CustomerID
    LEFT JOIN Person.Person AS pc
        ON c.PersonID = pc.BusinessEntityID
    LEFT JOIN Sales.Store AS s
        ON c.StoreID = s.BusinessEntityID
    LEFT JOIN Person.Person AS pv
        ON soh.SalesPersonID = pv.BusinessEntityID
    WHERE
        (@fecha_inicial IS NULL OR CAST(soh.OrderDate AS DATE) >= @fecha_inicial)
        AND (@fecha_final IS NULL OR CAST(soh.OrderDate AS DATE) <= @fecha_final)
        AND (@cliente_id IS NULL OR soh.CustomerID = @cliente_id)
        AND (@vendedor_id IS NULL OR soh.SalesPersonID = @vendedor_id)
    ORDER BY
        soh.OrderDate DESC,
        soh.SalesOrderNumber,
        p.Name;
END;
GO

-- Reporte 2: resumen de ventas por cliente y vendedor.
CREATE OR ALTER PROCEDURE Sales.USP_ReporteResumenVentas
    @fecha_inicial DATE = NULL,
    @fecha_final DATE = NULL,
    @cliente_id INT = NULL,
    @vendedor_id INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        COALESCE(CONCAT(pc.FirstName, ' ', pc.LastName), s.Name, c.AccountNumber) AS Cliente,
        COALESCE(CONCAT(pv.FirstName, ' ', pv.LastName), 'Sin vendedor') AS Vendedor,
        COUNT(DISTINCT soh.SalesOrderID) AS NumeroPedidos,
        CAST(SUM(sod.LineTotal) AS DECIMAL(18, 2)) AS TotalVendido
    FROM Sales.SalesOrderHeader AS soh
    INNER JOIN Sales.SalesOrderDetail AS sod
        ON soh.SalesOrderID = sod.SalesOrderID
    INNER JOIN Sales.Customer AS c
        ON soh.CustomerID = c.CustomerID
    LEFT JOIN Person.Person AS pc
        ON c.PersonID = pc.BusinessEntityID
    LEFT JOIN Sales.Store AS s
        ON c.StoreID = s.BusinessEntityID
    LEFT JOIN Person.Person AS pv
        ON soh.SalesPersonID = pv.BusinessEntityID
    WHERE
        (@fecha_inicial IS NULL OR CAST(soh.OrderDate AS DATE) >= @fecha_inicial)
        AND (@fecha_final IS NULL OR CAST(soh.OrderDate AS DATE) <= @fecha_final)
        AND (@cliente_id IS NULL OR soh.CustomerID = @cliente_id)
        AND (@vendedor_id IS NULL OR soh.SalesPersonID = @vendedor_id)
    GROUP BY
        COALESCE(CONCAT(pc.FirstName, ' ', pc.LastName), s.Name, c.AccountNumber),
        COALESCE(CONCAT(pv.FirstName, ' ', pv.LastName), 'Sin vendedor')
    ORDER BY
        TotalVendido DESC;
END;
GO

-- Reporte 3: resumen de unidades y valor vendido por producto.
CREATE OR ALTER PROCEDURE Sales.USP_ReporteVentasPorProducto
    @fecha_inicial DATE = NULL,
    @fecha_final DATE = NULL,
    @producto_id INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        p.Name AS Producto,
        SUM(sod.OrderQty) AS CantidadVendida,
        CAST(SUM(sod.LineTotal) AS DECIMAL(18, 2)) AS TotalVendido
    FROM Sales.SalesOrderHeader AS soh
    INNER JOIN Sales.SalesOrderDetail AS sod
        ON soh.SalesOrderID = sod.SalesOrderID
    INNER JOIN Production.Product AS p
        ON sod.ProductID = p.ProductID
    WHERE
        (@fecha_inicial IS NULL OR CAST(soh.OrderDate AS DATE) >= @fecha_inicial)
        AND (@fecha_final IS NULL OR CAST(soh.OrderDate AS DATE) <= @fecha_final)
        AND (@producto_id IS NULL OR p.ProductID = @producto_id)
    GROUP BY
        p.Name
    ORDER BY
        TotalVendido DESC;
END;
GO

-- Reporte 4: resumen de unidades y valor vendido por categoria.
CREATE OR ALTER PROCEDURE Sales.USP_ReporteVentasPorCategoria
    @fecha_inicial DATE = NULL,
    @fecha_final DATE = NULL,
    @categoria_id INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        pc.Name AS Categoria,
        SUM(sod.OrderQty) AS CantidadVendida,
        CAST(SUM(sod.LineTotal) AS DECIMAL(18, 2)) AS TotalVendido
    FROM Sales.SalesOrderHeader AS soh
    INNER JOIN Sales.SalesOrderDetail AS sod
        ON soh.SalesOrderID = sod.SalesOrderID
    INNER JOIN Production.Product AS p
        ON sod.ProductID = p.ProductID
    INNER JOIN Production.ProductSubcategory AS ps
        ON p.ProductSubcategoryID = ps.ProductSubcategoryID
    INNER JOIN Production.ProductCategory AS pc
        ON ps.ProductCategoryID = pc.ProductCategoryID
    WHERE
        (@fecha_inicial IS NULL OR CAST(soh.OrderDate AS DATE) >= @fecha_inicial)
        AND (@fecha_final IS NULL OR CAST(soh.OrderDate AS DATE) <= @fecha_final)
        AND (@categoria_id IS NULL OR pc.ProductCategoryID = @categoria_id)
    GROUP BY
        pc.Name
    ORDER BY
        TotalVendido DESC;
END;
GO

-- Reporte 5: resumen por territorio, categoria y producto.
CREATE OR ALTER PROCEDURE Sales.USP_ReporteVentasPorTerritorio
    @fecha_inicial DATE = NULL,
    @fecha_final DATE = NULL,
    @territorio_id INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        st.Name AS Territorio,
        pc.Name AS Categoria,
        p.Name AS Producto,
        SUM(sod.OrderQty) AS Cantidad,
        CAST(SUM(sod.LineTotal) AS DECIMAL(18, 2)) AS TotalVendido
    FROM Sales.SalesOrderHeader AS soh
    INNER JOIN Sales.SalesOrderDetail AS sod
        ON soh.SalesOrderID = sod.SalesOrderID
    INNER JOIN Sales.SalesTerritory AS st
        ON soh.TerritoryID = st.TerritoryID
    INNER JOIN Production.Product AS p
        ON sod.ProductID = p.ProductID
    INNER JOIN Production.ProductSubcategory AS ps
        ON p.ProductSubcategoryID = ps.ProductSubcategoryID
    INNER JOIN Production.ProductCategory AS pc
        ON ps.ProductCategoryID = pc.ProductCategoryID
    WHERE
        (@fecha_inicial IS NULL OR CAST(soh.OrderDate AS DATE) >= @fecha_inicial)
        AND (@fecha_final IS NULL OR CAST(soh.OrderDate AS DATE) <= @fecha_final)
        AND (@territorio_id IS NULL OR st.TerritoryID = @territorio_id)
    GROUP BY
        st.Name,
        pc.Name,
        p.Name
    ORDER BY
        st.Name,
        pc.Name,
        TotalVendido DESC;
END;
GO
