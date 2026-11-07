
from abc import ABC, abstractmethod

RECURSOS_BASE = ("Oxígeno", "Agua", "Comida", "Energía", "Materiales")
VITALES = ("Oxígeno", "Agua", "Comida")  
NIVEL_MAXIMO = 5                         
MAX_OBREROS = 3                           

def validar_texto(valor, campo):
    if not isinstance(valor, str):
        raise ValueError(campo + ": debe ser texto.")
    limpio = valor.strip()
    if limpio == "" or not limpio.replace(" ", "").isalnum():
        raise ValueError(campo + ": use solo letras, números y espacios.")
    return limpio


def validar_numero(valor, minimo, maximo, campo):
    """Valida un número entre minimo y maximo (None = sin límite)."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(campo + ": debe ser un número.")
    if valor != valor:  
        raise ValueError(campo + ": no es un número válido.")
    if minimo is not None and valor < minimo:
        raise ValueError(campo + ": no puede ser menor que " + str(minimo) + ".")
    if maximo is not None and valor > maximo:
        raise ValueError(campo + ": no puede ser mayor que " + str(maximo) + ".")
    return valor


def validar_entero(valor, minimo, maximo, campo):
    """Igual que validar_numero, pero exige un número entero."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError(campo + ": debe ser un número entero.")
    return validar_numero(valor, minimo, maximo, campo)


def validar_lista(valor, clase, campo):
    """Valida que sea una lista cuyos elementos son de la clase indicada."""
    if not isinstance(valor, list):
        raise ValueError(campo + ": debe ser una lista.")
    for elemento in valor:
        if not isinstance(elemento, clase):
            raise ValueError(campo + ": contiene un elemento inválido.")
    return list(valor)

class Recurso:
    """Un recurso de la colonia con su cantidad, producción y consumo."""

    def __init__(self, nombre, cantidad, produccion, consumo):

        self.nombre = nombre
        self.cantidad = cantidad
        self.produccion = produccion
        self.consumo = consumo
        self.suma = 0.0   
        self.neto = 0.0    
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = validar_texto(valor, "nombre")
        if valor not in RECURSOS_BASE:
            raise ValueError("nombre: debe ser " + ", ".join(RECURSOS_BASE) + ".")
        self._nombre = valor

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):

        self._cantidad = float(validar_numero(valor, 0, None, "cantidad"))

    @property
    def produccion(self):
        return self._produccion

    @produccion.setter
    def produccion(self, valor):
        self._produccion = float(validar_numero(valor, 0, None, "produccion"))

    @property
    def consumo(self):
        return self._consumo

    @consumo.setter
    def consumo(self, valor):
        self._consumo = float(validar_numero(valor, 0, None, "consumo"))

    @property
    def suma(self):
        return self._suma

    @suma.setter
    def suma(self, valor):
        self._suma = float(validar_numero(valor, 0, None, "suma"))

    @property
    def neto(self):
        return self._neto

    @neto.setter
    def neto(self, valor):
        self._neto = float(validar_numero(valor, None, None, "neto"))

    @property
    def es_vital(self):
        """Oxígeno, agua y comida: si se agotan, la colonia colapsa."""
        return self._nombre in VITALES

    def cambiar(self, delta):
        """Suma o resta sin permitir negativos. Devuelve el cambio real."""
        anterior = self._cantidad
        self.cantidad = round(max(0.0, anterior + delta), 1)
        return round(self._cantidad - anterior, 1)

    def promedio(self, ciclos):
        """Existencia promedio a lo largo de los ciclos simulados."""
        if ciclos <= 0:
            return self._cantidad
        return self._suma / ciclos

    # --- persistencia ----------------------------------------------------
    def a_fila(self):
        """Convierte el objeto en una fila para Pandas."""
        return {
            "nombre": self._nombre,
            "cantidad": round(self._cantidad, 2),
            "produccion": round(self._produccion, 2),
            "consumo": round(self._consumo, 2),
            "suma": round(self._suma, 2),
            "neto": round(self._neto, 2),
        }

    @classmethod
    def desde_fila(cls, fila):
        """Reconstruye el objeto desde una fila (KeyError si falta algo)."""
        recurso = cls(str(fila["nombre"]), float(fila["cantidad"]),
                      float(fila["produccion"]), float(fila["consumo"]))
        recurso.suma = float(fila["suma"])
        recurso.neto = float(fila["neto"])
        return recurso

    def __str__(self):
        return self._nombre + ": " + str(round(self._cantidad, 1))


# ---------------------------------------------------------------------
# COLONO (clase base: las subclases viven en jerarquia.py)
# ---------------------------------------------------------------------
class Colono:
    """Colono genérico. Cada rol hereda de esta clase y redefine
    bonificacion() y objetivo (polimorfismo)."""

    def __init__(self, nombre, edad, salud, habilidad, aporte=0.0,
                 destino="Ninguno"):
        self.nombre = nombre
        self.edad = edad
        self.salud = salud
        self.habilidad = habilidad
        self.aporte = aporte     
        self.destino = destino    

    # --- propiedades (encapsulamiento) --------------------------------
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre")

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, valor):
        self._edad = validar_entero(valor, 18, 65, "edad")

    @property
    def salud(self):
        return self._salud

    @salud.setter
    def salud(self, valor):
    
        self._salud = round(validar_numero(valor, 0, 100, "salud"), 2)

    @property
    def habilidad(self):
        return self._habilidad

    @habilidad.setter
    def habilidad(self, valor):
        self._habilidad = validar_texto(valor, "habilidad")

    @property
    def aporte(self):
        return self._aporte

    @aporte.setter
    def aporte(self, valor):
        self._aporte = validar_numero(valor, 0, None, "aporte")

    @property
    def destino(self):
        return self._destino

    @destino.setter
    def destino(self, valor):
        self._destino = validar_texto(valor, "destino")

    @property
    def rol(self):
        """El rol es el nombre de la clase (solo lectura)."""
        return self.__class__.__name__

    @property
    def objetivo(self):
        """Recurso (o 'Salud') que refuerza el rol. Lo redefine cada rol."""
        return ""

    # --- comportamiento ------------------------------------------------
    def bonificacion(self):
        """Aporte por sol según el rol. Lo redefine cada subclase."""
        return 0.0

    def herir(self, puntos):
        """Resta salud sin bajar de 0. Devuelve los puntos perdidos."""
        anterior = self._salud
        self.salud = max(0, anterior - puntos)
        return anterior - self._salud

    def sanar(self, puntos):
        """Suma salud sin pasar de 100. Devuelve los puntos recuperados."""
        anterior = self._salud
        self.salud = min(100, anterior + puntos)
        return self._salud - anterior

    def esta_vivo(self):
        return self._salud > 0

    def en_riesgo(self):
        return self._salud < 50

    # --- persistencia ----------------------------------------------------
    def a_fila(self):
        return {
            "nombre": self._nombre,
            "rol": self.rol,
            "edad": self._edad,
            "salud": self._salud,
            "habilidad": self._habilidad,
            "aporte": round(self._aporte, 2),
            "destino": self._destino,
        }

    @classmethod
    def desde_fila(cls, fila):
        """Como usa cls(...), Medico.desde_fila() crea un Medico, etc."""
        return cls(str(fila["nombre"]), int(fila["edad"]),
                   float(fila["salud"]), str(fila["habilidad"]),
                   float(fila["aporte"]), str(fila["destino"]))

    def __str__(self):
        return self._nombre + " (" + self.rol + ")"

class Edificio(ABC):
    """Edificio de la colonia. Las subclases (jerarquia.py) están
    obligadas a definir efecto, producir() y consumo_energia()."""

    def __init__(self, nombre, nivel, costo, construido=False,
                 producido=0.0, prioridad=3):
        self.nombre = nombre
        self.nivel = nivel
        self.costo = costo
        self.construido = construido    
        self.producido = producido     
        self.prioridad = prioridad     
        self.obreros = 0              
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre")

    @property
    def nivel(self):
        return self._nivel

    @nivel.setter
    def nivel(self, valor):
        self._nivel = validar_entero(valor, 1, NIVEL_MAXIMO, "nivel")

    @property
    def costo(self):
        return self._costo

    @costo.setter
    def costo(self, valor):
        self._costo = validar_entero(valor, 1, 10000, "costo")

    @property
    def construido(self):
        return self._construido

    @construido.setter
    def construido(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("construido: debe ser verdadero o falso.")
        self._construido = valor

    @property
    def producido(self):
        return self._producido

    @producido.setter
    def producido(self, valor):
        self._producido = validar_numero(valor, 0, None, "producido")

    @property
    def prioridad(self):
        return self._prioridad

    @prioridad.setter
    def prioridad(self, valor):
        self._prioridad = validar_entero(valor, 1, 5, "prioridad")

    @property
    def obreros(self):
        return self._obreros

    @obreros.setter
    def obreros(self, valor):
        self._obreros = validar_entero(valor, 0, MAX_OBREROS, "obreros")

    @property
    def tipo(self):
        """El tipo es el nombre de la clase (solo lectura)."""
        return self.__class__.__name__

    @property
    @abstractmethod
    def efecto(self):
        """Nombre del recurso que produce el edificio."""

    @abstractmethod
    def producir(self, hay_energia):
        """Cantidad producida en un sol."""

    @abstractmethod
    def consumo_energia(self):
        """Energía que consume el edificio en un sol."""

    def factor_obreros(self):
        """Cada colono asignado aumenta la producción un 20 %."""
        return 1.0 + 0.2 * self._obreros

    def costo_mejora(self):
        """Costo en materiales de subir un nivel."""
        return self._costo / 2 * self._nivel

    def mejorar(self):
        if self._nivel >= NIVEL_MAXIMO:
            raise ValueError("El edificio ya está en el nivel máximo.")
        self.nivel = self._nivel + 1


    def a_fila(self):
        return {
            "nombre": self._nombre,
            "tipo": self.tipo,
            "nivel": self._nivel,
            "costo": self._costo,
            "efecto": self.efecto,
            "construido": 1 if self._construido else 0,
            "producido": round(self._producido, 2),
            "prioridad": self._prioridad,
        }

    @classmethod
    def desde_fila(cls, fila):
        """Se llama sobre una subclase concreta (Granja.desde_fila...)."""
        return cls(str(fila["nombre"]), int(fila["nivel"]),
                   int(fila["costo"]), bool(int(fila["construido"])),
                   float(fila["producido"]), int(fila["prioridad"]))

    def __str__(self):
        return self._nombre + " (" + self.tipo + ", nivel " + str(self._nivel) + ")"
