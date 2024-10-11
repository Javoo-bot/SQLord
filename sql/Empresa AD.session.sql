-- Crear tabla Unidades Organizativas (OU)
CREATE TABLE OU (
    idOU INT PRIMARY KEY,
    nombre VARCHAR(50),
    descripcion TEXT,
    padre_idOU INT
);
-- Crear tabla Usuarios
CREATE TABLE Usuarios (
    idUsuario INT PRIMARY KEY,
    nombre VARCHAR(50),
    apellidos VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(50),
    OU_idOU INT,
    msDScloudExtensionAttribute1 VARCHAR(100)
);
-- Crear tabla Grupos
CREATE TABLE Grupos (
    idGrupo INT PRIMARY KEY,
    nombre VARCHAR(50),
    descripcion TEXT,
    OU_idOU INT
);
-- Crear tabla Sincronización
CREATE TABLE Sincronizacion (
    idSincronizacion INT PRIMARY KEY,
    fecha_sincronizacion DATETIME,
    resultado_sincronizacion VARCHAR(20)
);
-- Crear tabla Dispositivos
CREATE TABLE Dispositivos (
    idDispositivo INT PRIMARY KEY,
    nombre VARCHAR(100),
    tipo_dispositivo VARCHAR(50),
    estado_dispositivo VARCHAR(20),
    usuario_principal INT
);
-- Crear tabla Licencias
CREATE TABLE Licencias (
    idLicencia INT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    grupo_idGrupo INT
);

SELECT name
FROM sqlite_master
WHERE type = 'table';

-- Insertar datos en la tabla OU
INSERT INTO OU (idOU, nombre, descripcion, padre_idOU)
VALUES (
        1,
        'AAD-Synced',
        'Unidad organizativa para sincronizar con Azure AD',
        NULL
    ),
    (
        2,
        'Usuarios',
        'Unidad organizativa para usuarios',
        1
    ),
    (
        3,
        'Grupos',
        'Unidad organizativa para grupos',
        1
    );
-- Insertar datos en la tabla Usuarios
INSERT INTO Usuarios (
        idUsuario,
        nombre,
        apellidos,
        email,
        password,
        OU_idOU,
        msDScloudExtensionAttribute1
    )
VALUES (
        1,
        'domuser2',
        'apellidos',
        'domuser2@castur.local',
        'contraseña',
        2,
        'domuser2@castur.onmicrosoft.com'
    ),
    (
        2,
        'oturuser1',
        'apellidos',
        'oturuser1@castur.local',
        'contraseña',
        2,
        'oturuser1@castur.onmicrosoft.com'
    );
-- Insertar datos en la tabla Grupos
INSERT INTO Grupos (idGrupo, nombre, descripcion, OU_idOU)
VALUES (1, 'Otur', 'Grupo para usuarios de Otur', 3),
    (
        2,
        'F1_Intune',
        'Grupo para asignar licencias F1 de Intune',
        3
    );
-- Insertar datos en la tabla Sincronizacion
INSERT INTO Sincronizacion (
        idSincronizacion,
        fecha_sincronizacion,
        resultado_sincronizacion
    )
VALUES (1, '2023-02-20 10:00:00', 'éxito'),
    (2, '2023-02-20 11:00:00', 'éxito');
-- Insertar datos en la tabla Dispositivos
INSERT INTO Dispositivos (
        idDispositivo,
        nombre,
        tipo_dispositivo,
        estado_dispositivo,
        usuario_principal
    )
VALUES (
        1,
        'Equipo de pruebas',
        'computadora',
        'corporativo',
        1
    ),
    (
        2,
        'Equipo personal',
        'computadora',
        'personal',
        2
    );

-- Insertar datos en la tabla Licencias
INSERT INTO Licencias (idLicencia, nombre, descripcion, grupo_idGrupo)
VALUES (1, 'F1_Intune', 'Licencia F1 de Intune', 2);
