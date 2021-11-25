# Estudiantes: Tomás Granados y Pablo Arias Navarro

###################################################
# SECCIÓN DE MÓDULOS                              #
###################################################

from tkinter import *
from tkinter import messagebox
from functools import partial
import random


###################################################
# SECCIÓN DE CLASES                               #
###################################################


##################################################
############ Validaciones ########################
##################################################

def validacionFila(nuevoValor, indiceFila):
    global partida
    global matriz

    for fila in range(9):
        if indiceFila == fila:
            contadorElemento = 0
            for elemento in partida[fila]:
                if elemento == nuevoValor:
                    matriz[fila][contadorElemento].config(bg='red3')
                    messagebox.showwarning('ERROR', 'JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA FILA')
                    matriz[fila][contadorElemento].config(bg='#f0f0f0')
                    return True

                contadorElemento += 1

    return False


def validacionColumna(nuevoValor, indiceColumna):
    global partida
    global matriz

    for fila in range(9):
        columnaActual = 0
        for elemento in partida[fila]:
            if indiceColumna == columnaActual:
                if nuevoValor == elemento:
                    matriz[fila][columnaActual].config(bg='red3')
                    messagebox.showwarning('ERROR', 'JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA COLUMNA')
                    matriz[fila][columnaActual].config(bg='#f0f0f0')
                    return True

            columnaActual += 1

    return False


def validacionCuadricula(nuevoValor, indiceFila, indiceColumna):
    global partida
    global lista_grupos_matriz
    global matriz

    grupo = 0
    for cuadricula in lista_grupos_matriz:
        if (indiceFila, indiceColumna) in cuadricula:
            break
        grupo += 1

    cuadriculaNecesaria = lista_grupos_matriz[grupo]#Lista con posiciones de la cuadricula a la que pertenece la el boton presionado

    for elemento in cuadriculaNecesaria:  # Verifica si existe un numero igual al que se quiere colocar en la cuadricula
        fila = elemento[0]
        columna = elemento[1]

        if partida[fila][columna] == nuevoValor:
            matriz[fila][columna].config(bg='red3')
            messagebox.showwarning('ERROR', 'JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA CUADRÍCULA')
            matriz[fila][columna].config(bg='#f0f0f0')
            return True

    return False

def validacionNombre():
    global entryNombre

    nombre = entryNombre.get()

    if len(nombre) > 30:
        messagebox.showwarning('CUIDADO', 'EL NOMBRE INGRESADO NO PUEDE EXCEDER LOS 30 CARACTERES')
        return True

    if nombre == '':
        messagebox.showwarning('CUIDADO', 'ANTES DE INICIAR EL JUEGO DEBE DE INGRESAR UN NOMBRE')
        return True

    return False


def ganarPartida():
    global partida

    for fila in partida:
        for elemento in fila:
            if elemento == '':
                return False

    return True

#############################################################################################

def jugar():
    global ventanaPrincipal
    global botonUno
    global partida
    global matrizTeclado
    global entryNombre

    ventanaJuego = Toplevel(ventanaPrincipal)

    ventanaPrincipal.withdraw()

    ventanaJuego.geometry('800x700')
    ventanaJuego.title('Sudoku')
    ventanaJuego.configure(bg='#3e97b8')
    ventanaJuego.resizable(False, False)

    sudokuLabel = Label(ventanaJuego, text=' S   u   d   o   k   u ', borderwidth=4, relief='groove', fg='White',
                        bg='mediumOrchid', font=('Arial', '24', 'bold italic',))
    sudokuLabel.place(x=280, y=20)

    nombreJugador = Label(ventanaJuego, text='Jugador', fg='White', borderwidth=3, bg='#3e97b8',
                          font=('Arial', '16', 'bold italic'))
    nombreJugador.place(x=590, y=100)

    entryNombre = Entry(ventanaJuego, width=40)
    entryNombre.place(x=510, y=130)

    def updateGUI(i, j):
        global matriz
        global textoBotonTeclado
        global infoBotonTeclado
        global matrizTeclado
        global partida

        textoEnPosicion = matriz[i][j].cget('text')

        # No selecciono un el elemento que quiere añadir

        if infoBotonTeclado == []:

            messagebox.showwarning('ERROR', 'FALTA SELECCIONAR UN ELEMENTO')
            return

        # Validaciones

        listaValidaciones = []

        listaValidaciones.append(validacionFila(textoBotonTeclado, i))  # Validacion de fila

        listaValidaciones.append(validacionColumna(textoBotonTeclado, j))  # Validacion de columna

        listaValidaciones.append(validacionCuadricula(textoBotonTeclado, i, j))  # Validacion de cuadricula

        if True in listaValidaciones:  # Verifica si el numero no se puede colocar
            return

        if infoBotonTeclado != []:
            if textoEnPosicion == '':
                matriz[i][j].config(text=textoBotonTeclado)
                matrizTeclado[infoBotonTeclado[0]][infoBotonTeclado[1]].config(relief=RAISED, bg='#21dec8',
                                                                               state='active')
                partida[i][j] = textoBotonTeclado
                infoBotonTeclado = []
            else:
                messagebox.showwarning('Casilla ocupada', 'Esta casilla no se puede modificar')

        if ganarPartida():
            messagebox.showinfo('JUEGO COMPLETADO', '¡EXCELENTE! JUEGO COMPLETADO')
            ventanaJuego.destroy()
            jugar()

    def procesoSeleccionBotonesTeclado():
        global matriz
        global ventanaPrincipal
        global matrizTeclado
        global textoBotonTeclado
        global infoBotonTeclado

        # Resetea colores
        for fila in matrizTeclado:
            for boton in fila:
                boton.config(relief=RAISED, bg='#21dec8', state='active')

        botonActual = matrizTeclado[infoBotonTeclado[0]][infoBotonTeclado[1]]
        botonActual.config(relief=SUNKEN, bg='#51f577', state='disabled')
        textoBotonTeclado = botonActual.cget('text')

    # Creacion de botones  (Cuadricula donde se juega Sudoku)

    for i in range(9):
        fila = []
        for j in range(9):
            boton = Button(ventanaJuego, text='',bg= '#f0f0f0', width=4, height=2, font=('Arial', '10'),
                               command=partial(updateGUI, i, j))

            if j == 0:
                boton.grid(row=i, column=j, padx=(60, 0))

            if i == 0:
                boton.grid(row=i, column=j, pady=(80, 0))

            if j in [2, 5]:
                boton.grid(row=i, column=j, padx=(0, 5))

            if i in [2, 5]:
                boton.grid(row=i, column=j, pady=(0, 5))

            else:
                boton.grid(row=i, column=j)

            fila.append(boton)
        matriz.append(fila)

    def extraerInfoTecla(fila, columna):
        global infoBotonTeclado

        infoBotonTeclado = [fila, columna]
        procesoSeleccionBotonesTeclado()

    # Se crea la matriz con los botones que poseen los numeros que se pueden ingresar al sudoku

    contadorNumero = 0
    y = 200

    for fila in range(3):
        x = 530
        filaBotones = []
        for columna in range(3):
            contadorNumero += 1
            boton = Button(ventanaJuego, text=str(contadorNumero),
                           width=5, height=2, bg='#21dec8',state='disabled', activebackground='#21dec8',
                           command=partial(extraerInfoTecla, fila, columna))
            boton.place(x=x, y=y)
            x += 70

            filaBotones.append(boton)

        y += 60
        matrizTeclado.append(filaBotones)

    ################################### Config Botones (Opciones) ########################################

    def opcionIniciarJuego():
        global matriz
        global matrizTeclado

        if validacionNombre():
            return

        seleccionDePartida('Facil')

        # Actualiza la cuadricula con la partida seleccionada al azar
        for i in range(9):
            for j in range(9):
                botonActual = matriz[i][j]
                if partida[i][j] != '':
                    botonActual.config(text=partida[i][j])

        iniciar_juego.config(state='disabled', relief=SUNKEN)

        # Activa los botones con los digitos que se pueden ingresar en el juego
        for fila in range(3):
            for columna in range(3):
                matrizTeclado[fila][columna].config(state='active')

        validacionNombre()


    #Botones de funciones del juego

    iniciar_juego = Button(ventanaJuego, text="INICIAR\n JUEGO", bg="#ff7438", fg="black",
                           font=("Helvetica", "12", "italic"), command=opcionIniciarJuego)
    iniciar_juego.place(x=330, y=500, width=100, height=50)

    deshacer_jugada = Button(ventanaJuego, text="DESHACER\n JUGADA", bg="#4af9ff", fg="black",
                             font=("Helvetica", "12", "italic"))
    deshacer_jugada.place(x=450, y=500, width=100, height=50)

    rehacer_jugada = Button(ventanaJuego, text="REHACER\n JUGADA", bg="#4af9ff", fg="black",
                             font=("Helvetica", "12", "italic"))
    rehacer_jugada.place(x=450, y=575, width=100, height=50)

    borrar_juego = Button(ventanaJuego, text="BORRAR\n JUEGO", bg="#25b058", fg="black",
                            font=("Helvetica", "12", "italic"))
    borrar_juego.place(x=570, y=500, width=100, height=50)

    top_x = Button(ventanaJuego, text="TOP\n X", bg="#f2f280", fg="black",
                          font=("Helvetica", "12", "italic"))
    top_x.place(x=690, y=500, width=100, height=50)

    guardar_juego = Button(ventanaJuego, text="GUARDAR JUEGO", bg="#d8d9d4", fg="black",
                   font=("Helvetica", "12", "italic"))
    guardar_juego.place(x=350, y=650, width=175, height=30)

    cargar_juego = Button(ventanaJuego, text="CARGAR JUEGO", bg="#d8d9d4", fg="black",
                           font=("Helvetica", "12", "italic"))
    cargar_juego.place(x=550, y=650, width=175, height=30)



######################################
##############GLOBALES################
######################################

matriz = []

textoBotonTeclado = ''

matrizTeclado = []  # Botones con digitos que podemos ingresar en el sudoku

infoBotonTeclado = []

lista_grupos_matriz = [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
                       [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)],
                       [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)],
                       [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)],
                       [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)],
                       [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)],
                       [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)],
                       [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)],
                       [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]]

dificultadPartida = '' # Eleccion de dificultad del juego

#################################### Partidas y eleccion de partida #########################################

partidasFaciles = {
    1: [['2', '5', '7', '4', '', '', '', '6', '9'],
        ['6', '', '1', '2', '', '', '7', '', ''],
        ['', '', '8', '9', '', '', '', '', '5'],
        ['4', '', '', '8', '', '7', '', '2', '1'],
        ['', '', '', '6', '3', '4', '9', '7', '8'],
        ['7', '', '9', '5', '', '2', '4', '', '6'],
        ['', '', '', '', '', '', '', '5', '2'],
        ['', '', '', '', '', '', '1', '9', '7'],
        ['9', '', '', '7', '', '5', '', '', '']],

    2: [['', '6', '', '4', '5', '3', '7', '', ''],
        ['', '', '5', '6', '7', '3', '4', '2', ''],
        ['', '', '4', '', '', '', '', '', '1'],
        ['5', '', '', '7', '', '2', '', '', '4'],
        ['6', '', '9', '', '', '', '2', '5', ''],
        ['8', '', '7', '', '', '9', '', '', '3'],
        ['4', '9', '', '5', '1', '7', '8', '', ''],
        ['2', '1', '', '', '3', '6', '', '', ''],
        ['', '5', '', '', '2', '', '1', '', '']],

    3: [['5', '3', '', '', '7', '', '', '', ''],
        ['6', '', '', '1', '9', '5', '', '', ''],
        ['', '9', '8', '', '', '', '', '6', ''],
        ['8', '', '', '', '6', '', '', '', '3'],
        ['4', '', '', '8', '', '3', '', '', '1'],
        ['7', '', '', '', '2', '', '', '', '6'],
        ['', '6', '', '', '', '', '2', '8', ''],
        ['', '', '', '4', '1', '9', '', '', '5'],
        ['', '', '', '', '8', '', '', '7', '9']]
}

partidasIntermedias = {
    1: [['1', '', '', '4', '', '', '5', '8', ''],
        ['5', '9', '8', '', '', '', '', '3', '7'],
        ['7', '6', '', '', '', '8', '', '', ''],
        ['', '', '', '', '1', '3', '', '6', ''],
        ['9', '', '', '', '', '', '2', '', ''],
        ['', '', '', '', '', '', '7', '9', '1'],
        ['', '', '1', '', '4', '', '', '', ''],
        ['', '', '9', '', '2', '6', '', '', ''],
        ['', '', '6', '8', '9', '1', '', '', '4']],

    2: [['3', '1', '', '5', '6', '', '', '', ''],
        ['6', '', '', '', '', '', '', '3', '9'],
        ['', '', '', '3', '', '2', '5', '', '6'],
        ['', '9', '', '6', '', '1', '', '', '4'],
        ['7', '', '', '', '8', '4', '3', '6', ''],
        ['4', '', '', '2', '', '', '', '', ''],
        ['', '', '', '4', '9', '7', '6', '5', '1'],
        ['', '', '', '', '', '', '', '4', ''],
        ['', '4', '7', '', '', '', '', '9', '']],

    3: [['', '', '', '8', '', '4', '', '', '1'],
        ['', '3', '', '', '2', '', '6', '', '9'],
        ['', '4', '9', '1', '', '3', '', '', '7'],
        ['', '', '5', '7', '', '', '', '', ''],
        ['9', '', '8', '', '', '1', '', '', '4'],
        ['', '6', '', '', '', '9', '', '', ''],
        ['', '', '', '3', '', '2', '', '', ''],
        ['3', '9', '6', '', '', '', '2', '', '8'],
        ['', '8', '', '', '', '', '7', '', '3']]
}

partidasDificiles = {
                    1: [['6', '', '', '', '8', '', '', '', '1'],
                    ['', '3', '', '7', '', '', '6', '', ''],
                    ['', '', '', '', '1', '', '', '', '7'],
                    ['', '5', '', '', '3', '8', '4', '', ''],
                    ['', '', '', '', '4', '', '', '', ''],
                    ['', '', '4', '', '', '', '', '5', '3'],
                    ['', '1', '', '', '', '3', '', '6', ''],
                    ['', '', '3', '9', '', '', '', '8', '5'],
                    ['9', '2', '8', '1', '', '', '3', '', '']],

                    2: [['', '', '', '', '', '9', '', '3', ''],
                    ['3', '', '6', '', '5', '', '', '8', ''],
                    ['7', '', '', '', '', '2', '', '6', ''],
                    ['', '4', '', '', '9', '', '7', '', ''],
                    ['', '3', '9', '', '', '', '', '', ''],
                    ['5', '', '', '', '', '4', '1', '', ''],
                    ['6', '', '', '', '', '5', '2', '', ''],
                    ['', '', '', '', '', '', '', '', ''],
                    ['4', '', '', '8', '', '', '', '7', '']],

                    3: [['', '', '5', '9', '', '', '', '', ''],
                    ['6', '', '', '', '5', '3', '8', '', ''],
                    ['', '', '', '2', '', '', '', '', '3'],
                    ['', '', '', '', '9', '', '', '', ''],
                    ['2', '', '', '', '', '', '', '4', ''],
                    ['', '', '4', '', '8', '5', '', '', '1'],
                    ['', '', '2', '', '4', '1', '', '', '8'],
                    ['', '7', '', '', '', '', '6', '', ''],
                    ['', '', '', '3', '', '', '', '', '']]
}

partida = []


def seleccionDePartida(opcionElegida):
    global partida

    numero = random.randint(1, 3)

    if opcionElegida == 'Facil':
        partida = partidasFaciles[numero]
    elif opcionElegida == 'Intermedio':
        partida = partidasIntermedias[numero]
    else:
        partida = partidasDificiles[numero]



#######################################


ventanaPrincipal = Tk()
ventanaPrincipal.geometry('500x500')
ventanaPrincipal.title('Sudoku')
ventanaPrincipal.configure(bg='#3e97b8')
ventanaPrincipal.resizable(False, False)

labelNombre = Label(ventanaPrincipal, text='Sudoku', fg='white', bg='#3e97b8', font=('Arial', '30', 'bold italic'))
labelNombre.pack(pady=200)

# Menu de la ventana principal
menubar = Menu(ventanaPrincipal)
menubar.add_command(label="Jugar", command=lambda: jugar())  # Opcion jugar
menubar.add_command(label="Configurar", command=lambda: configurar())  # Opcion configurar
menubar.add_command(label="Ayuda", command=lambda: ayuda())  # PDF con el manual
menubar.add_command(label="Acerca de", command=lambda: messagebox.showinfo(title='Acerca de',
                                                                           message='Nombre del programa: Sudoku \n Desarrolladores: Tomás Granados y Pablo Arias \n Version: 1.0 \n Fecha de creacion: Noviembre 2021'))  # Informacion sobre el programa
menubar.add_command(label="Salir", command=ventanaPrincipal.destroy)  # Cerrar ventana
ventanaPrincipal.configure(menu=menubar)

ventanaPrincipal.mainloop()