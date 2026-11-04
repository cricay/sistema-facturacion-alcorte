# Sistema de Facturación para la Carnicería AL CORTE

## Descripción del proyecto

Aplicación web desarrollada para apoyar la gestión administrativa y comercial de la carnicería AL CORTE. Hace parte del proyecto formativo del programa Análisis y Desarrollo de Software (ADSO) del Servicio Nacional de Aprendizaje (SENA).

El sistema está orientado a centralizar la información del negocio y facilitar el registro, consulta y organización de sus operaciones.

## Objetivo

Desarrollar un sistema web que facilite la gestión de productos, categorías, clientes, usuarios e inventario, como base para los procesos de facturación y control comercial de la carnicería AL CORTE.

## Tecnologías utilizadas

- Python
- Flask
- MySQL
- HTML
- CSS
- Bootstrap
- Visual Studio Code
- Git y GitHub

## Módulos implementados

- **Inicio:** página principal del sistema.
- **Productos:** consulta y registro de productos.
- **Clientes:** consulta y registro de clientes.
- **Categorías:** consulta y registro de categorías.
- **Usuarios:** consulta y registro de usuarios, con asignación de roles.
- **Inventario:** consulta y gestión de la información de existencias.

## Organización del proyecto

El código se encuentra organizado por responsabilidades:

- `src/controllers/`: controladores y rutas de los módulos.
- `src/templates/`: plantillas HTML organizadas por módulo.
- `src/static/css/`: hojas de estilo de la aplicación.
- `src/utils/`: funciones auxiliares, incluida la gestión de consultas a la base de datos.
- `conexion.py`: configuración de la conexión a MySQL mediante variables de entorno.

## Configuración y ejecución

1. Instalar las dependencias indicadas en `requirements.txt`.
2. Crear un archivo `.env` en la raíz del proyecto con las variables de conexión a MySQL y la clave secreta de Flask.
3. Configurar la base de datos `facturacion_alcorte` y sus tablas.
4. Iniciar la aplicación desde la carpeta raíz con:

   ```powershell
   python -m src.app
   ```

5. Abrir en el navegador: `http://127.0.0.1:5000`.

El archivo `.env` contiene información privada y no debe publicarse en GitHub.

## Estado del proyecto

**En desarrollo.** Se cuenta con una estructura modular en Flask y con los módulos de inicio, productos, clientes, categorías, usuarios e inventario implementados. El sistema continúa en proceso de construcción, integración y validación de sus funcionalidades.

## Autoría

Proyecto formativo del programa Análisis y Desarrollo de Software (ADSO) del SENA.
