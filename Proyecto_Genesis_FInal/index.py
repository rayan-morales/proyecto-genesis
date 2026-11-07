class Receta:
    def __init__(self, nombre, ingredientes):
        self.__nombre = nombre
        self.__ingredientes = []

        if isinstance(ingredientes, list):
            for ingrediente in ingredientes:
                self.add_ingrediente(ingrediente)
        else:
            print("Se esperaba una lista de objetos de tipo Ingrediente")

    def add_ingrediente(self, ingrediente):
        if isinstance(ingrediente, ingrediente):
            self.__ingredientes.append(ingrediente)
        else:
            print("El elemento debe ser de tipo Ingrediente")

    def get_ingrediente(self, indice):
        if len(self.__ingredientes) == 0:
            print("No hay ingredientes registrados")
        else:
            if not 0 <= indice < len(self.__ingredientes):
                print("La posició n indicada no es vá lida")
            else:
                return self.__ingredientes[indice]
        return None
    
    def lst_ingredientes(self):
        if len(self.__ingredientes) == 0:
            print("No hay ingredientes registrados")
        else:
            for ingrediente in self.__ingredientes:
                print(f"Ingrediente: {ingrediente}")
    def __str__(self):
        return f"Receta: {self.__nombre}"
    
class Ingrediente:

    def __init__(self, nombre, procedencia):
        self.__nombre = nombre
        self.__procedencia = procedencia
    def __str__(self):
        return f"Ingrediente: {self.__nombre}, Procedencia: {self.__procedencia}"
# Programa principal
receta1 = Receta(
"Ensalada", [Ingrediente("Lechuga", "Chile"), Ingrediente("Tomate", "Ecuador")])
print(receta1)
receta1.lst_ingredientes()
ingrediente = receta1.get_ingrediente(0)
print(ingrediente)
ingrediente = receta1.get_ingrediente(1)
print(ingrediente)
receta1.add_ingrediente(Ingrediente("Cebolla", "Perú"))
receta1.lst_ingredientes()