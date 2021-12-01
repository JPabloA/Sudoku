# Estudiantes: Tomás Granados y Pablo Arias Navarro

###################################################
# SECCIÓN DE MÓDULOS                              #
###################################################

from tkinter import *
from tkinter import messagebox
from functools import partial
import random
import pickle
from fpdf import FPDF
import webbrowser
import copy

###################################################
# SECCIÓN DE CLASES                               #
###################################################

# Clase para implementar la funcion de deshacer jugadas
class Jugadas_hechas:
    def __init__(self, fila, columna, elementoAnterior, nuevoElemento):
        self.fila = fila
        self.columna = columna
        self.elementoAnterior = elementoAnterior
        self.nuevoElemento = nuevoElemento

    def obtener_jugada_hecha(self):
        return self.fila, self.columna, self.elementoAnterior, self.nuevoElemento

# Clase para implementar función rehacer jugadas
class Jugadas_eliminadas:
    def __init__(self, fila, columna, elementoAnterior, nuevoElemento):
        self.fila = fila
        self.columna = columna
        self.elementoAnterior = elementoAnterior
        self.nuevoElemento = nuevoElemento

    def obtener_jugada_eliminada(self):
        return self.fila, self.columna, self.elementoAnterior, self.nuevoElemento

# Clase para implementar la opcion de guardar y cargar los datos en el top X
class TopX:
    def __init__(self, dificultad, nombre, horas, minutos, segundos):
        self.dificultad = dificultad
        self.nombre = nombre
        self.horas = horas
        self.minuntos = minutos
        self.segundos = segundos

    def obtener_datos_tiempo(self):
        return self.dificultad, self.nombre,  self.horas,  self.minuntos, self.segundos

##################################################
############ Validaciones Juego ##################
##################################################

def validacionFila(nuevoValor, indiceFila): # Verifica que no haya un elemento igual al que se intenta colocar en la misma fila, en caso de haberlo, pinta en rojo la posicion en donde se encuentra ese elemento igual y muestra un mensaje de error.
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


def validacionColumna(nuevoValor, indiceColumna): # Verifica que no haya un elemento igual al que se intenta colocar en la misma columna, en caso de haberlo, pinta en rojo la posicion en donde se encuentra ese elemento igual y muestra un mensaje de error.
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


def validacionCuadricula(nuevoValor, indiceFila, indiceColumna): # Verifica que no haya un elemento igual al que se intenta colocar en la cuadricula 3x3, en caso de haberlo, pinta en rojo la posicion en donde se encuentra ese elemento igual y muestra un mensaje de error.
    global partida
    global lista_grupos_matriz
    global matriz

    grupo = 0
    for cuadricula in lista_grupos_matriz:
        if (indiceFila, indiceColumna) in cuadricula:
            break
        grupo += 1

    cuadriculaNecesaria = lista_grupos_matriz[
        grupo]  # Lista con posiciones de la cuadricula a la que pertenece la el boton presionado

    for elemento in cuadriculaNecesaria:  # Verifica si existe un numero igual al que se quiere colocar en la cuadricula
        fila = elemento[0]
        columna = elemento[1]

        if partida[fila][columna] == nuevoValor:
            matriz[fila][columna].config(bg='red3')
            messagebox.showwarning('ERROR', 'JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA CUADRÍCULA')
            matriz[fila][columna].config(bg='#f0f0f0')
            return True

    return False


def validacionNombre(): # Valida que se haya colocado un nombre en la casilla de nombre del jugador, esto para que se pueda iniciar la partida, ademas realiza ciertas validaciones que puede tener el nombre.
    global entryNombre

    nombre = entryNombre.get()

    if len(nombre) > 30:
        messagebox.showwarning('CUIDADO', 'EL NOMBRE INGRESADO NO PUEDE EXCEDER LOS 30 CARACTERES')
        return True

    if nombre == '':
        messagebox.showwarning('CUIDADO', 'ANTES DE INICIAR EL JUEGO DEBE DE INGRESAR UN NOMBRE')
        return True

    return False

def validacionElementoBaseCasilla(indiceFila, indiceColumna): # Valida que la casilla que se intenta modificar en la cuadricula del Sudoku no sea una casilla que ya tenia un elemento en esa posicion en la partida cargada.
    global dificultadSeleccionada, numero, partidasFaciles, copia_partida


    if dificultadSeleccionada == 'Facil':
        if copia_partidas_faciles[numero][indiceFila][indiceColumna] != '':
            messagebox.showwarning('CASILLA OCUPADA', 'ESTA CASILLA NO SE PUEDE MODIFICAR')
            return True

    elif dificultadSeleccionada == 'Intermedio':
        if copia_partidas_intermedias[numero][indiceFila][indiceColumna] != '':
            messagebox.showwarning('CASILLA OCUPADA', 'ESTA CASILLA NO SE PUEDE MODIFICAR')
            return True

    elif dificultadSeleccionada == 'Dificil':
        if copia_partidas_dificiles[numero][indiceFila][indiceColumna] != '':
            messagebox.showwarning('CASILLA OCUPADA', 'ESTA CASILLA NO SE PUEDE MODIFICAR')
            return True

    return False


def ganarPartida(): # Verifica si el jugador ha completado el juego, en caso de haberlo completado y tener la opcion de reloj o timer activado, se guarda su tiempo en el Top x dependiendo del tiempo logrado.
    global partida, dificultadSeleccionada, nombre, listaConTiemposTop

    for fila in partida:
        for elemento in fila:
            if elemento == '':
                return False

    if dificultadSeleccionada == 'Facil':
        if timer:
            conversion = tiempoTranscurridoTimer()
            ordenarTiempo((nombre, conversion[0], conversion[1], conversion[2]), listaConTiemposTop[0])
        elif reloj:
            ordenarTiempo((nombre, horas, minutos, segundos), listaConTiemposTop[0])

    elif dificultadSeleccionada == 'Intermedio':
        if timer:
            conversion = tiempoTranscurridoTimer()
            ordenarTiempo((nombre, conversion[0], conversion[1], conversion[2]), listaConTiemposTop[1])
        elif reloj:
            ordenarTiempo((nombre, horas, minutos, segundos), listaConTiemposTop[1])

    elif dificultadSeleccionada == 'Dificil':
        if timer:
            conversion = tiempoTranscurridoTimer()
            ordenarTiempo((nombre, conversion[0], conversion[1], conversion[2]), listaConTiemposTop[2])
        elif reloj:
            ordenarTiempo((nombre, horas, minutos, segundos), listaConTiemposTop[2])

    archivoAGuardar = open('sudoku2021topx.dat', 'wb' )
    pickle.dump(listaConTiemposTop, archivoAGuardar)
    archivoAGuardar.close()

    return True

def timerExpirado(): # Verifica si el timer ha acabado, en caso de que si haya acabado le da la opcion al jugador de seguir con ese juego o de reiniciar la partida.

    global timer,horas, minutos, segundos, c_horas, c_minutos, c_segundos, reloj, ventanaJuego,ventanaPrincipal, eleccionTimerDown
    global c_timer, c_reloj

    if timer == True and horas == 0 and minutos == 0 and segundos == 0:

        respuesta = messagebox.askyesno('TIEMPO EXPIRADO', '¿DESEA CONTINUAR EL MISMO JUEGO (SI O NO)?')

        if respuesta == 0:
            eleccionTimerDown = respuesta
            reseteoDeJuego()
            ventanaJuego.destroy()
            jugar()

            return True

        c_reloj = reloj
        c_timer = timer

        if respuesta == 1:
            eleccionTimerDown = respuesta

            reloj = True
            timer = False

            horas,minutos,segundos = c_horas, c_minutos, c_segundos
            return True

        else:
            return False

#############################################################################################
######################################CONFIGURACION##########################################
############################################################################################

#                                    FUNCIONES RELOJ
#############################################################################################

def cargarTopX(): # Carga a la lista el top actual
    global listaConTiemposTop
    try:
        archivoAAbrir = open('sudoku2021topx.dat', 'rb')
        listaConTiemposTop = pickle.load(archivoAAbrir)
        archivoAAbrir.close()
    except:
        pass

def ordenarTiempo(nuevoTiempo, listaConTiempos): # Ordena el tiempo de menor a mayor
    horasNT = nuevoTiempo[1]
    minutosNT = nuevoTiempo[2]
    segundosNT = nuevoTiempo[3]

    for indiceTiempoActual in range(len(listaConTiempos)):

        tiempoActual = listaConTiempos[indiceTiempoActual]
        horasTA = tiempoActual[1]
        minutosTA = tiempoActual[2]
        segundosTA = tiempoActual[3]

        if horasNT < horasTA:
            listaConTiempos.insert(indiceTiempoActual, nuevoTiempo)
            return
        elif horasNT == horasTA and minutosNT < minutosTA:
            listaConTiempos.insert(indiceTiempoActual, nuevoTiempo)
            return
        elif horasNT == horasTA and minutosNT == minutosTA and segundosNT < segundosTA:
            listaConTiempos.insert(indiceTiempoActual, nuevoTiempo)
            return

    listaConTiempos.append(nuevoTiempo)

def tiempoTranscurridoTimer(): # Determina el tiempo en caso de usar timer y que entre a el top x
    global horas, minutos, segundos, c_horas, c_minutos, c_segundos

    horasTranscurridas = c_horas - horas
    minutosTranscurridos = c_minutos - minutos
    segundosTranscurridos = c_segundos - segundos

    return (horasTranscurridas, minutosTranscurridos, segundosTranscurridos)

def reset_reloj():  # Devuelve el reloj a 0

    global timer_label
    global update_time
    global horas
    global minutos
    global segundos

    horas, minutos, segundos = 0, 0, 0

    timer_label.config(text='00:00:00')


def pausar_reloj():  # Pausa el reloj

    global timer_label
    global update_time

    timer_label.after_cancel(update_time)


def update_timer():  # Refresca y disminuye el timer cada segundo

    global horas
    global minutos
    global segundos
    global v_jugar
    global timer_label

    flag = False

    if timerExpirado():
        flag = True

    if flag:
        update_reloj()
        return

    if segundos == 0 and minutos != 0:
        minutos -= 1
        segundos = 60

    if segundos == 0 and minutos == 0:
        segundos = 60

    if minutos == 0 and horas != 0:
        horas -= 1
        minutos = 59

    segundos -= 1

    str_horas = f'{horas}' if horas > 9 else f'0{horas}'
    str_minutos = f'{minutos}' if minutos > 9 else f'0{minutos}'
    str_segundos = f'{segundos}' if segundos > 9 else f'0{segundos}'

    timer_label = Label(ventanaJuego, text=str_horas + ":" + str_minutos + ":" + str_segundos,
                        font=('Arial', 40, "bold italic"), bg='#3e97b8')
    timer_label.place(x=50, y=550)

    global update_time
    update_time = timer_label.after(1000, update_timer)


def update_reloj():  # Refresca y aumenta el reloj cada segundo

    global horas
    global minutos
    global segundos
    global v_jugar
    global timer_label

    if eleccionTimerDown == 0: # Se retorna para que no se siga llamando a si misma
        return

    segundos += 1

    if segundos == 60:
        minutos += 1
        segundos = 0

    if minutos == 60:
        horas += 1
        minutos = 0

    str_horas = f'{horas}' if horas > 9 else f'0{horas}'
    str_minutos = f'{minutos}' if minutos > 9 else f'0{minutos}'
    str_segundos = f'{segundos}' if segundos > 9 else f'0{segundos}'

    timer_label = Label(ventanaJuego, text=str_horas + ":" + str_minutos + ":" + str_segundos,
                        font=('Arial', 40, "bold italic"), bg='#3e97b8')
    timer_label.place(x=50, y=550)


    global update_time
    update_time = timer_label.after(1000, update_reloj)


def set_reloj():  # Muestra el reloj en la interfaz antes de iniciar

    global horas
    global minutos
    global segundos
    global timer_label

    str_horas = f'{horas}' if horas > 9 else f'0{horas}'
    str_minutos = f'{minutos}' if minutos > 9 else f'0{minutos}'
    str_segundos = f'{segundos}' if segundos > 9 else f'0{segundos}'

    timer_label = Label(ventanaJuego, text=str_horas + ":" + str_minutos + ":" + str_segundos,
                        font=('Arial', "40", "bold italic"), bg='#3e97b8').place(x=50, y=550)


###################################################################################################
###################################################################################################

############################### CONVERSIONES PARA EL ALMACENAMIENTO DE LOS DATOS #########################

# De objeto a binario

def objetoABinarioHechas(objeto):

    elemento = objeto.obtener_jugada_hecha()
    return elemento

def objetoABinarioEliminadas(objeto):

    elemento = objeto.obtener_jugada_eliminada()
    return elemento

def objetoABinarioTop(objeto):

    elemento = objeto.obtener_datos_tiempo()
    return elemento


# De binario objeto

def binarioAObjetoHechas(elemento):

    objeto = Jugadas_hechas(elemento[0], elemento[1], elemento[2], elemento[3])
    return objeto


def binarioAObjetoEliminadas(elemento):

    objeto = Jugadas_eliminadas(elemento[0], elemento[1], elemento[2], elemento[3])
    return objeto

def binarioAObjetoTop(elemento):
    objeto = TopX(elemento[0], elemento[1], elemento[2], elemento[3], elemento[4])
    return objeto

########################################################################################################################

def guardar_juego(): # Almacena los datos actuales de la partida en un archivo .dat

    global timer, reloj, pilaJugadasHechas, pilaJugadasEliminadas,horas,minutos,segundos,c_horas,c_minutos, c_segundos
    global dificultadSeleccionada, cantidadjugadasTopX, configElementos, nombre, partida, numero

    nombre_g = nombre

    pilaJugadasHechas_g = []
    for objeto in pilaJugadasHechas:
        pilaJugadasHechas_g.append(objetoABinarioHechas(objeto))

    pilaJugadasEliminadas_g = []
    for objeto in pilaJugadasEliminadas:
        pilaJugadasEliminadas_g.append(objetoABinarioEliminadas(objeto))

    horas_g = horas
    minutos_g = minutos
    segundos_g = segundos

    c_horas_g = c_horas
    c_minutos_g = c_minutos
    c_segundos_g = c_segundos

    dificultadSeleccionada_g = dificultadSeleccionada

    cantidadjugadasTopX_g = cantidadjugadasTopX

    configElementos_g = configElementos

    partida_g = partida

    tipo_reloj = 0

    numero_g = numero

    if reloj:
        tipo_reloj = 1

    elif timer:
        tipo_reloj = 2

    #Listas a guardar

    lista_pilas = [pilaJugadasHechas_g,pilaJugadasEliminadas_g]

    lista_reloj = [horas_g,minutos_g,segundos_g]

    lista_base_reloj = [c_horas_g,c_minutos_g,c_segundos_g]

    lista_con_todo = [nombre_g, lista_pilas, lista_reloj, lista_base_reloj, dificultadSeleccionada_g, cantidadjugadasTopX_g,
                      configElementos_g, tipo_reloj, partida_g, numero_g]


    archivo = open('sudoku2021juegoactual.dat','wb')
    pickle.dump(lista_con_todo, archivo)
    archivo.close()
    messagebox.showinfo("GUARDAR", "PARTIDA GUARDADA")


def cargar_juego(): # Carga los datos guardados a la partida actual

    global timer, reloj, pilaJugadasHechas, pilaJugadasEliminadas, horas, minutos, segundos, c_horas, c_minutos, c_segundos, flagCargarJuego
    global dificultadSeleccionada, cantidadjugadasTopX, configElementos, nombre, entryNombre, partida, ventanaJuego, opcionIniciarJuego, numero

    archivo = open('sudoku2021juegoactual.dat','rb')

    reseteoDeJuego()

    lista_con_todo = pickle.load(archivo)

    partida = lista_con_todo[8]

    if lista_con_todo[7] == 1:
        reloj = True
        timer = False

    if lista_con_todo[7] == 2:
        timer = True
        reloj = False

    nombre = lista_con_todo[0]

    pilaJugadasHechas = []
    for elemento in lista_con_todo[1][0]:
        pilaJugadasHechas.append(binarioAObjetoHechas(elemento))

    pilaJugadasEliminadas = []
    for elemento in lista_con_todo[1][1]:
        pilaJugadasEliminadas.append(binarioAObjetoEliminadas(elemento))

    horas = lista_con_todo[2][0]
    minutos = lista_con_todo[2][1]
    segundos = lista_con_todo[2][2]

    c_horas = lista_con_todo[3][0]
    c_minutos = lista_con_todo[3][1]
    c_segundos = lista_con_todo[3][2]

    dificultadSeleccionada = lista_con_todo[4]

    cantidadjugadasTopX = lista_con_todo[5]

    configElementos = lista_con_todo[6]

    numero = lista_con_todo[9]

    entryNombre.delete(0,END)

    entryNombre.insert(0,nombre)

    flagCargarJuego = True


    ventanaJuego.destroy()
    jugar()
    entryNombre.delete(0, END)
    entryNombre.insert(0, nombre)
    archivo.close()

def mostrarTopX(): # Muestra y crea la lista en formato '.pdf' del top X, dependiendo de la cantidad de jugadores a mostrar seleccionado en la configuracion del juego.

    global listaConTiemposTop, cantidadjugadasTopX

    pdf = FPDF('P', 'mm', 'a4')
    pdf.add_page()
    pdf.set_font('Arial', size=14)
    pdf.cell(120, 8, txt='Top X', ln=True)
    pdf.cell(120, 8, ln=True)

    pdf.cell(120, 8, txt='Dificil', ln=True)
    pdf.cell(w=75, h=15, txt='Jugador', border=1, align='C', fill=0)
    pdf.multi_cell(w=0, h=15, txt='Tiempo', border=1, align='C', fill=0)

    contador = 0
    for datosTiempoJugador in listaConTiemposTop[2]:
        if contador == cantidadjugadasTopX and cantidadjugadasTopX != 0:
            break

        str_horas = f'{datosTiempoJugador[1]}' if datosTiempoJugador[1] > 9 else f'0{datosTiempoJugador[1]}'
        str_minutos = f'{datosTiempoJugador[2]}' if datosTiempoJugador[2] > 9 else f'0{datosTiempoJugador[2]}'
        str_segundos = f'{datosTiempoJugador[3]}' if datosTiempoJugador[3] > 9 else f'0{datosTiempoJugador[3]}'

        pdf.cell(w=75, h=15, txt=datosTiempoJugador[0], border=1, align='C', fill=0)
        tiempoResultado = str_horas + ":" + str_minutos + ":" + str_segundos
        pdf.multi_cell(w=0, h=15, txt= tiempoResultado, border=1, align='C', fill=0)
        contador += 1

    pdf.cell(120, 8, ln=True)
    pdf.cell(120, 8, txt='Intermedio', ln=True)
    pdf.cell(w=75, h=15, txt='Jugador', border=1, align='C', fill=0)
    pdf.multi_cell(w=0, h=15, txt='Tiempo', border=1, align='C', fill=0)

    contador = 0
    for datosTiempoJugador in listaConTiemposTop[1]:
        if contador == cantidadjugadasTopX and cantidadjugadasTopX != 0:
            break

        str_horas = f'{datosTiempoJugador[1]}' if datosTiempoJugador[1] > 9 else f'0{datosTiempoJugador[1]}'
        str_minutos = f'{datosTiempoJugador[2]}' if datosTiempoJugador[2] > 9 else f'0{datosTiempoJugador[2]}'
        str_segundos = f'{datosTiempoJugador[3]}' if datosTiempoJugador[3] > 9 else f'0{datosTiempoJugador[3]}'

        pdf.cell(w=75, h=15, txt=datosTiempoJugador[0], border=1, align='C', fill=0)
        tiempoResultado = str_horas + ":" + str_minutos + ":" + str_segundos
        pdf.multi_cell(w=0, h=15, txt= tiempoResultado, border=1, align='C', fill=0)
        contador += 1

    pdf.cell(120, 8, ln=True)
    pdf.cell(120, 8, txt='Facil', ln=True)
    pdf.cell(w=75, h=15, txt='Jugador', border=1, align='C', fill=0)
    pdf.multi_cell(w=0, h=15, txt='Tiempo', border=1, align='C', fill=0)

    contador = 0
    for datosTiempoJugador in listaConTiemposTop[0]:
        if contador == cantidadjugadasTopX and cantidadjugadasTopX != 0:
            break

        str_horas = f'{datosTiempoJugador[1]}' if datosTiempoJugador[1] > 9 else f'0{datosTiempoJugador[1]}'
        str_minutos = f'{datosTiempoJugador[2]}' if datosTiempoJugador[2] > 9 else f'0{datosTiempoJugador[2]}'
        str_segundos = f'{datosTiempoJugador[3]}' if datosTiempoJugador[3] > 9 else f'0{datosTiempoJugador[3]}'

        pdf.cell(w=75, h=15, txt=datosTiempoJugador[0], border=1, align='C', fill=0)
        tiempoResultado = str_horas + ":" + str_minutos + ":" + str_segundos
        pdf.multi_cell(w=0, h=15, txt=tiempoResultado, border=1, align='C', fill=0)
        contador += 1

    pdf.output('TopX.pdf')
    webbrowser.open_new('TopX.pdf')

def configurar(): # Ventana de selección de configuración para el usuario
    global horas
    global minutos
    global segundos
    global ventanaPrincipal
    global ventanaConfig
    global timer
    global reloj
    global cantidadjugadasTopX

    ventanaPrincipal.withdraw()

    ventanaConfig = Toplevel(ventanaPrincipal)

    ventanaConfig.title("Configuración")
    ventanaConfig.config(bg='#3e97b8')
    ventanaConfig.geometry("800x800")
    ventanaConfig.resizable(False, False)

    # Nivel de dificultad
    nivel = Label(ventanaConfig, text="Nivel:", bg='#3e97b8', borderwidth=4,
                  font=("Helvetica", "19", "bold italic")).place(x=20, y=30)

    optionValueDificultad = StringVar()
    optionValueDificultad.set('Facil')

    opcionFacil = Radiobutton(ventanaConfig,
                              text="Facil",
                              padx=20,
                              variable=optionValueDificultad, value='Facil',
                              bg="#3e97b8",
                              font=("Helvetica", "15", "italic"),
                              activebackground='#3e97b8',command=lambda: verificarReloj(optionValueReloj.get(),optionValueDificultad.get())).place(x=60, y=80)

    opcionIntermedia = Radiobutton(ventanaConfig,
                                   text="Intermedia",
                                   padx=20,
                                   variable=optionValueDificultad, value='Intermedio',
                                   bg="#3e97b8",
                                   font=("Helvetica", "15", "italic"),
                                   activebackground='#3e97b8',command=lambda: verificarReloj(optionValueReloj.get(),optionValueDificultad.get())).place(x=60, y=120)

    opcionDificil = Radiobutton(ventanaConfig,
                                text="Dificil",
                                padx=20,
                                variable=optionValueDificultad, value='Dificil',
                                bg="#3e97b8",
                                font=("Helvetica", "15", "italic"),
                                activebackground='#3e97b8',command=lambda: verificarReloj(optionValueReloj.get(),optionValueDificultad.get())).place(x=60, y=160)

    # Timer o reloj

    labelReloj = Label(ventanaConfig, text='Reloj:', bg='#3e97b8', font=("Helvetica", "20", "bold italic")).place(x=20,
                                                                                                                  y=220)

    optionValueReloj = IntVar()
    optionValueReloj.set(1)

    opcionSiReloj = Radiobutton(ventanaConfig,
                                text="Si",
                                padx=20,
                                variable=optionValueReloj, value=1,
                                bg="#3e97b8",
                                font=("Helvetica", "15", "italic"),
                                activebackground='#3e97b8',
                                command=lambda: verificarReloj(optionValueReloj.get(),optionValueDificultad.get())
                                ).place(x=60, y=270)

    opcionNoReloj = Radiobutton(ventanaConfig,
                                text="No",
                                padx=20,
                                variable=optionValueReloj, value=2,
                                bg="#3e97b8",
                                font=("Helvetica", "15", "italic"),
                                activebackground='#3e97b8',
                                command=lambda: verificarReloj(optionValueReloj.get(),optionValueDificultad.get())
                                ).place(x=60, y=310)

    opcionTimer = Radiobutton(ventanaConfig,
                              text="Timer",
                              padx=20,
                              variable=optionValueReloj, value=3,
                              bg="#3e97b8",
                              font=("Helvetica", "15", "italic"),
                              activebackground='#3e97b8',
                              command=lambda: verificarReloj(optionValueReloj.get(),optionValueDificultad.get())
                              ).place(x=60, y=350)

    def verificarReloj(opcionMarcadaReloj,opcionMarcadaDificultad): # Valida los datos ingresados por el usuario en los entries del timer y realiza las recomendaciones de tiempo dependiendo de la dificultad seleccionada

        global timer, reloj, horas, minutos, segundos, c_timer, c_reloj


        if opcionMarcadaReloj == 1:

            horas,minutos,segundos = 0,0,0

            entryHoras.delete(0, END)
            entryMinutos.delete(0, END)
            entrySegundos.delete(0, END)

            reloj = True
            timer = False
            c_reloj = reloj
            c_timer = timer


        if opcionMarcadaReloj == 2:

            entryHoras.delete(0, END)
            entryMinutos.delete(0, END)
            entrySegundos.delete(0, END)

            timer = False
            reloj = False
            c_reloj = reloj
            c_timer = timer


        if opcionMarcadaReloj == 3:
            timer = True
            reloj = False
            c_reloj = reloj
            c_timer = timer

            entrySegundos.config(state=NORMAL, justify=CENTER)
            entryHoras.config(state=NORMAL, justify=CENTER)
            entryMinutos.config(state=NORMAL, justify=CENTER)

            if opcionMarcadaDificultad == 'Facil':

                entryHoras.delete(0,END)
                entryMinutos.delete(0, END)
                entrySegundos.delete(0, END)

                entrySegundos.insert(0, str(0))
                entryMinutos.insert(0, str(30))
                entryHoras.insert(0, str(0))

            if opcionMarcadaDificultad == 'Intermedio':

                entryHoras.delete(0, END)
                entryMinutos.delete(0, END)
                entrySegundos.delete(0, END)

                entrySegundos.insert(0, str(0))
                entryMinutos.insert(0, str(0))
                entryHoras.insert(0,str(1))

            if opcionMarcadaDificultad == 'Dificil':
                entryHoras.delete(0, END)
                entryMinutos.delete(0, END)
                entrySegundos.delete(0, END)

                entrySegundos.insert(0, str(0))
                entryMinutos.insert(0, str(0))
                entryHoras.insert(0, str(2))

        else:
            entrySegundos.config(state=DISABLED)
            entryHoras.config(state=DISABLED)
            entryMinutos.config(state=DISABLED)


    labelHoras = Label(ventanaConfig, text='   Horas  ', font=('Arial', '18'), bg='light gray', borderwidth=2,
                       relief='solid')
    labelHoras.place(x=310, y=250)
    entryHoras = Entry(ventanaConfig, width=8, font=('Arial', '16'), bd=10, borderwidth=4, state=DISABLED)
    entryHoras.place(x=310, y=290)

    labelMinutos = Label(ventanaConfig, text=' Minutos ', font=('Arial', '18'), bg='light gray', borderwidth=2,
                         relief='solid')
    labelMinutos.place(x=450, y=250)
    entryMinutos = Entry(ventanaConfig, width=8, font=('Arial', '16'), borderwidth=4, state=DISABLED)
    entryMinutos.place(x=450, y=290)

    labelSegundos = Label(ventanaConfig, text='Segundos', font=('Arial', '18'), bg='light gray', borderwidth=2,
                          relief='solid')
    labelSegundos.place(x=590, y=250)
    entrySegundos = Entry(ventanaConfig, width=9, font=('Arial', '16'), borderwidth=4, state=DISABLED)
    entrySegundos.place(x=590, y=290)

    # Cantidad de jugadas en el Top X:

    labelTopX = Label(ventanaConfig, text='Cantidad de jugadas desplegadas en el TOP X:', bg='#3e97b8',
                      font=("Helvetica", "18", "bold italic")).place(x=20, y=450)
    entryTopX = Entry(ventanaConfig, width=20, font=('Arial', '16'), bd=10, borderwidth=4)
    entryTopX.insert(0, str(cantidadjugadasTopX))
    entryTopX.place(x=50, y=500)

    # Elementos utilizados en el juego

    labelElementosCuadricula = Label(ventanaConfig, text=' Panel de elementos para llenar la cuadrícula:', bg='#3e97b8',
                                     font=("Helvetica", "18", "bold italic")).place(x=20, y=600)

    optionValueElementoCuadricula = StringVar()
    optionValueElementoCuadricula.set('Numeros')

    opcionNumerosenCuadricula = Radiobutton(ventanaConfig,
                                            text="Números",
                                            padx=20,
                                            variable=optionValueElementoCuadricula, value='Numeros',
                                            bg="#3e97b8",
                                            font=("Helvetica", "15", "italic"),
                                            activebackground='#3e97b8').place(x=80, y=650)

    opcionLetrasenCuadricula = Radiobutton(ventanaConfig,
                                           text="Letras",
                                           padx=20,
                                           variable=optionValueElementoCuadricula, value='Letras',
                                           bg="#3e97b8",
                                           font=("Helvetica", "15", "italic"),
                                           activebackground='#3e97b8').place(x=250, y=650)

    opcionSimbolosenCuadricula = Radiobutton(ventanaConfig,
                                             text="Símbolos",
                                             padx=20,
                                             variable=optionValueElementoCuadricula, value='Simbolos',
                                             bg="#3e97b8",
                                             font=("Helvetica", "15", "italic"),
                                             activebackground='#3e97b8').place(x=400, y=650)

    def guardar_config(): # Almacena los datos seleccionados por el usuario
        global horas, minutos, segundos, ventanaPrincipal, dificultadSeleccionada, cantidadjugadasTopX, configElementos
        global c_horas, c_minutos, c_segundos


        if timer:
            try:
                horas = int(entryHoras.get())
                c_horas = int(entryHoras.get())

                if horas >= 5 or horas < 0:
                    messagebox.showerror("ERROR", "LAS HORAS DEBEN ESTAR ENTRE 0 Y 4")
                    horas = 0
                    return

                minutos = int(entryMinutos.get())
                c_minutos = int(entryMinutos.get())

                if minutos > 59 or minutos < 0:
                    messagebox.showerror("ERROR", "LOS MINUTOS DEBEN SER MENORES QUE 59 Y MAYORES A 0")
                    minutos = 0
                    return

                segundos = int(entrySegundos.get())
                c_segundos = int(entrySegundos.get())


                if segundos > 59 or segundos < 0:
                    messagebox.showerror("ERROR", "LOS SEGUNDOS DEBEN SER MENORES QUE 59 Y MAYORES A 0")
                    segundos = 0
                    return

                if horas == 0 and minutos == 0 and segundos == 0:

                    messagebox.showerror("ERROR", "EL TIEMPO DEBE SER MAYOR A 0 PARA UTILIZAR EL TIMER")
                    return

            except ValueError:
                messagebox.showerror("ERROR","SE DEBE INGRESAR HORAS, MINUTOS, Y SEGUNDOS (NÚMEROS ENTEROS)")
                return

        dificultadSeleccionada = optionValueDificultad.get()


        configElementos = optionValueElementoCuadricula.get()

        try:

            cantidadjugadasTopX = int(entryTopX.get())

            if cantidadjugadasTopX < 0 or cantidadjugadasTopX > 100:

                messagebox.showerror("ERROR", "LA CANTIDAD DE JUGADAS DEBEN ENTRE 0 Y 100")
                return

        except ValueError:
            messagebox.showerror("ERROR", "LA CANTIDAD DE JUGADAS DEBE SER UN NUMERO ENTERO")
            return

        messagebox.showinfo('GUARDADO','LOS DATOS HAN SIDO GUARDADOS EXITOSAMENTE')

        ventanaPrincipal.deiconify()
        ventanaConfig.destroy()


    guardarConfig = Button(ventanaConfig, text="GUARDAR", bg="#6cdde0", fg="black",
                           font=("Helvetica", "14", "bold italic"), command=lambda: guardar_config()).place(x=600, y=700,
                                                                                                            width=120,
                                                                                                            height=60)

def reseteoDeJuego(): # Reinicia todas las variables de juego para poder empezar uno nuevo

    global matriz, textoBotonTeclado, matrizTeclado, partida, pilaJugadasHechas, pilaJugadasEliminadas
    global horas, minutos,segundos, c_horas, c_minutos, c_segundos, timer, reloj

    matriz = []

    textoBotonTeclado = ''

    matrizTeclado = []

    seleccionDePartida()

    pilaJugadasHechas = []

    pilaJugadasEliminadas = []


    horas, minutos, segundos = c_horas, c_minutos, c_segundos


def jugar(): # Ventena con interfaz principal de juego
    global ventanaPrincipal, guardar_juego
    global botonUno
    global partida
    global matrizTeclado
    global entryNombre
    global ventanaJuego
    global entryNombre
    global nombre, opcionIniciarJuego, dificultadSeleccionada

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

    nivel = Label(ventanaJuego, text='Nivel: ', fg='White', borderwidth=3, bg='#3e97b8',
                          font=('Arial', '18', 'bold italic'))
    nivel.place(x=80, y=640)

    dificultad = Label(ventanaJuego, text=dificultadSeleccionada, fg='White', borderwidth=3, bg='#3e97b8',
                          font=('Arial', '18', 'bold italic'))
    dificultad.place(x=150, y=640)

    entryNombre = Entry(ventanaJuego, width=40)
    entryNombre.place(x=510, y=130)

    actualizarListaDeJuego()
    cargarTopX()

    def updateGUI(i, j): # Muestra los cambios en el tablero cada vez que el usuario realiza una jugada
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

        listaValidaciones.append(validacionElementoBaseCasilla(i, j))

        if True in listaValidaciones:  # Verifica si el numero no se puede colocar
            return

        if infoBotonTeclado != []:
            matriz[i][j].config(text=textoBotonTeclado)
            matrizTeclado[infoBotonTeclado[0]][infoBotonTeclado[1]].config(relief=RAISED, bg='#21dec8',
                                                                           state='active')
            partida[i][j] = textoBotonTeclado
            infoBotonTeclado = []

            jugadaActual = Jugadas_hechas(i, j, textoEnPosicion, textoBotonTeclado)
            pilaJugadasHechas.append(jugadaActual)

        guardar_juego_boton.config(state='active', relief=RAISED, activebackground="#d8d9d4")
        borrar_juego.config(state='active', relief=RAISED, activebackground="#25b058")

        if pilaJugadasHechas != []:
            deshacer_jugada.config(relief=RAISED, state='active', activebackground='#4af9ff')

        if ganarPartida():
            messagebox.showinfo('JUEGO COMPLETADO', '¡EXCELENTE! JUEGO COMPLETADO')

            ventanaJuego.destroy()
            reseteoDeJuego()
            jugar()


    def procesoSeleccionBotonesTeclado(): # Selecciona una tecla con el elemento que se quiera colocar en el tablero
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
            boton = Button(ventanaJuego, text='', bg='#f0f0f0', width=4, height=2, font=('Arial', '10'),
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

    def extraerInfoTecla(fila, columna): # Extrae la ubicación del botón para identificarlo
        global infoBotonTeclado, timer, reloj

        infoBotonTeclado = [fila, columna]
        procesoSeleccionBotonesTeclado()

    # Se crea la matriz con los botones que poseen los numeros que se pueden ingresar al sudoku

    contadorNumero = 0
    y = 200

    for fila in range(3):
        x = 530
        filaBotones = []
        for columna in range(3):
            boton = Button(ventanaJuego, text=listaCaracteresElegidos[contadorNumero],
                           width=5, height=2, bg='#21dec8', state='disabled', activebackground='#21dec8',
                           command=partial(extraerInfoTecla, fila, columna))
            boton.place(x=x, y=y)
            x += 70
            contadorNumero += 1

            filaBotones.append(boton)

        y += 60
        matrizTeclado.append(filaBotones)

    if timer or reloj:
        set_reloj()



    ################################### Config Botones (Opciones) ########################################

    def opcionIniciarJuego(): # Función de iniciar el tablero
        global matriz
        global matrizTeclado
        global copia_partida
        global nombre
        global flagCargarJuego


        if validacionNombre():
            return

        entryNombre.config(state='disabled')

        if pilaJugadasHechas != []:
            deshacer_jugada.config(relief=RAISED, state='active', activebackground='#4af9ff')

        if pilaJugadasEliminadas != []:
            rehacer_jugada.config(relief=RAISED, state='active', activebackground='#4af9ff')

        if not flagCargarJuego:
            seleccionDePartida()

        cargar_juego_boton.config(relief=SUNKEN, state='disabled')

        if listaCaracteresElegidos != defaultList:
            modificaMatriz(partida, listaCaracteresElegidos, defaultList)


        # Actualiza la cuadricula con la partida seleccionada al azar
        for i in range(9):

            for j in range(9):
                botonActual = matriz[i][j]
                textoEliminar = botonActual.cget('text')

                if partida[i][j] != '':
                    botonActual.config(text=partida[i][j])

        iniciar_juego.config(state='disabled', relief=SUNKEN)

        # Activa los botones con los digitos que se pueden ingresar en el juego
        for fila in range(3):
            for columna in range(3):
                matrizTeclado[fila][columna].config(state='active')

        validacionNombre()

        terminar_juego.config(relief=RAISED, state='active', activebackground="#96027e")

        if flagCargarJuego:
            borrar_juego.config(relief=RAISED, state='active', activebackground="#25b058")

        nombre = str(entryNombre.get())

        if timer:
            update_timer()

        if reloj:
            update_reloj()

    def opcionTerminarJuego(): # Termina la partida actual y resetea todos los cambios hechos en las variables utilzadas.
        global reloj, timer, c_reloj, c_timer
        global matriz, partida

        respuesta = messagebox.askyesno('TERMINAR JUEGO','¿ESTÁ SEGURO DE TERMINAR EL JUEGO?')

        if respuesta == 1:
            reloj = c_reloj
            timer = c_timer
            reseteoDeJuego()
            ventanaJuego.destroy()
            jugar()

    def undo(): # Elimina la ultima jugada hecha en el tablero, ademas, modifica las pilas para ir guardando y eliminando las jugadas hechas en caso de querer rehacer el cambio.
        global pilaJugadasHechas, pilaJugadasEliminadas, matriz, partida

        if pilaJugadasHechas == []:  # Modificacion aqui
            messagebox.showwarning('ERROR', 'NO HAY JUGADAS PARA DESHACER')
        else:

            ultimaJugadaObjeto = pilaJugadasHechas.pop()

            jugadaAAgregar = Jugadas_eliminadas(ultimaJugadaObjeto.fila, ultimaJugadaObjeto.columna,
                                                ultimaJugadaObjeto.elementoAnterior, ultimaJugadaObjeto.nuevoElemento)
            pilaJugadasEliminadas.append(jugadaAAgregar)

            ultimaJugadaLista = ultimaJugadaObjeto.obtener_jugada_hecha()


            fila = ultimaJugadaLista[0]
            columna = ultimaJugadaLista[1]
            elemento = ultimaJugadaLista[2]

            for indiceFila in range(9):
                for indiceColumna in range(9):
                    if fila == indiceFila and columna == indiceColumna:
                        matriz[fila][columna].config(text=elemento)
                        partida[fila][columna] = elemento

            rehacer_jugada.config(state='active', relief=RAISED, activebackground="#4af9ff")

    def redo(): # Rehace la ultima jugada eliminada con deshacer, ademas, modifica las pilas para ir guardando y eliminando las jugadas eliminadas en caso de querer deshacer el cambio.
        global matriz, partida, pilaJugadasEliminadas, pilaJugadasHechas, textoBotonTeclado

        if pilaJugadasEliminadas == []:
            messagebox.showwarning('ERROR', 'NO HAY JUGADAS PARA REHACER')
        else:
            ultimaJugadaObjeto = pilaJugadasEliminadas.pop()

            jugadaAAgregar = Jugadas_hechas(ultimaJugadaObjeto.fila, ultimaJugadaObjeto.columna,
                                            ultimaJugadaObjeto.elementoAnterior, ultimaJugadaObjeto.nuevoElemento)
            pilaJugadasHechas.append(jugadaAAgregar)

            ultimaJugadaLista = ultimaJugadaObjeto.obtener_jugada_eliminada()

            fila = ultimaJugadaLista[0]
            columna = ultimaJugadaLista[1]
            elemento = ultimaJugadaLista[-1]

            for indiceFila in range(9):
                for indiceColumna in range(9):
                    if fila == indiceFila and columna == indiceColumna:
                        matriz[fila][columna].config(text=elemento)
                        partida[fila][columna] = elemento


    def opcionBorrar(): # Borra todos los movimientos que se han hecho en la partida que se esta jugando
        global pilaJugadasHechas, pilaJugadasEliminadas

        respuesta = messagebox.askyesno('Borrar', '¿ESTÁ SEGURO DE BORRAR EL JUEGO (SI o NO)?')

        if respuesta == 1:
            while pilaJugadasHechas != []:
                undo()

            rehacer_jugada.config(relief=SUNKEN, state='disabled')
            borrar_juego.config(relief=SUNKEN, state='disabled')
        else:
            return

        pilaJugadasHechas = []
        pilaJugadasEliminadas = []


    # Botones de funciones del juego

    iniciar_juego = Button(ventanaJuego, text="INICIAR\n JUEGO", bg="#ff7438", fg="black",
                           font=("Helvetica", "12", "italic"), command=opcionIniciarJuego)
    iniciar_juego.place(x=330, y=500, width=100, height=50)

    deshacer_jugada = Button(ventanaJuego, text="DESHACER\n JUGADA", bg="#4af9ff", fg="black", state='disabled',
                             relief=SUNKEN,
                             font=("Helvetica", "12", "italic"), command=undo)
    deshacer_jugada.place(x=450, y=500, width=100, height=50)

    rehacer_jugada = Button(ventanaJuego, text="REHACER\n JUGADA", state='disabled', relief=SUNKEN, bg="#4af9ff",
                            fg="black",
                            font=("Helvetica", "12", "italic"), command=redo)
    rehacer_jugada.place(x=450, y=575, width=100, height=50)

    borrar_juego = Button(ventanaJuego, text="BORRAR\n JUEGO", bg="#25b058", fg="black", state='disabled', relief=SUNKEN,
                          font=("Helvetica", "12", "italic"), command= opcionBorrar)
    borrar_juego.place(x=570, y=500, width=100, height=50)

    terminar_juego = Button(ventanaJuego, text="TERMINAR\n JUEGO", bg="#96027e", fg="black", state='disabled', relief=SUNKEN,
                          font=("Helvetica", "12", "italic"),command=opcionTerminarJuego)
    terminar_juego.place(x=570, y=575, width=100, height=50)

    top_x = Button(ventanaJuego, text="TOP\n X", bg="#f2f280", fg="black",
                   font=("Helvetica", "12", "italic"), command=mostrarTopX)
    top_x.place(x=690, y=500, width=100, height=50)

    guardar_juego_boton = Button(ventanaJuego, text="GUARDAR JUEGO", bg="#d8d9d4", fg="black", state='disabled', relief=SUNKEN,
                           font=("Helvetica", "12", "italic"), command=guardar_juego)
    guardar_juego_boton.place(x=350, y=650, width=175, height=30)

    cargar_juego_boton = Button(ventanaJuego, text="CARGAR JUEGO", bg="#d8d9d4", fg="black",
                          font=("Helvetica", "12", "italic"),command=cargar_juego)
    cargar_juego_boton.place(x=550, y=650, width=175, height=30)

def ayuda(): # Abre el manual de usuario del programa

    webbrowser.open_new('manual_de_usuario_sudoku.pdf')

######################################
##############FLAGS###################
######################################

flagCargarJuego = False

timer = False
reloj = True

c_reloj = reloj
c_timer = timer

reloj_reseteado = False


######################################
##############GLOBALES################
######################################

pilaJugadasHechas = []

pilaJugadasEliminadas = []

listaConTiemposTop = [[], [], []] #Orden: Dificil, Intermedio, Facil

# Variables para el reloj o timer
horas = 0
minutos = 0
segundos = 0

# Copias de las variables del reloj o timer
c_horas = 0
c_minutos = 0
c_segundos = 0


dificultadSeleccionada = 'Facil' # Guarda la dificultad seleccionada por el usuario en configuracion (Por default: La dificultad es facil)

cantidadjugadasTopX = 0 # Cantidad de jugadores que se quieren mostrar en el top

configElementos = '' # Guarda la opcion de elementos para jugar marcada por el usuario (Numeros, letras, simbolos)

eleccionTimerDown = 50 # Guarda la eleccion del usuario (Con respecto a que si quiere utilizar timer o no)

matriz = [] # Matriz que guarda los botones de la cuadricula en donde se juega

textoBotonTeclado = '' # Guarda el caracter que se quiere ingresar en el tablero de juego

matrizTeclado = []  # Botones con digitos que podemos ingresar en el sudoku

infoBotonTeclado = [] # Guarda la informacion sobre el caracter que se quiere colocar en el tablero de juego

lista_grupos_matriz = [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
                       [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)],
                       [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)],
                       [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)],
                       [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)],
                       [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)],
                       [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)],
                       [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)],
                       [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]]

dificultadPartida = ''  # Eleccion de dificultad del juego

#################################### Partidas y eleccion de partida #########################################

# Listas con los diferentes grupos de caracteres con los que se puede jugar al Sudoku.
listaLetras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
defaultList = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
listaSimbolos = ['*', '+', '=', '@', '$', '&', '!', '?', '#']
listaCaracteresElegidos = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

# Utilizados para la seleccion de una partida
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

# Copias de las partidas (Se utiliza para conocer los elementos base de la partida seleccionada)

copia_partidas_faciles = {
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

copia_partidas_intermedias = {
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

copia_partidas_dificiles = {
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

partida = [['2', '5', '7', '4', '2', '2', '2', '6', '9'], # Partida rapida en caso de querer ganar
        ['6', '2', '1', '2', '2', '2', '7', '2', '2'],
        ['2', '2', '8', '9', '2', '2', '2', '2', '5'],
        ['4', '2', '2', '8', '2', '7', '2', '2', '1'],
        ['2', '2', '2', '6', '3', '4', '9', '7', '8'],
        ['7', '2', '9', '5', '2', '2', '4', '2', '6'],
        ['2', '2', '2', '2', '2', '2', '2', '5', '2'],
        ['2', '2', '2', '2', '2', '2', '1', '9', '7'],
        ['9', '2', '2', '7', '2', '5', '2', '2', '']]



def seleccionDePartida(): # Crea un numero random para escoger una partida guardada en el diccionario de partidas depenediendo de la dificultad seleccionada por el usuario.
    global partida, dificultadSeleccionada, numero

    numero = random.randint(1, 3)

    if dificultadSeleccionada == 'Facil':
        partida = copy.deepcopy(partidasFaciles[numero])
    elif dificultadSeleccionada == 'Intermedio':
        partida = copy.deepcopy(partidasIntermedias[numero])
    else:
        partida = copy.deepcopy(partidasDificiles[numero])


def modificaMatriz(partida, listaNueva, defaultList): # Modifica los elementos de la matriz seleccionada como partida (Se encarga de pasar la matriz de numeros a simbolos o a letras y viceversa)
    for elemento in range(9):
        for fila in range(9):
            for columna in range(9):
                elementoActualM = partida[fila][columna]
                if elementoActualM == defaultList[elemento]:
                    partida[fila][columna] = listaNueva[elemento]

    return partida


def actualizarListaDeJuego(): # Actualiza la lista de caracteres que se utilizaran en la partida a jugar (Esto para posteriormente modificar la matriz en caso de que se haya elegido una opcion que no fueran numeros en la configuracion)
    global listaCaracteresElegidos, defaultList, listaLetras, listaSimbolos, configElementos

    if configElementos == 'Numeros':
        listaCaracteresElegidos = defaultList
    elif configElementos == 'Letras':
        listaCaracteresElegidos = listaLetras
    elif configElementos == 'Simbolos':
        listaCaracteresElegidos = listaSimbolos

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