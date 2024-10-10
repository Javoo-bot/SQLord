import sqlite3

# Conectar a la base de datos SQLite (o crearla si no existe)
conn = sqlite3.connect("empresa_ad.db")
cursor = conn.cursor()

# Crear la tabla UnidadesOrganizativas
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS UnidadesOrganizativas (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre VARCHAR(255) NOT NULL,
        Dominio VARCHAR(255),
        UNIQUE(Nombre)
    );
"""
)

# Crear la tabla Objetos
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Objetos (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre VARCHAR(255) NOT NULL,
        Tipo VARCHAR(50) CHECK (Tipo IN ('usuario', 'computadora', 'grupo')),
        UnidadOrganizativaId INTEGER,
        FOREIGN KEY (UnidadOrganizativaId) REFERENCES UnidadesOrganizativas(Id)
    );
"""
)

# Crear la tabla Sincronizaciones
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Sincronizaciones (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        FechaSincronización DATETIME NOT NULL,
        Resultado VARCHAR(255)
    );
"""
)

# Crear la tabla Usuarios
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Usuarios (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre VARCHAR(255) NOT NULL,
        UsuarioPrincipalName VARCHAR(255),
        ms_DS_cloudExtensionAttribute1 VARCHAR(255),
        UnidadOrganizativaId INTEGER,
        FOREIGN KEY (UnidadOrganizativaId) REFERENCES UnidadesOrganizativas(Id)
    );
"""
)

# Crear la tabla Grupos
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Grupos (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre VARCHAR(255) NOT NULL,
        UnidadOrganizativaId INTEGER,
        FOREIGN KEY (UnidadOrganizativaId) REFERENCES UnidadesOrganizativas(Id)
    );
"""
)

# Crear la tabla Equipos
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Equipos (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre VARCHAR(255) NOT NULL,
        VersiónSistema VARCHAR(255),
        TipoPropiedad VARCHAR(50) CHECK (TipoPropiedad IN ('personal', 'corporativo')),
        UsuarioPrimarioId INTEGER,
        FOREIGN KEY (UsuarioPrimarioId) REFERENCES Usuarios(Id)
    );
"""
)

# Crear índices en las tablas
cursor.execute("CREATE INDEX IF NOT EXISTS idx_unidades_organ_name ON UnidadesOrganizativas(Nombre);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_objetos_name_tipo ON Objetos(Nombre, Tipo, UnidadOrganizativaId);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_sincronizaciones_fecha ON Sincronizaciones(FechaSincronización);")
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_usuarios_name_attr ON Usuarios(Nombre, UsuarioPrincipalName, ms_DS_cloudExtensionAttribute1);"
)
cursor.execute("CREATE INDEX IF NOT EXISTS idx_grupos_name_unidad ON Grupos(Nombre, UnidadOrganizativaId);")
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_equipos_nombre_sistema ON Equipos(Nombre, VersiónSistema, TipoPropiedad);"
)

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos creada con éxito.")
