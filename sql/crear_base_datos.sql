CREATE DATABASE DatosAbiertosDB;
GO

USE DatosAbiertosDB;
GO

CREATE TABLE RegistrosAPI (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_api NVARCHAR(100) NOT NULL UNIQUE,
    cod_depto NVARCHAR(20) NULL,
    departamento NVARCHAR(150) NULL,
    municipio NVARCHAR(150) NULL,
    json_original NVARCHAR(MAX) NULL,
    fecha_captura DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO
