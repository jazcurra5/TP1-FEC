class GF:
    # Constructor con atributos
    def __init__(self, m, px):
        self.m = int(m)
        self.px = int(px)

    # # Función asociada (método) que imprime un saludo
    # def generar_polinomio(self):
    #     coef =bin(self.px)
    #     return f"El polinomio es {coef[2:]} "

    # Otra función asociada que verifica si es mayor de edad
    def mostrar_primitivo(self):
        entero_primitivo = (2 ** self.m) + self.px
        #return f"Los coeficientes del polinomio primitivo es {bin(entero_primitivo)[2:]}"
        polinomio_texto = self.a_polinomio(entero_primitivo)
        return f"El polinomio primitivo completo es: {polinomio_texto}"

    def a_polinomio(self, valor):
        if valor == 0:
            return "0"

        # 1. Pasamos el número a texto (ej: 7 se convierte en "111")
        bits = bin(valor)[2:] 
        largo = len(bits)
        terminos = []

        # 2. Recorremos cada '0' o '1' de izquierda a derecha
        for i, bit in enumerate(bits):
            if bit == '1':
                # La potencia de 'x' es el largo total menos 1, menos la posición actual
                potencia = largo - 1 - i 
                
                if potencia == 0:
                    terminos.append("1")
                elif potencia == 1:
                    terminos.append("x")
                else:
                    terminos.append(f"x^{potencia}")

        # 3. Unimos todo con el símbolo " + "
        return " + ".join(terminos)
    
# Crear un objeto (instancia) de la clase
p1 = GF(3, 3)

# Usar las funciones asociadas
#print(p1.generar_polinomio())            # Imprime el saludo
print(p1.mostrar_primitivo())  # Imprime True

