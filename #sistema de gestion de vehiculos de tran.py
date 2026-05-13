#sistema de gestion de vehiculos de transporte
import json
#gudgud
class Vehiculo:
    def __init__(self, placa, modelo, marca):
   
        self.__placa = placa
        self.__modelo = modelo
        self.__marca = marca

    def get_placa(self): return self.__placa
    def get_modelo(self): return self.__modelo
    def get_marca(self): return self.__marca

    def mostrar_informacion(self):
        return f"Placa: {self.__placa}, Marca: {self.__marca}, Modelo: {self.__modelo}"

    def to_dict(self):
        """Prepara los datos para persistencia en JSON"""
        return {
            "tipo": self.__class__.__name__,
            "placa": self.__placa,
            "modelo": self.__modelo,
            "marca": self.__marca
        }

class Bus(Vehiculo):
    def __init__(self, placa, modelo, marca, capacidad):
        super().__init__(placa, modelo, marca)
        self.__capacidad = capacidad

    def mostrar_informacion(self):
        return f"BUS {super().mostrar_informacion()}, Capacidad: {self.__capacidad} pasajeros"

    def to_dict(self):
        d = super().to_dict()
        d["capacidad"] = self.__capacidad
        return d

class Taxi(Vehiculo):
    def __init__(self, placa, modelo, marca, tarifa):
        super().__init__(placa, modelo, marca)
        self.__tarifa = tarifa

    def mostrar_informacion(self):
        return f"TAXI {super().mostrar_informacion()}, Tarifa: ${self.__tarifa}"

    def to_dict(self):
        d = super().to_dict()
        d["tarifa"] = self.__tarifa
        return d

class Camion(Vehiculo):
    def __init__(self, placa, modelo, marca, carga):
        super().__init__(placa, modelo, marca)
        self.__carga = carga

    def mostrar_informacion(self):
        return f"CAMIÓN {super().mostrar_informacion()}, Carga: {self.__carga} Ton"

    def to_dict(self):
        d = super().to_dict()
        d["carga"] = self.__carga
        return d

class GestionVehiculos:
    ARCHIVO = "vehiculos.json"

    def __init__(self):
        self.vehiculos = self.cargar_datos()

    def guardar_datos(self):
        with open(self.ARCHIVO, "w") as f:
            json.dump([v.to_dict() for v in self.vehiculos], f, indent=4)

    def cargar_datos(self):
        # Alternativa a 'import os': Manejo de excepciones
        try:
            with open(self.ARCHIVO, "r") as f:
                datos = json.load(f)
                lista = []
                for v in datos:
                    if v['tipo'] == 'Bus':
                        lista.append(Bus(v['placa'], v['modelo'], v['marca'], v['capacidad']))
                    elif v['tipo'] == 'Taxi':
                        lista.append(Taxi(v['placa'], v['modelo'], v['marca'], v['tarifa']))
                    elif v['tipo'] == 'Camion':
                        lista.append(Camion(v['placa'], v['modelo'], v['marca'], v['carga']))
                return lista
        except (FileNotFoundError, json.JSONDecodeError):
            # Si el archivo no existe o está vacío, retorna lista vacía
            return []

    def registrar(self, vehiculo):
        self.vehiculos.append(vehiculo)
        self.guardar_datos()

def menu():
    gestion = GestionVehiculos()
    
    while True:
        print("\n1. Registrar Bus\n2. Registrar Taxi\n3. Registrar Camion\n4. Consultar\n5. Salir")
        op = input("Opción: ")
        
        if op in ['1', '2', '3']:
            p, mod, mar = input("Placa: "), input("Modelo: "), input("Marca: ")
            if op == '1':
                gestion.registrar(Bus(p, mod, mar, input("Capacidad: ")))
            elif op == '2':
                gestion.registrar(Taxi(p, mod, mar, input("Tarifa: ")))
            else:
                gestion.registrar(Camion(p, mod, mar, input("Carga (Ton): ")))
        elif op == '4':
            for v in gestion.vehiculos:
                print(v.mostrar_informacion())
        elif op == '5':
            break

if __name__ == "__main__":
    menu()