-- Crear la tabla UnidadesOrganizativas
CREATE TABLE IF NOT EXISTS UnidadesOrganizativas (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    Dominio VARCHAR(255),
    UNIQUE(Nombre)
);

-- Crear la tabla Objetos
CREATE TABLE IF NOT EXISTS Objetos (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    Tipo VARCHAR(50) CHECK (Tipo IN ('usuario', 'computadora', 'grupo')),
    UnidadOrganizativaId INTEGER,
    FOREIGN KEY (UnidadOrganizativaId) REFERENCES UnidadesOrganizativas(Id)
);

-- Crear la tabla Sincronizaciones
CREATE TABLE IF NOT EXISTS Sincronizaciones (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    FechaSincronización DATETIME NOT NULL,
    Resultado VARCHAR(255)
);

-- Crear la tabla Usuarios
CREATE TABLE IF NOT EXISTS Usuarios (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    UsuarioPrincipalName VARCHAR(255),
    ms_DS_cloudExtensionAttribute1 VARCHAR(255),
    UnidadOrganizativaId INTEGER,
    FOREIGN KEY (UnidadOrganizativaId) REFERENCES UnidadesOrganizativas(Id)
);

-- Crear la tabla Grupos
CREATE TABLE IF NOT EXISTS Grupos (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    UnidadOrganizativaId INTEGER,
    FOREIGN KEY (UnidadOrganizativaId) REFERENCES UnidadesOrganizativas(Id)
);

-- Crear la tabla Equipos
CREATE TABLE IF NOT EXISTS Equipos (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    VersiónSistema VARCHAR(255),
    TipoPropiedad VARCHAR(50) CHECK (TipoPropiedad IN ('personal', 'corporativo')),
    UsuarioPrimarioId INTEGER,
    FOREIGN KEY (UsuarioPrimarioId) REFERENCES Usuarios(Id)
);

-- Crear índices para mejorar el rendimiento de las consultas
CREATE INDEX IF NOT EXISTS idx_unidades_organ_name ON UnidadesOrganizativas(Nombre);
CREATE INDEX IF NOT EXISTS idx_objetos_name_tipo ON Objetos(Nombre, Tipo, UnidadOrganizativaId);
CREATE INDEX IF NOT EXISTS idx_sincronizaciones_fecha ON Sincronizaciones(FechaSincronización);
CREATE INDEX IF NOT EXISTS idx_usuarios_name_attr ON Usuarios(Nombre, UsuarioPrincipalName, ms_DS_cloudExtensionAttribute1);
CREATE INDEX IF NOT EXISTS idx_grupos_name_unidad ON Grupos(Nombre, UnidadOrganizativaId);
CREATE INDEX IF NOT EXISTS idx_equipos_nombre_sistema ON Equipos(Nombre, VersiónSistema, TipoPropiedad);

SELECT name FROM sqlite_master WHERE type='table';

DELETE FROM sqlite_sequence;


