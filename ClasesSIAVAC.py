import pymongo
import threading
import secrets
import string
########################################################################################################################
# Definir la clase MongoDBConnection
class MongoDBConnection:
    # Definir una variable de clase que guarda la única instancia de la clase
    _instance = None

    # Definir un objeto lock para asegurar la exclusión mutua
    _lock = threading.Lock()

    # Definir el constructor de la clase
    def __init__(self):

        user = 'USUARIO'
        password = 'UB7JaTItv69sA2J7'

        # Crear el objeto MongoClient con la dirección del servidor de mongo db
        self.client = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@cluster0.zw562mt.mongodb.net/?retryWrites=true&w=majority")

    # Definir un método de clase que devuelve la única instancia de la clase
    @classmethod
    def get_instance(cls):
        # Si la instancia no existe, adquirir el lock y crearla
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        # Devolver la instancia de la clase
        return cls._instance

    # Definir el método get_connection que devuelve el objeto MongoClient
    def get_connection(self):
        return self.client

    def close(self):
        self.client.close()

########################################################################################################################

class Vacuna:
    pass
    def __init__(self):
        pass

    def __init__(self, cveVacuna, nombre, descripcion, descripcionAplicacion):
        self.__cveVacuna = cveVacuna
        self.__descripcion = descripcion
        self.__descripcionAplicacion = descripcionAplicacion
        self.__nombre = nombre

    #Getters

    def getCveVacuna(self):
        return self.__cveVacuna

    def getDescripcion(self):
        return self.__descripcion

    def getDescripcionAplicacion(self):
        return self.__descripcionAplicacion

    def getNombre(self):
        return self.__nombre

    #Setters

    def setCveVacuna(self, cveVacuna):
        self.__cveVacuna = cveVacuna

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

    def setDescripcionAplicacion(self, descripcionAplicacion):
        self.__descripcionAplicacion = descripcionAplicacion

    def setNombre(self, nombre):
        self.__nombre = nombre


class ModeloVacuna:
    # Obtener la instancia de la clase MongoDBConnection
    connection = MongoDBConnection.get_instance()

    # Obtener el objeto MongoClient
    client = connection.get_connection()

    # Acceder a la base de datos llamada "mi_app"
    db = client['SecretariaDeSalud']

    # Acceder a la colección llamada "usuarios"
    users = db["Vacunas"]

    listaVacunas = []

    def __init__(self):
        pass
        for user in self.users.find():
            self.listaVacunas.append(Vacuna(user['cveVacuna'], user['nombre'], user['descripcion'], user['descripcionAplicacion']))

        for item in self.listaVacunas:
            print(item.getCveVacuna() + ' / ' + item.getNombre() + ' / ' + item.getDescripcion()+ ' / ' + item.getDescripcionAplicacion())


    def obtener_lista_vacunas(self):
        return self.listaVacunas


class ControladorVacuna:
    modeloVacuna = ModeloVacuna()

    def obtener_lista_vacunas(self):
        return self.modeloVacuna.obtener_lista_vacunas()

########################################################################################################################
class Paciente:


    def __init__(self, correo, CURP, cvePaciente, direccion, fechaNacimiento, matriculaUnica, nombre, numeroTelefono):
        self.__correo = correo
        self.__CURP = CURP
        self.__cvePaciente = cvePaciente
        self.__direccion = direccion
        self.__fechaNacimiento = fechaNacimiento
        self.__matriculaUnica = matriculaUnica
        self.__nombre = nombre
        self.__numeroTelefono = numeroTelefono


    #Getters
    def getCorreo(self):
        return self.__correo

    def getCURP(self):
        return self.__CURP

    def getCvePaciente(self):
        return self.__cvePaciente

    def getDireccion(self):
        return self.__direccion

    def getFechaNacimiento(self):
        return self.__fechaNacimiento

    def getMatriculaUnica(self):
        return self.__matriculaUnica

    def getNombre(self):
        return self.__nombre

    def getNumeroTelefono(self):
        return self.__numeroTelefono

    # Setters
    def setCorreo(self, correo):
        self.__correo = correo

    def setCURP(self, CURP):
        self.__CURP = CURP

    def setCvePaciente(self, cvePaciente):
        self.__cvePaciente = cvePaciente

    def setDireccion(self, direccion):
        self.__direccion = direccion

    def setFechaNacimiento(self, fechaNacimiento):
        self.__fechaNacimiento = fechaNacimiento

    def setMatriculaUnica(self, matriculaUnica):
        self.__matriculaUnica = matriculaUnica

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setNumeroTelefono(self, telefono):
        self.__numeroTelefono = telefono


class ModeloPaciente:
    # Obtener la instancia de la clase MongoDBConnection
    connection = MongoDBConnection.get_instance()

    # Obtener el objeto MongoClient
    client = connection.get_connection()

    # Acceder a la base de datos llamada "mi_app"
    db = client['SecretariaDeSalud']

    # Acceder a la colección llamada "usuarios"
    users = db["Pacientes"]


    listaPacientes = []

    def __init__(self):
        for user in self.users.find():
            self.listaPacientes.append(Paciente(user['correo'], user['curp'], user['cvePaciente'], user['direccion'],
                                                user['fechaNacimiento'], user['matriculaUnica'], user['nombre'], user['telefono']))

        for item in self.listaPacientes:
            print(item.getCorreo() +' / '+item.getCURP()+' / '+str(item.getCvePaciente())+' / '+item.getDireccion()+' / '+
                  item.getFechaNacimiento() +' / '+item.getMatriculaUnica()+' / '+item.getNombre()+' / '+str(item.getNumeroTelefono())+'\n')


    #Busqueda de paciente mediante curp
    def buscar_paciente_curp(self, CURP):
        for item in self.listaPacientes:
            if item.getCURP() == CURP:
                print('--> Se encontró al paciente')
                return item

        return None

    #Validadción de credenciales para el usuario
    def comprobar_cuenta_paciente(self, email, password):
        for item in self.listaPacientes:
            if item.getCorreo() == email:
                print('--> Se encontró al paciente')
                if item.getMatriculaUnica() == password:
                    return item
                else:
                    return None

        return None

    #Generación de una matrícula única
    def generare_matriculaUnica(self):
        caracteres = string.ascii_letters + string.digits  # todos los caracteres posibles
        longitud = 14  # la longitud que quieres
        matriculaUnica = "".join(secrets.choice(caracteres) for i in range(longitud))  # elegir 10 caracteres al azar
        return matriculaUnica

    #Generación de una clave de paciente única
    def generare_cvePaciente(self):
        caracteres = string.digits  # todos los caracteres posibles
        longitud = 14  # la longitud que quieres
        cvePaciente = "".join(secrets.choice(caracteres) for i in range(longitud))  # elegir 10 caracteres al azar
        return cvePaciente

    #Verificar que la clave de paciente única no se repita
    def comprobar_cvePaciente(self, cvePaciente):
        for item in self.listaPacientes:
            if item.getCvePaciente() == int(cvePaciente):
                    return False

        return True

    #Verificar que la matrícula única del paciente no se repita
    def comprobar_matriculaUnica(self, matriculaUnica):
        for item in self.listaPacientes:
            if item.getMatriculaUnica() == matriculaUnica:
                    return False

        return True

    #Agregar un nuevo paciente a la base de datos
    def registrar_paciente(self, correo, CURP, direccion, fechaNacimiento, nombre, numeroTelefono):
        if not self.buscar_paciente_curp(CURP):

            cvePaciente = self.generare_cvePaciente()
            while True:
                if  self.comprobar_cvePaciente(cvePaciente) == True:
                    break
                else:
                    cvePaciente = self.generare_cvePaciente()

            matriculaUnica = self.generare_matriculaUnica()
            while True:
                if self.comprobar_matriculaUnica(matriculaUnica) == True:
                    break
                else:
                    matriculaUnica = self.generare_matriculaUnica()

            nuevo_paciente = Paciente(correo, CURP, cvePaciente, direccion, fechaNacimiento, matriculaUnica, nombre, numeroTelefono)
            self.listaPacientes.append(nuevo_paciente)
            user = {'correo':correo, 'curp': CURP, 'cvePaciente':int(cvePaciente), 'direccion': direccion, 'fechaNacimiento':fechaNacimiento,
                    'matriculaUnica':matriculaUnica, 'nombre':nombre, 'telefono':numeroTelefono}
            self.users.insert_one(user)

            return True

        else:
            return False

    def obtener_pacientes(self):
        return self.listaPacientes



class ControladorPaciente:

    modeloPaciente = ModeloPaciente()

    # buscar a un paciente por su curp
    def buscar_paciente_curp(self, CURP):
        #Regresa el objeto paciente u objeto vacío
        return (self.modeloPaciente.buscar_paciente_curp(CURP))

    # Valida la cuenta y contraseñas de quién desea entrar a la aplicación
    def comprobar_cuenta_paciente(self, email, password):
        #Regresa True o False
        return (self.modeloPaciente.comprobar_cuenta_paciente(email,password))

    def registrar_paciente(self, correo, CURP, direccion, fechaNacimiento, nombre, numeroTelefono):
        #Regresa True o False dependiendo si la CURP no se ha registrado antes
        return (self.modeloPaciente.registrar_paciente( correo, CURP, direccion, fechaNacimiento, nombre, numeroTelefono))

    def obtener_pacientes(self):
        return self.modeloPaciente.obtener_pacientes()

########################################################################################################################

class CartillaVacunacion:


    def __init__(self, cveCartilla, aplicacion):
        self.__cveCartilla = cveCartilla
        self.__aplicacion = aplicacion

    #Gettes
    def getCveCartilla(self):
        return self.__cveCartilla

    def getAplicacion(self):
        return self.__aplicacion


    #Setters

    def setCveCartilla(self, cveCartilla):
        self.__cveCartilla = cveCartilla

    def setAplicacion(self, aplicacion):
        self.__aplicacion = aplicacion



class ModeloCartillaVacunacion:
    # Obtener la instancia de la clase MongoDBConnection
    connection = MongoDBConnection.get_instance()

    # Obtener el objeto MongoClient
    client = connection.get_connection()

    # Acceder a la base de datos llamada "mi_app"
    db = client['SecretariaDeSalud']

    # Acceder a la colección llamada "usuarios"
    users = db["CartillaDeVacunacion"]

    listaCartillas = []

    def __init__(self):
        for user in self.users.find():
            self.listaCartillas.append(CartillaVacunacion(user['cveCartilla'], user['aplicacion']))

        for item in self.listaCartillas:
            print('Clave: '+str(item.getCveCartilla()))
            for index in item.getAplicacion():
                print('Nombre de vacuna: ' + index[0] + 'Fecha de aplicación: '+index[1])


    def crear_cartilla(self, cveCartilla):
        cartilla = CartillaVacunacion(int(cveCartilla), [])
        self.listaCartillas.append(cartilla)
        user = {'cveCartilla': int(cveCartilla), 'aplicacion': []}
        self.users.insert_one(user)


    def agregar_aplicacion(self, nombreVacuna, fechaAplicacion, cveCartilla):
        cartilla = self.obtener_cartilla(int(cveCartilla))
        if cartilla:
            aplicacion = [nombreVacuna, fechaAplicacion]
            cartilla.getAplicacion().append(aplicacion)
            self.users.update_one({"cveCartilla":int(cveCartilla)}, {"$push" : {"aplicacion" : aplicacion}})


    def obtener_cartilla(self, cveCartilla):
        for item in self.listaCartillas:
            if item.getCveCartilla() == int(cveCartilla):
                return item

        return None


    def encontrar_vacunas_menos_aplicadas(self):
        diccionario = {}
        for item in ControladorVacuna().obtener_lista_vacunas():
            #print(item.getNombre())
            diccionario[f'{item.getNombre()}'] = 0

        for item in self.listaCartillas:
            for index in item.getAplicacion():
                diccionario[f'{index[0]}'] +=1

        # Ordenar el diccionario del mayor al menor usando sorted y una función lambda
        diccionario = sorted(diccionario.items(), key=lambda x: x[1], reverse=True)

        # Convertir el resultado en un diccionario usando dict
        diccionario = dict(diccionario)

        #print(diccionario)

        return diccionario



class ControladorCartillaVacunacion:
    modeloCartillaVacunacion = ModeloCartillaVacunacion()

    def crear_carilla(self, cveCartilla):
        self.modeloCartillaVacunacion.crear_cartilla(cveCartilla)

    def obtener_cartilla(self, cveCartilla):
        return self.modeloCartillaVacunacion.obtener_cartilla(cveCartilla)

    def agregar_aplicacion(self, nombreVacuna, fechaAplicacion, cveCartilla):
        self.modeloCartillaVacunacion.agregar_aplicacion(nombreVacuna, fechaAplicacion, cveCartilla)

    def encontrar_vacunas_menos_aplicadas(self):
        return self.modeloCartillaVacunacion.encontrar_vacunas_menos_aplicadas()


########################################################################################################################

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)


class Data(Subject):
    def __init__(self, name=''):
        Subject.__init__(self)
        self.name = name
        self._data = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.notify()


class HexViewer:
    def update(self, subject):
        print(f'HexViewer: Subject {subject.name} has data 0x{subject.data:x}')


class DecimalViewer:
    def update(self, subject):
        print(f'DecimalViewer: Subject {subject.name} has data {subject.data}')







if __name__ == '__main__':

    #elimina observador detach
    #notifica observador notify
    #agrega observador attach


    #Objetos normales
    data1 = Data('Data 1')
    data2 = Data('Data 2')

    #Observadores
    view1 = DecimalViewer()
    view2 = HexViewer()

    #se asignan los observadores para que observen a quien se desea
    data1.attach(view1)
    data1.attach(view2)
    data2.attach(view2)
    data2.attach(view1)

    #Ejemplos de la actividad de observadores
    print('\nObservadores activados:\n')
    print("Setting Data 1 = 10")
    data1.data = 10
    print("Setting Data 2 = 15")
    data2.data = 15
    print("Setting Data 1 = 3")
    data1.data = 3
    print("Setting Data 2 = 5")
    data2.data = 5
    print("Detach HexViewer from data1 and data2.")

    print('\nObservadores desactivados\n')
    data1.detach(view2)
    data2.detach(view2)
    print("Setting Data 1 = 10")
    data1.data = 10
    print("Setting Data 2 = 15")
    data2.data = 15

    #ControladorCartillaVacunacion().encontrar_vacunas_menos_aplicadas()

  # cartilla = ControladorCartillaVacunacion()
  # #cartilla.crear_carilla(12345)
  # prueba = cartilla.obtener_cartilla(12345)
  # if prueba:
  #     print(prueba.getCveCartilla())
  #
  # cartilla.agregar_aplicacion('Vacuna prueba dos', '02/02/02', 12345)

    #paciente = ControladorPaciente()
    #
    # busqueda = paciente.buscar_paciente_curp('MARS960715MDFCNS06')
    # if busqueda:
    #     print(busqueda.getNombre())
    #
    # print(paciente.comprobar_cuenta_paciente('juan@gmail.com', '2021-123456'))
    #
    # print(paciente.registrar_paciente('correo@prueba', 'fadsfadsfadsfd','direccin¿opuregba','rfechapreuba','preuba 1', 329083409))
    #













