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
        self.tamanoActual += 1
        self.infiltArriba(self.tamanoActual)

    def infiltArriba(self, i):
        while i // 2 > 0:
            if self.es_menor(self.listaMonticulo[i], self.listaMonticulo[i // 2]):
                self.swap(i, i // 2)
            i = i // 2

    def infiltAbajo(self, i):
        while (i * 2) <= self.tamanoActual:
            hm : int = self.hijoMin(i)
            if self.es_menor(self.listaMonticulo[hm], self.listaMonticulo[i]):
                self.swap(i, hm)
            elif self.listaMonticulo[hm].gravedad == self.listaMonticulo[i].gravedad:
                if self.listaMonticulo[hm].prioridad < self.listaMonticulo[i].prioridad:
                    self.swap(i, hm)
                else:
                    break
            else:
                break
            i = hm

    def es_menor(self, persona1: Persona, persona2: Persona):
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
                if self.listaMonticulo[hijo_izquierdo].prioridad < self.listaMonticulo[hijo_derecho].prioridad:
                    return hijo_izquierdo
                elif self.listaMonticulo[hijo_izquierdo].prioridad > self.listaMonticulo[hijo_derecho].prioridad:
                    return hijo_derecho
                else:
                    return hijo_izquierdo if self.listaMonticulo[hijo_izquierdo].gravedad < self.listaMonticulo[hijo_derecho].gravedad else hijo_derecho

    def eliminarMin(self):
        if self.tamanoActual == 0:
            return None  # No hay elementos en el montículo

        valorSacado = self.listaMonticulo[1]
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual = self.tamanoActual - 1
        self.listaMonticulo.pop()
        self.infiltAbajo(1)
        return valorSacado

    def mostrar_cola(self, p=None):
        if len(self.listaMonticulo) <= 1:
            print("No hay personas en espera.")
            return

        monticulo_copia = self.listaMonticulo[1:]

        # Construir el montículo
        for i in range(len(monticulo_copia) // 2, 0, -1):
            self.infiltAbajo(i)

        # Ordenar el montículo
        personas_ordenadas = []
        while self.tamanoActual > 0:
            persona = self.eliminarMin()
            personas_ordenadas.append(persona)


        #Se devuelven los valores al monticulo
        self.listaMonticulo[1:] = personas_ordenadas
        self.tamanoActual = len(self.listaMonticulo)-1
        # Mostrar las personas ordenadas
        print("Cola de prioridad ordenada:")
        for persona in personas_ordenadas:
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
    gravedad = int(input("Ingrese la gravedad (1 a 5, siendo 1 la mayor gravedad): "))

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
    
    print("Cola de prioridad:")
    cola_prioridad.mostrar_cola()
    
     
#Para usar los casos de prueba quitar el '#' a la funcion test
#Para ingresar los casos por consola quitar el '#' a la funcion menu
#test()
menu()
