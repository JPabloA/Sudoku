# Estudiantes: Tomás Granados y Pablo Arias Navarro

###################################################
# SECCIÓN DE MÓDULOS                              #
###################################################

from tkinter import *
from tkinter import messagebox


###################################################
# SECCIÓN DE CLASES                               #
###################################################

class Jugar:

    def creaVentana(self):
        ventanaJuego = Tk()
        ventanaJuego.geometry('500x500')
        ventanaJuego.title('Sudoku')
        ventanaJuego.configure(bg='#3e97b8')
        ventanaJuego.resizable(False, False)


###################################################
# SECCIÓN DE FUNCIONES                            #
###################################################


ventanaPrincipal = Tk()
ventanaPrincipal.geometry('500x500')
ventanaPrincipal.title('Sudoku')
ventanaPrincipal.configure(bg='#3e97b8')
ventanaPrincipal.resizable(False, False)

labelNombre = Label( ventanaPrincipal, text='Sudoku', fg='white', bg='#3e97b8', font=('Arial', '30', 'bold italic'))
labelNombre.pack(pady=200)

def jugar():
    pass

def configurar():
    pass

def ayuda():
    pass


# Menu de la ventana principal
menubar = Menu(ventanaPrincipal)
menubar.add_command(label="Jugar", command=lambda: jugar()) # Opcion jugar
menubar.add_command(label="Configurar", command=lambda: configurar()) # Opcion configurar
menubar.add_command(label="Ayuda", command=lambda: ayuda()) # PDF con el manual
menubar.add_command(label="Acerca de", command=lambda: messagebox.showinfo(title='Acerca de', message= 'Nombre del programa: Sudoku \n Desarrolladores: Tomás Granados y Pablo Arias \n Version: 1.0 \n Fecha de creacion: Noviembre 2021')) # Informacion sobre el programa
menubar.add_command(label="Salir", command=ventanaPrincipal.destroy) # Cerrar ventana
ventanaPrincipal.configure(menu=menubar)
ventanaPrincipal.mainloop()


def pintarVerde(boton):
    texto = boton.cget('text')

    if texto != '':
        if int(texto) % 2 == 0:
            boton.configure(bg='green')

from tkinter import *

ventanaPrincipal = Tk()
ventanaPrincipal.geometry('1000x800')
ventanaPrincipal.title('Sudoku')
ventanaPrincipal.configure(bg='#3e97b8')
ventanaPrincipal.resizable(False, False)

contador = 0
matriz = []

# partida número 1
p1 = [[ '5', '3', '', '', '7', '', '', '', '' ],
[ '6', '', '', '1', '9', '5', '', '', '' ],
[ '', '9', '8', '', '', '', '', '6', '' ],
[ '8', '', '', '', '6', '', '', '', '3' ],
[ '4', '', '', '8', '' , '3', '', '', '1' ],
[ '7', '', '', '', '2', '', '', '', '6' ],
[ '', '6', '', '', '', '', '2', '8', '' ],
[ '', '', '', '4', '1', '9', '', '', '5' ],
[ '', '', '', '', '8', '', '', '7', '9' ]
]

for i in range(9):
    fila = []
    for j in range(9):
        contador += 1

        if p1[i][j] == '':
            nombreBoton = 'Boton_'+ str(contador)
            nombreBoton = Button( text='' ,width=10)
        else:
            nombreBoton = 'Boton_' + str(contador)
            nombreBoton = Button(text=p1[i][j], width=10)

        pintarVerde(nombreBoton)
        nombreBoton.grid(row= i,column= j, padx=10, pady=10)
        fila.append(nombreBoton)
    matriz.append(fila)

def cambiarColor (num):
    global matriz
    global ventanaPrincipal
    global p1

    contadorFila = 0

    for fila in matriz:
        contadorColumna = 0
        for boton in fila:
            texto = boton.cget('text')
            if texto == '1':
                boton.configure(text=num, bg ='red')
                p1 [contadorFila][contadorColumna] = num

            contadorColumna += 1

        contadorFila += 1

    ventanaPrincipal.update_idletasks()


botonUno = Button(ventanaPrincipal,text='1', width=20, command=lambda:cambiarColor('9'))
botonUno.place(x=300, y=600)
ventanaPrincipal.mainloop()

botonUno = Button(ventanaPrincipal,text='1', width=20, command=lambda:cambiarColor(matriz))
botonUno.place(x=300, y=600)
ventanaPrincipal.mainloop()

boton1 = Button(ventanaPrincipal, text='1', width=20, command=lambda:cambiarColor('9'))

