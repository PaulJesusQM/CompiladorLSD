import ply.lex as lex
import ply.yacc as yacc
import re

###########################################################################
############            ANALISIS LEXICO                  ##################

# TOKENS
tokens = [
    'CLAVE',
    'BPM',
    'NOTA',
    'DURACION',
    'PAUSA',
    'ACORDE',
    'COMA'
]

# EXPRESIONES REGULARES
t_NOTA = r'[A-G][b#]?[0-7]'   # NOTAS DE [A - G], SOSTENIDOS OPCIONAL Y OCTAVA
t_PAUSA = r'P'             # TOKEN PARA PAUSA
t_ACORDE = r'\[.*?\]'      # TOKEN PARA ACORDE ([])
t_COMA = r','              # TOKEN PARA COMA


def t_DURACION(t):
    r'redonda|blanca|negra|corchea|semic|fusa|semif'
    return t

def t_CLAVE(t):
    r'[A-G][-][>]'
    t.value = t.value.strip()
    return t

def t_BPM(t):
    r'BPM\s*=\s*(\d+)'
    t.value = int(t.value.strip().split('=')[1])
    return t

def t_COMMENT(t):
    r'\/\/.*'
    pass

# REGLA PARA IGNORAR ESPACIOS , | , //
t_ignore = ' \t'
t_ignore_acorde = r' \|'
t_ignore_COMMENT = r'\/\/.*'

# REGLA SALTO DE LINEA
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# REGLA ERRORES
def t_error(t):
    global lista_errores_lexico
    lista_errores_lexico.append(f"Token invalido '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()


###########################################################################
############            ANALISIS SINTACTICO              ##################

# Reglas de la gramatica
def p_pentagrama(p):
    '''pentagrama : config compas'''
    p[0] = ["pentagrama", p[1], p[2]]

def p_config(p):
    '''config : CLAVE BPM'''
    p[0] = ["config", p[1], p[2]]

def p_compas(p):
    '''compas : compas notacion
              | notacion'''
    if len(p) == 2:
        p[0] = ["compas", p[1]]
    else:
        p[0] = ["compas", p[1], p[2]]

def p_notacion(p):
    '''notacion : notacion elemento
                | elemento'''
    if len(p) == 2:
        p[0] = ["notacion", p[1]]
    else:
        p[0] = ["notacion", p[1], p[2]]

def p_elemento(p):
    '''elemento : nota
                | acorde
                | pausa'''
    p[0] = ["elemento", p[1]]

def p_nota(p):
    '''nota : NOTA COMA DURACION'''
    p[0] = ("nota", p[1], p[3])

def p_acorde(p):
    '''acorde : ACORDE COMA DURACION'''
    p[0] = ("acorde", p[1], p[3])

def p_pausa(p):
    '''pausa : PAUSA COMA DURACION'''
    p[0] = ("pausa", p[1], p[3])

def p_error(p):
    global lista_errores_sintacticos
    lista_errores_sintacticos.append(f"Error de sintaxis en '{p.value}'")

# Construir el parser
parser = yacc.yacc(debug=False)

###########################################################################
############            ARBOL A DOT             ##################

def arbol_a_dot(arbol):
    dot_str = 'digraph G {\n'

    def traverse(nodo, parent_id):
        nonlocal dot_str, nodo_id
        current_id = nodo_id
        nodo_id += 1

        if isinstance(nodo, list):
            dot_str += f'  {current_id} [label="{nodo[0]}"]\n'
            for hijo in nodo[1:]:
                hijo_id = traverse(hijo, current_id)
                dot_str += f'  {current_id} -> {hijo_id}\n'
        elif isinstance(nodo, tuple):
            dot_str += f'  {current_id} [label="{nodo[0]}"]\n'
            for hijo in nodo[1:]:
                hijo_id = traverse(hijo, current_id)
                dot_str += f'  {current_id} -> {hijo_id}\n'
        else:
            dot_str += f'  {current_id} [label="{nodo}"]\n'
        
        return current_id

    nodo_id = 0
    traverse(arbol, nodo_id)
    dot_str += '}\n'
    return dot_str

###########################################################################
############            ANALISIS SEMANTICO               ##################


def analizar_semantico(entrada):
    global lista_errores_semanticos
    lista_errores_semanticos = []

    lexer.input(entrada)
    bpm_valido = False
    for tok in lexer:
        if tok.type == 'BPM':
            bpm = tok.value
            if not (40 <= bpm <= 200):
                lista_errores_semanticos.append(f"BPM fuera de rango permitido: {bpm}")
                lista_errores_semanticos.append(f"En el contexto musical el rango del bpm va de 40 a 200")
            bpm_valido = True
        elif tok.type == 'CLAVE':
            clave = tok.value
            if clave not in ['C->', 'F->', 'G->']:
                lista_errores_semanticos.append(f"Clave no válida: '{clave}'")
                lista_errores_semanticos.append(f"En el contexto musical las claves solo pueden ser C, F, G")

        elif tok.type == 'ACORDE':
            acorde = tok.value
            patron_acorde = r'\[[A-G][b#]?[0-7](?:\|[A-G][b#]?[0-7])*\]'
            if not re.match(patron_acorde, acorde):
                lista_errores_semanticos.append(f"Acorde no válido: '{acorde}'")
                lista_errores_semanticos.append("El formato de los acordes debe ser '[nota1|nota2|...]'")
            else:
                notas = re.findall(r'[A-G][b#]?\d+', acorde)
                num_notas = len(notas)
                if not (2 <= num_notas <= 5):
                    lista_errores_semanticos.append(f"Acorde inválido: '{acorde}'")
                    lista_errores_semanticos.append("Un acorde debe contener entre 2 y 5 notas")
                else:
                    if len(set(notas)) != len(notas):
                        lista_errores_semanticos.append(f"Acorde con notas repetidas: '{acorde}'")
                        lista_errores_semanticos.append("Un acorde no puede contener notas repetidas")

    if not bpm_valido:
        lista_errores_semanticos.append("No se definió un valor válido para BPM")

        


###########################################################################
############           COMPILACION                       ##################


def analizar_entrada(entrada):
    global lista_errores_lexico, lista_errores_sintacticos, lista_errores_semanticos
    lista_errores_lexico = []
    lista_errores_sintacticos = []
    lista_errores_semanticos = []
    

    #LIMPIAR ARCHIVOS
    for archivo in ["SalidaLexica.txt", "SalidaSintactica.txt", "SalidaSemantica.txt", "listaErrores.txt"]:
        try:
            with open(archivo, "w") as f:
                pass 
        except Exception as e:
            print(f"No se pudo limpiar el archivo {archivo}")
    

    #ANALISIS LEXICO DEL CONTENIDO
    lexer.input(entrada)
    tokens = []
    for tok in lexer:
        tokens.append(tok)

    with open("SalidaLexica.txt", "w") as f:
        for token in tokens:
            f.write(f"LexToken({token.type},'{token.value}')\n")
            
                
    #ANALISIS SINTACTICO DEL CONTENIDO
    resultado = parser.parse(entrada)
    with open("SalidaSintactica.txt", "w") as f:
        arbol_dot = arbol_a_dot(resultado)
        f.write(arbol_dot)
        
    lista_errores_lexico = []
    
    #ANALISIS SEMANTICO DEL CONTENIDO
    analizar_semantico(entrada)
    with open("SalidaSemantica.txt", "w") as f:
        if lista_errores_semanticos:
            f.write("Se encontraron Errores\n")
        else:
            f.write("Analisis Semantico Correcto\n")
            
    
    # Guardar lista de errores combinados
    with open("listaErrores.txt", "a") as f:
        if lista_errores_lexico:
            f.write("Error Lexico:\n")
            for error in lista_errores_lexico:
                f.write(error + "\n")
        if lista_errores_sintacticos:
            f.write("Error Sintactico:\n")
            for error in lista_errores_sintacticos:
                f.write(error + "\n")
        if lista_errores_semanticos:
            f.write("Error Semantico:\n")
            for error in lista_errores_semanticos:
                f.write(error + "\n")


###########################################################################
############       VERIFICACION DE COMPILACION            #################
   
    try:
        with open("listaErrores.txt", 'r') as f:
            contenido = f.read()
            if contenido.strip() == "":
                return True 
            else:
                return False
  
    except FileNotFoundError:
        print("El archivo 'listaErrores.txt' no existe.")
        return True  