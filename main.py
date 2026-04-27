import pandas as pd
from utils.helpers import *
from utils.helpers import validar_texto_sin_numeros
from utils import db_manager
import sys

def formatear_precio(precio, moneda):

    # USD
    if moneda == "USD":
        return f"USD {int(precio)}"

    # ARS SIN DECIMALES
    precio_formateado = f"{int(precio):,}"
    precio_formateado = precio_formateado.replace(",", ".")

    return f"${precio_formateado}"

# ---------------------------------------------------------
# Mostrar tabla de obras
# ---------------------------------------------------------
def mostrar_tabla(productos):

    if not productos:
        print("\nNo se encontraron obras.\n")
        return

    encabezados = ("ID", "OBRA", "DESCRIPCIÓN", "PRECIO", "CANTIDAD")

    print(f"{encabezados[0]:<5} {encabezados[1]:<22} {encabezados[2]:<50} {encabezados[3]:<10} {encabezados[4]:<10}")
    print("-" * 100)

    for prod in productos:

        if not prod:
            continue

        if len(prod) == 7:
            id_, nombre, desc, cant, precio, categoria, tipo = prod
        else:
            id_, nombre, desc, cant, precio, categoria = prod

        descripcion = desc[:48] if desc else ""

        print(f"{id_:<5} {nombre[:20]:<22} {descripcion:<50} ${precio:<9.2f} {cant:<10}")

    print("-" * 100)

# ---------------------------------------------------------
# Agregar obra
# ---------------------------------------------------------
def menu_registrar():

    imprimir_titulo("Registrar Nueva Obra")

    print("Seleccione el tipo de obra:")
    print("1. Cuadro")
    print("2. Escultura")

    tipo_op = input("Opción (1/2): ").strip()

    if tipo_op not in ("1", "2"):
        imprimir_error("Opción inválida.")
        return

    # -----------------------------------------
    # CUADRO
    # -----------------------------------------
    if tipo_op == "1":

        nombre = validar_nombre_obra("Nombre de la obra")

        # 🔍 verificar si ya existe el cuadro
        cuadros = db_manager.obtener_cuadros()

        for c in cuadros:
            nombre_existente = c[1].strip().lower()

            if nombre_existente == nombre.strip().lower():
                imprimir_error("esta obra ya existe")
                return


        tecnica = validar_tecnica("Técnica / Material")
        anio = validar_anio("Año de realización")
        medidas = validar_medidas("Medidas (ancho x alto)")
        marco = validar_si_no("Incluye marco (si/no)")

        cantidad = validar_cantidad("Cantidad")

        print("\nSeleccione moneda:")
        print("1. Pesos")
        print("2. Dólares")

        moneda_op = input("Opción: ").strip()

        if moneda_op == "1":
            moneda = "ARS"
        elif moneda_op == "2":
            moneda = "USD"
        else:
            imprimir_error("Opción inválida.")
            return

        precio = validar_input_float("Precio")


        desc = f"{tecnica} | Año: {anio} | Medidas: {medidas} | Marco: {marco} | Moneda: {moneda}"        

        
        ok = db_manager.registrar_cuadro(
            nombre,
            desc,
            cantidad,
            precio,
            tecnica
        )

    # -----------------------------------------
    # ESCULTURA
    # -----------------------------------------
    else:

        nombre = validar_nombre_obra("Nombre de la escultura")
        tecnica = validar_texto_sin_numeros("Técnica / Material")
        anio = validar_anio("Año de realización")
        medidas = validar_medidas("Medidas (ancho x alto)")

        cantidad = validar_cantidad("Cantidad")

        print("\nSeleccione moneda:")
        print("1. Pesos")
        print("2. Dólares")

        moneda_op = input("Opción: ").strip()

        if moneda_op == "1":
            moneda = "ARS"
        elif moneda_op == "2":
            moneda = "USD"
        else:
            imprimir_error("Opción inválida.")
            return

        precio = validar_input_float("Precio")

        desc = f"Técnica/Material: {tecnica} | Año: {anio} | Medidas: {medidas} | Moneda: {moneda}"


       
    

        ok = db_manager.registrar_escultura(
            nombre,
            desc,
            cantidad,
            precio,
            tecnica
        )

    if ok:
        imprimir_exito("Obra registrada correctamente.")
# ---------------------------------------------------------
# Mostrar obras
# ---------------------------------------------------------
def menu_mostrar():

    while True:

        limpiar_pantalla()

        print("Seleccione qué desea Ver:\n")

        print("1. Cuadros")
        print("2. Esculturas")
        print("3. Volver al menú principal")

        opcion = input("\nOpción: ").strip()

        if opcion == "3":
            return

        elif opcion == "1":

            productos = db_manager.obtener_cuadros()
            resultado = mostrar_tabla_cuadros_paginado(productos)

            if resultado == "principal":
                return

        elif opcion == "2":

            while True:

                limpiar_pantalla()
                print(Fore.CYAN + Style.BRIGHT + "=== LISTADO DE ESCULTURAS ===".center(95))
                print()

                productos = db_manager.obtener_esculturas()
                mostrar_tabla_esculturas(productos)

                print("\n" + "-"*60)
                print("1. volver al menú anterior")
                print("2. volver al menú principal")
                print("3. salir")

                op = input("Opción: ").strip()

                if op == "1":
                    break  # 👈 vuelve a este menú (Mostrar Obras)

                elif op == "2":
                    return  # 👈 vuelve al menú principal

                elif op == "3":

                    confirm = input("¿Seguro que desea salir del sistema? (s/n): ").lower()

                    if confirm == "s":
                        print("Saliendo del sistema...")
                        exit()

                    elif confirm == "n":
                        continue

                    else:
                        imprimir_error("Opción inválida.")
                        input("Presione Enter para continuar...")

                else:
                    imprimir_error("Opción inválida.")
                    input("Presione Enter para continuar...")

        else:
            imprimir_error("Opción inválida.")
            input("Presione Enter para continuar...")



def mostrar_tabla_cuadros_paginado(productos):

    por_pagina = 20
    pagina = 0

    productos = db_manager.obtener_cuadros()

    total = len(productos)
    total_paginas = (total - 1) // por_pagina + 1


    while True:

        limpiar_pantalla()

        inicio = pagina * por_pagina
        fin = inicio + por_pagina
        pagina_actual = productos[inicio:fin]

        # INFO
        desde = inicio + 1
        hasta = min(fin, total)

        print(Fore.CYAN + Style.BRIGHT + f"=== LISTADO DE CUADROS (Página {pagina+1} de {total_paginas}) ===".center(95))
        print(Fore.WHITE + f"Mostrando {desde}–{hasta} de {total} obras\n")

        mostrar_tabla_cuadros(pagina_actual)

        print("\n" + "-"*60)

        # OPCIONES
# OPCIONES DINÁMICAS
        opciones = {}

        if total_paginas > 1:
            if pagina == 0:
                print("1. página siguiente")
                opciones["1"] = "siguiente"

            elif pagina == total_paginas - 1:
                print("1. volver a la página anterior")
                opciones["1"] = "anterior"

            else:
                print("1. página siguiente")
                print("2. página anterior")
                opciones["1"] = "siguiente"
                opciones["2"] = "anterior"

        # SIEMPRE
        base = len(opciones) + 1
        print(f"{base}. volver al menú principal")
        print(f"{base+1}. salir")

        op = input("Opción: ").strip()


        # ACCIONES
        if op in opciones:

            if opciones[op] == "siguiente":
                pagina += 1

            elif opciones[op] == "anterior":
                pagina -= 1

            continue

        elif op == str(len(opciones) + 1):
            return "principal"

        elif op == str(len(opciones) + 2):

            confirm = input("¿Seguro que desea salir del sistema? (s/n): ").lower()

            if confirm == "s":
                print("Saliendo del sistema...")
                exit()
            else:
                continue

        else:
            imprimir_error("Opción inválida.")
            input("Presione Enter para continuar...")
            continue




# OPCIONES
        if pagina < total_paginas - 1:
            print("1. página siguiente")

        print("2. volver al menú principal")
        print("3. salir")


        op = input("Opción: ").strip()

        if op == "1" and pagina == 0:
            pagina += 1
            continue

        elif op == "1" and pagina == total_paginas - 1:
            pagina -= 1
            continue

        elif op == "2":
            break

        elif op == "3":

            confirm = input("¿Seguro que desea salir del sistema? (s/n): ").lower()

            if confirm == "s":
                print("Saliendo del sistema...")
                exit()

            elif confirm == "n":
                continue

            else:
                imprimir_error("Opción inválida.")
                input("Presione Enter para continuar...")
                continue

        else:
            imprimir_error("Opción inválida.")
            input("Presione Enter para continuar...")
            continue






        op = input("Opción: ").strip()

        if op == "1" and pagina < total_paginas - 1:
            pagina += 1

        elif op == "2":
            break

        elif op == "3":
            exit()

        else:
            imprimir_error("Opción inválida.")


def mostrar_tabla_cuadros(productos):

    if not productos:
        print("\nNo se encontraron cuadros.\n")
        return

    print()
    print(f"{'ID':<4} {'OBRA':<25} {'TÉCNICA':<20} {'AÑO':<6} {'MEDIDAS':<14} {'MARCO':<6} {'CANT':<6} {'PRECIO':<13}")
    print("-" * 100)

    for prod in productos:

        id_, nombre, desc, cant, precio, categoria = prod

        datos = desc.split("|")

        tecnica = datos[0].strip()
        anio = datos[1].replace("Año:", "").strip() if len(datos) > 1 else ""
        medidas = datos[2].replace("Medidas:", "").strip()[:12] if len(datos) > 2 else ""
        marco = datos[3].replace("Marco:", "").strip() if len(datos) > 3 else ""

        moneda = "ARS"
        if "Moneda: USD" in desc:
            moneda = "USD"

        precio_str = formatear_precio(precio, moneda)

        print(f"{id_:<4} {nombre:<25} {tecnica:<20} {anio:<6} {medidas:<14} {marco:<6} {cant:<6} {precio_str:<13}")

    print("-" * 100)


def mostrar_tabla_esculturas(productos):

    if not productos:
        print("\nNo se encontraron esculturas.\n")
        return

    print()

    print(f"{'ID':<4} {'OBRA':<25} {'TÉCNICA / MATERIAL':<25} {'AÑO':<6} {'MEDIDAS':<14} {'CANT':<6} {'PRECIO':<13}")
    print("-" * 95)

    for prod in productos:

        id_, nombre, desc, cant, precio, categoria = prod

        datos = desc.split("|")

        tecnica = datos[0].replace("Técnica/Material:", "").strip()
        anio = datos[1].replace("Año:", "").strip() if len(datos) > 1 else ""
        medidas = datos[2].replace("Medidas:", "").strip()[:12] if len(datos) > 2 else ""

        moneda = "ARS"
        if "USD" in desc:
            moneda = "USD"

        precio_str = formatear_precio(precio, moneda)

        print(f"{id_:<4} {nombre:<25} {tecnica:<25} {anio:<6} {medidas:<14} {cant:<6} {precio_str:<13}")

    print("-" * 95)

# ---------------------------------------------------------
# Editar obra
# ---------------------------------------------------------
def menu_actualizar():
    imprimir_titulo("Editar Obra")
    print("Seleccione el tipo de obra:")
    print("1. Cuadro")
    print("2. Escultura")

    tipo = input("Opción: ").strip()

    if tipo == "1":

        productos = db_manager.obtener_cuadros()
        tipo_actual = "cuadro"

    elif tipo == "2":

        productos = db_manager.obtener_esculturas()
        tipo_actual = "escultura"

    else:
        imprimir_error("Opción inválida.")
        return


    # Mostrar tabla
    if tipo_actual == "cuadro":

        print(Fore.CYAN + Style.BRIGHT + "=== LISTADO DE CUADROS ===".center(100))
        print()
        mostrar_tabla_cuadros(productos)

    else:

        print(Fore.CYAN + Style.BRIGHT + "=== LISTADO DE ESCULTURAS ===".center(100))
        print()
        mostrar_tabla_esculturas(productos)


    id_prod = validar_input_int("Ingrese el ID de la obra")

    if tipo_actual == "cuadro":
        producto = db_manager.buscar_cuadro_id(id_prod)
    else:
        producto = db_manager.buscar_escultura_id(id_prod)

    if not producto:
        imprimir_error("Obra no encontrada.")
        return

    id_, nombre, desc, cant, precio, categ = producto

    print(f"\nEditando: {nombre}")

    # -------- SEPARAR LOS DATOS DE DESC --------

    datos = desc.split("|")

    tecnica = datos[0].strip()
    anio = datos[1].replace("Año:", "").strip() if len(datos) > 1 else ""
    medidas = datos[2].replace("Medidas:", "").strip() if len(datos) > 2 else ""
    marco = datos[3].replace("Marco:", "").strip() if len(datos) > 3 else ""




# -------- EDITAR CAMPOS --------
    nuevas_medidas = medidas




    while True:
        nombre_input = input(f"Obra [{nombre}]: ").strip()

        if not nombre_input:
            nuevo_nombre = nombre
            break

        if any(char.isdigit() for char in nombre_input):
            imprimir_error("los datos son incorrectos")
            continue

        nuevo_nombre = nombre_input
        break
    nueva_cant = cant
    marco_ing = marco

    if tipo_actual == "cuadro":

        cuadros = db_manager.obtener_cuadros()

        for c in cuadros:
            id_existente = c[0]
            nombre_existente = c[1].strip().lower()

            if id_existente != id_prod and nombre_existente == nuevo_nombre.strip().lower():
                imprimir_error("esta obra ya existe")
                return


    # 🔍 validar nombre duplicado (ESCULTURAS) ← ESTE ES EL NUEVO
    if tipo_actual == "escultura":

        esculturas = db_manager.obtener_esculturas()

        for e in esculturas:
            id_existente = e[0]
            nombre_existente = e[1].strip().lower()

            if id_existente != id_prod and nombre_existente == nuevo_nombre.strip().lower():
                imprimir_error("esta obra ya existe")
                return
        



    # -------- TÉCNICA --------
    while True:
        nueva_tecnica_input = input(f"Técnica/Material [{tecnica}]: ").strip()

        if not nueva_tecnica_input:
            nueva_tecnica = tecnica
            break

        # 👉 CUADROS
        if tipo_actual == "cuadro":
            if nueva_tecnica_input.lower() in ["oleo", "oleo sobre tela"]:
                nueva_tecnica = nueva_tecnica_input
                break

        # 👉 ESCULTURAS
        elif tipo_actual == "escultura":
            if nueva_tecnica_input.lower() == "bronce":
                nueva_tecnica = nueva_tecnica_input
                break

        imprimir_error("los datos son incorrectos")


    # -------- AÑO --------
    while True:
        anio_input = input(f"Año [{anio}]: ").strip()

        if not anio_input:
            nuevo_anio = anio
            break

        if anio_input.isdigit():
            anio_int = int(anio_input)

            if 1990 <= anio_int <= 2026:
                nuevo_anio = anio_int
                break

        imprimir_error("los datos son incorrectos")


# -------- MEDIDAS --------
    while True:
        medidas_input = input(f"Medidas [{medidas}]: ").strip()

        if not medidas_input:
            nuevas_medidas = medidas
            break

        partes = medidas_input.split(" x ")

        if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
            nuevas_medidas = medidas_input
            break

        imprimir_error("los datos son incorrectos")


    if tipo_actual == "cuadro":

        while True:
            marco_input = input("Marco (si/no): ").strip().lower()

            if not marco_input:
                marco_ing = marco
                break

            if marco_input in ["si", "no"]:
                marco_ing = marco_input
                break

            imprimir_error("los datos son incorrectos")


# -------- CANTIDAD --------
    while True:
        cant_input = input(f"Cantidad [{cant}]: ").strip()

        if not cant_input:
            nueva_cant = cant
            break

        if cant_input.isdigit():
            cant_int = int(cant_input)

            if 1 <= cant_int <= 5:
                nueva_cant = cant_int
                break

        imprimir_error("los datos son incorrectos")     


    print("\nSeleccione moneda:")
    print("1. Pesos")
    print("2. Dólares")

    moneda_op = input("Opción: ").strip()

    if moneda_op == "1":
        moneda = "ARS"
    elif moneda_op == "2":
        moneda = "USD"
    else:
        imprimir_error("Opción inválida.")
        return

    # 👉 DESPUÉS PRECIO
    nuevo_precio = precio

    precio_ing = input(f"Precio [{precio}]: ").strip()

    if precio_ing:
        precio_limpio = precio_ing.replace("$", "").replace(".", "").replace(",", ".")
        nuevo_precio = float(precio_limpio)
    

    if moneda_op == "1":
        moneda = "ARS"
    elif moneda_op == "2":
        moneda = "USD"
    else:
        imprimir_error("Opción inválida.")
        return



    # reconstruir desc
    if tipo_actual == "cuadro":
        nuevo_desc = f"{nueva_tecnica} | Año: {nuevo_anio} | Medidas: {nuevas_medidas} | Marco: {marco_ing} | Moneda: {moneda}"
    else:
         nuevo_desc = f"Técnica/Material: {nueva_tecnica} | Año: {nuevo_anio} | Medidas: {nuevas_medidas}"


    if tipo_actual == "cuadro":

        ok = db_manager.actualizar_cuadro(
            id_prod, nuevo_nombre, nuevo_desc,
            nueva_cant, nuevo_precio, categ
        )

    else:

        ok = db_manager.actualizar_escultura(
            id_prod, nuevo_nombre, nuevo_desc,
            nueva_cant, nuevo_precio, categ
        )


    if ok:
        imprimir_exito("Obra actualizada correctamente.")
    else:
        imprimir_error("No se pudo actualizar.")


# ---------------------------------------------------------
# Eliminar obra
# ---------------------------------------------------------
def menu_eliminar():

    imprimir_titulo("Eliminar Obra")

    print("Seleccione qué desea eliminar:\n")

    print("1. Cuadros")
    print("2. Esculturas")
    print("3. Volver al menú principal")

    opcion = input("\nOpción: ").strip()

    if opcion == "4":
        return

    elif opcion == "1":
        productos = db_manager.obtener_cuadros()
        mostrar_tabla_cuadros(productos)

    elif opcion == "2":
        productos = db_manager.obtener_esculturas()
        mostrar_tabla_esculturas(productos)

    elif opcion == "3":
        productos = db_manager.obtener_productos()
        mostrar_tabla(productos)

    else:
        imprimir_error("Opción inválida.")
        return


    id_prod = validar_input_int("ID de la obra")

    confirm = input(f"¿Eliminar ID {id_prod}? (s/n): ").lower()

    if confirm != "s":
        imprimir_error("Operación cancelada.")
        return

    if db_manager.eliminar_producto(id_prod):
        imprimir_exito("Obra eliminada.")
    else:
        imprimir_error("No se encontró el ID.")


# ---------------------------------------------------------
# Buscar obra
# ---------------------------------------------------------
def menu_buscar():

    imprimir_titulo("Buscar Obras")

    print("1. Buscar por ID")
    print("2. Buscar por texto")

    opcion = input("Opción: ")

    if opcion == "1":

        id_prod = validar_input_int("ID")

        res = db_manager.buscar_producto_id(id_prod)

        mostrar_tabla([res] if res else [])

    elif opcion == "2":

        termino = validar_input_string("Texto")

        res = db_manager.buscar_producto_texto(termino)

        mostrar_tabla(res)

    else:
        imprimir_error("Opción inválida.")


# ---------------------------------------------------------
# Exportar catálogo
# ---------------------------------------------------------
def menu_exportar():

    imprimir_titulo("Exportar Catálogo")
    productos = db_manager.obtener_productos()   # 👈 AGREGAR ESTO
    if not productos:
        imprimir_error("No hay obras para exportar.")
        return

    print("1. Exportar catálogo de cuadros")
    print("2. Exportar catálogo de esculturas")
    print("3. Volver al Menu Principal")

    opcion = input("\nOpción: ").strip()

    if opcion == "1":
        tipo = "cuadro"
        titulo = "Exportar Catálogo de Cuadros"

    elif opcion == "2":
        tipo = "escultura"
        titulo = "Exportar Catálogo de Esculturas"

    elif opcion == "3":
        return

    else:
        imprimir_error("Opción inválida.")
        return

    # 🔹 SEGUNDO MENÚ (SIEMPRE se muestra)
    imprimir_titulo(titulo)

    print("1. Exportar catálogo en TXT")
    print("2. Exportar catálogo en PDF")
    print("3. Volver al Menu Principal")

    opcion_formato = input("\nOpción: ").strip()

    # 🔹 Filtrar recién acá (IMPORTANTE)
    productos_filtrados = [
        p for p in productos if tipo in str(p[6]).lower()
    ]

    if not productos_filtrados:
        imprimir_error("No hay obras de este tipo para exportar.")
        return

    if opcion_formato == "1":  # TXT

        if tipo == "cuadro":
            ruta = db_manager.exportar_txt(productos_filtrados)

        elif tipo == "escultura":
            ruta = db_manager.exportar_esculturas_txt(productos_filtrados)

        os.startfile(ruta)
        imprimir_exito("Catálogo exportado con éxito")


    elif opcion_formato == "2":  # PDF

        if tipo == "cuadro":
            ruta = db_manager.exportar_pdf(productos_filtrados)

        elif tipo == "escultura":
            ruta = db_manager.exportar_esculturas_pdf(productos_filtrados)

        os.startfile(ruta)
        imprimir_exito("Catálogo exportado con éxito")

    elif opcion_formato == "3":
        return

    else:
        imprimir_error("Opción inválida.")





def menu_reportes():

    imprimir_titulo("Reportes")

    print("1. Reporte financiero")
    print("2. Reporte de inventario")
    print("3. Volver al Menu Principal")

    opcion = input("\nOpción: ").strip()

    if opcion == "1":
        reporte_financiero()

    elif opcion == "2":
        reporte_inventario()

    elif opcion == "3":
        return

    else:
        imprimir_error("Opción inválida.")  


def reporte_inventario():

    imprimir_titulo("Reporte de Inventario")

    productos = db_manager.obtener_productos()

    if not productos:
        imprimir_error("No hay obras cargadas.")
        return

    total_obras = len(productos)
    stock_total = 0
    sin_stock = 0

    cuadros = 0
    esculturas = 0

    for p in productos:
        
        _, _, _, cantidad, _, _, tipo = p

        stock_total += cantidad

        if cantidad == 0:
            sin_stock += 1

        if "cuadro" in str(tipo).lower():
            cuadros += 1
        elif "escultura" in str(tipo).lower():
            esculturas += 1

    print(f"\nTotal de obras: {total_obras}")
    print(f"Cuadros: {cuadros}")
    print(f"Esculturas: {esculturas}")

    print(f"Stock total: {stock_total}")
    print(f"Obras sin stock: {sin_stock}\n")



def reporte_financiero():

    imprimir_titulo("Reporte Financiero")

    productos = db_manager.obtener_productos()

    if not productos:
        imprimir_error("No hay obras cargadas.")
        return

    total_valor = 0
    precios = []

    for p in productos:

        _, _, _, cantidad, precio, _, _ = p

        total_valor += precio * cantidad
        precios.append(precio)

    total_obras = len(productos)
    precio_promedio = total_valor / total_obras if total_obras > 0 else 0
    precio_max = max(precios) if precios else 0

    # formato
    total_str = f"${int(total_valor):,}".replace(",", ".")
    promedio_str = f"${int(precio_promedio):,}".replace(",", ".")
    max_str = f"${int(precio_max):,}".replace(",", ".")

    print(f"\nValor total del inventario: {total_str}")
    print(f"Cantidad de obras: {total_obras}")
    print(f"Valor promedio de tus obras: {promedio_str}")
    print(f"Obra más cara: {max_str}\n")





# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():

    db_manager.inicializar_db()

    opciones = {
    "1": menu_registrar,
    "2": menu_mostrar,
    "3": menu_actualizar,
    "4": menu_eliminar,
    "5": menu_buscar,
    "6": menu_reportes,
    "7": menu_exportar,
    "8": "salir"
}

    while True:

        print("\n" + Fore.CYAN + "=" * 50)
        print(Fore.CYAN + Style.BRIGHT + "        🎨 SISTEMA DE GESTIÓN ARTÍSTICA")
        print(Fore.CYAN + Style.BRIGHT + "                ")
        print(Fore.CYAN + "=" * 50)

        print(Fore.GREEN + "1. 🖼️ Agregar Obra")
        print(Fore.CYAN + "2. 📦 Mostrar Obras")
        print(Fore.YELLOW + "3. ✏️ Editar Obra")
        print(Fore.RED + "4. 🗑️ Eliminar Obra")
        print(Fore.MAGENTA + "5. 🔍 Buscar Obra")
        print(Fore.BLUE + "6. 📊 Reportes")
        print(Fore.CYAN + "7. 📄 Exportar Catálogo")

        print(Fore.WHITE + "-" * 50)
        print(Fore.WHITE + "8. 🚪 Salir")

        opcion = input("\nSeleccione una opción: ")

      
        if opcion == "8":

            while True:
                confirm = input("¿Seguro que desea salir del sistema? (s/n): ").lower()

                if confirm == "s":
                    print("Saliendo del sistema...")
                    sys.exit()

                elif confirm == "n":
                    break

                else:
                    imprimir_error("❌ Error: Opción inválida.")

        else:

            accion = opciones.get(opcion)

            if accion and accion != "salir":
                accion()
            else:
                imprimir_error("Opción inválida.")

if __name__ == "__main__":


    main()