# SQLord 📊🗃️

## Description

This project converts unstructured data (Word and Excel files) from SharePoint into an SQL database for efficient querying. 🎯

## Technologies

- **Python** 🐍
- **SQLAlchemy** for SQL connection ⚙️
- **Pandas** for Excel data handling 📑
- **python-docx** to read Word files 📝
- **Office365-REST-Python-Client** for SharePoint access 🌐

## Purpose

Automate data extraction from documents and store them in SQL for quick and structured querying. 🚀

## How to Use

1. **Subir los Archivos a VS Code**
   - Puedes subir tus archivos directamente a Visual Studio Code o hacerlo a través de una API, según lo que mejor se adapte a tus necesidades.

2. **Crear un Archivo de Python para Verificar los Archivos**
   - Desarrolla un script en Python que compruebe si los archivos necesarios han sido subidos correctamente al entorno de trabajo.

3. **Estructurar la Información con un Modelo de Lenguaje**
   - Utiliza un modelo que pueda identificar imágenes y texto en documentos de Word.
   - Pide al modelo que genere tablas estructuradas para utilizar en SQL, facilitando la posterior extracción de datos siguiendo este esquema.

4. **Instalar SQLTools y el Driver SQLite**
   - **SQLTools**: Instala este paquete para gestionar la base de datos dentro de VS Code.
   - **SQLTools SQLite**: Instala este driver para habilitar la conexión con bases de datos SQLite.

5. **Crear el Archivo de la Base de Datos**
   - Crea manualmente un archivo llamado `empresa_ad.db`. Este archivo servirá como el punto de conexión entre tu script en VS Code y la base de datos SQLite.

6. **Configurar una Nueva Conexión en SQLTools**
   - Utiliza el comando `SQL Tools Management: New Connection`.
   - Completa los siguientes campos:
     - **Name**: `EmpresaAD`
     - **Database File**: Proporciona la ruta completa donde se encuentra el archivo `empresa_ad.db`.
   - Haz clic en **Test Connection** para verificar que la conexión se ha establecido correctamente.

7. **Verificar y Guardar la Base de Datos**
   - Se abrirá un archivo con la base de datos llamada "Empresa AD" en rojo dentro de VS Code.
   - Al cerrar la sesión, la base de datos se guardará automáticamente en tu directorio de trabajo.

8. **Ejecutar Consultas SQL**
   - Escribe tus consultas SQL en el editor de VS Code.
   - Para ejecutar una consulta, selecciona el fragmento de código correspondiente y utiliza la opción **Run Selected Query**.
   - Es importante ejecutar las consultas en porciones seleccionadas para evitar errores de ejecución.

9. **Enriquecer tabla**
   - En vez de procesar el texto como esquemas voy a añadir un paso intermedio que es crear a partir de las imagenes texto que contenga instrucciones
   - Puedo añadir nivel de importancia de la intruccion
   - Añadir error sino sigo la intruccion
   - Paso fundamental: Chatgpt es capaz de entender una imagen inventada sobre procedimientos y crear instrucciones
   - Es mejor almacenar y estructurar los datos de manera clara (diferenciando entre imágenes y texto) antes de pasárselos al modelo de lenguaje (LLM)
   - Truco 1: si tengo el mismo modelo en dos scripts se ejecuta en las dos pantallas a la vez
   - El modelo LLM aunque sea vision necesita texto para contextualizar la imagen porque sino no puede analizarla
   - link: [def]
   - No me deja usar Vision LLm porque tengo poco contexto. Mi idea de analizar imagenes y texto no funciona. Quizas es por poca capacidad del modelo.Pasamos a LLM imagen
   - Vamos a usar un modelo LLM para analizar solo las imagenes
   - Añadir procesamiento de imagenes a DocPicture
   - En vez de almacenar imagenes las puedo pasar como informacino binaria porque total voy a cargarlas en el LLM.

10. **Upgrade enfoque**
   -En vez de subir a sql, subir directamente a PostgreSQL
   -Continuamos en carpeta Tribe 

## Reminder

Have fun querying your data! 😎

[def]: https://medium.com/@alice.yang_10652/extract-images-from-word-documents-with-python-88144ca3c35e
