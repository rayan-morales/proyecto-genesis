import random

colonos = []         
recursos = []         
edificios = []        
eventos_dados = []    
historial = []        
soles = 0             
en_crisis = False     

roles = ["Ingeniero", "Médico", "Científico", "Agricultor", "Piloto"]
tipos = ["Hábitat", "Granja", "Planta de oxígeno", "Generador", "Laboratorio"]
recursos_base = ["Oxígeno", "Agua", "Comida", "Energía", "Materiales"]
vitales = ["Oxígeno", "Agua", "Comida"]   
textos_evento = [
    "Tormenta de polvo (-20 de energía)",
    "Fuga de oxígeno (-15 de oxígeno)",
    "Enfermedad (-10 de salud)",
    "Llegada de suministros (+25 de comida y agua)",
    "Descubrimiento científico (+30 materiales)",
    "Sin novedades",
]
 
def pedir_texto(mensaje):
    
    while True:
        dato = input(mensaje).strip()
        if dato != "" and dato.replace(" ", "").isalpha():
            return dato
        print("Error: ingrese solo letras y espacios.")

def pedir_entero(mensaje, minimo, maximo):
    
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
   
    respuesta = input(mensaje).lower()
    return respuesta == "s"

def buscar(lista, nombre):
    
    for elemento in lista:
        if elemento["nombre"].lower() == nombre.lower():
            return elemento
    return None

def elegir(opciones):
   
    for numero in range(len(opciones)):
        print(numero + 1, ".", opciones[numero])
    eleccion = pedir_entero("Elija el número: ", 1, len(opciones))
    return opciones[eleccion - 1]

def mostrar_colono(colono):
    print("-----------------------------")
    print("Nombre:", colono["nombre"])
    print("Rol:", colono["rol"])
    print("Edad:", colono["edad"])
    print("Salud:", colono["salud"])
    print("Habilidad:", colono["habilidad"])

def crear_colono():
  
    nombre = pedir_texto("Nombre del colono: ").title()
    if buscar(colonos, nombre) is not None:
        print("Error: ya existe un colono con ese nombre.")
        return
    print("Roles disponibles:")
    rol = elegir(roles)
    edad = pedir_entero("Edad (18-65): ", 18, 65)
    salud = pedir_entero("Salud (1-100): ", 1, 100)
    habilidad = pedir_texto("Habilidad principal: ")

    colono = {
        "nombre": nombre,
        "rol": rol,
        "edad": edad,
        "salud": salud,
        "habilidad": habilidad,
        "aporte": 0,   
    }
    colonos.append(colono)
    print("Colono registrado correctamente.")

def listar_colonos():
   
    if len(colonos) == 0:
        print("No hay colonos registrados.")
        return
    print("¿De qué rol desea listar?")
    rol = elegir(roles)
    cantidad = 0
    for colono in colonos:
        if colono["rol"] == rol:
            mostrar_colono(colono)
            cantidad = cantidad + 1
    if cantidad == 0:
        print("No hay colonos con ese rol.")

def editar_colono():

    nombre = pedir_texto("Nombre del colono a editar: ")
    colono = buscar(colonos, nombre)
    if colono is None:
        print("No se encontró ningún colono con ese nombre.")
        return

    mostrar_colono(colono)
    print("1. Nombre  2. Rol  3. Edad  4. Salud  5. Habilidad  6. Cancelar")
    opcion = pedir_entero("¿Qué desea editar?: ", 1, 6)

    if opcion == 1:
        nuevo = pedir_texto("Nuevo nombre: ").title()
        if buscar(colonos, nuevo) is not None:
            print("Error: ya existe un colono con ese nombre.")
            return
        colono["nombre"] = nuevo
    elif opcion == 2:
        colono["rol"] = elegir(roles)
    elif opcion == 3:
        colono["edad"] = pedir_entero("Nueva edad (18-65): ", 18, 65)
    elif opcion == 4:
        colono["salud"] = pedir_entero("Nueva salud (1-100): ", 1, 100)
    elif opcion == 5:
        colono["habilidad"] = pedir_texto("Nueva habilidad: ")
    else:
        print("Edición cancelada.")
        return
    print("Colono editado correctamente.")

def eliminar_colono():

    nombre = pedir_texto("Nombre del colono a eliminar: ")
    colono = buscar(colonos, nombre)
    if colono is None:
        print("No se encontró ningún colono con ese nombre.")
        return
    if confirmar("¿Seguro que desea eliminarlo? (s/n): "):
        colonos.remove(colono)
        print("Colono eliminado.")
    else:
        print("Eliminación cancelada.")

def menu_colonos():
    while True:
        print("\n--- GESTIÓN DE COLONOS ---")
        print("1. Listar colonos por rol")
        print("2. Editar colono")
        print("3. Eliminar colono")
        print("4. Volver")
        opcion = pedir_entero("Opción: ", 1, 4)
        if opcion == 1:
            listar_colonos()
        elif opcion == 2:
            editar_colono()
        elif opcion == 3:
            eliminar_colono()
        else:
            break

def crear_recurso():
    
    print("Recursos disponibles:")
    nombre = elegir(recursos_base)
    if buscar(recursos, nombre) is not None:
        print("Error: ese recurso ya está registrado.")
        return
    cantidad = pedir_cantidad("Cantidad actual: ")
    produccion = pedir_cantidad("Producción por ciclo: ")
    consumo = pedir_cantidad("Consumo por ciclo: ")

    recurso = {
        "nombre": nombre,
        "cantidad": cantidad,
        "produccion": produccion,
        "consumo": consumo,
        "suma": 0,    
        "neto": 0,    
    }
    recursos.append(recurso)
    print("Recurso registrado correctamente.")

def crear_edificio():
    
    nombre = pedir_texto("Nombre del edificio: ").title()
    if buscar(edificios, nombre) is not None:
        print("Error: ya existe un edificio con ese nombre.")
        return
    print("Tipos de edificio:")
    tipo = elegir(tipos)
    nivel = pedir_entero("Nivel inicial (1-3): ", 1, 3)
    costo = pedir_entero("Costo de construcción en Materiales: ", 1, 10000)
    print("¿Qué recurso produce este edificio?")
    efecto = elegir(recursos_base)

    edificio = {
        "nombre": nombre,
        "tipo": tipo,
        "nivel": nivel,
        "costo": costo,
        "efecto": efecto,
        "construido": False,
        "producido": 0,   
    }
    edificios.append(edificio)
    print("Edificio registrado (en plano).")

def construir():

    nombre = pedir_texto("Nombre del edificio a construir: ")
    edificio = buscar(edificios, nombre)
    if edificio is None:
        print("No se encontró ningún edificio con ese nombre.")
        return
    if edificio["construido"]:
        print("Ese edificio ya está construido.")
        return

    materiales = buscar(recursos, "Materiales")
    if materiales is None:
        print("Error: primero registre el recurso Materiales.")
        return
    if materiales["cantidad"] < edificio["costo"]:
        print("No hay materiales suficientes. Costo:", edificio["costo"])
        return

    if confirmar("¿Desea construirlo? (s/n): "):
        materiales["cantidad"] = materiales["cantidad"] - edificio["costo"]
        edificio["construido"] = True
        print("Edificio construido. Materiales restantes:", materiales["cantidad"])
    else:
        print("Construcción cancelada.")

def mejorar_nivel():
    
    nombre = pedir_texto("Nombre del edificio a mejorar: ")
    edificio = buscar(edificios, nombre)
    if edificio is None:
        print("No se encontró ningún edificio con ese nombre.")
        return
    if not edificio["construido"]:
        print("Primero debe construir el edificio.")
        return
    if edificio["nivel"] >= 5:
        print("El edificio ya está en el nivel máximo (5).")
        return

    materiales = buscar(recursos, "Materiales")
    if materiales is None:
        print("Error: primero registre el recurso Materiales.")
        return

    costo_mejora = edificio["costo"] / 2 * edificio["nivel"]
    print("Costo de la mejora:", costo_mejora)
    if materiales["cantidad"] < costo_mejora:
        print("No hay materiales suficientes para mejorar.")
        return

    if confirmar("¿Desea mejorarlo? (s/n): "):
        materiales["cantidad"] = materiales["cantidad"] - costo_mejora
        edificio["nivel"] = edificio["nivel"] + 1
        print("Edificio mejorado al nivel", edificio["nivel"])
    else:
        print("Mejora cancelada.")

def aporte_colono(colono):

    return 3 * colono["salud"] / 100

def recurso_rol(rol):
   
    if rol == "Ingeniero":
        return "Energía"
    if rol == "Científico":
        return "Oxígeno"
    if rol == "Agricultor":
        return "Comida"
    if rol == "Piloto":
        return "Materiales"
    return ""

def cambiar(nombre, cantidad):
   
    recurso = buscar(recursos, nombre)
    if recurso is not None:
        recurso["cantidad"] = max(0, recurso["cantidad"] + cantidad)

def aplicar_evento():
 
    numero = random.randint(1, 6)
    eventos_dados.append(numero)
    print("\n[EVENTO ALEATORIO]:", textos_evento[numero - 1])

    if numero == 1:
        cambiar("Energía", -20)
    elif numero == 2:
        cambiar("Oxígeno", -15)
    elif numero == 3:
        for colono in colonos:
            colono["salud"] = max(0, colono["salud"] - 10)
    elif numero == 4:
        cambiar("Comida", 25)
        cambiar("Agua", 25)
    elif numero == 5:
        cambiar("Materiales", 30)

def revisar_salud():

    for colono in colonos[:]:
        if colono["salud"] <= 0:
            colonos.remove(colono)
            print("El colono", colono["nombre"], "ha fallecido.")

def revisar_crisis():
 
    global en_crisis
    for recurso in recursos:
        if recurso["nombre"] in vitales and recurso["cantidad"] <= 0:
            print("\n¡CRISIS TERMINAL! Se agotó:", recurso["nombre"])
            en_crisis = True
    if len(colonos) == 0:
        print("\n¡CRISIS TERMINAL! No quedan colonos.")
        en_crisis = True

def avanzar_ciclo():
 
    global soles
    if en_crisis:
        print("La colonia está en crisis terminal. No se puede avanzar.")
        return
    if len(colonos) == 0:
        print("Error: registre al menos un colono.")
        return
    for nombre in recursos_base:
        if buscar(recursos, nombre) is None:
            print("Error: falta registrar el recurso", nombre)
            return

    soles = soles + 1
    print("\n===== SOL MARCIANO #", soles, "=====")

    energia = buscar(recursos, "Energía")
    hay_energia = energia["cantidad"] > 0
    if not hay_energia:
        print("¡COLAPSO ENERGÉTICO! Solo funcionan los edificios de energía.")

    curacion = 0
    for colono in colonos:
        colono["aporte"] = colono["aporte"] + aporte_colono(colono)
        if colono["rol"] == "Médico":
            curacion = curacion + 5

    total_producido = 0
    for recurso in recursos:
        produccion = recurso["produccion"]
        consumo = recurso["consumo"]

        if recurso["nombre"] in vitales:
            consumo = consumo + len(colonos)

        for colono in colonos:
            if recurso_rol(colono["rol"]) == recurso["nombre"]:
                produccion = produccion + aporte_colono(colono)

        for edificio in edificios:
            if edificio["construido"] and edificio["efecto"] == recurso["nombre"]:
                if hay_energia or recurso["nombre"] == "Energía":
                    ganancia = 5 * edificio["nivel"]
                    produccion = produccion + ganancia
                    edificio["producido"] = edificio["producido"] + ganancia

        nuevo = recurso["cantidad"] + produccion - consumo
        recurso["cantidad"] = round(max(0, nuevo), 1)
        recurso["neto"] = produccion - consumo
        total_producido = total_producido + produccion
        print(recurso["nombre"], "->", recurso["cantidad"],
              "(+", round(produccion, 1), "-", round(consumo, 1), ")")

    for colono in colonos:
        colono["salud"] = min(100, colono["salud"] + curacion)

    revisar_crisis()
    if not en_crisis:
        aplicar_evento()
        revisar_salud()
        revisar_crisis()

    for recurso in recursos:
        recurso["suma"] = recurso["suma"] + recurso["cantidad"]
    historial.append(round(total_producido, 1))

def mostrar_estado():
    print("\n===== ESTADO DE LA COLONIA =====")
    print("Soles transcurridos:", soles)
    if en_crisis:
        print("Estado: EN CRISIS TERMINAL")
    else:
        print("Estado: ESTABLE")

    print("\n--- Recursos ---")
    for recurso in recursos:
        print("-", recurso["nombre"], ":", round(recurso["cantidad"], 1),
              "| Producción:", recurso["produccion"],
              "| Consumo:", recurso["consumo"])
    if len(recursos) == 0:
        print("No hay recursos registrados.")

    print("\n--- Colonos ---")
    for colono in colonos:
        print("-", colono["nombre"], "|", colono["rol"], "| Salud:", colono["salud"])
    if len(colonos) == 0:
        print("No hay colonos registrados.")

    print("\n--- Edificios ---")
    for edificio in edificios:
        if edificio["construido"]:
            situacion = "Construido"
        else:
            situacion = "En plano"
        print("-", edificio["nombre"], "|", edificio["tipo"],
              "| Nivel:", edificio["nivel"], "| Produce:", edificio["efecto"],
              "|", situacion)
    if len(edificios) == 0:
        print("No hay edificios registrados.")


def promedio(recurso):

    if soles == 0:
        return recurso["cantidad"]
    return recurso["suma"] / soles

def reporte_1():

    if len(historial) == 0:
        print("Aún no se ejecutaron soles.")
        return
    mejor = 0
    for posicion in range(len(historial)):
        if historial[posicion] > historial[mejor]:
            mejor = posicion
    print("Sol con mayor producción: Sol", mejor + 1, "con", historial[mejor])

def reporte_2():

    if len(recursos) == 0:
        print("No hay recursos registrados.")
        return
    critico = recursos[0]
    for recurso in recursos:
        if promedio(recurso) < promedio(critico):
            critico = recurso
    print("Recurso más crítico:", critico["nombre"],
          "con promedio", round(promedio(critico), 1))

def reporte_3():
    
    mejor = None
    mejor_razon = 0
    for edificio in edificios:
        if edificio["construido"]:
            razon = edificio["producido"] / edificio["costo"]
            if mejor is None or razon > mejor_razon:
                mejor = edificio
                mejor_razon = razon
    if mejor is None:
        print("No hay edificios construidos.")
        return
    print("Edificio más rentable:", mejor["nombre"],
          "(producido/costo =", round(mejor_razon, 2), ")")

def reporte_4():

    if len(colonos) == 0 or soles == 0:
        print("Se necesitan colonos y al menos un sol ejecutado.")
        return
    mejor = colonos[0]
    for colono in colonos:
        if colono["aporte"] > mejor["aporte"]:
            mejor = colono
    print("Colono más productivo:", mejor["nombre"],
          "| Aporte:", round(mejor["aporte"], 1))

def reporte_5():
    
    if en_crisis:
        print("Ciclos sobrevividos:", soles - 1)
    else:
        print("Ciclos sobrevividos:", soles)

def reporte_6():
   
    if len(eventos_dados) == 0:
        print("Aún no ocurrieron eventos.")
        return
    mejor = 1
    for numero in range(1, 7):
        if eventos_dados.count(numero) > eventos_dados.count(mejor):
            mejor = numero
    print("Evento más frecuente:", textos_evento[mejor - 1],
          "(", eventos_dados.count(mejor), "veces )")
def reporte_7():


    hay_riesgo = False
    for colono in colonos:
        if colono["salud"] < 50:
            print("En riesgo:", colono["nombre"], "| Salud:", colono["salud"])
            hay_riesgo = True
    if not hay_riesgo:
        print("Ningún colono está en riesgo de salud.")

def reporte_8():
    
    if soles == 0:
        print("Aún no se ejecutaron soles.")
        return
    hay_deficit = False
    for recurso in recursos:
        print("-", recurso["nombre"], "| Balance del último sol:",
              round(recurso["neto"], 1))
        if recurso["nombre"] in vitales and recurso["neto"] < 0:
            hay_deficit = True
    if hay_deficit:
        print("Estado: LA COLONIA TIENE DÉFICIT en recursos vitales.")
    else:
        print("Estado: LA COLONIA ES AUTOSUSTENTABLE.")

def menu_reportes():
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
        if opcion == 1:
            reporte_1()
        elif opcion == 2:
            reporte_2()
        elif opcion == 3:
            reporte_3()
        elif opcion == 4:
            reporte_4()
        elif opcion == 5:
            reporte_5()
        elif opcion == 6:
            reporte_6()
        elif opcion == 7:
            reporte_7()
        elif opcion == 8:
            reporte_8()
        else:
            break

def cargar_demo():
    
    datos = [
        ("Oxígeno", 150, 4, 2),
        ("Agua", 150, 4, 2),
        ("Comida", 150, 3, 2),
        ("Energía", 100, 5, 10),
        ("Materiales", 120, 3, 0),
    ]
    for nombre, cantidad, produccion, consumo in datos:
        recursos.append({"nombre": nombre, "cantidad": cantidad,
                         "produccion": produccion, "consumo": consumo,
                         "suma": 0, "neto": 0})

    equipo = [
        ("Brayan Morales", "Ingeniero", 30, "Reparaciones"),
        ("Angelica Ramirez", "Médico", 41, "Cirugia"),
        ("Miguel Berrocal", "Científico", 35, "Genetica"),
        ("Roy Garcia", "Agricultor", 28, "Cultivos"),
        ("Anghelo Chavez", "Piloto", 33, "Navegacion"),
    ]
    for nombre, rol, edad, habilidad in equipo:
        colonos.append({"nombre": nombre, "rol": rol, "edad": edad,
                        "salud": 100, "habilidad": habilidad, "aporte": 0})

    planos = [
        ("Planta Alfa", "Planta de oxígeno", 40, "Oxígeno"),
        ("Granja Alfa", "Granja", 30, "Comida"),
        ("Generador Alfa", "Generador", 35, "Energía"),
        ("Habitat Alfa", "Hábitat", 25, "Agua"),
    ]
    for nombre, tipo, costo, efecto in planos:
        edificios.append({"nombre": nombre, "tipo": tipo, "nivel": 1,
                          "costo": costo, "efecto": efecto,
                          "construido": True, "producido": 0})
    print("Datos de ejemplo cargados.")

def principal():
    if confirmar("¿Cargar datos de ejemplo? (s/n): "):
        cargar_demo()

    while True:
        print("\n=============================")
        print(" PROYECTO GENESIS - SIMULADOR")
        print("=============================")
        print("1. Registrar colono")
        print("2. Listar y gestionar colonos")
        print("3. Registrar recurso")
        print("4. Registrar edificio")
        print("5. Construir edificio")
        print("6. Mejorar edificio")
        print("7. Avanzar ciclo (sol)")
        print("8. Ver estado de la colonia")
        print("9. Ver reportes")
        print("10. Salir")
        opcion = pedir_entero("Ingrese una opción: ", 1, 10)

        if en_crisis and opcion < 8:
            print("La colonia colapsó. Solo puede ver estado, reportes o salir.")
            continue

        if opcion == 1:
            crear_colono()
        elif opcion == 2:
            menu_colonos()
        elif opcion == 3:
            crear_recurso()
        elif opcion == 4:
            crear_edificio()
        elif opcion == 5:
            construir()
        elif opcion == 6:
            mejorar_nivel()
        elif opcion == 7:
            avanzar_ciclo()
        elif opcion == 8:
            mostrar_estado()
        elif opcion == 9:
            menu_reportes()
        else:
            print("Cerrando el simulador...")
            break

principal()
