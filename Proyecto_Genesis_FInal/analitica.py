import pandas as pd
import matplotlib.pyplot as plt

ORDEN_NIVEL = ["estable", "alerta", "critica", "colapso"]


class Reporte:

    def __init__(self, tablas):
        self.tablas = tablas

    # --- propiedades (encapsulamiento) --------------------------------
    @property
    def tablas(self):
        return self._tablas

    @tablas.setter
    def tablas(self, valor):
        if not isinstance(valor, dict):
            raise ValueError("tablas: debe ser un diccionario de DataFrames.")
        copia = {}
        for clave in ("colonos", "recursos", "edificios", "eventos", "ciclos"):
            if clave not in valor or not isinstance(valor[clave], pd.DataFrame):
                raise ValueError("tablas: falta el DataFrame de " + clave + ".")
            copia[clave] = valor[clave].copy()
        self._tablas = copia

    # =================================================================
    # MÉTRICAS (devuelven textos listos para imprimir)
    # =================================================================
    def metricas(self):
        """Devuelve {nombre de la métrica: resultado}."""
        resultado = {}
        resultado["Evolución de recursos"] = self.evolucion()
        resultado["Producción total por edificio"] = self.produccion_total()
        resultado["Supervivencia de colonos"] = self.supervivencia()
        resultado["Evento más costoso"] = self.evento_costoso()
        resultado["Colono más productivo por rol"] = self.mejor_por_rol()
        resultado["Nivel de crisis alcanzado"] = self.crisis_maxima()
        return resultado

    def evolucion(self):
        ciclos = self._tablas["ciclos"]
        if ciclos.empty:
            return "Aún no hay ciclos simulados."
        columnas = [("oxigeno", "Oxígeno"), ("agua", "Agua"),
                    ("comida", "Comida"), ("energia", "Energía"),
                    ("materiales", "Materiales")]
        partes = []
        for columna, etiqueta in columnas:
            inicio = round(float(ciclos[columna].iloc[0]), 1)
            final = round(float(ciclos[columna].iloc[-1]), 1)
            partes.append(etiqueta + " " + str(inicio) + " -> " + str(final))
        return " | ".join(partes)

    def produccion_total(self):
        edificios = self._tablas["edificios"]
        construidos = edificios[edificios["construido"] == 1]
        if construidos.empty:
            return "No hay edificios construidos."
        partes = []
        for fila in construidos.to_dict("records"):
            partes.append(str(fila["nombre"]) + ": "
                          + str(round(float(fila["producido"]), 1)))
        return " | ".join(partes)

    def supervivencia(self):
        ciclos = self._tablas["ciclos"]
        if ciclos.empty:
            return "Aún no hay ciclos simulados."
        base = float(ciclos["colonos"].max())
        if base <= 0:
            return "No hubo colonos."
        tasa = ciclos["colonos"] / base * 100
        return ("último ciclo " + str(round(float(tasa.iloc[-1]), 1))
                + " % | mínima " + str(round(float(tasa.min()), 1)) + " %")

    def evento_costoso(self):
        eventos = self._tablas["eventos"]
        if eventos.empty:
            return "Aún no ocurrieron eventos."
        peor = eventos.loc[eventos["impacto"].idxmin()]
        if float(peor["impacto"]) >= 0:
            return "Ningún evento causó pérdida de recursos."
        return (str(peor["nombre"]) + " (sol " + str(int(peor["ciclo"]))
                + "): " + str(round(float(peor["impacto"]), 1)))

    def mejor_por_rol(self):
        colonos = self._tablas["colonos"]
        if colonos.empty:
            return "No hay colonos registrados."
        partes = []
        for rol in colonos["rol"].unique():
            grupo = colonos[colonos["rol"] == rol]
            mejor = grupo.loc[grupo["aporte"].idxmax()]
            partes.append(str(rol) + ": " + str(mejor["nombre"])
                          + " (" + str(round(float(mejor["aporte"]), 1)) + ")")
        return " | ".join(partes)

    def crisis_maxima(self):
        ciclos = self._tablas["ciclos"]
        if ciclos.empty:
            return "estable (sin ciclos)"
        peor = 0
        for nivel in ciclos["nivel"]:
            if str(nivel) in ORDEN_NIVEL:
                peor = max(peor, ORDEN_NIVEL.index(str(nivel)))
        return ORDEN_NIVEL[peor]

    # =================================================================
    # GRÁFICOS (cada método devuelve la figura de Matplotlib)
    # =================================================================
    def graf_recursos(self):
        ciclos = self._tablas["ciclos"]
        if ciclos.empty:
            raise ValueError("No hay ciclos simulados para graficar.")
        figura, eje = plt.subplots(figsize=(8, 4.5))
        eje.plot(ciclos["numero"], ciclos["oxigeno"], label="Oxígeno")
        eje.plot(ciclos["numero"], ciclos["agua"], label="Agua")
        eje.plot(ciclos["numero"], ciclos["comida"], label="Comida")
        eje.set_title("Evolución de oxígeno, agua y comida por ciclo")
        eje.set_xlabel("Ciclo (sol)")
        eje.set_ylabel("Cantidad")
        eje.grid(True, alpha=0.3)
        eje.legend()
        figura.tight_layout()
        return figura

    def graf_edificios(self):
        edificios = self._tablas["edificios"]
        construidos = edificios[edificios["construido"] == 1]
        if construidos.empty:
            raise ValueError("No hay edificios construidos para graficar.")
        figura, eje = plt.subplots(figsize=(8, 4.5))
        eje.bar(construidos["nombre"], construidos["producido"],
                color="tab:green")
        eje.set_title("Producción acumulada por edificio")
        eje.set_xlabel("Edificio")
        eje.set_ylabel("Unidades producidas")
        eje.tick_params(axis="x", labelrotation=30)
        figura.tight_layout()
        return figura

    def graf_eventos(self):
        """Pastel: distribución de los eventos ocurridos."""
        eventos = self._tablas["eventos"]
        if eventos.empty:
            raise ValueError("Aún no ocurrieron eventos para graficar.")
        conteo = eventos["nombre"].value_counts()
        figura, eje = plt.subplots(figsize=(6, 6))
        eje.pie(conteo.values, labels=list(conteo.index), autopct="%1.0f%%")
        eje.set_title("Distribución de eventos ocurridos")
        figura.tight_layout()
        return figura

    def graf_colonos(self):
        """Barras: productividad (aporte acumulado) por colono."""
        colonos = self._tablas["colonos"]
        if colonos.empty:
            raise ValueError("No hay colonos para graficar.")
        figura, eje = plt.subplots(figsize=(8, 4.5))
        eje.bar(colonos["nombre"], colonos["aporte"], color="tab:orange")
        eje.set_title("Productividad por colono")
        eje.set_xlabel("Colono")
        eje.set_ylabel("Aporte acumulado")
        eje.tick_params(axis="x", labelrotation=30)
        figura.tight_layout()
        return figura

    def graf_histograma(self):
        """Histograma: distribución de los recursos vitales por ciclo."""
        ciclos = self._tablas["ciclos"]
        if ciclos.empty:
            raise ValueError("No hay ciclos simulados para graficar.")
        figura, eje = plt.subplots(figsize=(8, 4.5))
        eje.hist([ciclos["oxigeno"], ciclos["agua"], ciclos["comida"]],
                 bins=10, label=["Oxígeno", "Agua", "Comida"])
        eje.set_title("Distribución de recursos vitales al final de cada ciclo")
        eje.set_xlabel("Cantidad")
        eje.set_ylabel("Cantidad de ciclos")
        eje.legend()
        figura.tight_layout()
        return figura

    def generar_todos(self, mostrar=True, guardar=True):
        """Genera los 5 gráficos. Si guardar=True crea los PNG (g_*.png).
        Devuelve cuántos gráficos se pudieron generar."""
        graficos = (
            ("g_recursos.png", self.graf_recursos),
            ("g_edificios.png", self.graf_edificios),
            ("g_eventos.png", self.graf_eventos),
            ("g_colonos.png", self.graf_colonos),
            ("g_histograma.png", self.graf_histograma),
        )
        creados = 0
        for archivo, funcion in graficos:
            try:
                figura = funcion()
            except ValueError as error:
                print("No se generó", archivo, "->", error)
                continue
            if guardar:
                figura.savefig(archivo, dpi=120)
            creados = creados + 1
        if mostrar and creados > 0:
            plt.show()
        plt.close("all")
        return creados
