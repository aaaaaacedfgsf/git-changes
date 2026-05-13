import json

class Usuario:
    def __init__(self, id_usuario, nombre, email):
        # Atributos encapsulados
        self.__id = id_usuario
        self.__nombre = nombre
        self.__email = email

    # Getters necesarios para la persistencia y búsqueda
    def get_id(self): return self.__id
    def get_nombre(self): return self.__nombre
    def get_email(self): return self.__email

    def mostrar_perfil(self):
        return f"ID: {self.__id} | Nombre: {self.__nombre} | Email: {self.__email}"

    def to_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "id": self.__id,
            "nombre": self.__nombre,
            "email": self.__email
        }

class Estudiante(Usuario):
    def __init__(self, id_usuario, nombre, email, carrera):
        super().__init__(id_usuario, nombre, email)
        self.__carrera = carrera

    # Polimorfismo: Sobrescritura de método
    def mostrar_perfil(self):
        base = super().mostrar_perfil()
        return f"[ESTUDIANTE] {base} | Carrera: {self.__carrera}"

    def to_dict(self):
        d = super().to_dict()
        d["carrera"] = self.__carrera
        return d

class Profesor(Usuario):
    def __init__(self, id_usuario, nombre, email, departamento):
        super().__init__(id_usuario, nombre, email)
        self.__departamento = departamento

    # Polimorfismo: Sobrescritura de método
    def mostrar_perfil(self):
        base = super().mostrar_perfil()
        return f"[PROFESOR] {base} | Departamento: {self.__departamento}"

    def to_dict(self):
        d = super().to_dict()
        d["departamento"] = self.__departamento
        return d

class PlataformaVirtual:
    ARCHIVO = "usuarios_plataforma.json"

    def __init__(self):
        self.usuarios = self.cargar_datos()

    def guardar_datos(self):
        with open(self.ARCHIVO, "w") as f:
            json.dump([u.to_dict() for u in self.usuarios], f, indent=4)

    def cargar_datos(self):
        try:
            with open(self.ARCHIVO, "r") as f:
                datos = json.load(f)
                lista = []
                for u in datos:
                    if u['tipo'] == 'Estudiante':
                        lista.append(Estudiante(u['id'], u['nombre'], u['email'], u['carrera']))
                    elif u['tipo'] == 'Profesor':
                        lista.append(Profesor(u['id'], u['nombre'], u['email'], u['departamento']))
                return lista
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def registrar_usuario(self, usuario):
        self.usuarios.append(usuario)
        self.guardar_datos()

    def buscar_por_id(self, id_busqueda):
        # Implementación de búsqueda requerida en image_3a331a.png
        for u in self.usuarios:
            if u.get_id() == id_busqueda:
                return u
        return None

def ejecutar_plataforma():
    plataforma = PlataformaVirtual()
    
    while True:
        print("\n--- PLATAFORMA VIRTUAL ---")
        print("1. Registrar Estudiante\n2. Registrar Profesor\n3. Buscar Usuario (ID)\n4. Ver Todos\n5. Salir")
        op = input("Seleccione: ")
        
        if op in ['1', '2']:
            id_u = input("ID: ")
            nom = input("Nombre: ")
            em = input("Email: ")
            
            if op == '1':
                car = input("Carrera: ")
                plataforma.registrar_usuario(Estudiante(id_u, nom, em, car))
            else:
                dep = input("Departamento: ")
                plataforma.registrar_usuario(Profesor(id_u, nom, em, dep))
            print("Usuario registrado.")

        elif op == '3':
            busqueda = input("Ingrese ID a buscar: ")
            resultado = plataforma.buscar_por_id(busqueda)
            if resultado:
                print(f"\nResultado:\n{resultado.mostrar_perfil()}")
            else:
                print("\nUsuario no encontrado.")

        elif op == '4':
            print("\nListado General:")
            for u in plataforma.usuarios:
                print(u.mostrar_perfil())
        
        elif op == '5':
            break

if __name__ == "__main__":
    ejecutar_plataforma()