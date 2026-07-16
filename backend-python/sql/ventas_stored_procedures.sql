USE AdventureWorks2025;
GO

CREATE OR ALTER PROCEDURE dbo.USP_VentaListar
    @venta_id INT = NULL,
    @cliente_id INT = NULL,
    @vendedor_id INT = NULL,
    @fecha_desde DATE = NULL,
    @fecha_hasta DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        h.SalesOrderID AS VentaID,
        h.CustomerID AS ClienteID,
        h.SalesPersonID AS VendedorID,
        h.TerritoryID AS TerritorioID,
        h.OrderDate AS FechaVenta,
        CASE h.Status
            WHEN 1 THEN 'Pendiente'
            WHEN 2 THEN 'Aprobada'
            WHEN 3 THEN 'En proceso'
            WHEN 4 THEN 'Rechazada'
            WHEN 5 THEN 'Completada'
            ELSE 'Desconocido'
        END AS Estado,
        CAST(0 AS BIT) AS Anulada,
        NULL AS FechaAnulacion,
        h.TotalDue AS TotalVenta,
        NULL AS Observaciones,
        0 AS ItemCount
    FROM Sales.SalesOrderHeader h
    WHERE (@venta_id IS NULL OR h.SalesOrderID = @venta_id)
      AND (@cliente_id IS NULL OR h.CustomerID = @cliente_id)
      AND (@vendedor_id IS NULL OR h.SalesPersonID = @vendedor_id)
      AND (@fecha_desde IS NULL OR CAST(h.OrderDate AS DATE) >= @fecha_desde)
      AND (@fecha_hasta IS NULL OR CAST(h.OrderDate AS DATE) <= @fecha_hasta)
    ORDER BY h.OrderDate DESC, h.SalesOrderID DESC;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_VentaObtener
    @venta_id INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        h.SalesOrderID AS VentaID,
        h.CustomerID AS ClienteID,
        h.SalesPersonID AS VendedorID,
        h.TerritoryID AS TerritorioID,
        h.OrderDate AS FechaVenta,
        CASE h.Status
            WHEN 1 THEN 'Pendiente'
            WHEN 2 THEN 'Aprobada'
            WHEN 3 THEN 'En proceso'
            WHEN 4 THEN 'Rechazada'
            WHEN 5 THEN 'Completada'
            ELSE 'Desconocido'
        END AS Estado,
        CAST(0 AS BIT) AS Anulada,
        NULL AS FechaAnulacion,
        h.TotalDue AS TotalVenta,
        NULL AS Observaciones,
        0 AS ItemCount
    FROM Sales.SalesOrderHeader h
    WHERE h.SalesOrderID = @venta_id;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_VentaDetalleListar
    @venta_id INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        d.SalesOrderDetailID AS VentaDetalleID,
        d.SalesOrderID AS VentaID,
        d.ProductID AS ProductoID,
        d.OrderQty AS Cantidad,
        d.UnitPrice AS PrecioUnitario,
        d.LineTotal AS Importe,
        CAST(1 AS BIT) AS Activo
    FROM Sales.SalesOrderDetail d
    WHERE d.SalesOrderID = @venta_id
    ORDER BY d.SalesOrderDetailID;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_VentaCrear
    @cliente_id INT,
    @vendedor_id INT = NULL,
    @territorio_id INT = NULL,
    @observaciones NVARCHAR(250) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @venta_id INT;

    INSERT INTO Sales.SalesOrderHeader
    (
        RevisionNumber,
        OrderDate,
        DueDate,
        ShipDate,
        Status,
        OnlineOrderFlag,
        PurchaseOrderNumber,
        AccountNumber,
        CustomerID,
        SalesPersonID,
        TerritoryID,
        BillToAddressID,
        ShipToAddressID,
        ShipMethodID,
        SubTotal,
        TaxAmt,
        Freight,
        Comment
    )
    VALUES
    (
        1,
        CAST(GETDATE() AS DATE),
        CAST(DATEADD(DAY, 7, GETDATE()) AS DATE),
        CAST(DATEADD(DAY, 2, GETDATE()) AS DATE),
        5,
        0,
        NULL,
        NULL,
        @cliente_id,
        @vendedor_id,
        @territorio_id,
        1,
        1,
        5,
        0,
        0,
        0,
        @observaciones
    );

    SET @venta_id = SCOPE_IDENTITY();
    SELECT @venta_id AS VentaID;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_VentaActualizar
    @venta_id INT,
    @cliente_id INT,
    @vendedor_id INT = NULL,
    @territorio_id INT = NULL,
    @observaciones NVARCHAR(250) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE Sales.SalesOrderHeader
    SET
        CustomerID = @cliente_id,
        SalesPersonID = @vendedor_id,
        TerritoryID = @territorio_id,
        Comment = @observaciones
    WHERE SalesOrderID = @venta_id;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_VentaDetalleAgregar
    @venta_id INT,
    @producto_id INT,
    @cantidad INT,
    @precio_unitario DECIMAL(19,4)
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Sales.SalesOrderDetail
    (
        SalesOrderID,
        CarrierTrackingNumber,
        OrderQty,
        ProductID,
        SpecialOfferID,
        UnitPrice,
        UnitPriceDiscount,
        rowguid,
        ModifiedDate
    )
    VALUES
    (
        @venta_id,
        NULL,
        @cantidad,
        @producto_id,
        1,
        @precio_unitario,
        0,
        NEWID(),
        GETDATE()
    );
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_VentaDetalleActualizar
    @venta_id INT,
    @venta_detalle_id INT,
    @producto_id INT,
    @cantidad INT,
    @precio_unitario DECIMAL(19,4)
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE Sales.SalesOrderDetail
    SET
        ProductID = @producto_id,
        OrderQty = @cantidad,
        UnitPrice = @precio_unitario,
        ModifiedDate = GETDATE()
    WHERE SalesOrderID = @venta_id AND SalesOrderDetailID = @venta_detalle_id;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_VentaDetalleEliminar
    @venta_id INT,
    @venta_detalle_id INT
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM Sales.SalesOrderDetail
    WHERE SalesOrderID = @venta_id AND SalesOrderDetailID = @venta_detalle_id;
END;
GO

CREATE OR ALTER PROCEDURE dbo.USP_VentaAnular
    @venta_id INT,
    @motivo NVARCHAR(250) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE Sales.SalesOrderHeader
    SET
        Status = 4,
        Comment = COALESCE(@motivo, Comment)
    WHERE SalesOrderID = @venta_id;
END;
GO
