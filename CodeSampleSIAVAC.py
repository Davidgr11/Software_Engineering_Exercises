import time
import secrets
import string
from PySide6.QtCore import Qt

import Clases as C

from PySide6.QtWidgets import QApplication, QMainWindow, QFrame
from mainwindow import Ui_MainWindow
import sys
from qt_material import apply_stylesheet
from PySide6.QtCore import QTimer

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)




    #Función trigger para detectar el llenado de la barra de progreso
    def actualizar_progreso(self):
        value = self.progressBar.value() + 1
        self.progressBar.setValue(value)
        if value == self.progressBar.maximum():
            timer.stop()
            self.stackedWidget.setCurrentIndex(1)

    def pagina_registro(self):
        self.stackedWidget.setCurrentIndex(2)

    def pagina_bienvenida(self):
        self.stackedWidget.setCurrentIndex(1)
        self.limpiar_paginaRegistro()

    def pagina_ciudadanosPacientes(self):
        self.stackedWidget.setCurrentIndex(4)

    def pagina_perfilDigital(self):
         self.actualizar_informacion_perfil_digital()
         self.stackedWidget.setCurrentIndex(5)

    def pagina_cartillaVacunacionDigital(self):
        self.cargar_cartillaVacunacionDigital()
        self.stackedWidget.setCurrentIndex(6)

    def cargar_cartillaVacunacionDigital(self):
        vacunas = C.ControladorVacuna()
        self.listWidget.clear()
        self.textBrowser.clear()
        for item in vacunas.obtener_lista_vacunas():
            self.listWidget.addItem(str(item.getNombre()))

    def mostrar_informacion(self):
        vacunas = C.ControladorVacuna()
        self.textBrowser.clear()
        for item in vacunas.obtener_lista_vacunas():
            if item.getNombre() == self.listWidget.currentItem().text():
                self.textBrowser.setText('Previene:\n'+ item.getDescripcion() + '\n\nAplicación:\n' +
                                         item.getDescripcionAplicacion())

    def actualizar_informacion_perfil_digital(self):
        self.textBrowser_2.clear()

        email = self.lineEdit_7.text()

        password = self.lineEdit_8.text()

        pacientes = C.ControladorPaciente()

        paciente = pacientes.comprobar_cuenta_paciente(email, password)

        cartillas = C.ControladorCartillaVacunacion()

        cartilla = cartillas.obtener_cartilla(paciente.getCvePaciente())

        for item in cartilla.getAplicacion():
            self.textBrowser_2.append('Vacuna '+item[0]+' aplicada el '+item[1])

    def confirmar_registroVacunacion(self):
        if self.lineEdit_9.text() != '' and self.listWidget.currentItem():
            print(self.listWidget.currentItem().text()+'  '+self.lineEdit_9.text())

            email = self.lineEdit_7.text()

            password = self.lineEdit_8.text()

            pacientes = C.ControladorPaciente()

            paciente = pacientes.comprobar_cuenta_paciente(email, password)

            cartillas = C.ControladorCartillaVacunacion()

            cartillas.agregar_aplicacion(self.listWidget.currentItem().text(), self.lineEdit_9.text(), paciente.getCvePaciente())

            self.lineEdit_9.setText('')

    def pagina_loginAutoridades(self):
        self.stackedWidget.setCurrentIndex(7)

    def pagina_administracion(self):
        self.stackedWidget.setCurrentIndex(8)



    def pagina_inventarioSuministros(self):
        self.stackedWidget.setCurrentIndex(10)


    def pagina_surtidoVacunas(self):
        self.stackedWidget.setCurrentIndex(11)

    def pagina_confirmacionPedido(self):
        self.stackedWidget.setCurrentIndex(12)

    def pagina_administrarPerfilDigital(self):
        #eliminar estrá función de la función principal
        self.mosntrar_pacientes()
        self.vacunas_palicadas()
        self.stackedWidget.setCurrentIndex(9)


    #Eliminar esta función
    def mosntrar_pacientes(self):
        self.listWidget_2.clear()
        self.textBrowser_3.clear()

        pacientes = C.ControladorPaciente().obtener_pacientes()
        for item in pacientes:
            self.listWidget_2.addItem(str(item.getCURP()))
            #self.textBrowser_3.append(str(value))


    def vacunas_palicadas(self):
        self.textBrowser_4.clear()
        vacunas = C.ControladorCartillaVacunacion().encontrar_vacunas_menos_aplicadas()
        for key, value in vacunas.items():
            print(key + str(value))
            self.textBrowser_4.append(key + ' = '+str(value))

    #función experimental
    def buscar_paciente_curp(self):
        buscar = self.lineEdit_12.text()
        if buscar != '':
            paciente = C.ControladorPaciente().buscar_paciente_curp(buscar)
            if paciente:
                elemento = self.listWidget_2.findItems(paciente.getCURP(), Qt.MatchExactly)
                self.listWidget_2.setCurrentItem(elemento[0])
                self.lineEdit_12.setText('')
            else:
                print('--> El elemento no se encontró')
        else:
            print('--> No se ha ingresado la curp a buscar')


    def mostrar_informacion_paciente_seleccionado(self):
        #vacunas = C.ControladorVacuna()
        self.textBrowser_3.clear()
        curp = self.listWidget_2.currentItem().text()
        print(str(curp))
        paciente = C.ControladorPaciente().buscar_paciente_curp(curp)
        if paciente:
            cartilla = C.ControladorCartillaVacunacion().obtener_cartilla(paciente.getCvePaciente())
            self.textBrowser_3.setText('Nombre:\n'+ paciente.getNombre() + '\n\nAplicación:\n')
            for item in cartilla.getAplicacion():
                self.textBrowser_3.append(item[0]+' / '+item[1])





    def completar_registro(self):
         controlador_paciente = C.ControladorPaciente()
         if ((self.lineEdit_3.text() and self.lineEdit_4.text() and self.lineEdit_5.text() and self.lineEdit.text() and self.lineEdit_2.text()) != '') and ((self.spinBox.value() and self.spinBox_2.value() and self.spinBox_3.value()) != 0):
             fecha = (str(self.spinBox.text())+'/'+str(self.spinBox_2.text())+'/'+str(self.spinBox_3.text()))
             if controlador_paciente.registrar_paciente(self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(), fecha, self.lineEdit.text(),self.lineEdit_2.text()):
                 paciente = controlador_paciente.buscar_paciente_curp(self.lineEdit_4.text())
                 self.lineEdit_6.setText(paciente.getMatriculaUnica())
                 self.stackedWidget.setCurrentIndex(3)

                 cartilla = C.ControladorCartillaVacunacion()
                 cartilla.crear_carilla(paciente.getCvePaciente())

                 self.limpiar_paginaRegistro()

                 print('--> Se creó el registro del paciente')
             else:
                 print('--> No se puedo crear el registro del paciente')
         else:
             print('--> Hacen campos por llenar')

    def acceso_usuario(self):
        controlador_paciente = C.ControladorPaciente()
        email = self.lineEdit_7.text()
        password = self.lineEdit_8.text()
        paciente = controlador_paciente.comprobar_cuenta_paciente(email, password)
        if paciente:
            cartilla = C.ControladorCartillaVacunacion()
            if  not cartilla.obtener_cartilla(paciente.getCvePaciente()):
                print('--> No encontró la cartilla')
                cartilla.crear_carilla(paciente.getCvePaciente())
            else:
                print('--> Encontró la cartilla')

            self.pagina_perfilDigital()

            print('--> Perfil autenticado')


        else:
            print('--> Credenciales no validas')


    def limpiar_paginaRegistro(self):
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.spinBox.setValue(0)
        self.spinBox_2.setValue(0)
        self.spinBox_3.setValue(0)
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')















if __name__ == '__main__':
    app = QApplication(sys.argv)
    #Crecia una instancia de Singleton
    conexion = C.MongoDBConnection.get_instance()

    #app.setStyle("Fusion")
    # ['bb10dark', 'bb10bright', 'cleanlooks', 'cde', 'motif', 'plastique', 'Windows', 'Fusion']



    apply_stylesheet(app, theme="dark_teal.xml")
    window = Mainwindow()
    #Se acomoda a la pantalla 1
    window.stackedWidget.setCurrentIndex(0)
    #Se muestra la pantalla
    window.show()
    #Simular la carga del progressbar
    timer = QTimer()
    timer.timeout.connect(window.actualizar_progreso)
    timer.start(20)
    window.pushButton.pressed.connect(window.pagina_registro)
    window.pushButton_2.pressed.connect(window.pagina_loginAutoridades)
    window.pushButton_3.pressed.connect(window.pagina_bienvenida)
    window.pushButton_4.pressed.connect(window.completar_registro)
    window.pushButton_5.pressed.connect(window.pagina_ciudadanosPacientes)
    window.pushButton_6.pressed.connect(window.pagina_ciudadanosPacientes)
    window.pushButton_8.pressed.connect(window.pagina_bienvenida)
    window.pushButton_7.pressed.connect(window.acceso_usuario)
    window.pushButton_10.pressed.connect(window.pagina_bienvenida)
    window.pushButton_9.pressed.connect(window.pagina_cartillaVacunacionDigital)
    window.pushButton_12.pressed.connect(window.pagina_perfilDigital)
    window.listWidget.itemSelectionChanged.connect(window.mostrar_informacion)
    window.pushButton_11.pressed.connect(window.confirmar_registroVacunacion)
    window.pushButton_13.pressed.connect(window.pagina_administracion)
    window.pushButton_14.pressed.connect(window.pagina_bienvenida)
    window.pushButton_16.pressed.connect(window.pagina_administrarPerfilDigital)
    window.pushButton_17.pressed.connect(window.pagina_bienvenida)
    window.pushButton_19.pressed.connect(window.pagina_administracion)



    window.pushButton_15.pressed.connect(window.pagina_inventarioSuministros)
    window.pushButton_21.pressed.connect(window.pagina_surtidoVacunas)
    window.pushButton_23.pressed.connect(window.pagina_confirmacionPedido)
    window.pushButton_24.pressed.connect(window.pagina_inventarioSuministros)
    window.pushButton_22.pressed.connect(window.pagina_inventarioSuministros)
    window.pushButton_20.pressed.connect(window.pagina_administracion)




    window.listWidget_2.itemSelectionChanged.connect(window.mostrar_informacion_paciente_seleccionado)
    window.pushButton_18.pressed.connect(window.buscar_paciente_curp)

    #Cierra la conexión a la base de datos
    app.aboutToQuit.connect(conexion.close())
    #Final de ejecución de app
    sys.exit(app.exec())
