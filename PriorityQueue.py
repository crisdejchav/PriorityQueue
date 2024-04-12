class Persona:
    def __init__(self, nombre : str, edad : int, direccion : str, motivo : str, gravedad : float) -> None:
        self.nombre : str = nombre
        self.edad : int = edad
        self.direccion : str = direccion
        self.motivo : str= motivo
        self.gravedad : int = gravedad
        self.unidad_movil : bool = self.gravedad == 1 or self.gravedad == 2 # Determina si se requiere unidad móvil según la gravedad
        self.prioridad = self.calcular_prioridad()

    def calcular_prioridad(self):
        if self.edad < 12:
            return 1  # Prioridad 1 para niños menores de 12 años
        elif self.edad > 65:
            return 2  # Prioridad 2 para adultos mayores de 65 años
        else:
            return 4  # Prioridad 4 para demás personas
        
    def __str__(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Dirección: {self.direccion}, Motivo: {self.motivo}, Gravedad: {self.gravedad}, Unidad Móvil: {'Motorizada' if self.unidad_movil<3 else 'Con patrulla y unidades de refuerzo'}"


class MonticuloBinario:
    def __init__(self):
        self.listaMonticulo = [Persona("", 0, "", "", float('inf'))]  # Agregamos una persona ficticia con gravedad infinita
        self.tamanoActual = 0

    def encolar(self, persona):
        self.listaMonticulo.append(persona)
        self.tamanoActual = self.tamanoActual + 1
        self.infiltArriba(self.tamanoActual)


    def infiltArriba(self, i):
        while i // 2 > 0:
            if self.es_menor(self.listaMonticulo[i], self.listaMonticulo[i // 2]):
                self.swap(i, i // 2)
            i = i // 2

    def infiltAbajo(self, i):
        while (i * 2) <= self.tamanoActual:
            hm = self.hijoMin(i)
            if self.es_menor(self.listaMonticulo[hm], self.listaMonticulo[i]):
                self.swap(i, hm)
            i = hm

    def es_menor(self, persona1, persona2):
        if persona1.gravedad < persona2.gravedad:
            return True
        elif persona1.gravedad == persona2.gravedad:
            return persona1.prioridad < persona2.prioridad
        return False

    def swap(self, i, j):
        self.listaMonticulo[i], self.listaMonticulo[j] = self.listaMonticulo[j], self.listaMonticulo[i]

    def hijoMin(self, i):
        if i * 2 + 1 > self.tamanoActual:
            return i * 2
        else:
            hijo_izquierdo = i * 2
            hijo_derecho = i * 2 + 1
            if self.listaMonticulo[hijo_izquierdo].gravedad < self.listaMonticulo[hijo_derecho].gravedad:
                return hijo_izquierdo
            elif self.listaMonticulo[hijo_izquierdo].gravedad > self.listaMonticulo[hijo_derecho].gravedad:
                return hijo_derecho
            else:
                # Si la gravedad de los hijos es la misma, se compara la prioridad
                if self.listaMonticulo[hijo_izquierdo].prioridad < self.listaMonticulo[hijo_derecho].prioridad:
                    return hijo_izquierdo
                elif self.listaMonticulo[hijo_izquierdo].prioridad > self.listaMonticulo[hijo_derecho].prioridad:
                    return hijo_derecho
                else:
                    # Si la prioridad de los hijos también es la misma, se elige el hijo con el menor nombre
                    return hijo_izquierdo if self.listaMonticulo[hijo_izquierdo].nombre < self.listaMonticulo[hijo_derecho].nombre else hijo_derecho



    def eliminarMin(self):
        valorSacado = self.listaMonticulo[1]
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual = self.tamanoActual - 1
        self.listaMonticulo.pop()
        self.infiltAbajo(1)
        return valorSacado

    def mostrar_cola(self,p=None):
        if len(self.listaMonticulo) <= 1:
            print("No hay personas en espera.")
            return

        # Creamos una lista temporal para almacenar las personas en orden de gravedad y prioridad
        personas_ordenadas = []

        # Creamos una copia del montículo para no modificarlo
        monticulo_copia = self.listaMonticulo[1:]

        # Ordenamos la copia del montículo primero por gravedad de menor a mayor y luego por prioridad dentro de cada grupo de igual gravedad
        for i in range(len(monticulo_copia)):
            for j in range(len(monticulo_copia) - 1):
                # Comparar gravedad y prioridad de dos personas
                if monticulo_copia[j].gravedad > monticulo_copia[j + 1].gravedad or \
                        (monticulo_copia[j].gravedad == monticulo_copia[j + 1].gravedad and
                        monticulo_copia[j].prioridad > monticulo_copia[j + 1].prioridad):
                    # Intercambiar las personas si están en el orden incorrecto
                    monticulo_copia[j], monticulo_copia[j + 1] = monticulo_copia[j + 1], monticulo_copia[j]

        # Mostramos las personas ordenadas
        print("Cola de prioridad ordenada:")
        for persona in monticulo_copia:
            print(persona)
    
    def posicion(self, llamada):
        for i in range(1, len(self.listaMonticulo)):
            if self.listaMonticulo[i] == llamada:
                return i
        return None


def menu():
    cola_prioridad = MonticuloBinario()
    opciones = {
        1: ingresar_persona,
        2: pasar_siguiente_solicitud,
        3: cola_prioridad.mostrar_cola
    }

    while True:
        print("\nMenú de Atención de Unidades Móviles")
        print("1. Ingresar persona")
        print("2. Pasar siguiente solicitud")
        print("3. Mostrar la cola")
        print("0. Salir")

        opcion = int(input("Ingrese una opción: "))

        if opcion == 0:
            break
        elif opcion in opciones:
            opciones[opcion](cola_prioridad)
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

def ingresar_persona(cola_prioridad: MonticuloBinario):
    nombre = input("Ingrese el nombre completo del solicitante: ")
    edad = int(input("Ingrese la edad del solicitante: "))
    direccion = input("Ingrese la dirección del solicitante: ")
    motivo = input("Ingrese el motivo de la llamada: ")
    gravedad = int(input("Ingrese la gravedad (1 a 4, siendo 1 la mayor gravedad): "))

    persona = Persona(nombre, edad, direccion, motivo, gravedad)
    cola_prioridad.encolar(persona)
    print(f"La solicitud de {persona.nombre} será atendida en la posición {cola_prioridad.posicion(persona)}.")

def pasar_siguiente_solicitud(cola_prioridad: MonticuloBinario):
    if len(cola_prioridad.listaMonticulo)<=1:
        print("No hay solicitudes pendientes en la cola.")
    else:
        persona = cola_prioridad.eliminarMin()
        print(f"Atendiendo la solicitud de {persona}.")


def test():
    cola_prioridad = MonticuloBinario()

    # Casos de prueba
    persona1 = Persona("Juan", 24, "Calle A", "Emergencia", 1)
    persona2 = Persona("Ana", 70, "Calle B", "Emergencia", 1)
    persona3 = Persona("Pedro", 11, "Calle C", "Emergencia", 1)
    persona4 = Persona("Carlos", 24, "Calle D", "Emergencia", 2)
    persona5 = Persona("Eduardo", 70, "Calle F", "Emergencia", 2)
    persona6 = Persona("Camilo", 11, "Calle F", "Emergencia", 2)

    cola_prioridad.encolar(persona1)
    cola_prioridad.encolar(persona2)
    cola_prioridad.encolar(persona3)
    cola_prioridad.encolar(persona4)
    cola_prioridad.encolar(persona5)
    cola_prioridad.encolar(persona6)

    print("Cola de prioridad:")
    cola_prioridad.mostrar_cola()
    
    print("\nAtendiendo siguiente solicitud:")
    siguiente_solicitud = cola_prioridad.eliminarMin()
    print("Solicitud atendida:", siguiente_solicitud) 
    


#Para usar los casos de prueba quitar el '#' a la funcion test
#Para ingresar los casos por consola quitar el '#' a la funcion menu
#test()
menu()
