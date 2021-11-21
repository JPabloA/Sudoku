
# Ejercicio 1 (Extrae digitos)

#E: Dos numeros naturales (El primero debe ser entre 1 y 9, mientras que el segundo debe ser un numero natural de 5 digitos exactos)
#S: Un numero entero o un string , el string solamente en caso de que haya un error.
#D: Retorna una variable conteniendo todos los dígitos del segundo número de entrada que sean iguales a la primer entrada de la funcion.
# En caso de no encontrar el dígito en el número la función retorna -1.

def extrae_digitos(digito, numero):

    # Validaciones
    if (digito < 1 or digito > 9) and (numero < 10000 or numero > 99999):
        return 'ERROR: TANTO EL DIGITO COMO EL NUMERO INGRESADO SON INCORRECTOS, EL DIGITO DEBE SER UN NUMERO NATURAL ENTRE 1 Y 9 Y EL NUMERO DEBE SER NATURAL DE 5 DIGITOS EXACTOS'
    elif digito < 1 or digito > 9:
        return 'ERROR: DIGITO DEBE SER UN NUMERO NATURAL ENTRE 1 Y 9'
    elif numero < 10000 or numero > 99999:
        return 'ERROR: NUMERO DEBE SER NATURAL DE 5 DIGITOS EXACTOS'
    
    # Procesos (desglose del numero)
    unidades = numero % 10
    decenas = (numero // 10) % 10
    centenas = (numero // 100) % 10
    unidadesMil = (numero // 1000) % 10
    decenasMil = numero // 10000
    
    # Proceso para identificar si el digito ingresado en la funcion es igual a algun digito del numero dado e ir formando el resultado
    resultado = 0
    exponente = 0

    if digito == unidades:
        resultado += digito * 10 ** exponente
        exponente += 1
    
    if digito == decenas:
        resultado += digito * 10 ** exponente
        exponente += 1
    
    if digito == centenas:
        resultado += digito * 10 ** exponente
        exponente += 1
    
    if digito == unidadesMil:
        resultado += digito * 10 ** exponente
        exponente += 1
    
    if digito == decenasMil:
        resultado += digito * 10 ** exponente
        exponente += 1
    
    # Retornar resultados de la funcion (Salidas)
    if exponente == 0: 
        return -1
    else:
        return resultado
