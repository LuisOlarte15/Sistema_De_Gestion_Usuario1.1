# ============================================================
# SISTEMA DE GESTIÓN DE USUARIOS
# TKINTER + SQLITE
# INTERFAZ ORGANIZADA, AJUSTABLE Y RESPONSIVA
# ============================================================

from tkinter import *
from tkinter import ttk, messagebox, filedialog
import sqlite3
import re
from pathlib import Path
import shutil

try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False


# ============================================================
# RUTAS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "usuarios.db"

IMAGENES_DIR = BASE_DIR / "imagenes"
IMAGENES_DIR.mkdir(exist_ok=True)

ARCHIVOS_DIR = BASE_DIR / "archivos"
ARCHIVOS_DIR.mkdir(exist_ok=True)


# ============================================================
# BASE DE DATOS
# ============================================================

def conectar():
    return sqlite3.connect(DB_PATH)


def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            direccion TEXT,
            ciudad TEXT,
            codigo_postal TEXT,
            genero TEXT,
            estado TEXT,
            tipo_usuario TEXT,
            correo TEXT,
            puesto TEXT,
            tipo_sangre TEXT,
            observaciones TEXT,
            imagen TEXT,
            archivo TEXT
        )
    """)

    cursor.execute("PRAGMA table_info(usuarios)")
    columnas_existentes = {fila[1] for fila in cursor.fetchall()}

    for columna in ("correo", "puesto", "tipo_sangre", "observaciones"):
        if columna not in columnas_existentes:
            cursor.execute(f"ALTER TABLE usuarios ADD COLUMN {columna} TEXT")

    conexion.commit()
    conexion.close()


# ============================================================
# VENTANA
# ============================================================

ventana = Tk()
ventana.title("SISTEMA DE GESTION USUARIOS")

icono = PhotoImage(file=BASE_DIR / "impresora.png.png")
ventana.iconphoto(True, icono)


ventana.geometry("1120x720")
ventana.minsize(950, 620)
ventana.configure(bg="#F2F2F2")

# ============================================================
# BARRA DE MENÚ
# ============================================================

barra_menu = Menu(ventana)

# BBDD USUARIOS
menu_bbdd = Menu(barra_menu, tearoff=0)
menu_bbdd.add_command(
    label="Mostrar todos los usuarios",
    command=lambda: mostrar_todos()
)
menu_bbdd.add_command(
    label="Limpiar formulario",
    command=lambda: limpiar()
)
menu_bbdd.add_separator()
menu_bbdd.add_command(
    label="Salir",
    command=lambda: salir()
)
barra_menu.add_cascade(
    label="MENU",
    menu=menu_bbdd
)

# AYUDA
menu_ayuda = Menu(barra_menu, tearoff=0)
menu_ayuda.add_command(
    label="Ayuda",
    command=lambda: mostrar_ayuda()
)
menu_ayuda.add_command(
    label="Acerca del sistema",
    command=lambda: acerca_del_sistema()
)
barra_menu.add_cascade(
    label="Ayuda",
    menu=menu_ayuda
)

ventana.config(menu=barra_menu)


# ============================================================
# VARIABLES
# ============================================================

id_usuario = StringVar()
nombre = StringVar()
apellido = StringVar()
direccion = StringVar()
ciudad = StringVar()
codigo_postal = StringVar()
genero = StringVar(value="Masculino")
usuario_activo = BooleanVar(value=False)
tipo_usuario = StringVar(value="Seleccione")
correo = StringVar()
puesto = StringVar(value="Seleccione")
tipo_sangre = StringVar(value="Seleccione")
imagen_seleccionada = StringVar()
archivo_seleccionado = StringVar()
buscar_texto = StringVar()


# ============================================================
# ESTILO
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except TclError:
    pass

# Paleta basada en la interfaz de referencia:
# Verde INSERTAR, naranja ACTUALIZAR, rojo ELIMINAR,
# azul oscuro LIMPIAR, gris SALIR, azul BUSCAR,
# turquesa MOSTRAR TODOS, celeste IMAGEN y morado ARCHIVO.

COLOR_VERDE = "#18A84A"
COLOR_NARANJA = "#F39C12"
COLOR_ROJO = "#E74C3C"
COLOR_AZUL_OSCURO = "#34495E"
COLOR_GRIS = "#7F8C8D"
COLOR_AZUL = "#2980B9"
COLOR_TURQUESA = "#16A085"
COLOR_CELESTE = "#1597D3"
COLOR_MORADO = "#9B59B6"
COLOR_BORDE = "#C8CDD1"

style.configure(
    "TFrame",
    background="#F2F2F2"
)

style.configure(
    "TLabelframe",
    background="#F2F2F2",
    bordercolor="#C8CDD1"
)

style.configure(
    "TLabelframe.Label",
    background="#F2F2F2",
    foreground="#222222",
    font=("Segoe UI", 10, "bold")
)

style.configure(
    "TButton",
    font=("Segoe UI", 9, "bold"),
    padding=(10, 6)
)

style.configure(
    "Treeview",
    font=("Segoe UI", 9),
    rowheight=28,
    background="white",
    fieldbackground="white",
    bordercolor=COLOR_BORDE
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 9, "bold"),
    background="#E9ECEF",
    foreground="#222222",
    padding=(5, 7)
)

style.configure(
    "TLabelframe.Label",
    font=("Segoe UI", 10, "bold")
)

style.configure(
    "TLabel",
    font=("Segoe UI", 9)
)

# Botón personalizado con los colores de la captura.
def boton_color(parent, texto, comando, color, ancho=13):
    boton = Button(
        parent,
        text=texto,
        command=comando,
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        disabledforeground="#E5E7EB",
        relief="raised",
        bd=1,
        highlightthickness=0,
        cursor="hand2",
        font=("Segoe UI", 9, "bold"),
        width=ancho,
        padx=8,
        pady=6
    )

    def entrar(event):
        boton.configure(relief="sunken")

    def salir_boton(event):
        boton.configure(relief="raised")

    boton.bind("<Enter>", entrar)
    boton.bind("<Leave>", salir_boton)

    return boton


# ============================================================
# CONFIGURACIÓN PRINCIPAL DE GRID
# ============================================================

ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(2, weight=1)


# ============================================================
# FUNCIONES
# ============================================================

def limpiar():
    id_usuario.set("")
    nombre.set("")
    apellido.set("")
    direccion.set("")
    ciudad.set("")
    codigo_postal.set("")
    genero.set("Masculino")
    usuario_activo.set(False)
    tipo_usuario.set("Seleccione")
    correo.set("")
    puesto.set("Seleccione")
    tipo_sangre.set("Seleccione")
    observaciones.delete("1.0", "end")
    imagen_seleccionada.set("")
    archivo_seleccionado.set("")

    etiqueta_archivo.config(text="Archivo: No adjunto")
    mostrar_imagen(None)

    entrada_nombre.focus_set()


def seleccionar_imagen():
    archivo = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[
            ("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("Todos los archivos", "*.*")
        ]
    )

    if not archivo:
        return

    origen = Path(archivo)
    destino = IMAGENES_DIR / origen.name

    try:
        if origen.resolve() != destino.resolve():
            shutil.copy2(origen, destino)

        imagen_seleccionada.set(str(destino))
        mostrar_imagen(str(destino))

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No se pudo copiar la imagen:\n{error}"
        )


def mostrar_imagen(ruta):
    for widget in marco_imagen.winfo_children():
        widget.destroy()

    if not ruta:
        Label(
            marco_imagen,
            text="Vista previa\nsin imagen",
            bg="white",
            fg="#777777",
            font=("Segoe UI", 10)
        ).pack(expand=True)
        return

    if not PIL_DISPONIBLE:
        Label(
            marco_imagen,
            text="Instale Pillow\npara visualizar",
            bg="white",
            fg="#777777",
            font=("Segoe UI", 9)
        ).pack(expand=True)
        return

    try:
        imagen = Image.open(ruta)

    # Convertir a RGB para evitar problemas con algunas imágenes
        if imagen.mode not in ("RGB", "RGBA"):
            imagen = imagen.convert("RGB")

    # Tamaño máximo de una fotografía empresarial
        imagen.thumbnail((200, 240))

        imagen_tk = ImageTk.PhotoImage(imagen)

        etiqueta = Label(
            marco_imagen,
            image=imagen_tk,
            bg="white"
        )
        etiqueta.image = imagen_tk
        etiqueta.pack(expand=True)

    except Exception:
        Label(
            marco_imagen,
            text="Imagen no disponible",
            bg="white",
            fg="#777777"
        ).pack(expand=True)


def adjuntar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Todos los archivos", "*.*")]
    )

    if not archivo:
        return

    origen = Path(archivo)
    destino = ARCHIVOS_DIR / origen.name

    try:
        if origen.resolve() != destino.resolve():
            shutil.copy2(origen, destino)

        archivo_seleccionado.set(str(destino))
        etiqueta_archivo.config(
            text=f"Archivo: {origen.name}"
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No se pudo adjuntar el archivo:\n{error}"
        )


def validar():
    if not nombre.get().strip():
        messagebox.showwarning(
            "Validación",
            "Debe ingresar el nombre."
        )
        entrada_nombre.focus_set()
        return False

    if not apellido.get().strip():
        messagebox.showwarning(
            "Validación",
            "Debe ingresar el apellido."
        )
        entrada_apellido.focus_set()
        return False

    if tipo_usuario.get() == "Seleccione":
        messagebox.showwarning(
            "Validación",
            "Debe seleccionar el tipo de usuario."
        )
        combo_tipo.focus_set()
        return False

    if correo.get().strip():
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", correo.get().strip()):
            messagebox.showwarning(
                "Validación",
                "Ingrese un correo electrónico válido."
            )
            entrada_correo.focus_set()
            return False

    if puesto.get() == "Seleccione":
        messagebox.showwarning(
            "Validación",
            "Debe seleccionar el puesto."
        )
        combo_puesto.focus_set()
        return False

    if tipo_sangre.get() == "Seleccione":
        messagebox.showwarning(
            "Validación",
            "Debe seleccionar el tipo de sangre."
        )
        combo_sangre.focus_set()
        return False

    return True


def insertar():
    if not validar():
        return

    estado = "Activo" if usuario_activo.get() else "Inactivo"

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (
                nombre, apellido, direccion, ciudad,
                codigo_postal, genero, estado, tipo_usuario,
                correo, puesto, tipo_sangre, observaciones, imagen, archivo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nombre.get().strip(),
            apellido.get().strip(),
            direccion.get().strip(),
            ciudad.get().strip(),
            codigo_postal.get().strip(),
            genero.get(),
            estado,
            tipo_usuario.get(),
            correo.get().strip(),
            puesto.get(),
            tipo_sangre.get(),
            observaciones.get("1.0", "end-1c").strip(),
            imagen_seleccionada.get(),
            archivo_seleccionado.get()
        ))

        conexion.commit()

        messagebox.showinfo(
            "Registro exitoso",
            "El usuario fue registrado correctamente."
        )

        limpiar()
        mostrar_todos()

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No se pudo insertar el usuario:\n{error}"
        )

    finally:
        conexion.close()


def actualizar():
    if not id_usuario.get():
        messagebox.showwarning(
            "Actualizar",
            "Seleccione primero un usuario de la tabla."
        )
        return

    if not validar():
        return

    estado = "Activo" if usuario_activo.get() else "Inactivo"

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            UPDATE usuarios
            SET
                nombre = ?,
                apellido = ?,
                direccion = ?,
                ciudad = ?,
                codigo_postal = ?,
                genero = ?,
                estado = ?,
                tipo_usuario = ?,
                correo = ?,
                puesto = ?,
                tipo_sangre = ?,
                observaciones = ?,
                imagen = ?,
                archivo = ?
            WHERE id = ?
        """, (
            nombre.get().strip(),
            apellido.get().strip(),
            direccion.get().strip(),
            ciudad.get().strip(),
            codigo_postal.get().strip(),
            genero.get(),
            estado,
            tipo_usuario.get(),
            correo.get().strip(),
            puesto.get(),
            tipo_sangre.get(),
            observaciones.get("1.0", "end-1c").strip(),
            imagen_seleccionada.get(),
            archivo_seleccionado.get(),
            id_usuario.get()
        ))

        conexion.commit()

        messagebox.showinfo(
            "Actualización exitosa",
            "El usuario fue actualizado correctamente."
        )

        limpiar()
        mostrar_todos()

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No se pudo actualizar:\n{error}"
        )

    finally:
        conexion.close()


def eliminar():
    if not id_usuario.get():
        messagebox.showwarning(
            "Eliminar",
            "Seleccione primero un usuario de la tabla."
        )
        return

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        "¿Está seguro de eliminar el usuario seleccionado?"
    )

    if not confirmar:
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "DELETE FROM usuarios WHERE id = ?",
            (id_usuario.get(),)
        )

        conexion.commit()

        messagebox.showinfo(
            "Eliminación exitosa",
            "El usuario fue eliminado correctamente."
        )

        limpiar()
        mostrar_todos()

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No se pudo eliminar:\n{error}"
        )

    finally:
        conexion.close()


def mostrar_todos():
    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id, nombre, apellido, direccion, ciudad,
            codigo_postal, genero, estado, tipo_usuario,
            correo, puesto, tipo_sangre, observaciones
        FROM usuarios
        ORDER BY id DESC
    """)

    registros = cursor.fetchall()
    conexion.close()

    for registro in registros:
        tabla.insert("", END, values=registro)


def buscar():
    texto = buscar_texto.get().strip()

    for fila in tabla.get_children():
        tabla.delete(fila)

    if not texto:
        mostrar_todos()
        return

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id, nombre, apellido, direccion, ciudad,
            codigo_postal, genero, estado, tipo_usuario,
            correo, puesto, tipo_sangre, observaciones
        FROM usuarios
        WHERE
            CAST(id AS TEXT) LIKE ?
            OR nombre LIKE ?
            OR apellido LIKE ?
            OR direccion LIKE ?
            OR ciudad LIKE ?
            OR codigo_postal LIKE ?
            OR genero LIKE ?
            OR estado LIKE ?
            OR tipo_usuario LIKE ?
            OR correo LIKE ?
            OR puesto LIKE ?
            OR tipo_sangre LIKE ?
            OR observaciones LIKE ?
        ORDER BY id DESC
    """, (
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%"
    ))

    registros = cursor.fetchall()
    conexion.close()

    for registro in registros:
        tabla.insert("", END, values=registro)


def seleccionar_usuario(event=None):
    seleccion = tabla.selection()

    if not seleccion:
        return

    valores = tabla.item(
        seleccion[0],
        "values"
    )

    if not valores:
        return

    id_usuario.set(valores[0])
    nombre.set(valores[1])
    apellido.set(valores[2])
    direccion.set(valores[3])
    ciudad.set(valores[4])
    codigo_postal.set(valores[5])
    genero.set(valores[6])
    usuario_activo.set(valores[7] == "Activo")
    tipo_usuario.set(valores[8])
    correo.set(valores[9] or "")
    puesto.set(valores[10] or "Seleccione")
    tipo_sangre.set(valores[11] or "Seleccione")

    observaciones.delete("1.0", "end")
    observaciones.insert("1.0", valores[12] or "")

    cargar_datos_adicionales(valores[0])


def cargar_datos_adicionales(id_seleccionado):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT imagen, archivo
        FROM usuarios
        WHERE id = ?
    """, (id_seleccionado,))

    registro = cursor.fetchone()
    conexion.close()

    if not registro:
        return

    ruta_imagen, ruta_archivo = registro

    imagen_seleccionada.set(ruta_imagen or "")
    archivo_seleccionado.set(ruta_archivo or "")

    if ruta_imagen and Path(ruta_imagen).exists():
        mostrar_imagen(ruta_imagen)
    else:
        mostrar_imagen(None)

    if ruta_archivo:
        etiqueta_archivo.config(
            text=f"Archivo: {Path(ruta_archivo).name}"
        )
    else:
        etiqueta_archivo.config(
            text="Archivo: No adjunto"
        )


def mostrar_ayuda():
    messagebox.showinfo(
        "Ayuda - Sistema de Gestión de Usuarios",
        "SISTEMA DE GESTIÓN DE USUARIOS\n\n"
        "• Complete los datos del usuario.\n"
        "• Seleccione el tipo de usuario y el puesto.\n"
        "• El correo electrónico debe tener un formato válido.\n"
        "• Puede escribir observaciones o comentarios.\n"
        "• Use INSERTAR para registrar un usuario.\n"
        "• Seleccione un usuario de la tabla para ACTUALIZAR o ELIMINAR.\n"
        "• Use el buscador para localizar registros.\n"
        "• La información se almacena en SQLite."
    )


def acerca_del_sistema():
    messagebox.showinfo(
        "Acerca del sistema",
        "SISTEMA DE GESTIÓN DE USUARIOS\n\n"
        "Aplicación de escritorio desarrollada con Tkinter + SQLite.\n"
        "Permite registrar, consultar, actualizar y eliminar usuarios."
    )


def salir():
    if messagebox.askyesno(
        "Salir",
        "¿Desea salir del sistema?"
    ):
        ventana.destroy()


# ============================================================
# ENCABEZADO
# ============================================================

marco_titulo = ttk.Frame(ventana, padding=(18, 12))
marco_titulo.grid(
    row=0,
    column=0,
    sticky="ew"
)

marco_titulo.columnconfigure(0, weight=1)

Label(
    marco_titulo,
    text="📇 FORMULARIO DE REGISTRO DE USUARIOS 🗄️",
    font=("Segoe UI", 16, "bold"),
    fg="#111111",
    bg="#FFFFFF"
).grid(row=0, column=0, sticky="w")

Label(
    marco_titulo,
    text="Registro, consulta y administración de usuarios",
    font=("Segoe UI", 9),
    fg="#666666",
    bg="#F2F2F2"
).grid(row=1, column=0, sticky="w", pady=(2, 0))


# ============================================================
# FORMULARIO
# ============================================================

formulario = ttk.LabelFrame(
    ventana,
    text="  DATOS DEL USUARIO  ",
    padding=14
)

formulario.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=15,
    pady=(0, 10)
)

# Columnas adaptables
for columna in (1, 3, 5):
    formulario.columnconfigure(columna, weight=1)

# ---------------- CAMPOS ----------------

Label(formulario, text="Nombre:").grid(
    row=0, column=0, sticky="e", padx=(0, 8), pady=6
)

entrada_nombre = ttk.Entry(
    formulario,
    textvariable=nombre
)
entrada_nombre.grid(
    row=0, column=1, sticky="ew", pady=6
)

Label(formulario, text="Apellido:").grid(
    row=0, column=2, sticky="e", padx=(18, 8), pady=6
)

entrada_apellido = ttk.Entry(
    formulario,
    textvariable=apellido
)
entrada_apellido.grid(
    row=0, column=3, sticky="ew", pady=6
)

Label(formulario, text="Ciudad:").grid(
    row=0, column=4, sticky="e", padx=(18, 8), pady=6
)

ttk.Entry(
    formulario,
    textvariable=ciudad
).grid(
    row=0, column=5, sticky="ew", pady=6
)


Label(formulario, text="Dirección:").grid(
    row=1, column=0, sticky="e", padx=(0, 8), pady=6
)

ttk.Entry(
    formulario,
    textvariable=direccion
).grid(
    row=1, column=1, sticky="ew", pady=6
)

Label(formulario, text="Código Postal:").grid(
    row=1, column=2, sticky="e", padx=(18, 8), pady=6
)

ttk.Entry(
    formulario,
    textvariable=codigo_postal
).grid(
    row=1, column=3, sticky="ew", pady=6
)

Label(formulario, text="Tipo de usuario:").grid(
    row=1, column=4, sticky="e", padx=(18, 8), pady=6
)

combo_tipo = ttk.Combobox(
    formulario,
    textvariable=tipo_usuario,
    values=[
        "Administrador",
        "Supervisor",
        "Empleado",
        "Cliente",
        "Invitado"
    ],
    state="readonly"
)

combo_tipo.grid(
    row=1, column=5, sticky="ew", pady=6
)

Label(formulario, text="Correo electrónico:").grid(
    row=2, column=0, sticky="e", padx=(0, 8), pady=6
)

entrada_correo = ttk.Entry(
    formulario,
    textvariable=correo
)
entrada_correo.grid(
    row=2, column=1, sticky="ew", pady=6
)

Label(formulario, text="Puesto:").grid(
    row=2, column=2, sticky="e", padx=(18, 8), pady=6
)

combo_puesto = ttk.Combobox(
    formulario,
    textvariable=puesto,
    values=[
        "Gerente",
        "Administrador",
        "Supervisor",
        "Coordinador",
        "Analista",
        "Auxiliar",
        "Operario",
        "Técnico",
        "Otro"
    ],
    state="readonly"
)
combo_puesto.grid(
    row=2, column=3, sticky="ew", pady=6
)

Label(formulario, text="Tipo de sangre:").grid(
    row=3, column=0, sticky="e", padx=(0, 8), pady=6
)

combo_sangre = ttk.Combobox(
    formulario,
    textvariable=tipo_sangre,
    values=[
        "O+",
        "O-",
        "A+",
        "A-",
        "B+",
        "B-",
        "AB+",
        "AB-"
    ],
    state="readonly"
)
combo_sangre.grid(
    row=3, column=1, sticky="ew", pady=6
)


# ---------------- GÉNERO Y ESTADO ----------------

Label(formulario, text="Género:").grid(
    row=4, column=0, sticky="e", padx=(0, 8), pady=6
)

marco_genero = ttk.Frame(formulario)
marco_genero.grid(
    row=4,
    column=1,
    sticky="w",
    pady=6
)

ttk.Radiobutton(
    marco_genero,
    text="Masculino",
    variable=genero,
    value="Masculino"
).pack(side="left", padx=(0, 15))

ttk.Radiobutton(
    marco_genero,
    text="Femenino",
    variable=genero,
    value="Femenino"
).pack(side="left")


Label(formulario, text="Estado:").grid(
    row=4, column=2, sticky="e", padx=(18, 8), pady=6
)

ttk.Checkbutton(
    formulario,
    text="Usuario activo",
    variable=usuario_activo
).grid(
    row=4,
    column=3,
    sticky="w",
    pady=6
)


# ============================================================
# OBSERVACIONES / COMENTARIOS
# ============================================================

Label(formulario, text="Observaciones:").grid(
    row=4, column=0, sticky="ne", padx=(0, 8), pady=6
)

marco_observaciones = ttk.Frame(formulario)
marco_observaciones.grid(
    row=4, column=1, columnspan=5, sticky="ew", pady=6
)
marco_observaciones.columnconfigure(0, weight=1)

observaciones = Text(
    marco_observaciones,
    height=3,
    wrap="word",
    font=("Segoe UI", 9),
    relief="solid",
    borderwidth=1
)
observaciones.grid(row=0, column=0, sticky="ew")

scroll_observaciones = ttk.Scrollbar(
    marco_observaciones,
    orient="vertical",
    command=observaciones.yview
)
scroll_observaciones.grid(row=0, column=1, sticky="ns")
observaciones.configure(yscrollcommand=scroll_observaciones.set)


# ============================================================
# ARCHIVOS E IMAGEN
# ============================================================

multimedia = ttk.LabelFrame(
    ventana,
    text="  Imagen y archivo adjunto  ",
    padding=10
)

multimedia.grid(
    row=1,
    column=0,
    sticky="e",
    padx=15,
    pady=(0, 10)
)

# Reubicar multimedia visualmente mediante un frame independiente
# sobre el mismo espacio se evita; se usa una segunda fila real.
multimedia.grid_forget()

# Formulario ocupa la primera fila y multimedia se agrega debajo.
# Para mantener todo compacto, se crea dentro del formulario.
marco_multimedia = ttk.Frame(formulario)
marco_multimedia.grid(
    row=6,
    column=0,
    columnspan=6,
    sticky="ew",
    pady=(8, 0)
)

marco_multimedia.columnconfigure(3, weight=1)

marco_botones_media = ttk.Frame(marco_multimedia)
marco_botones_media.grid(
    row=0,
    column=0,
    sticky="nw"
)

boton_color(
    marco_botones_media,
    "Seleccionar imagen",
    seleccionar_imagen,
    COLOR_CELESTE,
    18
).grid(
    row=0,
    column=0,
    padx=(0, 8),
    pady=2
)

boton_color(
    marco_botones_media,
    "Adjuntar archivo",
    adjuntar_archivo,
    COLOR_MORADO,
    18
).grid(
    row=1,
    column=0,
    padx=(0, 8),
    pady=6
)

etiqueta_archivo = Label(
    marco_botones_media,
    text="Archivo: No adjunto",
    fg="#6b7280",
    anchor="w"
)

etiqueta_archivo.grid(
    row=2,
    column=0,
    sticky="w"
)


marco_imagen = Frame(
    marco_multimedia,
    width=220,
    height=260,
    bg="white",
    relief="solid",
    borderwidth=1
)

marco_imagen.grid(
    row=0,
    column=1,
    rowspan=3,
    padx=(15, 0),
    sticky="w"
)

marco_imagen.grid_propagate(False)

mostrar_imagen(None)


# ============================================================
# BOTONES CRUD
# ============================================================

acciones = ttk.Frame(
    ventana,
    padding=(15, 0, 15, 10)
)

acciones.grid(
    row=2,
    column=0,
    sticky="nsew"
)

# La tabla será la que realmente se expanda.
acciones.grid_remove()

# Volvemos a usar la fila 2 para contenido principal.
# Crear contenedor vertical para acciones + tabla.
contenido = ttk.Frame(ventana)
contenido.grid(
    row=2,
    column=0,
    sticky="nsew",
    padx=15,
    pady=(0, 15)
)

contenido.columnconfigure(0, weight=1)
contenido.rowconfigure(2, weight=1)

# ---------------- ACCIONES ----------------

barra_acciones = ttk.Frame(contenido)
barra_acciones.grid(
    row=0,
    column=0,
    sticky="ew",
    pady=(0, 8)
)

for i in range(6):
    barra_acciones.columnconfigure(i, weight=1)

boton_color(
    barra_acciones,
    "✚  INSERTAR",
    insertar,
    COLOR_VERDE,
    14
).grid(
    row=0, column=0, sticky="ew", padx=3
)

boton_color(
    barra_acciones,
    "✎  ACTUALIZAR",
    actualizar,
    COLOR_NARANJA,
    14
).grid(
    row=0, column=1, sticky="ew", padx=3
)

boton_color(
    barra_acciones,
    "▣  ELIMINAR",
    eliminar,
    COLOR_ROJO,
    14
).grid(
    row=0, column=2, sticky="ew", padx=3
)

boton_color(
    barra_acciones,
    "▱  LIMPIAR",
    limpiar,
    COLOR_AZUL_OSCURO,
    14
).grid(
    row=0, column=3, sticky="ew", padx=3
)

boton_color(
    barra_acciones,
    "▣  SALIR",
    salir,
    COLOR_GRIS,
    14
).grid(
    row=0, column=4, sticky="ew", padx=3
)

boton_color(
    barra_acciones,
    "EXIT",
    salir,
    COLOR_ROJO,
    10
).grid(
    row=0, column=5, sticky="ew", padx=3
)


# ============================================================
# BUSCADOR
# ============================================================

barra_busqueda = ttk.LabelFrame(
    contenido,
    text="  BÚSQUEDA DE USUARIOS  ",
    padding=8
)

barra_busqueda.grid(
    row=1,
    column=0,
    sticky="ew",
    pady=(0, 8)
)

barra_busqueda.columnconfigure(1, weight=1)

Label(
    barra_busqueda,
    text="Buscar:"
).grid(
    row=0,
    column=0,
    padx=(0, 8)
)

entrada_buscar = ttk.Entry(
    barra_busqueda,
    textvariable=buscar_texto
)

entrada_buscar.grid(
    row=0,
    column=1,
    sticky="ew",
    padx=(0, 8)
)

boton_color(
    barra_busqueda,
    "🔍  BUSCAR",
    buscar,
    COLOR_AZUL,
    13
).grid(
    row=0,
    column=2,
    padx=3
)

boton_color(
    barra_busqueda,
    "MOSTRAR TODOS",
    mostrar_todos,
    COLOR_TURQUESA,
    16
).grid(
    row=0,
    column=3,
    padx=3
)


# ============================================================
# TABLA
# ============================================================

marco_tabla = ttk.Frame(contenido)
marco_tabla.grid(
    row=2,
    column=0,
    sticky="nsew"
)

marco_tabla.columnconfigure(0, weight=1)
marco_tabla.rowconfigure(0, weight=1)

columnas = (
    "ID",
    "Nombre",
    "Apellido",
    "Dirección",
    "Ciudad",
    "Código Postal",
    "Género",
    "Estado",
    "Tipo Usuario",
    "Correo",
    "Puesto",
    "Tipo Sangre",
    "Observaciones"
)

tabla = ttk.Treeview(
    marco_tabla,
    columns=columnas,
    show="headings",
    selectmode="browse"
)

anchos = {
    "ID": 55,
    "Nombre": 120,
    "Apellido": 120,
    "Dirección": 180,
    "Ciudad": 120,
    "Código Postal": 105,
    "Género": 100,
    "Estado": 90,
    "Tipo Usuario": 140,
    "Correo": 190,
    "Puesto": 130,
    "Tipo Sangre": 100,
    "Observaciones": 240
}

for columna in columnas:
    tabla.heading(
        columna,
        text=columna
    )

    tabla.column(
        columna,
        width=anchos[columna],
        minwidth=60,
        anchor="center",
        stretch=True
    )

tabla.grid(
    row=0,
    column=0,
    sticky="nsew"
)

scroll_vertical = ttk.Scrollbar(
    marco_tabla,
    orient="vertical",
    command=tabla.yview
)

scroll_vertical.grid(
    row=0,
    column=1,
    sticky="ns"
)

scroll_horizontal = ttk.Scrollbar(
    marco_tabla,
    orient="horizontal",
    command=tabla.xview
)

scroll_horizontal.grid(
    row=1,
    column=0,
    sticky="ew"
)

tabla.configure(
    yscrollcommand=scroll_vertical.set,
    xscrollcommand=scroll_horizontal.set
)

tabla.bind(
    "<<TreeviewSelect>>",
    seleccionar_usuario
)

entrada_buscar.bind(
    "<Return>",
    lambda event: buscar()
)


# ============================================================
# ATAJOS DE TECLADO
# ============================================================

ventana.bind(
    "<Control-f>",
    lambda event: entrada_buscar.focus_set()
)

ventana.bind(
    "<Escape>",
    lambda event: limpiar()
)


# ============================================================
# INICIO
# ============================================================

crear_tabla()
mostrar_todos()
entrada_nombre.focus_set()

ventana.mainloop()
