
from entidades import Recurso, Colono, Edificio
from entidades import VITALES, NIVEL_MAXIMO, MAX_OBREROS
from entidades import validar_texto, validar_numero, validar_entero, validar_lista
from jerarquia import Evento

# Niveles de crisis, de menor a mayor gravedad.
NIVELES = ("estable", "alerta", "critica", "colapso")


# =====================================================================
# CICLO (un sol simulado)
# =====================================================================
class Ciclo:


    def __init__(self, numero, produccion, consumo, evento, nivel,
                 colonos, existencias):
        self.numero = numero
        self.produccion = produccion
        self.consumo = consumo
        self.evento = evento
        self.nivel = nivel
        self.colonos = colonos
        self.existencias = existencias   

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, valor):
        self._numero = validar_entero(valor, 1, None, "numero")

    @property
    def produccion(self):
        return self._produccion

    @produccion.setter
    def produccion(self, valor):
        self._produccion = validar_numero(valor, 0, None, "produccion")

    @property
    def consumo(self):
        return self._consumo

    @consumo.setter
    def consumo(self, valor):
        self._consumo = validar_numero(valor, 0, None, "consumo")

    @property
    def evento(self):
        return self._evento

    @evento.setter
    def evento(self, valor):
        self._evento = validar_texto(valor, "evento")

    @property
    def nivel(self):
        return self._nivel

    @nivel.setter
    def nivel(self, valor):
        if valor not in NIVELES:
            raise ValueError("nivel: debe ser " + ", ".join(NIVELES) + ".")
        self._nivel = valor

    @property
    def colonos(self):
        return self._colonos

    @colonos.setter
    def colonos(self, valor):
        self._colonos = validar_entero(valor, 0, None, "colonos")

    @property
    def existencias(self):
        return dict(self._existencias)

    @existencias.setter
    def existencias(self, valor):
        if not isinstance(valor, dict):
            raise ValueError("existencias: debe ser un diccionario.")
        limpio = {}
        for nombre in valor:
            limpio[nombre] = validar_numero(valor[nombre], 0, None, "existencias")
        self._existencias = limpio

    # --- persistencia ----------------------------------------------------
    def a_fila(self):
        return {
            "numero": self._numero,
            "produccion": self._produccion,
            "consumo": self._consumo,
            "evento": self._evento,
            "nivel": self._nivel,
            "colonos": self._colonos,
            "oxigeno": self._existencias.get("Oxígeno", 0.0),
            "agua": self._existencias.get("Agua", 0.0),
            "comida": self._existencias.get("Comida", 0.0),
            "energia": self._existencias.get("Energía", 0.0),
            "materiales": self._existencias.get("Materiales", 0.0),
        }

    @classmethod
    def desde_fila(cls, fila):
        existencias = {
            "Oxígeno": float(fila["oxigeno"]),
            "Agua": float(fila["agua"]),
            "Comida": float(fila["comida"]),
            "Energía": float(fila["energia"]),
            "Materiales": float(fila["materiales"]),
        }
        return cls(int(fila["numero"]), float(fila["produccion"]),
                   float(fila["consumo"]), str(fila["evento"]),
                   str(fila["nivel"]), int(fila["colonos"]), existencias)


# =====================================================================
# COLONIA (contenedor)
# =====================================================================
class Colonia:
    """La colonia contiene colonos, recursos, edificios, eventos y ciclos.
    Las listas son privadas: se modifican solo con los métodos de la clase,
    que validan cada operación."""

    def __init__(self, nombre="Genesis"):
        self.nombre = nombre
        self._colonos = []
        self._recursos = []
        self._edificios = []
        self._eventos = []
        self._ciclos = []

  
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre")

    @property
    def colonos(self):
        return list(self._colonos)

    @colonos.setter
    def colonos(self, valor):
        self._colonos = validar_lista(valor, Colono, "colonos")

    @property
    def recursos(self):
        return list(self._recursos)

    @recursos.setter
    def recursos(self, valor):
        self._recursos = validar_lista(valor, Recurso, "recursos")

    @property
    def edificios(self):
        return list(self._edificios)

    @edificios.setter
    def edificios(self, valor):
        self._edificios = validar_lista(valor, Edificio, "edificios")

    @property
    def eventos(self):
        return list(self._eventos)

    @eventos.setter
    def eventos(self, valor):
        self._eventos = validar_lista(valor, Evento, "eventos")

    @property
    def ciclos(self):
        return list(self._ciclos)

    @ciclos.setter
    def ciclos(self, valor):
        self._ciclos = validar_lista(valor, Ciclo, "ciclos")

    # =================================================================
    # COLONOS
    # =================================================================
    def buscar_colono(self, nombre):
        for colono in self._colonos:
            if colono.nombre.lower() == str(nombre).strip().lower():
                return colono
        return None

    def agregar_colono(self, colono):
        if not isinstance(colono, Colono):
            raise ValueError("Debe indicar un colono válido.")
        if self.buscar_colono(colono.nombre) is not None:
            raise ValueError("Ya existe un colono con ese nombre.")
        self._colonos.append(colono)

    def eliminar_colono(self, nombre):
        colono = self.buscar_colono(nombre)
        if colono is None:
            raise ValueError("No se encontró ningún colono con ese nombre.")
        self._colonos.remove(colono)

    def renombrar_colono(self, nombre_actual, nombre_nuevo):
        colono = self.buscar_colono(nombre_actual)
        if colono is None:
            raise ValueError("No se encontró ningún colono con ese nombre.")
        otro = self.buscar_colono(nombre_nuevo)
        if otro is not None and otro is not colono:
            raise ValueError("Ya existe un colono con ese nombre.")
        colono.nombre = nombre_nuevo

    def cambiar_rol(self, nombre, clase_rol):
        """Reemplaza al colono por otro del nuevo rol con los mismos datos."""
        colono = self.buscar_colono(nombre)
        if colono is None:
            raise ValueError("No se encontró ningún colono con ese nombre.")
        nuevo = clase_rol(colono.nombre, colono.edad, colono.salud,
                          colono.habilidad, colono.aporte, colono.destino)
        self._colonos[self._colonos.index(colono)] = nuevo
        return nuevo

    def herir_colonos(self, puntos):
        """Resta salud a todos. Devuelve el total de puntos perdidos."""
        total = 0.0
        for colono in self._colonos:
            total = total + colono.herir(puntos)
        return total

    def sanar_colonos(self, puntos):
        for colono in self._colonos:
            colono.sanar(puntos)

    def retirar_muertos(self):
        """Quita a los colonos sin salud y devuelve sus nombres."""
        nombres = []
        for colono in list(self._colonos):
            if not colono.esta_vivo():
                self._colonos.remove(colono)
                nombres.append(colono.nombre)
        return nombres

    # =================================================================
    # RECURSOS
    # =================================================================
    def buscar_recurso(self, nombre):
        for recurso in self._recursos:
            if recurso.nombre.lower() == str(nombre).strip().lower():
                return recurso
        return None

    def agregar_recurso(self, recurso):
        if not isinstance(recurso, Recurso):
            raise ValueError("Debe indicar un recurso válido.")
        if self.buscar_recurso(recurso.nombre) is not None:
            raise ValueError("Ese recurso ya está registrado.")
        self._recursos.append(recurso)

    def cambiar_recurso(self, nombre, delta):
        """Suma o resta a un recurso. Devuelve el cambio real (0 si no existe)."""
        recurso = self.buscar_recurso(nombre)
        if recurso is None:
            return 0.0
        return recurso.cambiar(delta)

    # =================================================================
    # EDIFICIOS
    # =================================================================
    def buscar_edificio(self, nombre):
        for edificio in self._edificios:
            if edificio.nombre.lower() == str(nombre).strip().lower():
                return edificio
        return None

    def agregar_edificio(self, edificio):
        if not isinstance(edificio, Edificio):
            raise ValueError("Debe indicar un edificio válido.")
        if self.buscar_edificio(edificio.nombre) is not None:
            raise ValueError("Ya existe un edificio con ese nombre.")
        self._edificios.append(edificio)

    def exigir_material(self, costo):
        """Devuelve el recurso Materiales si alcanza para pagar el costo."""
        materiales = self.buscar_recurso("Materiales")
        if materiales is None:
            raise ValueError("Primero registre el recurso Materiales.")
        if materiales.cantidad < costo:
            raise ValueError("Materiales insuficientes. Costo: " + str(costo)
                             + " | Disponibles: " + str(materiales.cantidad))
        return materiales

    def construir(self, nombre):
        """Convierte un plano en edificio construido pagando su costo."""
        edificio = self.buscar_edificio(nombre)
        if edificio is None:
            raise ValueError("No se encontró ningún edificio con ese nombre.")
        if edificio.construido:
            raise ValueError("Ese edificio ya está construido.")
        materiales = self.exigir_material(edificio.costo)
        materiales.cantidad = materiales.cantidad - edificio.costo
        edificio.construido = True
        return edificio

    def mejorar(self, nombre):
        """Sube un nivel al edificio pagando el costo de mejora."""
        edificio = self.buscar_edificio(nombre)
        if edificio is None:
            raise ValueError("No se encontró ningún edificio con ese nombre.")
        if not edificio.construido:
            raise ValueError("Primero debe construir el edificio.")
        if edificio.nivel >= NIVEL_MAXIMO:
            raise ValueError("El edificio ya está en el nivel máximo.")
        costo = edificio.costo_mejora()
        materiales = self.exigir_material(costo)
        materiales.cantidad = materiales.cantidad - costo
        edificio.mejorar()
        return edificio

    # --- decisiones estratégicas ---------------------------------------
    def contar_obreros(self, nombre_edificio):
        """Cantidad de colonos asignados a un edificio."""
        total = 0
        for colono in self._colonos:
            if colono.destino.lower() == str(nombre_edificio).strip().lower():
                total = total + 1
        return total

    def asignar_colono(self, nombre_colono, nombre_edificio):
        """Asigna un colono a un edificio construido (+20 % de producción)."""
        colono = self.buscar_colono(nombre_colono)
        if colono is None:
            raise ValueError("No se encontró ningún colono con ese nombre.")
        edificio = self.buscar_edificio(nombre_edificio)
        if edificio is None:
            raise ValueError("No se encontró ningún edificio con ese nombre.")
        if not edificio.construido:
            raise ValueError("El edificio aún no está construido.")
        if colono.destino.lower() == edificio.nombre.lower():
            raise ValueError("El colono ya trabaja en ese edificio.")
        if self.contar_obreros(edificio.nombre) >= MAX_OBREROS:
            raise ValueError("El edificio ya tiene el máximo de colonos ("
                             + str(MAX_OBREROS) + ").")
        colono.destino = edificio.nombre
        return edificio

    def liberar_colono(self, nombre_colono):
        colono = self.buscar_colono(nombre_colono)
        if colono is None:
            raise ValueError("No se encontró ningún colono con ese nombre.")
        colono.destino = "Ninguno"

    def priorizar(self, nombre, prioridad):
        """Cambia la prioridad (1 = primero) de un plano sin construir."""
        edificio = self.buscar_edificio(nombre)
        if edificio is None:
            raise ValueError("No se encontró ningún edificio con ese nombre.")
        if edificio.construido:
            raise ValueError("Solo se prioriza un plano (aún sin construir).")
        edificio.prioridad = prioridad

    def plano_siguiente(self):
        """Plano con mejor prioridad (y menor costo si hay empate)."""
        elegido = None
        for edificio in self._edificios:
            if edificio.construido:
                continue
            if elegido is None or edificio.prioridad < elegido.prioridad:
                elegido = edificio
            elif (edificio.prioridad == elegido.prioridad
                  and edificio.costo < elegido.costo):
                elegido = edificio
        return elegido

    def construir_cola(self):
        plano = self.plano_siguiente()
        if plano is None:
            raise ValueError("No hay edificios en plano para construir.")
        return self.construir(plano.nombre)

    # =================================================================
    # EVENTOS Y CICLOS (historial)
    # =================================================================
    def agregar_evento(self, evento):
        if not isinstance(evento, Evento):
            raise ValueError("Debe indicar un evento válido.")
        self._eventos.append(evento)

    def agregar_ciclo(self, ciclo):
        if not isinstance(ciclo, Ciclo):
            raise ValueError("Debe indicar un ciclo válido.")
        self._ciclos.append(ciclo)

    # =================================================================
    # CRISIS POR NIVELES: estable, alerta, critica, colapso
    # =================================================================
    def evaluar_crisis(self):
        """Calcula el nivel de crisis con el estado actual de la colonia.
          colapso : sin colonos o un recurso vital en 0.
          critica : un vital se agota en menos de 3 soles o hay colonos con
                    menos de 25 de salud.
          alerta  : un vital se agota en menos de 10 soles, sin energía o
                    hay colonos con menos de 50 de salud.
          estable : en cualquier otro caso."""
        if len(self._colonos) == 0:
            return "colapso"
        gravedad = 0
        for recurso in self._recursos:
            if recurso.es_vital:
                if recurso.cantidad <= 0:
                    return "colapso"
                if recurso.neto < 0:
                    soles = recurso.cantidad / (-recurso.neto)
                    if soles < 3:
                        gravedad = max(gravedad, 2)
                    elif soles < 10:
                        gravedad = max(gravedad, 1)
        energia = self.buscar_recurso("Energía")
        if energia is not None and energia.cantidad <= 0:
            gravedad = max(gravedad, 1)
        for colono in self._colonos:
            if colono.salud < 25:
                gravedad = max(gravedad, 2)
            elif colono.salud < 50:
                gravedad = max(gravedad, 1)
        return NIVELES[gravedad]

    def nivel_actual(self):
        """Nivel registrado en el último ciclo ('estable' si no hay ciclos)."""
        if len(self._ciclos) == 0:
            return "estable"
        return self._ciclos[-1].nivel

    # =================================================================
    # REPORTES DEL TRABAJO PARCIAL (devuelven datos; el menú los imprime)
    # =================================================================
    def mejor_ciclo(self):
        """Ciclo con mayor producción total (o None)."""
        mejor = None
        for ciclo in self._ciclos:
            if mejor is None or ciclo.produccion > mejor.produccion:
                mejor = ciclo
        return mejor

    def recurso_critico(self):
        """(recurso, promedio) con menor existencia promedio (o None)."""
        if len(self._recursos) == 0 or len(self._ciclos) == 0:
            return None
        critico = None
        menor = 0.0
        for recurso in self._recursos:
            promedio = recurso.promedio(len(self._ciclos))
            if critico is None or promedio < menor:
                critico = recurso
                menor = promedio
        return critico, menor

    def mejor_edificio(self):
        """(edificio, producido/costo) del edificio más rentable (o None)."""
        mejor = None
        razon_mejor = 0.0
        for edificio in self._edificios:
            if edificio.construido:
                razon = edificio.producido / edificio.costo
                if mejor is None or razon > razon_mejor:
                    mejor = edificio
                    razon_mejor = razon
        if mejor is None:
            return None
        return mejor, razon_mejor

    def mejor_colono(self):
        """Colono con mayor aporte acumulado (o None si no hay ciclos)."""
        if len(self._colonos) == 0 or len(self._ciclos) == 0:
            return None
        mejor = self._colonos[0]
        for colono in self._colonos:
            if colono.aporte > mejor.aporte:
                mejor = colono
        return mejor

    def ciclos_vividos(self):
        """Soles sobrevividos (el sol del colapso no cuenta)."""
        if len(self._ciclos) == 0:
            return 0
        if self._ciclos[-1].nivel == "colapso":
            return len(self._ciclos) - 1
        return len(self._ciclos)

    def evento_comun(self):
        """(nombre, veces) del evento más frecuente (o None)."""
        if len(self._eventos) == 0:
            return None
        conteo = {}
        for evento in self._eventos:
            conteo[evento.nombre] = conteo.get(evento.nombre, 0) + 1
        mejor = None
        for nombre in conteo:
            if mejor is None or conteo[nombre] > conteo[mejor]:
                mejor = nombre
        return mejor, conteo[mejor]

    def colonos_riesgo(self):
        """Colonos con menos de 50 de salud."""
        riesgo = []
        for colono in self._colonos:
            if colono.en_riesgo():
                riesgo.append(colono)
        return riesgo

    def sostenibilidad(self):
        """(es_sostenible, recursos_en_deficit) o None si no hay ciclos."""
        if len(self._ciclos) == 0:
            return None
        deficit = []
        for recurso in self._recursos:
            if recurso.es_vital and recurso.neto < 0:
                deficit.append(recurso.nombre)
        return len(deficit) == 0, deficit
