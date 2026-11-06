
import pandas as pd
from clases_base import Colono, Recurso, CLASES_EDIFICIO


def leer_csv(nombre, columnas):
    try:
        tabla = pd.read_csv(nombre)

    except FileNotFoundError:
        raise ValueError(
            "No se encontró el archivo: " + nombre
        )

    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        raise ValueError(
            "El archivo CSV está dañado: " + nombre
        )

    except UnicodeError:
        raise ValueError(
            "No se puede leer el archivo: " + nombre
        )

    for columna in columnas:
        if columna not in tabla.columns:
            raise ValueError(
                "Falta la columna " + columna + " en " + nombre
            )
    return tabla


def leer_entero(valor):
    numero = float(valor)

    if numero != numero:
        raise ValueError("Número entero inválido.")

    if numero in (float("inf"), float("-inf")):
        raise ValueError("Número entero inválido.")

    if numero != int(numero):
        raise ValueError("Se esperaba un número entero.")

    return int(numero)


def leer_decimal(valor):
    numero = float(valor)

    if numero != numero:
        raise ValueError("Número decimal inválido.")

    if numero in (float("inf"), float("-inf")):
        raise ValueError("Número decimal inválido.")

    return numero

# GUARDAR COLONOS

def guardar_colonos(colonos):
    filas = []

    for colono in colonos:
        filas.append({
            "nombre": colono.nombre,
            "rol": colono.rol,
            "edad": colono.edad,
            "salud": colono.salud,
            "habilidad": colono.habilidad,
            "aporte": colono.aporte
        })

    tabla = pd.DataFrame(
        filas,
        columns=[
            "nombre", "rol", "edad",
            "salud", "habilidad", "aporte"
        ]
    )
    tabla.to_csv("colonos.csv", index=False)

# GUARDAR RECURSOS

def guardar_recursos(recursos):
    filas = []

    for recurso in recursos:
        filas.append({
            "nombre": recurso.nombre,
            "cantidad": recurso.cantidad,
            "produccion": recurso.produccion,
            "consumo": recurso.consumo,
            "suma": recurso.suma,
            "neto": recurso.neto
        })

    tabla = pd.DataFrame(
        filas,
        columns=[
            "nombre", "cantidad", "produccion",
            "consumo", "suma", "neto"
        ]
    )
    tabla.to_csv("recursos.csv", index=False)


# GUARDAR EDIFICIOS

def guardar_edificio(edificios):
    filas = []

    for edificio in edificios:
        filas.append({
            "nombre": edificio.nombre,
            "tipo": edificio.tipo,
            "nivel": edificio.nivel,
            "costo": edificio.costo,
            "efecto": edificio.efecto,
            "construido": edificio.construido,
            "producido": edificio.producido
        })

    tabla = pd.DataFrame(
        filas,
        columns=[
            "nombre", "tipo", "nivel", "costo",
            "efecto", "construido", "producido"
        ]
    )
    tabla.to_csv("edificios.csv", index=False)

# GUARDAR EVENTOS

def guardar_eventos(eventos_dados):
    filas = []

    for numero in eventos_dados:
        filas.append({
            "evento": numero
        })
    tabla = pd.DataFrame(
        filas,
        columns=["evento"]
    )
    tabla.to_csv("eventos.csv", index=False)

# GUARDAR CICLOS

def guardar_ciclos(historial, en_crisis):
    filas = []

    if len(historial) == 0:
        filas.append({
            "sol": 0,
            "produccion": 0.0,
            "en_crisis": en_crisis
        })

    else:
        for i in range(len(historial)):
            filas.append({
                "sol": i + 1,
                "produccion": historial[i],
                "en_crisis": en_crisis
            })
    tabla = pd.DataFrame(
        filas,
        columns=["sol", "produccion", "en_crisis"]
    )

    tabla.to_csv("ciclos.csv", index=False)


# CARGAR COLONOS

def cargar_colonos():
    tabla = leer_csv(
        "colonos.csv",
        [
            "nombre", "rol", "edad",
            "salud", "habilidad", "aporte"
        ]
    )
    colonos = []

    for _, fila in tabla.iterrows():
        colono = Colono(
            fila["nombre"],
            fila["rol"],
            leer_entero(fila["edad"]),
            leer_entero(fila["salud"]),
            fila["habilidad"]
        )
        colono.aporte = leer_decimal(fila["aporte"])
        colonos.append(colono)

    return colonos

# CARGAR RECURSOS

def cargar_recursos():
    tabla = leer_csv(
        "recursos.csv",
        [
            "nombre", "cantidad", "produccion",
            "consumo", "suma", "neto"
        ]
    )
    recursos = []

    for _, fila in tabla.iterrows():
        recurso = Recurso(
            fila["nombre"],
            leer_decimal(fila["cantidad"]),
            leer_decimal(fila["produccion"]),
            leer_decimal(fila["consumo"])
        )

        recurso.suma = leer_decimal(fila["suma"])
        recurso.neto = leer_decimal(fila["neto"])

        recursos.append(recurso)

    return recursos

# CARGAR EDIFICIOS

def cargar_edificios():
    tabla = leer_csv(
        "edificios.csv",
        [
            "nombre", "tipo", "nivel", "costo",
            "efecto", "construido", "producido"
        ]
    )

    edificios = []

    for _, fila in tabla.iterrows():
        tipo = fila["tipo"]

        if tipo not in CLASES_EDIFICIO:
            raise ValueError(
                "Tipo de edificio incorrecto: " + str(tipo)
            )
        clase = CLASES_EDIFICIO[tipo]

        edificio = clase(
            fila["nombre"],
            tipo,
            leer_entero(fila["nivel"]),
            leer_entero(fila["costo"]),
            fila["efecto"]
        )
        valor = str(fila["construido"]).lower()

        if valor not in ("true", "false"):
            raise ValueError(
                "Estado de edificio incorrecto."
            )

        edificio.construido = valor == "true"
        edificio.producido = leer_decimal(fila["producido"])

        edificios.append(edificio)

    return edificios

# CARGAR EVENTOS

def cargar_eventos():
    tabla = leer_csv(
        "eventos.csv",
        ["evento"]
    )
    eventos = []

    for _, fila in tabla.iterrows():
        numero = leer_entero(fila["evento"])

        if numero < 1 or numero > 6:
            raise ValueError(
                "Número de evento incorrecto."
            )
        eventos.append(numero)

    return eventos

# CARGAR CICLOS

def cargar_ciclos():
    tabla = leer_csv(
        "ciclos.csv",
        ["sol", "produccion", "en_crisis"]
    )
    historial = []
    soles = 0
    en_crisis = False

    if len(tabla) == 0:
        raise ValueError(
            "El archivo ciclos.csv no tiene registros."
        )

    for _, fila in tabla.iterrows():
        sol = leer_entero(fila["sol"])

        if sol == 0:
            if len(tabla) != 1:
                raise ValueError(
                    "Historial de ciclos incorrecto."
                )
        elif sol > 0:
            if sol != len(historial) + 1:
                raise ValueError(
                    "Orden de ciclos incorrecto."
                )
            produccion = leer_decimal(fila["produccion"])

            if produccion < 0:
                raise ValueError(
                    "Producción del ciclo incorrecta."
                )
            historial.append(produccion)
            soles = sol
        else:
            raise ValueError(
                "Número de sol incorrecto."
            )
        estado = str(fila["en_crisis"]).lower()

        if estado not in ("true", "false"):
            raise ValueError(
                "Estado de crisis incorrecto."
            )
        en_crisis = estado == "true"

    return historial, soles, en_crisis

# TABLAS PARA ANALÍTICA CON PANDAS

def tablas_analisis():
    tablas = {}
    tablas["colonos"] = leer_csv(
        "colonos.csv",
        [
            "nombre", "rol", "edad",
            "salud", "habilidad", "aporte"
        ]
    )
    tablas["recursos"] = leer_csv(
        "recursos.csv",
        [
            "nombre", "cantidad", "produccion",
            "consumo", "suma", "neto"
        ]
    )
    tablas["edificios"] = leer_csv(
        "edificios.csv",
        [
            "nombre", "tipo", "nivel", "costo",
            "efecto", "construido", "producido"
        ]
    )
    tablas["eventos"] = leer_csv(
        "eventos.csv",
        ["evento"]
    )
    tablas["ciclos"] = leer_csv(
        "ciclos.csv",
        ["sol", "produccion", "en_crisis"]
    )
    return tablas