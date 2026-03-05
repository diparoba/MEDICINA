"""
validaciones.py

Este archivo contiene todas las restricciones y validaciones
de la aplicación web de evaluación APGAR para neonatología.

Las restricciones garantizan que los datos ingresados sean correctos,
seguros y coherentes con los criterios médicos del test APGAR.

Autor: Adrián
"""
# =====================================================
# RESTRICCIONES GENERALES DEL SISTEMA
# =====================================================

"""
RESTRICCIONES DEL SISTEMA

1. El sistema evalúa únicamente el test APGAR para recién nacidos.
2. Cada evaluación debe tener exactamente cinco parámetros.
3. Cada parámetro solo puede tener valores 0, 1 o 2.
4. El puntaje total del APGAR debe estar entre 0 y 10.
5. Los datos ingresados deben ser coherentes clínicamente.
6. El sistema funciona con un servidor Flask local.
7. Los datos se almacenan en una base de datos SQLite.
8. El nombre del paciente debe contener solo letras.
9. El sistema no reemplaza el diagnóstico médico profesional.
10. Solo debe utilizarse para apoyo educativo o clínico básico.
"""

# =====================================================
# VALIDACIONES DEL NOMBRE DEL PACIENTE
# =====================================================

def validar_nombre_vacio(nombre):
    """
    Verifica que el nombre del recién nacido no esté vacío.

    Parámetro:
    nombre (str)

    Retorna:
    True si es válido, False si está vacío
    """
    return nombre.strip() != ""


def validar_nombre_letras(nombre):
    """
    Verifica que el nombre solo contenga letras y espacios.

    Parámetro:
    nombre (str)

    Retorna:
    True si solo contiene letras
    """
    return nombre.replace(" ", "").isalpha()


def validar_longitud_nombre(nombre):
    """
    Verifica que el nombre tenga una longitud adecuada.

    Restricción:
    mínimo 2 caracteres
    máximo 30 caracteres
    """
    return 2 <= len(nombre.strip()) <= 30


def validar_caracteres_seguridad(nombre):
    """
    Evita caracteres peligrosos que puedan afectar la base de datos.

    Caracteres prohibidos:
    '  "  ;  --
    """
    caracteres_prohibidos = ["'", '"', ";", "--"]

    for c in caracteres_prohibidos:
        if c in nombre:
            return False

    return True


# =====================================================
# VALIDACIONES DEL TEST APGAR
# =====================================================

def validar_cantidad_parametros(valores):
    """
    Verifica que existan exactamente 5 parámetros del test APGAR.
    """
    return len(valores) == 5


def validar_valores_numericos(valores):
    """
    Verifica que todos los valores puedan convertirse a números.
    """
    try:
        for v in valores.values():
            int(v)
        return True
    except:
        return False


def validar_rango_parametros(valores):
    """
    Verifica que cada parámetro del APGAR esté en el rango permitido.

    Valores permitidos: 0, 1, 2
    """
    for v in valores.values():
        if int(v) not in [0, 1, 2]:
            return False
    return True


def calcular_puntaje(valores):
    """
    Calcula el puntaje total del test APGAR.

    Parámetro:
    valores (dict)

    Retorna:
    puntaje total
    """
    return sum(int(v) for v in valores.values())


def validar_rango_puntaje(puntaje):
    """
    Verifica que el puntaje total del APGAR
    esté dentro del rango válido (0 a 10).
    """
    return 0 <= puntaje <= 10


# =====================================================
# VALIDACIONES CLÍNICAS BÁSICAS
# =====================================================

def clasificar_estado_apgar(puntaje):
    """
    Clasifica el estado clínico según el puntaje APGAR.

    7-10  -> bebé vigoroso
    4-6   -> depresión moderada
    0-3   -> depresión severa
    """

    if puntaje >= 7:
        return "VIGOROSO", "Bebé en buenas condiciones.", "#27ae60"

    elif 4 <= puntaje <= 6:
        return "DEPRESIÓN MODERADA", "Requiere estimulación y vigilancia.", "#f39c12"

    else:
        return "DEPRESIÓN SEVERA", "Requiere reanimación inmediata.", "#c0392b"