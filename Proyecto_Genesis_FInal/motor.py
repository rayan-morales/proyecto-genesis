
import random
from entidades import RECURSOS_BASE, validar_entero
from colonia import Colonia, Ciclo
from jerarquia import Tormenta, Fuga, Enfermedad, Suministro, Descubrimiento


class Motor:
    

    def __init__(self, colonia):
        self.colonia = colonia
        self._mensajes = []
      
        self._clases = (Tormenta, Fuga, Enfermedad, Suministro, Descubrimiento)


    @property
    def colonia(self):
        return self._colonia

    @colonia.setter
    def colonia(self, valor):
        if not isinstance(valor, Colonia):
            raise ValueError("colonia: debe ser un objeto Colonia.")
        self._colonia = valor

    @property
    def catalogo(self):
        return self._clases

    def vaciar_mensajes(self):
        """Devuelve los mensajes acumulados y deja la lista vacía."""
        mensajes = self._mensajes
        self._mensajes = []
        return mensajes

   
    def validar_inicio(self):
        """Lanza ValueError si la colonia no puede avanzar un ciclo."""
        colonia = self._colonia
        if colonia.nivel_actual() == "colapso":
            raise ValueError("La colonia está en colapso. No se puede avanzar.")
        if len(colonia.colonos) == 0:
            raise ValueError("Registre al menos un colono.")
        for nombre in RECURSOS_BASE:
            if colonia.buscar_recurso(nombre) is None:
                raise ValueError("Falta registrar el recurso " + nombre + ".")
    def sortear_evento(self):
        """Devuelve un Evento al azar o None (1 de cada 6: sin novedades)."""
        numero = random.randint(0, len(self._clases))
        if numero == len(self._clases):
            return None
        return self._clases[numero]()

    def avanzar_ciclo(self):
        """Simula UN sol y devuelve el objeto Ciclo registrado."""
        self.validar_inicio()
        colonia = self._colonia
        numero = len(colonia.ciclos) + 1
        self._mensajes.append("===== SOL MARCIANO #" + str(numero) + " =====")

        hay_energia = colonia.buscar_recurso("Energía").cantidad > 0
        if not hay_energia:
            self._mensajes.append(
                "¡COLAPSO ENERGÉTICO! Solo funcionan los generadores.")

        extra = {"Salud": 0.0}
        gasto = {}
        for nombre in RECURSOS_BASE:
            extra[nombre] = 0.0
            gasto[nombre] = 0.0

        for colono in colonia.colonos:
            bono = colono.bonificacion()
            colono.aporte = colono.aporte + bono
            if colono.objetivo in extra:
                extra[colono.objetivo] = extra[colono.objetivo] + bono

        for edificio in colonia.edificios:
            if not edificio.construido:
                continue
            edificio.obreros = colonia.contar_obreros(edificio.nombre)
            ganancia = round(edificio.producir(hay_energia), 2)
            edificio.producido = edificio.producido + ganancia
            extra[edificio.efecto] = extra[edificio.efecto] + ganancia
            gasto["Energía"] = gasto["Energía"] + edificio.consumo_energia()

        poblacion = len(colonia.colonos)
        total_prod = 0.0
        total_cons = 0.0
        for recurso in colonia.recursos:
            produccion = recurso.produccion + extra[recurso.nombre]
            consumo = recurso.consumo + gasto[recurso.nombre]
            if recurso.es_vital:
                consumo = consumo + poblacion      
            nuevo = recurso.cantidad + produccion - consumo
            recurso.cantidad = round(max(0.0, nuevo), 1)
            recurso.neto = round(produccion - consumo, 1)
            total_prod = total_prod + produccion
            total_cons = total_cons + consumo
            self._mensajes.append(
                recurso.nombre + " -> " + str(recurso.cantidad)
                + "  (+" + str(round(produccion, 1))
                + " -" + str(round(consumo, 1)) + ")")

        if extra["Salud"] > 0:
            colonia.sanar_colonos(extra["Salud"])

        nivel = colonia.evaluar_crisis()
        nombre_evento = "Ninguno"
        if nivel != "colapso":
            evento = self.sortear_evento()
            if evento is None:
                self._mensajes.append("[EVENTO] Sin novedades")
            else:
                evento.ciclo = numero
                texto = evento.aplicar(colonia)  
                colonia.agregar_evento(evento)
                nombre_evento = evento.nombre
                self._mensajes.append("[EVENTO] " + texto)
            for nombre in colonia.retirar_muertos():
                self._mensajes.append("El colono " + nombre + " ha fallecido.")
            nivel = colonia.evaluar_crisis()

        if nivel == "colapso":
            self._mensajes.append("¡COLAPSO TERMINAL! La colonia no sobrevivió.")
        elif nivel != "estable":
            self._mensajes.append("Nivel de crisis: " + nivel.upper())

        existencias = {}
        for recurso in colonia.recursos:
            recurso.suma = round(recurso.suma + recurso.cantidad, 1)
            existencias[recurso.nombre] = recurso.cantidad
        ciclo = Ciclo(numero, round(total_prod, 1), round(total_cons, 1),
                      nombre_evento, nivel, len(colonia.colonos), existencias)
        colonia.agregar_ciclo(ciclo)
        return ciclo

    def simular(self, cantidad):
        """Simula varios soles seguidos. Se detiene si hay colapso."""
        cantidad = validar_entero(cantidad, 1, 1000, "cantidad")
        ciclos = []
        for _ in range(cantidad):
            try:
                ciclo = self.avanzar_ciclo()
            except ValueError as error:
                self._mensajes.append("Simulación detenida: " + str(error))
                break
            ciclos.append(ciclo)
            if ciclo.nivel == "colapso":
                break
        return ciclos
