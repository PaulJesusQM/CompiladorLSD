import pygame
import os
import re

def reproducir_musica(input_str):

    pygame.init()
    pygame.mixer.init()

    # Crear canales de mezcla
    canal1 = pygame.mixer.Channel(0)
    canal2 = pygame.mixer.Channel(1)
    canal3 = pygame.mixer.Channel(2)
    canal4 = pygame.mixer.Channel(3)
    canal5 = pygame.mixer.Channel(4)

    def parsear_lista_notas(input_str):
        lineas = input_str.splitlines()
        lista_notas = []
        for linea in lineas:
            linea = linea.strip()
            if linea.startswith('['):
                # Es un acorde
                lista_notas.append(linea)
            elif linea.startswith('P,'):
                # Pausa
                pausa, duracion = linea.split(',')
                lista_notas.append(f"{pausa},{float(duracion) * 1000}") 
            else:
                # Es una nota individual
                nota, duracion = linea.split(',')
                lista_notas.append(f"{nota},{float(duracion) * 1000}")  # Convertir duración a milisegundos
        
        return lista_notas

    def reproducir_notas(lista_notas, carpeta_notas):
        for info_nota in lista_notas:
            info_nota = info_nota.strip()
            if info_nota.startswith('['):
                # Es un acorde
                acorde_match = re.match(r'\[(.*?)\],(\d+\.?\d*)', info_nota)
                if acorde_match:
                    notas_acorde = acorde_match.group(1).split('|')
                    duracion = float(acorde_match.group(2)) * 1000  # Convertir duración a milisegundos
                    reproducir_acorde(notas_acorde, carpeta_notas, duracion)
                else:
                    print(f"Error al procesar acorde: {info_nota}")
            elif info_nota.startswith('P'):
                # Pausa
                try:
                    pausa, duracion = info_nota.split(',')
                    reproducir_nota_individual(os.path.join(carpeta_notas, f"{pausa}.wav"), int(float(duracion)))
                except ValueError:
                    print(f"Error al procesar nota: {info_nota}")
            else:
                # Es una nota individual
                try:
                    nota, duracion = info_nota.split(',')
                    reproducir_nota_individual(os.path.join(carpeta_notas, f"{nota}.wav"), int(float(duracion)))
                except ValueError:
                    print(f"Error al procesar nota: {info_nota}")

    def reproducir_nota_individual(filename, duracion):
        if os.path.isfile(filename):
            sonido = pygame.mixer.Sound(filename)
            canal1.play(sonido)
            pygame.time.wait(duracion)
            canal1.stop()
        else:
            print(f"Archivo {filename} no encontrado")

    def reproducir_acorde(notas_acorde, carpeta_notas, duracion):
        if len(notas_acorde) > 5:
            print("No se pueden reproducir acordes con más de 5 notas.")
            return
        
        # Mapa de canales para cada nota en el acorde
        mapa_canales = {
            0: canal1,
            1: canal2,
            2: canal3,
            3: canal4,
            4: canal5
        }

        # Cargar sonidos de las notas del acorde
        sonidos = []
        for nota in notas_acorde:
            filename = os.path.join(carpeta_notas, f"{nota}.wav")
            if os.path.isfile(filename):
                sonido = pygame.mixer.Sound(filename)
                sonidos.append(sonido)
            else:
                print(f"Archivo {filename} no encontrado")
                return

        # Reproducir cada nota del acorde en su canal correspondiente
        for idx, sonido in enumerate(sonidos):
            canal = mapa_canales[idx]
            canal.play(sonido)

        pygame.time.wait(int(duracion))

        # Detener la reproducción de todas las notas del acorde
        for idx, _ in enumerate(sonidos):
            canal = mapa_canales[idx]
            canal.stop()


    # Parsear las notas del archivo de entrada
    lista_notas = parsear_lista_notas(input_str)
    
    # Directorio donde se encuentran los archivos WAV
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    carpeta_notas = os.path.join(directorio_actual, 'notes')
    
    # Reproducir las notas con sus respectivas duraciones
    reproducir_notas(lista_notas, carpeta_notas)

    # Finalizar Pygame
    pygame.quit()
