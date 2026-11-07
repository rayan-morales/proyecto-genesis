
import pandas as pd
from entidades import Recurso
from jerarquia import colono_de_fila, edificio_de_fila, evento_de_fila
from colonia import Colonia, Ciclo


class Almacen:

    def __init__(self, prefijo=""):
        self.prefijo = prefijo  
        self._columnas = {
            "colonos": ["nombre", "rol", "edad", "salud", "habilidad",
                        "aporte", "destino"],
            "recursos": ["nombre", "cantidad", "produccion", "consumo",
                         "suma", "neto"],
            "edificios": ["nombre", "tipo", "nivel", "costo", "efecto",
                          "construido", "producido", "prioridad"],
            "eventos": ["tipo", "nombre", "magnitud", "ciclo", "impacto"],
            "ciclos": ["numero", "produccion", "consumo", "evento", "nivel",
                       "colonos", "oxigeno", "agua", "comida", "energia",
                       "materiales"],
        }

    @property
    def prefijo(self):
        return self._prefijo

    @prefijo.setter
    def prefijo(self, valor):
        if not isinstance(valor, str):
            raise ValueError("prefijo: debe ser texto.")
        self._prefijo = valor

    @property
    def claves(self):
        """Nombres de las tablas, en el orden en que se guardan."""
        return list(self._columnas.keys())

    def ruta(self, clave):
        """Nombre del archivo CSV de una tabla (ej. colonos.csv)."""
        if clave not in self._columnas:
            raise ValueError("Tabla desconocida: " + str(clave))
        return self._prefijo + clave + ".csv"

    def armar_tabla(self, clave, objetos):
        """Convierte una lista de objetos en un DataFrame usando a_fila()."""
        filas = []
        for objeto in objetos:
            filas.append(objeto.a_fila())
        return pd.DataFrame(filas, columns=self._columnas[clave])

    def a_tablas(self, colonia):
        """Devuelve {clave: DataFrame} con el estado actual de la colonia.
        Es lo que recibe el Reporte (analitica.py)."""
        if not isinstance(colonia, Colonia):
            raise ValueError("Debe indicar una colonia válida.")
        return {
            "colonos": self.armar_tabla("colonos", colonia.colonos),
            "recursos": self.armar_tabla("recursos", colonia.recursos),
            "edificios": self.armar_tabla("edificios", colonia.edificios),
            "eventos": self.armar_tabla("eventos", colonia.eventos),
            "ciclos": self.armar_tabla("ciclos", colonia.ciclos),
        }
    def guardar(self, colonia):
        """Escribe los 5 CSV. Devuelve cuántos archivos guardó."""
        tablas = self.a_tablas(colonia)
        for clave in tablas:
            archivo = self.ruta(clave)
            try:
                tablas[clave].to_csv(archivo, index=False, encoding="utf-8")
            except OSError as error:
                raise OSError("No se pudo escribir " + archivo + ": "
                              + str(error))
        return len(tablas)

    def hay_datos(self):
        """True si existen los 5 archivos CSV."""
        for clave in self._columnas:
            try:
                abierto = open(self.ruta(clave), "r", encoding="utf-8")
                abierto.close()
            except OSError:
                return False
        return True

    def leer_tabla(self, clave):
        """Lee un CSV. FileNotFoundError si no existe, ValueError si está
        dañado o le faltan columnas."""
        archivo = self.ruta(clave)
        try:
            tabla = pd.read_csv(archivo, encoding="utf-8")
        except FileNotFoundError:
            raise FileNotFoundError("No existe el archivo " + archivo)
        except (pd.errors.EmptyDataError, pd.errors.ParserError,
                UnicodeDecodeError):
            raise ValueError("El archivo " + archivo + " está vacío o dañado.")
        faltan = []
        for columna in self._columnas[clave]:
            if columna not in tabla.columns:
                faltan.append(columna)
        if len(faltan) > 0:
            raise ValueError("Al archivo " + archivo
                             + " le faltan las columnas: " + ", ".join(faltan))
        return tabla

    def leer_tablas(self):
        """Lee los 5 CSV y devuelve {clave: DataFrame}."""
        tablas = {}
        for clave in self._columnas:
            tablas[clave] = self.leer_tabla(clave)
        return tablas

    def cargar(self):
        """Reconstruye una Colonia completa a partir de los CSV."""
        tablas = self.leer_tablas()
        colonia = Colonia()
        try:
            for fila in tablas["recursos"].to_dict("records"):
                colonia.agregar_recurso(Recurso.desde_fila(fila))
            for fila in tablas["colonos"].to_dict("records"):
                colonia.agregar_colono(colono_de_fila(fila))
            for fila in tablas["edificios"].to_dict("records"):
                colonia.agregar_edificio(edificio_de_fila(fila))
            for fila in tablas["eventos"].to_dict("records"):
                colonia.agregar_evento(evento_de_fila(fila))
            for fila in tablas["ciclos"].to_dict("records"):
                colonia.agregar_ciclo(Ciclo.desde_fila(fila))
        except (KeyError, ValueError, TypeError) as error:
            raise ValueError("Los datos guardados están dañados: " + str(error))
        return colonia
