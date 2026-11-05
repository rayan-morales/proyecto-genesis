# ABC es la clase de Python que permite crear clases abstractas.
# Aquí la importamos con un nombre propio de la temática (PlanoMarciano).
from abc import ABC as PlanoMarciano, abstractmethod

# ---------------------------------------------------------------
# Constantes (las mismas listas de tu código original)
# ---------------------------------------------------------------
ROLES = ["Ingeniero", "Médico", "Científico", "Agricultor", "Piloto"]
TIPOS = ["Hábitat", "Granja", "Planta de oxígeno", "Generador", "Laboratorio"]
RECURSOS_BASE = ["Oxígeno", "Agua", "Comida", "Energía", "Materiales"]
VITALES = ["Oxígeno", "Agua", "Comida"]


# ---------------------------------------------------------------
# Funciones de validación (reemplazan a pedir_texto, pedir_entero
# y pedir_cantidad, pero lanzando ValueError en vez de usar input)
# ---------------------------------------------------------------
def validar_texto(valor, campo):
    """Solo letras y espacios, no vacío."""
    if type(valor) != str:
        raise ValueError(f"{campo}: debe ser texto.")
    valor = valor.strip()
    if valor == "" or not valor.replace(" ", "").isalpha():
        raise ValueError(f"{campo}: ingrese solo letras y espacios.")
    return valor


def validar_entero(valor, campo, minimo, maximo):
    """Entero (no bool) dentro de un rango."""
    if type(valor) != int:
        raise ValueError(f"{campo}: debe ser un número entero.")
    if valor < minimo or valor > maximo:
        raise ValueError(f"{campo}: debe estar entre {minimo} y {maximo}.")
    return valor


def validar_cantidad(valor, campo):
    """Número real finito y no negativo."""
    if type(valor) != int and type(valor) != float:
        raise ValueError(f"{campo}: debe ser un número.")
    if valor != valor or valor in (float("inf"), float("-inf")):
        raise ValueError(f"{campo}: debe ser un número válido.")
    if valor < 0:
        raise ValueError(f"{campo}: no puede ser negativo.")
    return float(valor)


def validar_opcion(valor, campo, opciones):
    """El valor debe estar en la lista de opciones permitidas."""
    if valor not in opciones:
        raise ValueError(f"{campo}: debe ser una de {opciones}.")
    return valor


# ---------------------------------------------------------------
# Clase Colono
# ---------------------------------------------------------------
class Colono:
    def __init__(self, nombre, rol, edad, salud, habilidad):
        self.__nombre = ""
        self.__rol = ""
        self.__edad = 18
        self.__salud = 100
        self.__habilidad = ""
        self.__aporte = 0.0
        # Se asigna con los setters para que se validen
        self.nombre = nombre
        self.rol = rol
        self.edad = edad
        self.salud = salud
        self.habilidad = habilidad

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = validar_texto(valor, "Nombre").title()

    @property
    def rol(self):
        return self.__rol

    @rol.setter
    def rol(self, valor):
        self.__rol = validar_opcion(valor, "Rol", ROLES)

    @property
    def edad(self):
        return self.__edad

    @edad.setter
    def edad(self, valor):
        self.__edad = validar_entero(valor, "Edad", 18, 65)

    @property
    def salud(self):
        return self.__salud

    @salud.setter
    def salud(self, valor):
        # Entre 0 y 100 (0 = fallecido)
        self.__salud = validar_entero(valor, "Salud", 0, 100)

    @property
    def habilidad(self):
        return self.__habilidad

    @habilidad.setter
    def habilidad(self, valor):
        self.__habilidad = validar_texto(valor, "Habilidad")

    @property
    def aporte(self):
        return self.__aporte

    @aporte.setter
    def aporte(self, valor):
        self.__aporte = validar_cantidad(valor, "Aporte")

    # --- Métodos ---
    def aporte_por_ciclo(self):
        return 3 * self.__salud / 100

    def esta_vivo(self):
        return self.__salud > 0

    def modificar_salud(self, cambio):
        """Suma o resta salud sin salirse de 0-100."""
        self.__salud = max(0, min(100, self.__salud + cambio))

    def __str__(self):
        return (f"{self.__nombre} | {self.__rol} | Edad: {self.__edad} | "
                f"Salud: {self.__salud} | Habilidad: {self.__habilidad}")


# ---------------------------------------------------------------
# Clase Recurso
# ---------------------------------------------------------------
class Recurso:
    def __init__(self, nombre, cantidad, produccion, consumo):
        self.__nombre = ""
        self.__cantidad = 0.0
        self.__produccion = 0.0
        self.__consumo = 0.0
        self.__suma = 0.0
        self.__neto = 0.0
        self.nombre = nombre
        self.cantidad = cantidad
        self.produccion = produccion
        self.consumo = consumo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = validar_opcion(valor, "Recurso", RECURSOS_BASE)

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor):
        # Nunca negativo
        self.__cantidad = validar_cantidad(valor, "Cantidad")

    @property
    def produccion(self):
        return self.__produccion

    @produccion.setter
    def produccion(self, valor):
        self.__produccion = validar_cantidad(valor, "Producción")

    @property
    def consumo(self):
        return self.__consumo

    @consumo.setter
    def consumo(self, valor):
        self.__consumo = validar_cantidad(valor, "Consumo")

    @property
    def suma(self):
        return self.__suma

    @suma.setter
    def suma(self, valor):
        self.__suma = validar_cantidad(valor, "Suma")

    @property
    def neto(self):
        return self.__neto

    @neto.setter
    def neto(self, valor):
        # El balance neto SÍ puede ser negativo (déficit)
        if type(valor) != int and type(valor) != float:
            raise ValueError("Neto: debe ser un número.")
        self.__neto = float(valor)

    # --- Métodos ---
    def es_vital(self):
        return self.__nombre in VITALES

    def modificar(self, cambio):
        """Suma o resta cantidad; si bajaría de 0, queda en 0."""
        self.__cantidad = max(0.0, self.__cantidad + cambio)

    def __str__(self):
        return (f"{self.__nombre}: {round(self.__cantidad, 1)} | "
                f"Producción: {self.__produccion} | Consumo: {self.__consumo}")


# ---------------------------------------------------------------
# Clase Edificio (ABSTRACTA)
# ---------------------------------------------------------------
class Edificio(PlanoMarciano):
    NIVEL_MAXIMO = 5

    def __init__(self, nombre, tipo, nivel, costo, efecto):
        self.__nombre = ""
        self.__tipo = ""
        self.__nivel = 1
        self.__costo = 1
        self.__efecto = ""
        self.__construido = False
        self.__producido = 0.0
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel
        self.costo = costo
        self.efecto = efecto

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = validar_texto(valor, "Nombre del edificio").title()

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, valor):
        self.__tipo = validar_opcion(valor, "Tipo", TIPOS)

    @property
    def nivel(self):
        return self.__nivel

    @nivel.setter
    def nivel(self, valor):
        self.__nivel = validar_entero(valor, "Nivel", 1, self.NIVEL_MAXIMO)

    @property
    def costo(self):
        return self.__costo

    @costo.setter
    def costo(self, valor):
        self.__costo = validar_entero(valor, "Costo", 1, 10000)

    @property
    def efecto(self):
        return self.__efecto

    @efecto.setter
    def efecto(self, valor):
        self.__efecto = validar_opcion(valor, "Efecto", RECURSOS_BASE)

    @property
    def construido(self):
        return self.__construido

    @construido.setter
    def construido(self, valor):
        if type(valor) != bool:
            raise ValueError("Construido: debe ser True o False.")
        self.__construido = valor

    @property
    def producido(self):
        return self.__producido

    @producido.setter
    def producido(self, valor):
        self.__producido = validar_cantidad(valor, "Producido")

    # --- Métodos ---
    def costo_mejora(self):
        return self.__costo / 2 * self.__nivel

    def mejorar(self):
        if not self.__construido:
            raise ValueError("Primero debe construir el edificio.")
        if self.__nivel >= self.NIVEL_MAXIMO:
            raise ValueError("El edificio ya está en el nivel máximo.")
        self.__nivel += 1

    def sumar_produccion(self, cantidad):
        self.__producido += validar_cantidad(cantidad, "Producción acumulada")

    @abstractmethod
    def producir(self):
        """Cada tipo de edificio define cuánto produce por ciclo."""
        pass

    def __str__(self):
        estado = "Construido" if self.__construido else "En plano"
        return (f"{self.__nombre} | {self.__tipo} | Nivel: {self.__nivel} | "
                f"Produce: {self.__efecto} | {estado}")


# ---------------------------------------------------------------
# Subclases de Edificio (una por cada tipo de tu lista TIPOS)
# ---------------------------------------------------------------
class Habitat(Edificio):
    def producir(self):
        if self.construido:
            return 5 * self.nivel
        return 0


class Granja(Edificio):
    def producir(self):
        if self.construido:
            return 5 * self.nivel
        return 0


class PlantaOxigeno(Edificio):
    def producir(self):
        if self.construido:
            return 5 * self.nivel
        return 0


class Generador(Edificio):
    def producir(self):
        if self.construido:
            return 5 * self.nivel
        return 0


class Laboratorio(Edificio):
    def producir(self):
        if self.construido:
            return 5 * self.nivel
        return 0


# Diccionario: tipo de edificio -> clase que se debe crear
CLASES_EDIFICIO = {
    "Hábitat": Habitat,
    "Granja": Granja,
    "Planta de oxígeno": PlantaOxigeno,
    "Generador": Generador,
    "Laboratorio": Laboratorio,
}