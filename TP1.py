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

        # pasamos el número a texto
        bits = bin(valor)[2:] 
        largo = len(bits)
        terminos = []

        # recorremos cada bit de izquierda a derecha
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

        # unimos
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

    def producto(self,a,b,c):
        self.validar_elemento(a)
        self.validar_elemento(b)

        polinomio_primitivo = (2 ** self.m) + self.px

        #creo registros temporales
        resultado = 0
        a_temp = a
        b_temp = b

        while a_temp > 0:

            if a_temp & 1:
                resultado = resultado ^ b_temp

            a_temp >>= 1
            b_temp <<= 1

            if b_temp & (1 << self.m):#formo filtro de m bits con un 1 en msb
                b_temp = b_temp ^ polinomio_primitivo

        if c == True:
                #printeos condicional
            polinomio_a = self.a_polinomio(a)
            polinomio_b = self.a_polinomio(b)
            polinomio_res = self.a_polinomio(resultado)
        
            print(f"Producto en GF(2^{self.m}) | ({polinomio_a}) * ({polinomio_b}) = {polinomio_res}") 

        return resultado

    def inverso(self,a,c):
        self.validar_elemento(a)

        #creo registros temporales
        resultado = 0
        a_temp = a
        #b_temp = a

        if(a_temp == 0):
            print(f"No tiene inverso")

        else:
            for i in range(2 ** self.m):
                resultado = self.producto(a,i,False)
                if resultado == 1:
                    if c == True:
                        pol_a = self.a_polinomio(a)
                        pol_inv = self.a_polinomio(i)
                        print(f"El inverso de ({pol_a}) es ({pol_inv}) | en decimal: {i}")
                        
                    return i

    def division(self,a,b):
        
        if b==0:
            print (f"Error, el divisor es igual a cero")
            return None

        aux = self.inverso(b,False)
        resultado = self.producto(a,aux,False)
        print (f"La division de elementos es: {self.a_polinomio(resultado)}")
        return resultado

    def potencia(self,a,n):

        resultado = a

        if n < 0:
            print (f"No se puede realizar potencias negativas")
            return None
        
        if n == 0:
            print (f"La potencia del elemento es igual a 1")
            return 1

        for _ in range(1,n):
            resultado = self.producto(resultado,a,False)

        print (f"La {n} potencia del elemento [{self.a_polinomio(a)}] es: [{self.a_polinomio(resultado)}]")
        return resultado

class GFPoly:

    def __init__(self,campo,coef):

        self.campo = campo
        lista_temp = list(coef)
        
        #limpio los ceros a la izq
        while len(lista_temp) > 1 and lista_temp[0] == 0:
            lista_temp.pop(0)
            
        #valido
        for c in lista_temp:
            self.campo.validar_elemento(c)
            
        # guardo como tupla
        self.coef = tuple(lista_temp)

    # printeo modificado para que reciba lista
    def __str__(self):
        # si es el polinomio cero
        if len(self.coef) == 1 and self.coef[0] == 0:
            return "0"

        largo = len(self.coef)
        terminos = []

        # recorremos cada coeficiente de izquierda a derecha
        for i, c in enumerate(self.coef):
            if c != 0:
                # La potencia de 'X' es el largo total menos 1, menos la posición actual
                potencia = largo - 1 - i 
                
                if potencia == 0:
                    terminos.append(f"{c}")
                elif potencia == 1:
                    terminos.append(f"{c}X")
                else:
                    terminos.append(f"{c}X^{potencia}")

        # unimos
        return " + ".join(terminos)

    def __add__(self, a):
        #comparo
        largo_max = max(len(self.coef), len(a.coef))
        
        #compleot con ceros
        c1 = [0] * (largo_max - len(self.coef)) + list(self.coef)
        c2 = [0] * (largo_max - len(a.coef)) + list(a.coef)
        
        resultado = []
        
        #Sumo
        for i in range(largo_max):
            suma_ladrillos = c1[i] ^ c2[i]
            resultado.append(suma_ladrillos)
            
        return GFPoly(self.campo, resultado)

    def __mul__(self, a):
        largo_p1 = len(self.coef)
        largo_p2 = len(a.coef)
        
        # armo la lista de resultado llena de ceros
        resultado = [0] * (largo_p1 + largo_p2 - 1)
        
        # recorro ambos polinomios
        for i in range(largo_p1):
            for j in range(largo_p2):
                
                mult = self.campo.producto(self.coef[i], a.coef[j], False)
    
                resultado[i + j] = resultado[i + j] ^ mult
                
        # devuelvo polinomio limpio
        return GFPoly(self.campo, resultado)

    def escalar(self,k):

        resultado = []#lista auxiliar vacia
        largo = len(self.coef)

        for i in range (largo) :
            aux = self.campo.producto(self.coef[i],k,False)
            resultado.append(aux)#enlisto 


        return GFPoly(self.campo, resultado)

    def evaluar(self, a): # metodo de Horner

        resultado = 0
        
        for i in (self.coef):
            
            aux = self.campo.producto(resultado, a, False)
            
            resultado = aux ^ i

        return resultado

    @staticmethod# para evitar tener qwue generar un polinomio aux
    def construccion(campo,raices):


        for i in range(len(raices)):

            base = GFPoly(campo, [1, raices[i]])
          
            if i == 0:

                poli = base

            else:

                poli = poli * base

        return poli
    







         

    
                
                    
                 
                
                


            





        





    

    






# /////////// TESTs //////////////
p1 = GF(5, 3) 


# p1.suma(17, 5)
# p1.producto(15, 2, True)
# p1.inverso(5, True)
# p1.division(17, 0)
# p1.potencia(17, 9)
# polinomio_prueba = GFPoly(p1, [0, 0, 15, 2])
# print(polinomio_prueba)


# ==========================================
# ZONA DE PRUEBAS - CLASE GFPoly
# ==========================================
print("\n--- INICIANDO PRUEBAS DE POLINOMIOS ---")

# 1. Creamos el campo de Galois GF(2^3) con px=3 (polinomio primitivo x^3 + x + 1)
campo_prueba = GF(3, 3)

# 2. Creamos dos polinomios de prueba
# pol1 = 2x^2 + 3x + 1  |  pol2 = 5x + 4
pol1 = GFPoly(campo_prueba, [2, 3, 1])
pol2 = GFPoly(campo_prueba, [5, 4])

print(f"Polinomio 1: {pol1}")
print(f"Polinomio 2: {pol2}")

# 3. Probamos la suma (+)
suma_poly = pol1 + pol2
print(f"\n[+] Suma (pol1 + pol2): {suma_poly}")

# 4. Probamos la multiplicación (*)
mult_poly = pol1 * pol2
print(f"[*] Multiplicación (pol1 * pol2): {mult_poly}")

# 5. Probamos el escalado (multiplicar pol1 por el escalar 3)
esc_poly = pol1.escalar(3)
print(f"[Escalar] pol1 multiplicado por 3: {esc_poly}")

# 6. Probamos la evaluación en un punto (ej: x = 2)
eval_poly = pol1.evaluar(2)
print(f"[Evaluar] pol1 evaluado en x=2 da como resultado: {eval_poly}")

# 7. Probamos la construcción desde raíces (ej: raíces 2 y 3)
raices_prueba = [2, 3]
pol_construido = GFPoly.construccion(campo_prueba, raices_prueba)
print(f"[Construcción] Polinomio armado desde raíces {raices_prueba}: {pol_construido}")

print("---------------------------------------\n")