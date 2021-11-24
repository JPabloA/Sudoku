# Estudiantes: Tomás Granados y Pablo Arias Navarro

###################################################
# SECCIÓN DE MÓDULOS                              #
###################################################

from tkinter import *
from tkinter import messagebox
from functools import partial
from itertools import product



###################################################
# SECCIÓN DE CLASES                               #
###################################################





###################################################



def jugar():

    global ventanaPrincipal
    global botonUno
    global partida

    ventanaJuego = Toplevel(ventanaPrincipal)
    
    ventanaPrincipal.withdraw()

    
    ventanaJuego.geometry('500x500')
    ventanaJuego.title('Sudoku')
    ventanaJuego.configure(bg='#3e97b8')
    ventanaJuego.resizable(False, False)

    contador = 0
    

    botonUno = Button(ventanaJuego, text='1', width=20, command=lambda: cambiarColor('9'))
    botonUno.place(x=300, y=480)


    def conocerPosicion(i, j):
        global matriz
        global botonApretado
        global botonUno

        textoEnPosicion = matriz[i][j].cget('text')

        if textoEnPosicion == '':
            matriz[i][j].config(text=botonApretado, bg='purple')
            botonUno.config(relief=RAISED, bg='light gray', state='active')
        else:
            messagebox.showwarning('Casilla ocupada', 'Esta casilla no se puede modificar')
    
    def cambiarColor(num):
        global matriz
        global ventanaPrincipal
        global botonUno
        global botonApretado

        botonUno.config(relief=SUNKEN, bg='green', state='disabled')
        botonApretado = botonUno.cget('text')

        ventanaPrincipal.update_idletasks()

    #Creacion de botones   
    for i in range(9):
        fila = []
        for j in range(9):
            contador += 1
            elemento = []
            if partida[i][j] == '':
                boton = Button(ventanaJuego,text='', width=5, command=partial(conocerPosicion, i, j))
            else:
                boton = Button(ventanaJuego,text=partida[i][j], width=5, command=partial(conocerPosicion, i, j))

            if j == 0:
                boton.grid(row=i, column=j,padx=(40,0))

            if i == 0:
                boton.grid(row=i, column=j,pady=(40,0))
            
            if j in [2,5]:
                
                boton.grid(row=i, column=j,padx=(0,5))

            if i in [2,5]:
                boton.grid(row=i, column=j,pady=(0,5))
                
            else:
                boton.grid(row=i, column=j)
                
            
            fila.append(boton)
        matriz.append(fila)
    


######################################
##############GLOBALES################
######################################

matriz = []

botonApretado = ''

partida = [['5', '3', '', '', '7', '', '', '', ''],
          ['6', '', '', '1', '9', '5', '', '', ''],
          ['', '9', '8', '', '', '', '', '6', ''],
          ['8', '', '', '', '6', '', '', '', '3'],
          ['4', '', '', '8', '', '3', '', '', '1'],
          ['7', '', '', '', '2', '', '', '', '6'],
          ['', '6', '', '', '', '', '2', '8', ''],
          ['', '', '', '4', '1', '9', '', '', '5'],
          ['', '', '', '', '8', '', '', '7', '9']
          ]

#######################################


ventanaPrincipal = Tk()
ventanaPrincipal.geometry('500x500')
ventanaPrincipal.title('Sudoku')
ventanaPrincipal.configure(bg='#3e97b8')
ventanaPrincipal.resizable(False, False)

labelNombre = Label( ventanaPrincipal, text='Sudoku', fg='white', bg='#3e97b8', font=('Arial', '30', 'bold italic'))
labelNombre.pack(pady=200)



# Menu de la ventana principal
menubar = Menu(ventanaPrincipal)
menubar.add_command(label="Jugar", command=lambda: jugar()) # Opcion jugar
menubar.add_command(label="Configurar", command=lambda: configurar()) # Opcion configurar
menubar.add_command(label="Ayuda", command=lambda: ayuda()) # PDF con el manual
menubar.add_command(label="Acerca de", command=lambda: messagebox.showinfo(title='Acerca de', message= 'Nombre del programa: Sudoku \n Desarrolladores: Tomás Granados y Pablo Arias \n Version: 1.0 \n Fecha de creacion: Noviembre 2021')) # Informacion sobre el programa
menubar.add_command(label="Salir", command=ventanaPrincipal.destroy) # Cerrar ventana
ventanaPrincipal.configure(menu=menubar)


ventanaPrincipal.mainloop()
