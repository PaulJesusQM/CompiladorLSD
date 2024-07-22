###########################################################################
############         GENERACION DE CODIGO OBJETO         ##################

def generar_codigo(entrada):
    lineas = entrada.splitlines()
    
    # BUSCO LA LINEA DONDE APAREZCA BPM
    bpm = None
    for linea in lineas:
        if 'BPM' in linea:
            # DIVIDIR EN PALABRAS
            palabras = linea.split()
            for i in range(len(palabras)):
                if palabras[i] == 'BPM':
                    bpm = int(palabras[i + 2])  # + 2 SUPONIENDO QUE EL VALOR VA ESTAR A 2 VALORES DE M
    
    if bpm is None:
        print("No se encontró el valor de BPM en la entrada.")
        
    duracion_map = {
        'redonda': 4 * 60 / bpm,
        'blanca': 2 * 60 / bpm,
        'negra': 1 * 60 / bpm,
        'corchea': 0.5 * 60 / bpm,
        'semic': 0.25 * 60 / bpm,
        'fusa': 0.125 * 60 / bpm,
        'semif': 0.0625 * 60 / bpm,
    }
        
    # Dividir la entrada en líneas
    lineas = entrada.splitlines()
    resultado = []
    
    for linea in lineas:
        # SE IGNORA G Y BPM Y COMENTARIOS
        if linea.startswith('G') or 'BPM' in linea or linea.strip().startswith('//'):
            continue
        
        # REEMPLAZO DE DURACIONES POR EL MAP
        for duracion in duracion_map:
            if duracion in linea:
                linea = linea.replace(duracion, str(duracion_map[duracion]))
        
        resultado.append(linea)
    
    with open("codigoGenerado.txt", 'w') as archivo:
        for linea in resultado:
            # PONER CADA ELEMENTO EN UNA LINEA
            elementos = linea.split()
            for elemento in elementos:
                archivo.write(f"{elemento}\n")