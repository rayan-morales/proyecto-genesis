
from abc import ABC, abstractmethod
from entidades import Colono, Edificio
from entidades import validar_texto, validar_numero, validar_entero


# =====================================================================
# 1) ROLES DE COLONO  (herencia desde Colono)
# =====================================================================
class Ingeniero(Colono):
    """Ingeniero: refuerza la producción de Energía."""

    @property
    def objetivo(self):
        return "Energía"

    def bonificacion(self):
        return 4.0 * self.salud / 100


class Medico(Colono):
    """Médico: cura a toda la colonia en cada sol (objetivo 'Salud')."""

    @property
    def objetivo(self):
        return "Salud"

    def bonificacion(self):
        return 5.0 * self.salud / 100


class Cientifico(Colono):
    """Científico: refuerza la producción de Oxígeno."""

    @property
    def objetivo(self):
        return "Oxígeno"

    def bonificacion(self):
        return 3.0 * self.salud / 100


class Agricultor(Colono):
    """Agricultor: refuerza la producción de Comida."""

    @property
    def objetivo(self):
        return "Comida"

    def bonificacion(self):
        return 3.0 * self.salud / 100


class Piloto(Colono):
    """Piloto: consigue Materiales en sus expediciones."""

    @property
    def objetivo(self):
        return "Materiales"

    def bonificacion(self):
        return 2.0 * self.salud / 100


# =====================================================================
# 2) TIPOS DE EDIFICIO  (herencia desde la clase abstracta Edificio)
#    Todos usan factor_obreros(), definido en la clase base.
# =====================================================================
class Habitat(Edificio):
    """Hábitat con reciclaje: produce Agua si hay energía."""

    @property
    def efecto(self):
        return "Agua"

    def producir(self, hay_energia):
        if not hay_energia:
            return 0.0
        return 4.0 * self.nivel * self.factor_obreros()

    def consumo_energia(self):
        return 1.0 * self.nivel


class Granja(Edificio):
    """Granja: produce Comida si hay energía."""

    @property
    def efecto(self):
        return "Comida"

    def producir(self, hay_energia):
        if not hay_energia:
            return 0.0
        return 6.0 * self.nivel * self.factor_obreros()

    def consumo_energia(self):
        return 2.0 * self.nivel


class PlantaOxigeno(Edificio):
    """Planta de oxígeno: produce Oxígeno si hay energía."""

    @property
    def efecto(self):
        return "Oxígeno"

    def producir(self, hay_energia):
        if not hay_energia:
            return 0.0
        return 5.0 * self.nivel * self.factor_obreros()

    def consumo_energia(self):
        return 2.0 * self.nivel


class Generador(Edificio):
    """Generador: produce Energía y es el único que funciona sin ella."""

    @property
    def efecto(self):
        return "Energía"

    def producir(self, hay_energia):
        return 7.0 * self.nivel * self.factor_obreros()

    def consumo_energia(self):
        return 0.0


class Laboratorio(Edificio):
    """Laboratorio: investiga y produce Materiales si hay energía."""

    @property
    def efecto(self):
        return "Materiales"

    def producir(self, hay_energia):
        if not hay_energia:
            return 0.0
        return 4.0 * self.nivel * self.factor_obreros()

    def consumo_energia(self):
        return 2.0 * self.nivel


# =====================================================================
# 3) EVENTOS ALEATORIOS  (clase base abstracta + 5 derivadas)
# =====================================================================
class Evento(ABC):
    """Evento aleatorio. Cada subclase redefine aplicar(colonia)."""

    def __init__(self, nombre, magnitud, ciclo=0, impacto=0.0):
        self.nombre = nombre
        self.magnitud = magnitud    # intensidad del evento
        self.ciclo = ciclo          # sol en que ocurrió (0 = aún no)
        self.impacto = impacto      # cambio real en recursos (+ gana, - pierde)

    # --- propiedades (encapsulamiento) --------------------------------
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre")

    @property
    def magnitud(self):
        return self._magnitud

    @magnitud.setter
    def magnitud(self, valor):
        self._magnitud = validar_numero(valor, 0, None, "magnitud")

    @property
    def ciclo(self):
        return self._ciclo

    @ciclo.setter
    def ciclo(self, valor):
        self._ciclo = validar_entero(valor, 0, None, "ciclo")

    @property
    def impacto(self):
        return self._impacto

    @impacto.setter
    def impacto(self, valor):
        self._impacto = validar_numero(valor, None, None, "impacto")

    @property
    def tipo(self):
        return self.__class__.__name__

    # --- polimorfismo ----------------------------------------------------
    @abstractmethod
    def aplicar(self, colonia):
        """Aplica el efecto sobre la colonia y devuelve un texto."""

    # --- persistencia ----------------------------------------------------
    def a_fila(self):
        return {
            "tipo": self.tipo,
            "nombre": self._nombre,
            "magnitud": self._magnitud,
            "ciclo": self._ciclo,
            "impacto": round(self._impacto, 2),
        }

    @classmethod
    def desde_fila(cls, fila):
        """Todas las subclases comparten esta firma de constructor."""
        return cls(float(fila["magnitud"]), int(fila["ciclo"]),
                   float(fila["impacto"]))


class Tormenta(Evento):
    """Tormenta de polvo: reduce la energía."""

    def __init__(self, magnitud=20.0, ciclo=0, impacto=0.0):
        super().__init__("Tormenta de polvo", magnitud, ciclo, impacto)

    def aplicar(self, colonia):
        cambio = colonia.cambiar_recurso("Energía", -self.magnitud)
        self.impacto = cambio
        return self.nombre + ": Energía " + str(cambio)


class Fuga(Evento):
    """Fuga de oxígeno: reduce el oxígeno."""

    def __init__(self, magnitud=15.0, ciclo=0, impacto=0.0):
        super().__init__("Fuga de oxígeno", magnitud, ciclo, impacto)

    def aplicar(self, colonia):
        cambio = colonia.cambiar_recurso("Oxígeno", -self.magnitud)
        self.impacto = cambio
        return self.nombre + ": Oxígeno " + str(cambio)


class Enfermedad(Evento):
    """Enfermedad: baja la salud de todos los colonos.
    No consume recursos, por eso su impacto en recursos es 0."""

    def __init__(self, magnitud=10.0, ciclo=0, impacto=0.0):
        super().__init__("Enfermedad", magnitud, ciclo, impacto)

    def aplicar(self, colonia):
        perdida = round(colonia.herir_colonos(self.magnitud), 1)
        self.impacto = 0.0      # daña la salud, no los recursos
        return self.nombre + ": salud perdida en total " + str(perdida)


class Suministro(Evento):
    """Llegada de suministros: suma comida y agua."""

    def __init__(self, magnitud=25.0, ciclo=0, impacto=0.0):
        super().__init__("Llegada de suministros", magnitud, ciclo, impacto)

    def aplicar(self, colonia):
        comida = colonia.cambiar_recurso("Comida", self.magnitud)
        agua = colonia.cambiar_recurso("Agua", self.magnitud)
        self.impacto = comida + agua
        return (self.nombre + ": Comida +" + str(comida)
                + " y Agua +" + str(agua))


class Descubrimiento(Evento):
    """Descubrimiento científico: suma materiales."""

    def __init__(self, magnitud=30.0, ciclo=0, impacto=0.0):
        super().__init__("Descubrimiento científico", magnitud, ciclo, impacto)

    def aplicar(self, colonia):
        cambio = colonia.cambiar_recurso("Materiales", self.magnitud)
        self.impacto = cambio
        return self.nombre + ": Materiales +" + str(cambio)


# =====================================================================
# 4) FÁBRICAS: eligen la subclase correcta a partir de una fila.
#    La persistencia usa estas funciones y así no conoce las subclases.
# =====================================================================
ROLES = {
    "Ingeniero": Ingeniero,
    "Medico": Medico,
    "Cientifico": Cientifico,
    "Agricultor": Agricultor,
    "Piloto": Piloto,
}

TIPOS = {
    "Habitat": Habitat,
    "Granja": Granja,
    "PlantaOxigeno": PlantaOxigeno,
    "Generador": Generador,
    "Laboratorio": Laboratorio,
}

EVENTOS = {
    "Tormenta": Tormenta,
    "Fuga": Fuga,
    "Enfermedad": Enfermedad,
    "Suministro": Suministro,
    "Descubrimiento": Descubrimiento,
}


def colono_de_fila(fila):
    """Crea el colono del rol que indica la fila."""
    rol = str(fila["rol"])
    if rol not in ROLES:
        raise ValueError("Rol desconocido: " + rol)
    return ROLES[rol].desde_fila(fila)


def edificio_de_fila(fila):
    """Crea el edificio del tipo que indica la fila."""
    tipo = str(fila["tipo"])
    if tipo not in TIPOS:
        raise ValueError("Tipo de edificio desconocido: " + tipo)
    return TIPOS[tipo].desde_fila(fila)


def evento_de_fila(fila):
    """Crea el evento del tipo que indica la fila."""
    tipo = str(fila["tipo"])
    if tipo not in EVENTOS:
        raise ValueError("Tipo de evento desconocido: " + tipo)
    return EVENTOS[tipo].desde_fila(fila)
