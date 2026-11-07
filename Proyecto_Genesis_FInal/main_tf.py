
from entidades import Recurso, RECURSOS_BASE
from jerarquia import ROLES, TIPOS
from jerarquia import Ingeniero, Medico, Cientifico, Agricultor, Piloto
from jerarquia import Habitat, Granja, PlantaOxigeno, Generador, Laboratorio
from colonia import Colonia
from motor import Motor
from persistencia import Almacen
from analitica import Reporte

def pedir_texto(mensaje):
    """Pide texto (letras, números y espacios) hasta que sea válido."""
    while True:
        dato = input(mensaje).strip()
        if dato != "" and dato.replace(" ", "").isalnum():
            return dato
        print("Error: ingrese solo letras, números y espacios.")


def pedir_entero(mensaje, minimo, maximo):
    """Pide un entero entre minimo y maximo."""
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Error: ingrese un número entero.")
            continue
        if numero >= minimo and numero <= maximo:
            return numero
        print("Error: el número debe estar entre", minimo, "y", maximo)


def pedir_cantidad(mensaje):
    """Pide un número real que no sea negativo."""
    while True:
        try:
            cantidad = float(input(mensaje))
        except ValueError:
            print("Error: ingrese un número válido.")
            continue
        if cantidad >= 0:
            return cantidad
        print("Error: la cantidad no puede ser negativa.")


def confirmar(mensaje):
    """Devuelve True si el usuario responde 's'."""
    return input(mensaje).strip().lower() == "s"


def elegir(opciones):
    """Muestra una lista numerada y devuelve la opción elegida."""
    lista = list(opciones)
    for numero in range(len(lista)):
        print(numero + 1, ".", lista[numero])
    eleccion = pedir_entero("Elija el número: ", 1, len(lista))
    return lista[eleccion - 1]


def mostrar_colono(colono):
    print("-----------------------------")
    print("Nombre:", colono.nombre)
    print("Rol:", colono.rol)
    print("Edad:", colono.edad)
    print("Salud:", colono.salud)
    print("Habilidad:", colono.habilidad)
    print("Trabaja en:", colono.destino)

def crear_demo():
    """Colonia de ejemplo con 5 colonos, 5 recursos y 6 edificios."""
    colonia = Colonia("Genesis")
    recursos = (("Oxígeno", 150, 4, 2), ("Agua", 150, 4, 2),
                ("Comida", 150, 3, 2), ("Energía", 100, 5, 8),
                ("Materiales", 120, 3, 0))
    for nombre, cantidad, produccion, consumo in recursos:
        colonia.agregar_recurso(Recurso(nombre, cantidad, produccion, consumo))

    equipo = (("Brayan Morales", Ingeniero, 30, "Reparaciones"),
              ("Angelica Ramirez", Medico, 41, "Cirugia"),
              ("Miguel Berrocal", Cientifico, 35, "Genetica"),
              ("Roy Garcia", Agricultor, 28, "Cultivos"),
              ("Anghelo Chavez", Piloto, 33, "Navegacion"))
    for nombre, clase, edad, habilidad in equipo:
        colonia.agregar_colono(clase(nombre, edad, 100, habilidad))

    edificios = (("Planta Alfa", PlantaOxigeno, 40, True, 3),
                 ("Granja Alfa", Granja, 30, True, 3),
                 ("Generador Alfa", Generador, 35, True, 3),
                 ("Habitat Alfa", Habitat, 25, True, 3),
                 ("Granja Beta", Granja, 30, False, 1),
                 ("Laboratorio Alfa", Laboratorio, 45, False, 2))
    for nombre, clase, costo, construido, prioridad in edificios:
        colonia.agregar_edificio(
            clase(nombre, 1, costo, construido, 0.0, prioridad))
    return colonia


class Menu:
    """Interfaz de consola. Coordina Colonia, Motor, Almacen y Reporte."""

    def __init__(self, colonia, almacen):
        self.colonia = colonia
        self.almacen = almacen

    @property
    def colonia(self):
        return self._colonia

    @colonia.setter
    def colonia(self, valor):
        if not isinstance(valor, Colonia):
            raise ValueError("colonia: debe ser un objeto Colonia.")
        self._colonia = valor
        self._motor = Motor(valor)    

    @property
    def motor(self):
        return self._motor

    @property
    def almacen(self):
        return self._almacen

    @almacen.setter
    def almacen(self, valor):
        if not isinstance(valor, Almacen):
            raise ValueError("almacen: debe ser un objeto Almacen.")
        self._almacen = valor

    def ejecutar(self):
        while True:
            print("\n=============================")
            print(" PROYECTO GENESIS - SIMULADOR")
            print("=============================")
            print("Nivel de crisis:", self._colonia.nivel_actual().upper())
            print("1. Gestión de colonos")
            print("2. Registrar recurso")
            print("3. Gestión de edificios")
            print("4. Simulación (avanzar soles)")
            print("5. Ver estado de la colonia")
            print("6. Reportes")
            print("7. Métricas y gráficos")
            print("8. Guardar datos (CSV)")
            print("9. Cargar datos (CSV)")
            print("10. Salir")
            opcion = pedir_entero("Ingrese una opción: ", 1, 10)

            if self._colonia.nivel_actual() == "colapso" and opcion <= 4:
                print("La colonia colapsó. Solo puede ver el estado, los "
                      "reportes, los gráficos, guardar, cargar o salir.")
                continue

            if opcion == 1:
                self.menu_colonos()
            elif opcion == 2:
                self.nuevo_recurso()
            elif opcion == 3:
                self.menu_edificios()
            elif opcion == 4:
                self.menu_simulacion()
            elif opcion == 5:
                self.mostrar_estado()
            elif opcion == 6:
                self.menu_reportes()
            elif opcion == 7:
                self.menu_graficos()
            elif opcion == 8:
                self.guardar_datos()
            elif opcion == 9:
                self.cargar_datos()
            else:
                if confirmar("¿Guardar los datos antes de salir? (s/n): "):
                    self.guardar_datos()
                print("Cerrando el simulador...")
                break

    def menu_colonos(self):
        while True:
            print("\n--- GESTIÓN DE COLONOS ---")
            print("1. Registrar colono")
            print("2. Listar colonos por rol")
            print("3. Editar colono")
            print("4. Eliminar colono")
            print("5. Asignar colono a un edificio")
            print("6. Liberar colono de su edificio")
            print("7. Volver")
            opcion = pedir_entero("Opción: ", 1, 7)
            if opcion == 1:
                self.nuevo_colono()
            elif opcion == 2:
                self.listar_colonos()
            elif opcion == 3:
                self.editar_colono()
            elif opcion == 4:
                self.quitar_colono()
            elif opcion == 5:
                self.asignar_obrero()
            elif opcion == 6:
                self.liberar_obrero()
            else:
                break

    def nuevo_colono(self):
        nombre = pedir_texto("Nombre del colono: ").title()
        if self._colonia.buscar_colono(nombre) is not None:
            print("Error: ya existe un colono con ese nombre.")
            return
        print("Roles disponibles:")
        rol = elegir(ROLES.keys())
        edad = pedir_entero("Edad (18-65): ", 18, 65)
        salud = pedir_entero("Salud (1-100): ", 1, 100)
        habilidad = pedir_texto("Habilidad principal: ")
        try:
            colono = ROLES[rol](nombre, edad, salud, habilidad)
            self._colonia.agregar_colono(colono)
        except ValueError as error:
            print("Error:", error)
            return
        print("Colono registrado correctamente.")

    def listar_colonos(self):
        if len(self._colonia.colonos) == 0:
            print("No hay colonos registrados.")
            return
        print("¿De qué rol desea listar?")
        rol = elegir(ROLES.keys())
        cantidad = 0
        for colono in self._colonia.colonos:
            if colono.rol == rol:
                mostrar_colono(colono)
                cantidad = cantidad + 1
        if cantidad == 0:
            print("No hay colonos con ese rol.")

    def editar_colono(self):
        nombre = pedir_texto("Nombre del colono a editar: ")
        colono = self._colonia.buscar_colono(nombre)
        if colono is None:
            print("No se encontró ningún colono con ese nombre.")
            return
        mostrar_colono(colono)
        print("1. Nombre  2. Rol  3. Edad  4. Salud  5. Habilidad  6. Cancelar")
        opcion = pedir_entero("¿Qué desea editar?: ", 1, 6)
        try:
            if opcion == 1:
                nuevo = pedir_texto("Nuevo nombre: ").title()
                self._colonia.renombrar_colono(colono.nombre, nuevo)
            elif opcion == 2:
                rol = elegir(ROLES.keys())
                self._colonia.cambiar_rol(colono.nombre, ROLES[rol])
            elif opcion == 3:
                colono.edad = pedir_entero("Nueva edad (18-65): ", 18, 65)
            elif opcion == 4:
                colono.salud = pedir_entero("Nueva salud (1-100): ", 1, 100)
            elif opcion == 5:
                colono.habilidad = pedir_texto("Nueva habilidad: ")
            else:
                print("Edición cancelada.")
                return
        except ValueError as error:
            print("Error:", error)
            return
        print("Colono editado correctamente.")

    def quitar_colono(self):
        nombre = pedir_texto("Nombre del colono a eliminar: ")
        if self._colonia.buscar_colono(nombre) is None:
            print("No se encontró ningún colono con ese nombre.")
            return
        if confirmar("¿Seguro que desea eliminarlo? (s/n): "):
            self._colonia.eliminar_colono(nombre)
            print("Colono eliminado.")
        else:
            print("Eliminación cancelada.")

    def asignar_obrero(self):
        nombre = pedir_texto("Nombre del colono: ")
        edificio = pedir_texto("Nombre del edificio donde trabajará: ")
        try:
            self._colonia.asignar_colono(nombre, edificio)
        except ValueError as error:
            print("Error:", error)
            return
        print("Colono asignado. El edificio produce 20 % más por colono.")

    def liberar_obrero(self):
        nombre = pedir_texto("Nombre del colono a liberar: ")
        try:
            self._colonia.liberar_colono(nombre)
        except ValueError as error:
            print("Error:", error)
            return
        print("Colono liberado.")

    def nuevo_recurso(self):
        print("Recursos disponibles:")
        nombre = elegir(RECURSOS_BASE)
        if self._colonia.buscar_recurso(nombre) is not None:
            print("Error: ese recurso ya está registrado.")
            return
        cantidad = pedir_cantidad("Cantidad actual: ")
        produccion = pedir_cantidad("Producción por ciclo: ")
        consumo = pedir_cantidad("Consumo por ciclo: ")
        try:
            recurso = Recurso(nombre, cantidad, produccion, consumo)
            self._colonia.agregar_recurso(recurso)
        except ValueError as error:
            print("Error:", error)
            return
        print("Recurso registrado correctamente.")

    def menu_edificios(self):
        while True:
            print("\n--- GESTIÓN DE EDIFICIOS ---")
            print("1. Registrar edificio (plano)")
            print("2. Construir edificio")
            print("3. Mejorar edificio")
            print("4. Priorizar un plano")
            print("5. Construir el plano más prioritario")
            print("6. Volver")
            opcion = pedir_entero("Opción: ", 1, 6)
            if opcion == 1:
                self.nuevo_edificio()
            elif opcion == 2:
                self.construir()
            elif opcion == 3:
                self.mejorar()
            elif opcion == 4:
                self.priorizar()
            elif opcion == 5:
                self.construir_plano()
            else:
                break

    def nuevo_edificio(self):
        nombre = pedir_texto("Nombre del edificio: ").title()
        if self._colonia.buscar_edificio(nombre) is not None:
            print("Error: ya existe un edificio con ese nombre.")
            return
        print("Tipos de edificio:")
        tipo = elegir(TIPOS.keys())
        nivel = pedir_entero("Nivel inicial (1-3): ", 1, 3)
        costo = pedir_entero("Costo de construcción en Materiales: ", 1, 10000)
        prioridad = pedir_entero("Prioridad (1 = primero, 5 = al final): ", 1, 5)
        try:
            edificio = TIPOS[tipo](nombre, nivel, costo, False, 0.0, prioridad)
            self._colonia.agregar_edificio(edificio)
        except ValueError as error:
            print("Error:", error)
            return
        print("Edificio registrado (en plano). Produce:", edificio.efecto)

    def construir(self):
        nombre = pedir_texto("Nombre del edificio a construir: ")
        edificio = self._colonia.buscar_edificio(nombre)
        if edificio is None:
            print("No se encontró ningún edificio con ese nombre.")
            return
        if edificio.construido:
            print("Ese edificio ya está construido.")
            return
        mensaje = "Costo: " + str(edificio.costo) + " materiales. ¿Construir? (s/n): "
        if not confirmar(mensaje):
            print("Construcción cancelada.")
            return
        try:
            self._colonia.construir(edificio.nombre)
        except ValueError as error:
            print("Error:", error)
            return
        print("Edificio construido.")

    def mejorar(self):
        nombre = pedir_texto("Nombre del edificio a mejorar: ")
        edificio = self._colonia.buscar_edificio(nombre)
        if edificio is None:
            print("No se encontró ningún edificio con ese nombre.")
            return
        if not edificio.construido:
            print("Primero debe construir el edificio.")
            return
        mensaje = ("Costo de la mejora: " + str(edificio.costo_mejora())
                   + " materiales. ¿Mejorar? (s/n): ")
        if not confirmar(mensaje):
            print("Mejora cancelada.")
            return
        try:
            self._colonia.mejorar(edificio.nombre)
        except ValueError as error:
            print("Error:", error)
            return
        print("Edificio mejorado al nivel", edificio.nivel)

    def priorizar(self):
        nombre = pedir_texto("Nombre del plano a priorizar: ")
        prioridad = pedir_entero("Nueva prioridad (1 = primero, 5 = al final): ", 1, 5)
        try:
            self._colonia.priorizar(nombre, prioridad)
        except ValueError as error:
            print("Error:", error)
            return
        print("Prioridad actualizada.")

    def construir_plano(self):
        plano = self._colonia.plano_siguiente()
        if plano is None:
            print("No hay edificios en plano para construir.")
            return
        print("Plano más prioritario:", plano.nombre, "| Prioridad:",
              plano.prioridad, "| Costo:", plano.costo)
        if not confirmar("¿Construirlo ahora? (s/n): "):
            print("Construcción cancelada.")
            return
        try:
            self._colonia.construir_cola()
        except ValueError as error:
            print("Error:", error)
            return
        print("Edificio construido.")

    def menu_simulacion(self):
        while True:
            print("\n--- SIMULACIÓN ---")
            print("1. Avanzar UN sol")
            print("2. Simular varios soles seguidos")
            print("3. Volver")
            opcion = pedir_entero("Opción: ", 1, 3)
            if opcion == 1:
                self.avanzar_un_sol()
            elif opcion == 2:
                self.simular_varios()
            else:
                break
            if self._colonia.nivel_actual() == "colapso":
                print("La colonia colapsó. Se termina la simulación.")
                break

    def ver_mensajes(self):
        """Imprime lo que el motor registró durante la simulación."""
        for linea in self._motor.vaciar_mensajes():
            print(linea)

    def avanzar_un_sol(self):
        try:
            self._motor.avanzar_ciclo()
        except ValueError as error:
            print("Error:", error)
        self.ver_mensajes()

    def simular_varios(self):
        cantidad = pedir_entero("¿Cuántos soles desea simular? (1-100): ", 1, 100)
        ciclos = self._motor.simular(cantidad)
        self.ver_mensajes()
        print("\nSoles simulados:", len(ciclos))

    def mostrar_estado(self):
        colonia = self._colonia
        print("\n===== ESTADO DE LA COLONIA", colonia.nombre.upper(), "=====")
        print("Soles transcurridos:", len(colonia.ciclos))
        print("Nivel de crisis:", colonia.nivel_actual().upper())

        print("\n--- Recursos ---")
        for recurso in colonia.recursos:
            print("-", recurso.nombre, ":", round(recurso.cantidad, 1),
                  "| Producción:", recurso.produccion,
                  "| Consumo:", recurso.consumo,
                  "| Balance último sol:", recurso.neto)
        if len(colonia.recursos) == 0:
            print("No hay recursos registrados.")

        print("\n--- Colonos ---")
        for colono in colonia.colonos:
            print("-", colono.nombre, "|", colono.rol, "| Salud:",
                  colono.salud, "| Trabaja en:", colono.destino)
        if len(colonia.colonos) == 0:
            print("No hay colonos registrados.")

        print("\n--- Edificios ---")
        for edificio in colonia.edificios:
            if edificio.construido:
                situacion = "Construido"
            else:
                situacion = "En plano (prioridad " + str(edificio.prioridad) + ")"
            print("-", edificio.nombre, "|", edificio.tipo,
                  "| Nivel:", edificio.nivel, "| Produce:", edificio.efecto,
                  "|", situacion,
                  "| Colonos:", colonia.contar_obreros(edificio.nombre))
        if len(colonia.edificios) == 0:
            print("No hay edificios registrados.")

    def menu_reportes(self):
        while True:
            print("\n--- REPORTES ---")
            print("1. Ciclo con mayor producción")
            print("2. Recurso más crítico")
            print("3. Edificio más rentable")
            print("4. Colono más productivo")
            print("5. Ciclos sobrevividos")
            print("6. Evento más frecuente")
            print("7. Colonos en riesgo de salud")
            print("8. Balance de sostenibilidad")
            print("9. Volver")
            opcion = pedir_entero("Opción: ", 1, 9)
            print()
            if opcion == 9:
                break
            self.mostrar_reporte(opcion)

    def mostrar_reporte(self, opcion):
        colonia = self._colonia
        if opcion == 1:
            ciclo = colonia.mejor_ciclo()
            if ciclo is None:
                print("Aún no se ejecutaron soles.")
            else:
                print("Sol con mayor producción: Sol", ciclo.numero,
                      "con", ciclo.produccion)
        elif opcion == 2:
            dato = colonia.recurso_critico()
            if dato is None:
                print("Se necesitan recursos y al menos un sol ejecutado.")
            else:
                print("Recurso más crítico:", dato[0].nombre,
                      "con promedio", round(dato[1], 1))
        elif opcion == 3:
            dato = colonia.mejor_edificio()
            if dato is None:
                print("No hay edificios construidos.")
            else:
                print("Edificio más rentable:", dato[0].nombre,
                      "(producido/costo =", round(dato[1], 2), ")")
        elif opcion == 4:
            colono = colonia.mejor_colono()
            if colono is None:
                print("Se necesitan colonos y al menos un sol ejecutado.")
            else:
                print("Colono más productivo:", colono.nombre,
                      "| Aporte:", round(colono.aporte, 1))
        elif opcion == 5:
            print("Ciclos sobrevividos:", colonia.ciclos_vividos())
        elif opcion == 6:
            dato = colonia.evento_comun()
            if dato is None:
                print("Aún no ocurrieron eventos.")
            else:
                print("Evento más frecuente:", dato[0], "(", dato[1], "veces )")
        elif opcion == 7:
            riesgo = colonia.colonos_riesgo()
            for colono in riesgo:
                print("En riesgo:", colono.nombre, "| Salud:", colono.salud)
            if len(riesgo) == 0:
                print("Ningún colono está en riesgo de salud.")
        else:
            dato = colonia.sostenibilidad()
            if dato is None:
                print("Aún no se ejecutaron soles.")
            elif dato[0]:
                print("Estado: LA COLONIA ES AUTOSUSTENTABLE.")
            else:
                print("Estado: LA COLONIA TIENE DÉFICIT en:", ", ".join(dato[1]))

    def menu_graficos(self):
        while True:
            print("\n--- MÉTRICAS Y GRÁFICOS ---")
            print("1. Ver métricas estadísticas")
            print("2. Generar los 5 gráficos")
            print("3. Volver")
            opcion = pedir_entero("Opción: ", 1, 3)
            if opcion == 3:
                break
            try:
                tablas = self._almacen.a_tablas(self._colonia)
                reporte = Reporte(tablas)
                if opcion == 1:
                    metricas = reporte.metricas()
                    for nombre in metricas:
                        print("-", nombre, ":", metricas[nombre])
                else:
                    creados = reporte.generar_todos(True, True)
                    print("Gráficos generados:", creados,
                          "(también guardados como g_*.png)")
            except ValueError as error:
                print("Error:", error)

    def guardar_datos(self):
        try:
            archivos = self._almacen.guardar(self._colonia)
        except (OSError, ValueError) as error:
            print("Error al guardar:", error)
            return
        print("Se guardaron", archivos, "archivos CSV.")

    def cargar_datos(self):
        if not self._almacen.hay_datos():
            print("No hay datos guardados para cargar.")
            return
        if not confirmar("Se reemplazará la colonia actual. ¿Continuar? (s/n): "):
            print("Carga cancelada.")
            return
        try:
            self.colonia = self._almacen.cargar()
        except (FileNotFoundError, ValueError) as error:
            print("Error al cargar:", error)
            return
        print("Datos cargados correctamente.")

def principal():
    almacen = Almacen()
    colonia = Colonia()
    cargado = False

    if almacen.hay_datos():
        if confirmar("Se encontraron datos guardados. ¿Cargarlos? (s/n): "):
            try:
                colonia = almacen.cargar()
                cargado = True
                print("Datos cargados correctamente.")
            except (FileNotFoundError, ValueError) as error:
                print("No se pudieron cargar los datos:", error)

    if not cargado and confirmar("¿Cargar datos de ejemplo? (s/n): "):
        colonia = crear_demo()
        print("Datos de ejemplo cargados.")

    Menu(colonia, almacen).ejecutar()


if __name__ == "__main__":
    principal()
