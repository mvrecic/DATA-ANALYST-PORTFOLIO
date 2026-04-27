import sqlite3
from utils.helpers import imprimir_error
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .config import DB_NAME


# =========================================================
# Conexión
# =========================================================

def conectar_db():
    return sqlite3.connect(DB_NAME)


# =========================================================
# Inicializar DB
# =========================================================

def inicializar_db():
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cuadros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS esculturas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gastos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    monto REAL NOT NULL,
                    tipo TEXT,
                    fecha TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS honorarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    persona TEXT NOT NULL,
                    descripcion TEXT,
                    monto REAL NOT NULL,
                    fecha TEXT
                )
            """)

    except sqlite3.Error as e:
        imprimir_error(f"Error al inicializar la base de datos: {e}")


# =========================================================
# CRUD CUADROS
# =========================================================

def registrar_cuadro(nombre, descripcion, cantidad, precio, categoria):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO cuadros
                (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, descripcion, cantidad, precio, categoria))

            conn.commit()
            return True

    except sqlite3.Error as e:
        imprimir_error(f"Error al registrar cuadro: {e}")
        return False


def obtener_cuadros():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cuadros")
        return cursor.fetchall()


def buscar_cuadro_id(id_prod):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cuadros WHERE id = ?", (id_prod,))
        return cursor.fetchone()


def actualizar_cuadro(id_prod, nombre, descripcion, cantidad, precio, categoria):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE cuadros SET
                nombre=?, descripcion=?, cantidad=?, precio=?, categoria=?
                WHERE id=?
            """, (nombre, descripcion, cantidad, precio, categoria, id_prod))

            conn.commit()
            return cursor.rowcount > 0

    except sqlite3.Error as e:
        imprimir_error(f"Error al actualizar cuadro: {e}")
        return False


def eliminar_cuadro(id_prod):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cuadros WHERE id = ?", (id_prod,))
        conn.commit()
        return cursor.rowcount > 0


# =========================================================
# CRUD ESCULTURAS
# =========================================================

def registrar_escultura(nombre, descripcion, cantidad, precio, categoria):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO esculturas
                (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, descripcion, cantidad, precio, categoria))

            conn.commit()
            return True

    except sqlite3.Error as e:
        imprimir_error(f"Error al registrar escultura: {e}")
        return False


def obtener_esculturas():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM esculturas")
        return cursor.fetchall()


def buscar_escultura_id(id_prod):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM esculturas WHERE id = ?", (id_prod,))
        return cursor.fetchone()


def actualizar_escultura(id_prod, nombre, descripcion, cantidad, precio, categoria):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE esculturas SET
                nombre=?, descripcion=?, cantidad=?, precio=?, categoria=?
                WHERE id=?
            """, (nombre, descripcion, cantidad, precio, categoria, id_prod))

            conn.commit()
            return cursor.rowcount > 0

    except sqlite3.Error as e:
        imprimir_error(f"Error al actualizar escultura: {e}")
        return False


def eliminar_escultura(id_prod):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM esculturas WHERE id = ?", (id_prod,))
        conn.commit()
        return cursor.rowcount > 0


# =========================================================
# FUNCIONES GENERALES PARA EL MAIN
# =========================================================

def obtener_productos():

    with conectar_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, nombre, descripcion, cantidad, precio, categoria, 'cuadro'
        FROM cuadros
        """)

        cuadros = cursor.fetchall()

        cursor.execute("""
        SELECT id, nombre, descripcion, cantidad, precio, categoria, 'escultura'
        FROM esculturas
        """)

        esculturas = cursor.fetchall()

    return cuadros + esculturas


def buscar_producto_id(id_prod):

    with conectar_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cuadros WHERE id=?", (id_prod,))
        cuadro = cursor.fetchone()

        if cuadro:
            return (*cuadro, "cuadro")

        cursor.execute("SELECT * FROM esculturas WHERE id=?", (id_prod,))
        escultura = cursor.fetchone()

        if escultura:
            return (*escultura, "escultura")

    return None


def buscar_producto_texto(texto):

    with conectar_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, nombre, descripcion, cantidad, precio, categoria, 'cuadro'
        FROM cuadros
        WHERE nombre LIKE ?
        """, (f"%{texto}%",))

        cuadros = cursor.fetchall()

        cursor.execute("""
        SELECT id, nombre, descripcion, cantidad, precio, categoria, 'escultura'
        FROM esculturas
        WHERE nombre LIKE ?
        """, (f"%{texto}%",))

        esculturas = cursor.fetchall()

    return cuadros + esculturas


def actualizar_producto(id_prod, nombre, descripcion, cantidad, precio, categoria, tipo):

    if tipo == "cuadro":
        return actualizar_cuadro(id_prod, nombre, descripcion, cantidad, precio, categoria)

    if tipo == "escultura":
        return actualizar_escultura(id_prod, nombre, descripcion, cantidad, precio, categoria)

    return False


def eliminar_producto(id_prod):

    if eliminar_cuadro(id_prod):
        return True

    if eliminar_escultura(id_prod):
        return True

    return False


def reporte_bajo_stock(limite):

    productos = obtener_productos()

    return [p for p in productos if p[3] <= limite]

# =========================================================
# REGISTRO DE GASTOS
# ========================================================
 
def obtener_gastos():
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gastos ORDER BY fecha DESC")
            return cursor.fetchall()
    except sqlite3.Error as e:
        imprimir_error(f"Error al obtener gastos: {e}")
        return []


def registrar_gasto(descripcion, monto, tipo, fecha):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO gastos (descripcion, monto, tipo, fecha)
                VALUES (?, ?, ?, ?)
            """, (descripcion, monto, tipo, fecha))

            conn.commit()
            return True

    except sqlite3.Error as e:
        imprimir_error(f"Error al registrar gasto: {e}")
        return False

def buscar_gasto_id(id_gasto):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gastos WHERE id = ?", (id_gasto,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        imprimir_error(f"Error al buscar gasto: {e}")
        return None
    

def eliminar_gasto(id_gasto):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM gastos WHERE id = ?", (id_gasto,))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        imprimir_error(f"Error al eliminar gasto: {e}")
        return False
    
    
def actualizar_gasto(id_gasto, descripcion, monto, tipo, fecha):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE gastos
                SET descripcion = ?, monto = ?, tipo = ?, fecha = ?
                WHERE id = ?
            """, (descripcion, monto, tipo, fecha, id_gasto))

            conn.commit()
            return cursor.rowcount > 0

    except sqlite3.Error as e:
        imprimir_error(f"Error al actualizar gasto: {e}")
        return False

# =========================================================
# HONORARIOS
# =========================================================

def obtener_honorarios():
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM honorarios ORDER BY fecha DESC")
            return cursor.fetchall()
    except sqlite3.Error as e:
        imprimir_error(f"Error al obtener honorarios: {e}")
        return []


    
def registrar_honorario(persona, descripcion, monto, fecha):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO honorarios (persona, descripcion, monto, fecha)
                VALUES (?, ?, ?, ?)
            """, (persona, descripcion, monto, fecha))
            conn.commit()
            return True
    except Exception as e:
        imprimir_error(f"Error al registrar honorario: {e}")
        return False
    

def registrar_honorario(persona, descripcion, monto, fecha):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO honorarios (persona, descripcion, monto, fecha)
                VALUES (?, ?, ?, ?)
            """, (persona, descripcion, monto, fecha))
            conn.commit()
            return True
    except Exception as e:
        imprimir_error(f"Error al registrar honorario: {e}")
        return False


def buscar_honorario_id(id_honorario):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM honorarios WHERE id = ?", (id_honorario,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        imprimir_error(f"Error al buscar honorario: {e}")
        return None


def actualizar_honorario(id_honorario, nombre, descripcion, monto, fecha):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE honorarios
                SET persona = ?, descripcion = ?, monto = ?, fecha = ?
                WHERE id = ?
            """, (nombre, descripcion, monto, fecha, id_honorario))

            conn.commit()
            return cursor.rowcount > 0

    except sqlite3.Error as e:
        imprimir_error(f"Error al actualizar honorario: {e}")
        return False
    
def eliminar_honorario(id_honorario):

    try:
        conn = conectar_db()  # o como tengas tu conexión
        cursor = conn.cursor()

        cursor.execute("DELETE FROM honorarios WHERE id = ?", (id_honorario,))
        conn.commit()

        if cursor.rowcount > 0:
            return True
        return False

    except Exception as e:
        print("Error al eliminar honorario:", e)
        return False

    finally:
        conn.close()

# =========================================================
# EXPORTAR
# =========================================================

def exportar_txt(productos, ruta="catalogo de Cuadros.txt"):

    with open(ruta, "w", encoding="utf-8") as f:

        f.write("🎨 CATALOGO DE CUADROS\n")
        f.write("=" * 40 + "\n\n")

        for p in productos:

            id_, nombre, desc, cant, precio, categ, tipo = p

            f.write(f"[Nombre de obra]: {nombre}\n")
            partes = desc.split("|")

            for parte in partes:
                parte = parte.strip()

                if "Año" in parte:
                    valor = parte.split(":")[1].strip()
                    f.write(f"[Año]: {valor}\n")

                elif "Medidas" in parte:
                    valor = parte.split(":")[1].strip()
                    f.write(f"[Medidas]: {valor}\n")

                elif "Marco" in parte:
                    valor = parte.split(":")[1].strip()
                    f.write(f"[Marco]: {valor}\n")

                else:
                    f.write(f"[Técnica]: {parte}\n")

            precio_formateado = f"{int(precio):,}".replace(",", ".")

            f.write(f"\n[Precio]: ${precio_formateado}\n")
            f.write("=" * 40 + "\n\n")

    return ruta


def exportar_pdf(productos, ruta="catalogo de Cuadros.pdf"):

    c = canvas.Canvas(ruta, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 40, "Catalogo de Cuadros")

    y = height - 70

    c.setFont("Helvetica", 10)

    for p in productos:

        id_, nombre, desc, cant, precio, categ, tipo = p

        c.setFont("Helvetica", 10)
        c.drawString(30, y, f"[Nombre de obra]: {nombre}")
        y -= 15

        partes = desc.split("|")

        for parte in partes:
            parte = parte.strip()

            if "Año" in parte:
                valor = parte.split(":")[1].strip()
                c.drawString(30, y, f"[Año]: {valor}")

            elif "Medidas" in parte:
                valor = parte.split(":")[1].strip()
                c.drawString(30, y, f"[Medidas]: {valor}")

            elif "Marco" in parte:
                valor = parte.split(":")[1].strip()
                c.drawString(30, y, f"[Marco]: {valor}")

            else:
                c.drawString(30, y, f"[Técnica]: {parte}")

            y -= 15

        # espacio antes del precio
        y -= 5

        precio_formateado = f"{int(precio):,}".replace(",", ".")

        c.drawString(30, y, f"[Precio]: ${precio_formateado}")
        y -= 20

        # separador tipo TXT
        c.drawString(30, y, "=" * 40)
        y -= 20

        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50

    c.save()


    return ruta


def exportar_productos(productos, formato="txt", tipo="catalogo"):

    if formato == "pdf":
        return exportar_pdf(productos)

    return exportar_txt(productos)

def exportar_esculturas_txt(productos):

    ruta = "catalogo de esculturas.txt"

    with open(ruta, "w", encoding="utf-8") as f:

        f.write("🎨 CATALOGO DE ESCULTURAS\n")
        f.write("=" * 40 + "\n\n")

        for p in productos:

            id_, nombre, desc, cant, precio, categ, tipo = p

            f.write(f"ID: {id_}\n")
            f.write(f"Nombre: {nombre}\n")
            f.write(f"Tipo: {tipo}\n")
            f.write(f"Categoría: {categ}\n")
            f.write(f"Descripción: {desc}\n")
            f.write(f"Cantidad: {cant}\n")
            f.write(f"Precio: ${precio}\n")
            f.write("-" * 40 + "\n\n")

    return ruta



def exportar_esculturas_pdf(productos):

    ruta = "catalogo de esculturas.pdf"

    c = canvas.Canvas(ruta, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 40, "Catalogo de Esculturas")

    y = height - 70

    c.setFont("Helvetica", 10)

    for p in productos:

        id_, nombre, desc, cant, precio, categ, tipo = p

        c.drawString(30, y, f"[Nombre de obra]: {nombre}")
        y -= 15

        partes = desc.split("|")

        for parte in partes:
            parte = parte.strip()

            if "Año" in parte:
                valor = parte.split(":")[1].strip()
                c.drawString(30, y, f"[Año]: {valor}")

            elif "Medidas" in parte:
                valor = parte.split(":")[1].strip()
                c.drawString(30, y, f"[Medidas]: {valor}")

            elif "Técnica" in parte or "Material" in parte:
                valor = parte.split(":")[1].strip()
                c.drawString(30, y, f"[Técnica]: {valor}")

            y -= 15

        # espacio antes del precio
        y -= 5

        precio_formateado = f"{int(precio):,}".replace(",", ".")

        c.drawString(30, y, f"[Precio]: ${precio_formateado}")
        y -= 20

        # separador tipo TXT
        c.drawString(30, y, "=" * 40)
        y -= 20

        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50

    c.save()

    return ruta