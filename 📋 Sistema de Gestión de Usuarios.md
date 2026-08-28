# 📋 Sistema de Gestión de Usuarios

Aplicación de escritorio desarrollada en **Python** utilizando **Tkinter** para la interfaz gráfica y **SQLite** para la gestión de la base de datos.

El sistema permite registrar, consultar, actualizar y eliminar usuarios desde una interfaz gráfica organizada, ajustable y responsiva. También permite asociar imágenes y archivos a cada usuario.

---

## 🚀 Características

- ✅ Registro de usuarios.
- ✅ Actualización de usuarios.
- ✅ Eliminación de usuarios.
- ✅ Limpieza del formulario.
- ✅ Búsqueda de usuarios.
- ✅ Visualización de todos los usuarios.
- ✅ Selección de registros directamente desde la tabla.
- ✅ Carga automática de los datos seleccionados al formulario.
- ✅ Registro del nombre y apellido.
- ✅ Dirección y ciudad.
- ✅ Código postal.
- ✅ Selección de género.
- ✅ Estado del usuario: activo/inactivo.
- ✅ Tipo de usuario.
- ✅ Selección y almacenamiento de imágenes.
- ✅ Vista previa de imágenes.
- ✅ Asociación de archivos adjuntos.
- ✅ Base de datos SQLite creada automáticamente.
- ✅ Interfaz adaptable al tamaño de la ventana.
- ✅ Botones con colores diferenciados para las operaciones.
- ✅ Icono personalizado para la ventana.
- ✅ Atajos de teclado para facilitar el uso.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Tkinter | Interfaz gráfica |
| SQLite | Base de datos |
| Pillow | Manejo y visualización de imágenes |
| pathlib | Manejo de rutas |
| shutil | Copia de imágenes y archivos |

Las librerías principales utilizadas en el proyecto se encuentran en las primeras líneas del programa.

---

## 📂 Estructura del proyecto

Al ejecutar el programa, se utilizan las siguientes carpetas:

```text
Sistema-Gestion-Usuarios/
│
├── Descargar Sistema_Gestion_Usuarios_COLORES.py
├── impresora.png.png
│
├── database/
│   └── usuarios.db
│
├── imagenes/
│   └── fotografías de usuarios
│
└── archivos/
    └── documentos adjuntos
```

Las carpetas `database`, `imagenes` y `archivos` se crean automáticamente si no existen.

---

## 🗄️ Base de datos

El sistema utiliza una base de datos SQLite llamada:

```text
usuarios.db
```

La tabla principal se denomina:

```text
usuarios
```

La tabla contiene los siguientes campos:

```text
id
nombre
apellido
direccion
ciudad
codigo_postal
genero
estado
tipo_usuario
imagen
archivo
```

La tabla se crea automáticamente mediante `CREATE TABLE IF NOT EXISTS`, por lo que no es necesario crear manualmente la base de datos.

---

## 👤 Información del usuario

Cada registro puede almacenar:

- **Nombre**
- **Apellido**
- **Dirección**
- **Ciudad**
- **Código postal**
- **Género**
- **Estado**
- **Tipo de usuario**
- **Imagen**
- **Archivo adjunto**

El campo `estado` permite determinar si el usuario se encuentra **Activo** o **Inactivo**.

---

## 👥 Tipos de usuario

Actualmente el sistema permite seleccionar:

```text
Administrador
Supervisor
Empleado
Cliente
Invitado
```

---

## 🖼️ Gestión de imágenes

El sistema permite seleccionar imágenes desde el computador.

Formatos contemplados:

```text
JPG
JPEG
PNG
GIF
BMP
```

La imagen seleccionada se copia automáticamente a la carpeta:

```text
imagenes/
```

y posteriormente se muestra en el área de vista previa.

Para visualizar las imágenes correctamente se utiliza **Pillow**. El programa contempla además el caso en que Pillow no esté instalado.

---

## 📎 Archivos adjuntos

El sistema permite seleccionar cualquier archivo desde el computador.

El archivo seleccionado se copia automáticamente a:

```text
archivos/
```

y queda asociado al registro correspondiente del usuario.

---

## 🔄 Operaciones CRUD

### ➕ Insertar

Permite crear un nuevo usuario.

Antes de guardar se valida que:

- El nombre haya sido ingresado.
- El apellido haya sido ingresado.
- Se haya seleccionado un tipo de usuario.



### ✏️ Actualizar

Para actualizar un usuario se selecciona primero un registro de la tabla.

Después se modifican los datos y se utiliza el botón:

```text
ACTUALIZAR
```

El registro se actualiza directamente en SQLite.

### 🗑️ Eliminar

Permite eliminar un usuario seleccionado.

Antes de eliminarlo, el sistema solicita confirmación al usuario.

### 🧹 Limpiar

Restablece los campos del formulario y elimina la selección actual.

También limpia la vista previa de la imagen y el archivo adjunto mostrado.

---

## 🔎 Búsqueda

El sistema incluye un buscador que permite consultar usuarios utilizando diferentes campos.

La búsqueda puede realizarse por:

- ID
- Nombre
- Apellido
- Dirección
- Ciudad
- Código postal
- Género
- Estado
- Tipo de usuario



También existe el botón:

```text
MOSTRAR TODOS
```

para volver a cargar todos los registros.

---

## 📊 Tabla de usuarios

Los registros se muestran mediante un `Treeview` de Tkinter.

Las columnas disponibles son:

```text
ID
Nombre
Apellido
Dirección
Ciudad
Código Postal
Género
Estado
Tipo Usuario
```

La tabla incorpora desplazamiento vertical y horizontal para facilitar la visualización de los registros.

Al seleccionar un registro, sus datos se cargan nuevamente en el formulario para poder consultarlos o modificarlos.

---

## 🎨 Interfaz gráfica

La interfaz utiliza una paleta de colores para diferenciar las principales acciones:

| Acción | Color |
|---|---|
| INSERTAR | 🟢 Verde |
| ACTUALIZAR | 🟠 Naranja |
| ELIMINAR | 🔴 Rojo |
| LIMPIAR | 🔵 Azul oscuro |
| SALIR | ⚫ Gris |
| BUSCAR | 🔵 Azul |
| MOSTRAR TODOS | 🟢 Turquesa |
| SELECCIONAR IMAGEN | 🔷 Celeste |
| ADJUNTAR ARCHIVO | 🟣 Morado |

Los colores están definidos mediante constantes dentro del programa.

La ventana utiliza una distribución basada en `grid`, permitiendo que diferentes elementos de la interfaz se adapten al tamaño de la ventana.

---

## 🖨️ Icono de la aplicación

La ventana utiliza una imagen personalizada como icono:

```text
impresora.png.png
```

El icono se carga desde la misma carpeta del programa mediante `BASE_DIR`.

> **Importante:** si cambias el nombre de la imagen, debes actualizar también el nombre utilizado en `PhotoImage`.

---

## ⌨️ Atajos de teclado

El sistema incorpora:

### `Ctrl + F`

Coloca el cursor directamente en el campo de búsqueda.

### `Esc`

Limpia el formulario.



---

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/TU-REPOSITORIO.git
```

Entrar en la carpeta:

```bash
cd TU-REPOSITORIO
```

### 2. Comprobar Python

Se recomienda utilizar una versión moderna de Python.

Comprobar la instalación:

```bash
python --version
```

### 3. Instalar Pillow

Para utilizar la visualización de imágenes:

```bash
pip install pillow
```

### 4. Ejecutar el programa

```bash
python "Descargar Sistema_Gestion_Usuarios_COLORES.py"
```

---

## ⚙️ Funcionamiento

Al iniciar el programa:

1. Se crea o abre la base de datos SQLite.
2. Se verifica la existencia de la tabla `usuarios`.
3. Se cargan los registros existentes.
4. Se muestra el formulario de gestión.
5. El usuario puede crear, consultar, modificar o eliminar registros.

La inicialización de la base de datos y la carga inicial de registros se realizan al final del programa.

---

## 🔐 Validaciones

El sistema realiza validaciones básicas antes de registrar o actualizar usuarios.

Actualmente se comprueba que:

```text
Nombre → obligatorio
Apellido → obligatorio
Tipo de usuario → obligatorio
```

Si algún dato requerido falta, se muestra un mensaje de advertencia y el cursor vuelve al campo correspondiente.

---

## 🎯 Objetivo del proyecto

El objetivo de este proyecto es desarrollar una aplicación CRUD de escritorio utilizando Python, Tkinter y SQLite, aplicando conceptos de:

- Programación orientada a objetos y programación estructurada de interfaz.
- Interfaces gráficas.
- Bases de datos.
- Operaciones CRUD.
- Manejo de archivos.
- Manejo de imágenes.
- Validación de datos.
- Organización de proyectos.
- Diseño de interfaces adaptables.

---

## 📚 Proyecto académico

Este proyecto puede utilizarse como práctica para aprender:

```text
Python
Tkinter
SQLite
CRUD
Pillow
Manejo de archivos
Interfaces gráficas
Bases de datos
```

---

## 👨‍💻 Autor

**Luis Alberto Olarte Castaño**

Proyecto desarrollado con fines académicos y de aprendizaje.

---

## 📄 Licencia

Este proyecto puede ser utilizado con fines educativos y de aprendizaje.

Si deseas utilizarlo o modificarlo para otros fines, se recomienda mantener la referencia al autor original.

---

## ⭐ Contribuciones

Las sugerencias y mejoras son bienvenidas.

Puedes realizar un `fork`, crear una nueva rama, realizar tus cambios y posteriormente enviar un `pull request`.

```bash
git checkout -b nueva-funcionalidad
git add .
git commit -m "Agrega nueva funcionalidad"
git push origin nueva-funcionalidad
```

---

## 📌 Estado del proyecto

**En desarrollo 🚧**

El sistema funciona como aplicación CRUD de escritorio y puede continuar ampliándose con nuevas funcionalidades, mejoras visuales, seguridad, reportes y administración avanzada de usuarios.