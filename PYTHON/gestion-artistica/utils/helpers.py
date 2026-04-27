import os
from colorama import init, Fore, Style


# ---------------------------------------------------------
# Inicialización de Colorama (colores para Windows/Linux)
# ---------------------------------------------------------
init(autoreset=True)


# ---------------------------------------------------------
# Función: limpiar_pantalla
# Descripción: Limpia la pantalla de la terminal.
# ---------------------------------------------------------
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


# ---------------------------------------------------------
# Funciones de impresión con estilo
# ---------------------------------------------------------
def imprimir_titulo(texto):
    """Imprime un título destacado en color azul."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {texto.upper()} ==={Style.RESET_ALL}")


def imprimir_error(texto):
    """Imprime un mensaje de error en rojo."""
    print(f"{Fore.RED}❌ Error: {texto}{Style.RESET_ALL}")


def imprimir_exito(texto):
    """Imprime un mensaje de éxito en verde."""
    print(f"{Fore.GREEN}✅ {texto}{Style.RESET_ALL}")


# ---------------------------------------------------------
# Funciones de validación de inputs
# ---------------------------------------------------------
def validar_input_string(prompt):
    """
    Solicita un texto al usuario.
    Repite hasta que se ingrese algo válido (no vacío).
    """
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip()
        if dato:
            return dato
        imprimir_error("El campo no puede estar vacío.")


def validar_input_float(prompt):
    while True:
        try:
            dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}")

            # limpiar símbolos comunes de dinero
            dato = dato.replace("$", "")
            dato = dato.replace(".", "")
            dato = dato.replace(",", ".")

            valor = float(dato)

            if valor >= 0:
                return valor

            imprimir_error("El número debe ser positivo.")

        except ValueError:
            imprimir_error("Debe ingresar un número válido.")

def validar_input_int(prompt):
    """
    Solicita un número entero positivo.
    Repite hasta que se ingresa un valor válido.
    """
    while True:
        try:
            dato = int(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}"))
            if dato >= 0:
                return dato
            imprimir_error("El número debe ser positivo.")
        except ValueError:
            imprimir_error("Debe ingresar un número entero.")



def validar_nombre_obra(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip()

        if not dato:
            imprimir_error("El campo no puede estar vacío.")
            continue

        # ❌ no permitir números
        if any(char.isdigit() for char in dato):
            imprimir_error("los datos son incorrectos")
            continue

        return dato
    

def validar_tecnica(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip().lower()

        if not dato:
            imprimir_error("El campo no puede estar vacío.")
            continue

        if dato not in ["oleo", "oleo sobre tela"]:
            imprimir_error("los datos son incorrectos")
            continue

        return dato
    

def validar_anio(prompt):
    while True:
        try:
            dato = int(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}"))

            if 1990 <= dato <= 2026:
                return dato

            imprimir_error("los datos son incorrectos")

        except ValueError:
            imprimir_error("los datos son incorrectos")


def validar_medidas(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip()

        if not dato:
            imprimir_error("El campo no puede estar vacío.")
            continue

        # validar formato "numero x numero"
        partes = dato.split(" x ")

        if len(partes) != 2:
            imprimir_error("los datos son incorrectos")
            continue

        ancho, alto = partes

        if not (ancho.isdigit() and alto.isdigit()):
            imprimir_error("los datos son incorrectos")
            continue

        return dato
    

def validar_si_no(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip().lower()

        if dato in ["si", "no"]:
            return dato

        imprimir_error("los datos son incorrectos")


def validar_cantidad(prompt):
    while True:
        try:
            dato = int(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}"))

            if 1 <= dato <= 5:
                return dato

            imprimir_error("los datos son incorrectos")

        except ValueError:
            imprimir_error("los datos son incorrectos")


import os
from colorama import init, Fore, Style


# ---------------------------------------------------------
# Inicialización de Colorama (colores para Windows/Linux)
# ---------------------------------------------------------
init(autoreset=True)


# ---------------------------------------------------------
# Función: limpiar_pantalla
# Descripción: Limpia la pantalla de la terminal.
# ---------------------------------------------------------
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


# ---------------------------------------------------------
# Funciones de impresión con estilo
# ---------------------------------------------------------
def imprimir_titulo(texto):
    """Imprime un título destacado en color azul."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {texto.upper()} ==={Style.RESET_ALL}")


def imprimir_error(texto):
    """Imprime un mensaje de error en rojo."""
    print(f"{Fore.RED}❌ Error: {texto}{Style.RESET_ALL}")


def imprimir_exito(texto):
    """Imprime un mensaje de éxito en verde."""
    print(f"{Fore.GREEN}✅ {texto}{Style.RESET_ALL}")


# ---------------------------------------------------------
# Funciones de validación de inputs
# ---------------------------------------------------------
def validar_input_string(prompt):
    """
    Solicita un texto al usuario.
    Repite hasta que se ingrese algo válido (no vacío).
    """
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip()
        if dato:
            return dato
        imprimir_error("El campo no puede estar vacío.")


def validar_input_float(prompt):
    while True:
        try:
            dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}")

            # limpiar símbolos comunes de dinero
            dato = dato.replace("$", "")
            dato = dato.replace(".", "")
            dato = dato.replace(",", ".")

            valor = float(dato)

            if valor >= 0:
                return valor

            imprimir_error("El número debe ser positivo.")

        except ValueError:
            imprimir_error("Debe ingresar un número válido.")

def validar_input_int(prompt):
    """
    Solicita un número entero positivo.
    Repite hasta que se ingresa un valor válido.
    """
    while True:
        try:
            dato = int(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}"))
            if dato >= 0:
                return dato
            imprimir_error("El número debe ser positivo.")
        except ValueError:
            imprimir_error("Debe ingresar un número entero.")



def validar_nombre_obra(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip()

        if not dato:
            imprimir_error("El campo no puede estar vacío.")
            continue

        # ❌ no permitir números
        if any(char.isdigit() for char in dato):
            imprimir_error("los datos son incorrectos")
            continue

        return dato
    

def validar_tecnica(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip().lower()

        if not dato:
            imprimir_error("El campo no puede estar vacío.")
            continue

        if dato not in ["oleo", "oleo sobre tela"]:
            imprimir_error("los datos son incorrectos")
            continue

        return dato
    

def validar_anio(prompt):
    while True:
        try:
            dato = int(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}"))

            if 1990 <= dato <= 2026:
                return dato

            imprimir_error("los datos son incorrectos")

        except ValueError:
            imprimir_error("los datos son incorrectos")


def validar_medidas(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip().lower()

        if not dato:
            imprimir_error("El campo no puede estar vacío.")
            continue

        # normalizar (reemplaza X o x sin espacios)
        dato = dato.replace("x", " x ")

        partes = dato.split(" x ")

        if len(partes) != 2:
            imprimir_error("los datos son incorrectos")
            continue

        ancho, alto = partes

        if not (ancho.strip().isdigit() and alto.strip().isdigit()):
            imprimir_error("los datos son incorrectos")
            continue

        return f"{ancho.strip()} x {alto.strip()}"

def validar_si_no(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip().lower()

        if dato in ["si", "no"]:
            return dato

        imprimir_error("los datos son incorrectos")


def validar_cantidad(prompt):
    while True:
        try:
            dato = int(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}"))

            if 1 <= dato <= 5:
                return dato

            imprimir_error("los datos son incorrectos")

        except ValueError:
            imprimir_error("los datos son incorrectos")


def validar_texto_sin_numeros(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip()

        if not dato:
            imprimir_error("El campo no puede estar vacío.")
            continue

        if any(char.isdigit() for char in dato):
            imprimir_error("los datos son incorrectos")
            continue

        return dato