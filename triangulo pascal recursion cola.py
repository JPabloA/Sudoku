def triangulo_de_pascal(n):

    if not isinstance(n, int):
        return "ERROR: DEBE DE SER UN NUMERO ENTERO"

    if not n > 0:
        return "ERROR: DEBE SER UN NUMERO ENTERO MAYOR O IGUAL A 1"

    fila = []

    for i in range(n):

        fila.append(())

        for s in range(i + 1):

            if s == 0 or s == i:  # si valor es igual a 0 o el valor inicial (numero)

                fila[i] = fila[i] + (1,)

            else:
                f = fila[i - 1][s] + fila[i - 1][s - 1]  # suma primera posicion con el siguiente valor

                fila[i] = fila[i] + (f,)  # concatena los valores guardados en la lista de fila con el nuevo valor

    return fila

def triangulo_de_pascal_c(n):

    if not isinstance(n, int):
        return "ERROR: DEBE DE SER UN NUMERO ENTERO"

    if not n > 0:
        return "ERROR: DEBE SER UN NUMERO ENTERO MAYOR O IGUAL A 1"

    return triangulo_de_pascal_c_aux(n, [], 0)

def triangulo_de_pascal_c_aux(n,fila,i):

    if n == i:
        return fila

    else:
        fila.append(())
        triangulo_de_pascal_c_aux1(i,fila,0)
        return triangulo_de_pascal_c_aux(n,fila,i+1)
        
def triangulo_de_pascal_c_aux1(i,fila,s):

    if s == i+1:

        return fila

    else:

        if s == 0 or s == i:  # si valor es igual a 0 o el valor inicial (numero)
            
            fila[i] = fila[i] + (1,)

        else:
            f = fila[i - 1][s] + fila[i - 1][s - 1]  # suma primera posicion con el siguiente valor

            fila[i] = fila[i] + (f,)

        return triangulo_de_pascal_c_aux1(i,fila,s+1)

        

        
        
    


    




    

    
