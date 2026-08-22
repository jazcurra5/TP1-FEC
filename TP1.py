class GF:
    # Constructor con atributos
    def __init__(self, m, px):
        self.m = int(m)
        self.px = int(px)

  
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

# ---------------------------------------------------------
    # valido que el elemento  pertenezca al grupo
    def validar_elemento(self, valor):
        limite = 2 ** self.m
        if valor < 0 or valor >= limite:
            # Si el valor se pasa, frena el programa y tira un error claro
            raise ValueError(f"Error: El elemento {valor} está fuera del campo GF(2^{self.m}). Debe estar entre 0 y {limite - 1}.")



    def suma(self,a,b):
        #valido
        self.validar_elemento(a)
        self.validar_elemento(b)

        #sumo
        suma = a^b

        #genero polinomios
        polinomio_a = self.a_polinomio(a)
        polinomio_b = self.a_polinomio(b)
        polinomio_resultado = self.a_polinomio(suma)

        #printeo
        print(f"Suma en GF(2^{self.m}) | ({polinomio_a}) + ({polinomio_b}) = {polinomio_resultado}")

        return suma

    





#///////////test//////////////
# INstancia de la clase
# /////////// TEST //////////////
p1 = GF(4, 3) 

# Con solo llamar a la función, ya te imprime el texto en pantalla
p1.suma(17, 5)