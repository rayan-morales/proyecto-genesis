import pygame
import sys
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

from colonia import Colonia, Ciclo
from motor import Motor
from persistencia import Almacen
from main_tf import crear_demo
from analitica import Reporte
from entidades import Recurso
from jerarquia import ROLES, TIPOS

root = tk.Tk()
root.withdraw()

pygame.init()

# =====================================================================
# CONFIGURACIÓN VISUAL
# =====================================================================
ANCHO = 1000
ALTO = 700
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Proyecto Génesis - Interfaz Gráfica")

# Colores
BLANCO = (240, 240, 240)
NEGRO = (10, 10, 15)
AZUL_MARTE = (40, 80, 150)
AZUL_HOVER = (60, 110, 190)
ROJO_ALERTA = (200, 50, 50)
VERDE_OK = (50, 200, 50)
GRIS_PANEL = (30, 30, 40, 210)

# Fuentes
try:
    FUENTE_TITULO = pygame.font.SysFont("impact", 42)
    FUENTE_BTN = pygame.font.SysFont("arial", 18, bold=True)
    FUENTE_TEXTO = pygame.font.SysFont("arial", 16)
    FUENTE_METRICAS = pygame.font.SysFont("consolas", 18)
except:
    FUENTE_TITULO = pygame.font.Font(None, 42)
    FUENTE_BTN = pygame.font.Font(None, 24)
    FUENTE_TEXTO = pygame.font.Font(None, 20)
    FUENTE_METRICAS = pygame.font.Font(None, 22)

try:
    FONDO_IMG = pygame.image.load("fondo_espacio.jpg")
    FONDO_IMG = pygame.transform.scale(FONDO_IMG, (ANCHO, ALTO))
except:
    FONDO_IMG = None


# =====================================================================
# CLASE BOTÓN INTERACTIVO
# =====================================================================
class Boton:
    def __init__(self, x, y, ancho, alto, texto, accion):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.accion = accion
        self.color = AZUL_MARTE

    def dibujar(self, superficie):
        pos_mouse = pygame.mouse.get_pos()
        self.color = AZUL_HOVER if self.rect.collidepoint(pos_mouse) else AZUL_MARTE

        pygame.draw.rect(superficie, self.color, self.rect, border_radius=8)
        pygame.draw.rect(superficie, BLANCO, self.rect, width=2, border_radius=8)

        texto_render = FUENTE_BTN.render(self.texto, True, BLANCO)
        rect_texto = texto_render.get_rect(center=self.rect.center)
        superficie.blit(texto_render, rect_texto)

    def procesar_clic(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.accion()


class InterfazGenesis:
    def __init__(self, colonia, almacen):
        self.colonia = colonia
        self.motor = Motor(colonia)
        self.almacen = almacen
        self.reloj = pygame.time.Clock()
        self.mensajes_log = ["[SISTEMA] Inicialización completada."]

        self.estrellas = [
            [random.randint(0, ANCHO), random.randint(0, ALTO), random.randint(1, 3)]
            for _ in range(120)
        ]
        self.datos_pantalla_completa = []

        self.estado_menu = "PRINCIPAL"
        self.menus = {}
        self._construir_menus()

    def log(self, mensaje):
        self.mensajes_log.append(mensaje)
        if len(self.mensajes_log) > 10:
            self.mensajes_log.pop(0)

    def _crear_lista_botones(self, lista_datos):
        botones = []
        x_base, y_base, espacio = 25, 90, 45
        for i, (texto, accion) in enumerate(lista_datos):
            btn = Boton(x_base, y_base + (i * espacio), 310, 38, texto, accion)
            botones.append(btn)
        return botones

    def _construir_menus(self):
        self.menus["PRINCIPAL"] = self._crear_lista_botones(
            [
                ("1. Gestión de colonos", lambda: self.cambiar_menu("COLONOS")),
                ("2. Registrar recurso", self.registrar_recurso),
                ("3. Gestión de edificios", lambda: self.cambiar_menu("EDIFICIOS")),
                (
                    "4. Simulación (avanzar soles)",
                    lambda: self.cambiar_menu("SIMULACION"),
                ),
                ("5. Ver estado de la colonia", self.ver_estado),
                ("6. Reportes", lambda: self.cambiar_menu("REPORTES")),
                ("7. Métricas y gráficos", lambda: self.cambiar_menu("GRAFICOS")),
                ("8. Guardar datos (CSV)", self.guardar_datos),
                ("9. Cargar datos (CSV)", self.cargar_datos),
                ("10. Salir", self.salir),
            ]
        )

        self.menus["COLONOS"] = self._crear_lista_botones(
            [
                ("1. Registrar colono", self.registrar_colono),
                ("2. Eliminar colono", self.eliminar_colono),
                ("3. Asignar a un edificio", self.asignar_colono),
                ("4. Liberar de funciones", self.liberar_colono),
                ("5. Volver", lambda: self.cambiar_menu("PRINCIPAL")),
            ]
        )

        self.menus["EDIFICIOS"] = self._crear_lista_botones(
            [
                ("1. Registrar plano", self.registrar_plano),
                ("2. Construir edificio", self.construir_edificio),
                ("3. Mejorar edificio", self.mejorar_edificio),
                ("4. Priorizar un plano", self.priorizar_plano),
                ("5. Construir plano prioritario", self.construir_prioritario),
                ("6. Volver", lambda: self.cambiar_menu("PRINCIPAL")),
            ]
        )

        self.menus["SIMULACION"] = self._crear_lista_botones(
            [
                ("1. Avanzar UN sol", self.avanzar_un_sol),
                ("2. Simular varios soles", self.simular_varios),
                ("3. Volver", lambda: self.cambiar_menu("PRINCIPAL")),
            ]
        )

        self.menus["REPORTES"] = self._crear_lista_botones(
            [
                ("1. Ciclo mayor producción", lambda: self.mostrar_reporte(1)),
                ("2. Recurso más crítico", lambda: self.mostrar_reporte(2)),
                ("3. Edificio más rentable", lambda: self.mostrar_reporte(3)),
                ("4. Colono más productivo", lambda: self.mostrar_reporte(4)),
                ("5. Ciclos sobrevividos", lambda: self.mostrar_reporte(5)),
                ("6. Evento más frecuente", lambda: self.mostrar_reporte(6)),
                ("7. Riesgo de salud", lambda: self.mostrar_reporte(7)),
                ("8. Balance sostenibilidad", lambda: self.mostrar_reporte(8)),
                ("9. Volver", lambda: self.cambiar_menu("PRINCIPAL")),
            ]
        )

        self.menus["GRAFICOS"] = self._crear_lista_botones(
            [
                ("1. Ver métricas en pantalla", self.ver_metricas_pantalla),
                ("2. Generar gráficos (Matplotlib)", self.generar_graficos),
                ("3. Volver", lambda: self.cambiar_menu("PRINCIPAL")),
            ]
        )

        self.menus["VISTA_METRICAS"] = self._crear_lista_botones(
            [("Volver al Menú", lambda: self.cambiar_menu("GRAFICOS"))]
        )

    def cambiar_menu(self, nuevo_estado):
        self.estado_menu = nuevo_estado

    # FUNCIONALIDADES LOGICAS

    def registrar_colono(self):
        nombre = simpledialog.askstring("Nuevo Colono", "Nombre del colono:")
        if not nombre:
            return
        rol = simpledialog.askstring(
            "Nuevo Colono", f"Rol ({', '.join(ROLES.keys())}):"
        )
        if not rol or rol.title() not in ROLES:
            messagebox.showerror("Error", "Rol no válido.")
            return
        try:
            edad = int(simpledialog.askinteger("Nuevo Colono", "Edad (18-65):"))
            salud = int(
                simpledialog.askinteger(
                    "Nuevo Colono", "Salud (1-100):", initialvalue=100
                )
            )
            habilidad = simpledialog.askstring("Nuevo Colono", "Habilidad principal:")
            nuevo = ROLES[rol.title()](nombre.title(), edad, salud, habilidad)
            self.colonia.agregar_colono(nuevo)
            self.log(f"Colono {nombre.title()} registrado.")
        except Exception as e:
            self.log(f"Error: {e}")

    def eliminar_colono(self):
        nombre = simpledialog.askstring("Eliminar", "Nombre a eliminar:")
        if nombre:
            try:
                self.colonia.eliminar_colono(nombre)
                self.log(f"Colono {nombre} eliminado.")
            except Exception as e:
                self.log(f"Error: {e}")

    def asignar_colono(self):
        colono = simpledialog.askstring("Asignar", "Nombre del colono:")
        edificio = simpledialog.askstring("Asignar", "Nombre del edificio:")
        if colono and edificio:
            try:
                self.colonia.asignar_colono(colono, edificio)
                self.log(f"Colono {colono} asignado a {edificio}.")
            except Exception as e:
                self.log(f"Error: {e}")

    def liberar_colono(self):
        nombre = simpledialog.askstring("Liberar", "Nombre del colono:")
        if nombre:
            try:
                self.colonia.liberar_colono(nombre)
                self.log(f"Colono {nombre} liberado.")
            except Exception as e:
                self.log(f"Error: {e}")

    def registrar_recurso(self):
        nombre = simpledialog.askstring("Recurso", "Nombre:")
        if not nombre:
            return
        try:
            cant = simpledialog.askfloat("Recurso", "Cantidad inicial:")
            prod = simpledialog.askfloat("Recurso", "Producción:")
            cons = simpledialog.askfloat("Recurso", "Consumo:")
            self.colonia.agregar_recurso(Recurso(nombre.title(), cant, prod, cons))
            self.log(f"Recurso {nombre} registrado con éxito.")
        except Exception as e:
            self.log(f"Error: {e}")

    def registrar_plano(self):
        nombre = simpledialog.askstring("Edificio", "Nombre:")
        if not nombre:
            return
        tipo = simpledialog.askstring("Edificio", f"Tipo ({', '.join(TIPOS.keys())}):")
        if not tipo or tipo.title() not in TIPOS:
            return
        try:
            costo = simpledialog.askfloat("Edificio", "Costo de construcción:")
            prio = simpledialog.askinteger(
                "Edificio", "Prioridad (1-5):", initialvalue=1
            )
            nuevo = TIPOS[tipo.title()](nombre.title(), 1, costo, False, 0.0, prio)
            self.colonia.agregar_edificio(nuevo)
            self.log(f"Plano de {nombre.title()} agregado a la lista.")
        except Exception as e:
            self.log(f"Error: {e}")

    def construir_edificio(self):
        nombre = simpledialog.askstring("Construir", "Nombre del plano:")
        if nombre:
            try:
                self.colonia.construir(nombre)
                self.log(f"Edificio {nombre} construido exitosamente.")
            except Exception as e:
                self.log(f"Error: {e}")

    def mejorar_edificio(self):
        nombre = simpledialog.askstring("Mejorar", "Nombre del edificio:")
        if nombre:
            try:
                self.colonia.mejorar(nombre)
                self.log(f"Edificio {nombre} mejorado.")
            except Exception as e:
                self.log(f"Error: {e}")

    def priorizar_plano(self):
        nombre = simpledialog.askstring("Priorizar", "Nombre del plano:")
        prio = simpledialog.askinteger("Priorizar", "Nueva prioridad (1-5):")
        if nombre and prio:
            try:
                self.colonia.priorizar(nombre, prio)
                self.log(f"Prioridad de {nombre} cambiada a {prio}.")
            except Exception as e:
                self.log(f"Error: {e}")

    def construir_prioritario(self):
        try:
            self.colonia.construir_cola()
            self.log("Edificio de mayor prioridad construido.")
        except Exception as e:
            self.log(f"Error: {e}")

    def avanzar_un_sol(self):
        self.motor.avanzar_ciclo()
        for msg in self.motor.vaciar_mensajes():
            self.log(msg)
        self.log(f"--- Sol {len(self.colonia.ciclos)} completado ---")

    def simular_varios(self):
        dias = simpledialog.askinteger("Simular", "¿Cuántos soles deseas avanzar?")
        if dias:
            for _ in range(dias):
                self.motor.avanzar_ciclo()
            self.motor.vaciar_mensajes()
            self.log(f"Se han simulado {dias} soles consecutivamente.")

    def ver_estado(self):
        self.log("[SISTEMA] El estado en tiempo real se refleja en el panel lateral.")

    # --- REPORTES REPARADOS (8, 3 y 4) ---
    def mostrar_reporte(self, op):
        msg = "Reporte en desarrollo."
        try:
            if op == 1:
                ciclo = self.colonia.mejor_ciclo()
                msg = (
                    f"Mejor ciclo productivo: Sol {ciclo.numero}"
                    if ciclo
                    else "No hay ciclos."
                )
            elif op == 2:
                crit = self.colonia.recurso_critico()
                if crit:
                    rec = crit[0] if isinstance(crit, tuple) else crit
                    msg = f"Recurso en estado crítico: {rec.nombre}"
                else:
                    msg = "No hay recursos críticos."
            elif op == 3:
                # Verificamos si existe el metodo o lo calculamos manual
                if hasattr(self.colonia, "edificio_mas_rentable"):
                    ed = self.colonia.edificio_mas_rentable()
                    msg = (
                        f"Edificio más rentable: {ed.nombre}"
                        if ed
                        else "Faltan edificios operativos."
                    )
                else:
                    msg = "Eror"
            elif op == 4:
                if hasattr(self.colonia, "colono_mas_productivo"):
                    col = self.colonia.mejor_colono()
                    msg = (
                        f"Colono más productivo: {col.nombre}"
                        if col
                        else "Faltan datos de colonos."
                    )
                else:
                    msg = "Eror"
            elif op == 5:
                msg = f"Ciclos sobrevividos: {self.colonia.ciclos_vividos()}"
            elif op == 6:
                msg = "Evento más frecuente:"
            elif op == 7:
                riesgos = [c.nombre for c in self.colonia.colonos if c.salud < 50]
                msg = (
                    f"En riesgo de salud: {', '.join(riesgos)}"
                    if riesgos
                    else "Nadie en riesgo grave."
                )
            elif op == 8:
                sos = self.colonia.sostenibilidad()
                if not sos:
                    msg = "Faltan datos de ciclos."
                elif sos[0]:
                    msg = "La colonia es autosustentable (Producción >= Consumo)."
                else:
                    msg = f"Déficit en: {', '.join(sos[1])}"
        except Exception as e:
            msg = f"Error: {e}"

        self.log(f"[REPORTE] {msg}")

    # --- MÉTRICAS Y GUARDADO ---
    def ver_metricas_pantalla(self):
        try:
            reporte = Reporte(self.almacen.a_tablas(self.colonia))
            metricas = reporte.metricas()
            self.datos_pantalla_completa = [f"{k}: {v}" for k, v in metricas.items()]
            self.cambiar_menu("VISTA_METRICAS")
        except Exception as e:
            self.log(f"Error al calcular métricas: {e}")

    def generar_graficos(self):
        try:
            self.log("Abriendo gráficos en Matplotlib...")
            Reporte(self.almacen.a_tablas(self.colonia)).generar_todos(True, True)
            self.log("Gráficos generados.")
        except Exception as e:
            self.log(f"Error: {e}")

    def guardar_datos(self):
        try:
            n = self.almacen.guardar(self.colonia)
            self.log(f"Guardado completado exitosamente ({n} archivos).")
        except Exception as e:
            self.log(f"Error: {e}")

    def cargar_datos(self):
        try:
            self.colonia = self.almacen.cargar()
            self.motor = Motor(self.colonia)
            self.log("Datos de la colonia cargados desde CSV.")
        except Exception as e:
            self.log(f"Error: {e}")

    def salir(self):
        pygame.quit()
        sys.exit()

    # =================================================================
    # RENDERIZADO VISUAL
    # =================================================================
    def dibujar_fondo(self):
        if FONDO_IMG:
            PANTALLA.blit(FONDO_IMG, (0, 0))
        else:
            PANTALLA.fill(NEGRO)
            for estrella in self.estrellas:
                estrella[1] += 1
                if estrella[1] > ALTO:
                    estrella[1] = 0
                    estrella[0] = random.randint(0, ANCHO)
                pygame.draw.circle(
                    PANTALLA, BLANCO, (estrella[0], estrella[1]), estrella[2]
                )

    def dibujar_panel_lateral(self):
        panel_rect = pygame.Rect(350, 20, 620, 480)
        superficie = pygame.Surface((620, 480), pygame.SRCALPHA)
        superficie.fill(GRIS_PANEL)
        PANTALLA.blit(superficie, panel_rect.topleft)
        pygame.draw.rect(PANTALLA, BLANCO, panel_rect, width=2, border_radius=5)

        PANTALLA.blit(
            FUENTE_BTN.render(
                f"ESTADO DE LA COLONIA: {self.colonia.nombre.upper()}", True, VERDE_OK
            ),
            (370, 35),
        )
        PANTALLA.blit(
            FUENTE_BTN.render(f"Día (Sol): {len(self.colonia.ciclos)}", True, BLANCO),
            (800, 35),
        )

        y = 70
        PANTALLA.blit(
            FUENTE_BTN.render("RECURSOS ACTUALES", True, AZUL_MARTE), (370, y)
        )
        y += 25
        for r in self.colonia.recursos:
            txt = f"{r.nombre}: {r.cantidad:.1f} (Balance Neto: {r.neto:+.1f})"
            color = ROJO_ALERTA if r.cantidad < 10 else BLANCO
            PANTALLA.blit(FUENTE_TEXTO.render(txt, True, color), (380, y))
            y += 20

        y += 10
        PANTALLA.blit(
            FUENTE_BTN.render("POBLACIÓN (Muestra)", True, AZUL_MARTE), (370, y)
        )
        y += 25
        for c in self.colonia.colonos[:5]:
            txt = f"- {c.nombre} | Rol: {c.rol} | Salud: {c.salud} | Asignado a: {c.destino}"
            color = ROJO_ALERTA if c.salud < 30 else BLANCO
            PANTALLA.blit(FUENTE_TEXTO.render(txt, True, color), (380, y))
            y += 20

        y += 10
        PANTALLA.blit(FUENTE_BTN.render("INFRAESTRUCTURA", True, AZUL_MARTE), (370, y))
        y += 25
        for e in self.colonia.edificios[:5]:
            estado = "Operativo" if e.construido else f"Plano (Prio: {e.prioridad})"
            PANTALLA.blit(
                FUENTE_TEXTO.render(
                    f"- {e.nombre} (Nivel {e.nivel}) | Estado: {estado}", True, BLANCO
                ),
                (380, y),
            )
            y += 20

    def dibujar_consola_inferior(self):
        panel_rect = pygame.Rect(350, 520, 620, 160)
        superficie = pygame.Surface((620, 160), pygame.SRCALPHA)
        superficie.fill(GRIS_PANEL)
        PANTALLA.blit(superficie, panel_rect.topleft)
        pygame.draw.rect(PANTALLA, AZUL_MARTE, panel_rect, width=2, border_radius=5)

        PANTALLA.blit(
            FUENTE_BTN.render("REGISTRO DE EVENTOS (Consola)", True, VERDE_OK),
            (370, 530),
        )

        y = 560
        for msg in self.mensajes_log[-6:]:
            PANTALLA.blit(FUENTE_TEXTO.render(f"> {msg}", True, BLANCO), (370, y))
            y += 20

    # FUNCIÓN PARA CORTE DE LÍNEA AUTOMÁTICO (Evita que el texto se salga de la caja)
    def renderizar_texto_multilinea(self, texto, x, y, max_ancho):
        palabras = str(texto).split(" ")
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            test_linea = linea_actual + palabra + " "
            if FUENTE_METRICAS.size(test_linea)[0] < max_ancho:
                linea_actual = test_linea
            else:
                lineas.append(linea_actual)
                linea_actual = palabra + " "
        lineas.append(linea_actual)

        for i, linea in enumerate(lineas):
            PANTALLA.blit(
                FUENTE_METRICAS.render(linea, True, BLANCO), (x, y + (i * 22))
            )

        return y + (len(lineas) * 22)

    def dibujar_pantalla_metricas(self):
        panel_rect = pygame.Rect(350, 20, 620, 660)
        superficie = pygame.Surface((620, 660), pygame.SRCALPHA)
        superficie.fill(GRIS_PANEL)
        PANTALLA.blit(superficie, panel_rect.topleft)
        pygame.draw.rect(PANTALLA, AZUL_MARTE, panel_rect, width=2, border_radius=5)

        PANTALLA.blit(
            FUENTE_TITULO.render("MÉTRICAS DETALLADAS", True, VERDE_OK), (370, 40)
        )

        y = 100
        if not self.datos_pantalla_completa:
            PANTALLA.blit(
                FUENTE_METRICAS.render(
                    "No hay suficientes datos procesados.", True, BLANCO
                ),
                (380, y),
            )
        else:
            for metrica in self.datos_pantalla_completa:

                y = self.renderizar_texto_multilinea(metrica, 380, y, 580)
                y += 12

    def ejecutar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()

                for btn in self.menus[self.estado_menu]:
                    btn.procesar_clic(evento)

            self.dibujar_fondo()

            titulos = {
                "PRINCIPAL": "MENÚ PRINCIPAL",
                "COLONOS": "COLONOS",
                "EDIFICIOS": "EDIFICIOS",
                "SIMULACION": "SIMULACIÓN",
                "REPORTES": "REPORTES",
                "GRAFICOS": "GRÁFICOS",
                "VISTA_METRICAS": "VOLVER",
            }
            texto_tit = FUENTE_TITULO.render(titulos[self.estado_menu], True, VERDE_OK)
            PANTALLA.blit(texto_tit, (30, 25))

            for btn in self.menus[self.estado_menu]:
                btn.dibujar(PANTALLA)

            if self.estado_menu == "VISTA_METRICAS":
                self.dibujar_pantalla_metricas()
            else:
                self.dibujar_panel_lateral()
                self.dibujar_consola_inferior()

            pygame.display.flip()
            self.reloj.tick(60)


if __name__ == "__main__":
    almacen = Almacen()
    colonia = almacen.cargar() if almacen.hay_datos() else crear_demo()
    app = InterfazGenesis(colonia, almacen)
    app.ejecutar()
