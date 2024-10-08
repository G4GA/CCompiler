import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk  # Para la tabla dinámica
import re  # Importar la biblioteca de expresiones regulares

# Clase Lexemas
class Lexema:
    def __init__(self, tipo, valor, descripcion):
        self.tipo = tipo
        self.valor = valor
        self.descripcion = descripcion

    def __repr__(self):
        return f"Lexema({self.tipo}, '{self.valor}', '{self.descripcion}')"

# Tabla de tipos y valores asociados
tabla_tipos = {
    "identificador": 0,
    "entero": 1,
    "real": 2,
    "cadena": 3,
    "tipo": 4,
    "operador de adición": 5,
    "operador de multiplicación": 6,
    "operador relacional": 7,
    "operador lógico OR": 8,
    "operador lógico AND": 9,
    "operador lógico NOT": 10,
    "operador igualdad": 11,
    "punto y coma": 12,
    "coma": 13,
    "paréntesis": 14,
    "llave": 16,
    "asignación": 18,
    "palabra reservada if": 19,
    "palabra reservada while": 20,
    "palabra reservada return": 21,
    "palabra reservada else": 22,
}

# Función del analizador léxico
def analizador_lexico(cadena):
    cadena += "$"
    lexico = []
    contador_chars = 0

    while contador_chars < len(cadena):
        aux_palabra = ""
        uso_punto_decimal = False
        cha = cadena[contador_chars]

        if cha.isalpha():  # Palabras reservadas o identificadores
            while cadena[contador_chars].isalpha() or cadena[contador_chars].isdigit():
                if cadena[contador_chars] == ' ':
                    break
                aux_palabra += cadena[contador_chars]
                contador_chars += 1
                if contador_chars == len(cadena):
                    break

            if aux_palabra in ["if", "while", "return", "else", "int", "float", "void"]:
                lexico.append(Lexema(9, aux_palabra, f"palabra reservada {aux_palabra}"))
            else:
                lexico.append(Lexema(1, aux_palabra, "identificador"))

        elif cha.isdigit():  # Números enteros y reales
            while cadena[contador_chars].isdigit() or cadena[contador_chars] == '.':
                if cadena[contador_chars] == '.':
                    uso_punto_decimal = True
                aux_palabra += cadena[contador_chars]
                contador_chars += 1
                if contador_chars == len(cadena):
                    break

            if uso_punto_decimal:
                lexico.append(Lexema(13, aux_palabra, "número decimal"))
            else:
                lexico.append(Lexema(13, aux_palabra, "número entero"))

        elif cha in ['+', '-']:  # Operadores de adición
            aux_palabra += cha
            contador_chars += 1
            lexico.append(Lexema(14, aux_palabra, "operador de adición"))

        elif cha in ['*', '/']:  # Operadores de multiplicación
            aux_palabra += cha
            contador_chars += 1
            lexico.append(Lexema(14, aux_palabra, "operador de multiplicación"))

        elif cha == '=' and cadena[contador_chars + 1] != '=':  # Operador de asignación
            aux_palabra += cha
            contador_chars += 1
            lexico.append(Lexema(15, aux_palabra, "operador de asignación"))

        elif cha == '|' and cadena[contador_chars + 1] == '|':  # Operador lógico OR
            aux_palabra = "||"
            contador_chars += 2
            lexico.append(Lexema(16, aux_palabra, "operador lógico OR"))

        elif cha == '&' and cadena[contador_chars + 1] == '&':  # Operador lógico AND
            aux_palabra = "&&"
            contador_chars += 2
            lexico.append(Lexema(16, aux_palabra, "operador lógico AND"))

        elif cha == '!':  # Operador lógico NOT
            if cadena[contador_chars + 1] == '=':
                aux_palabra = "!="  # Operador relacional !=
                contador_chars += 2
                lexico.append(Lexema(17, aux_palabra, "operador relacional"))
            else:
                aux_palabra = "!"
                contador_chars += 1
                lexico.append(Lexema(16, aux_palabra, "operador lógico NOT"))

        elif cha == '=' and cadena[contador_chars + 1] == '=':  # Operador relacional ==
            aux_palabra = "=="
            contador_chars += 2
            lexico.append(Lexema(17, aux_palabra, "operador relacional"))

        elif cha in ['<', '>']:  # Operadores relacionales
            if cadena[contador_chars + 1] == '=':
                aux_palabra = cha + '='
                contador_chars += 2
            else:
                aux_palabra = cha
                contador_chars += 1
            lexico.append(Lexema(17, aux_palabra, "operador relacional"))

        elif cha in ['(', ')']:  # Paréntesis
            aux_palabra += cha
            contador_chars += 1
            lexico.append(Lexema(18, aux_palabra, "paréntesis"))

        elif cha in ['{', '}']:  # Llaves
            aux_palabra += cha
            contador_chars += 1
            lexico.append(Lexema(19, aux_palabra, "llave"))

        elif cha == ';':  # Punto y coma
            aux_palabra += cha
            contador_chars += 1
            lexico.append(Lexema(20, aux_palabra, "punto y coma"))

        elif cha.isspace():  # Ignorar espacios
            contador_chars += 1
            continue

        else:
            contador_chars += 1
            continue

    return lexico

# Función para validar el código
def validate_code():
    code = text_input.get("1.0", tk.END).strip()  # Obtener el texto del área de entrada y eliminar espacios en blanco
    lineas = code.split('\n')
    output_label.config(text="", fg="green")  # Limpiar mensaje anterior
    line_status_tree.delete(*line_status_tree.get_children())  # Limpiar la tabla de líneas y estados

    # Expresión regular para validar el código C básico
    regex = r'''
        ^                              # Inicio de la cadena
        (//.*\n|\s)*                   # Comentarios de una línea y espacios en blanco
        (/\*.*?\*/\s*)*               # Comentarios de múltiples líneas
        (int\s+\w+\s*=\s*\d+\s*;\s*)*  # Declaraciones de enteros
        (float\s+\w+\s*=\s*\d+\.\d+\s*;\s*)*  # Declaraciones de flotantes
        (char\s+\w+\s*=\s*\'\w\'\s*;\s*)*  # Declaraciones de caracteres
        (double\s+\w+\s*=\s*\d+\.\d+\s*;\s*)* # Declaraciones de dobles
        (long\s+\w+\s*=\s*\d+\s*;\s*)*  # Declaraciones de long
        (short\s+\w+\s*=\s*\d+\s*;\s*)* # Declaraciones de short
        (unsigned\s+int\s+\w+\s*=\s*\d+\s*;\s*)* # Declaraciones de unsigned int

        (for\s*\(\s*int\s+\w+\s*=\s*\d+\s*;\s*\w+\s*(<|>|<=|>=|==|!=)\s*\d+\s*;\s*\w+\+\+\)\s*{  # Estructura for
            (\s*\w+\s*=\s*\w+\s*([+\-*\/]\s*\w+)?\s*;\s*)*  # Instrucciones dentro del for
        }\s*)*

        (while\s*\(\s*\w+\s*(<|>|<=|>=|==|!=)\s*\w+\s*\)\s*{  # Estructura while
            (\s*\w+\s*=\s*\w+\s*([+\-*\/]\s*\w+)?\s*;\s*)*  # Instrucciones dentro del while
        }\s*)*

        (if\s*\(\s*\w+\s*(<|>|<=|>=|==|!=)\s*\w+\s*\)\s*{  # Estructura if
            (\s*\w+\s*=\s*\w+\s*([+\-*\/]\s*\w+)?\s*;\s*)*  # Instrucciones dentro del if
        }\s*else\s*{  # Estructura else
            (\s*\w+\s*=\s*\w+\s*([+\-*\/]\s*\w+)?\s*;\s*)*  # Instrucciones dentro del else
        }\s*)*

        (\w+\s*=\s*\w+\s*([+\-*\/]\s*\w+)?\s*;\s*)* # Asignaciones finales
        $                              # Fin de la cadena
    '''
        
    # Validar cada línea y agregar resultados a la tabla
    for i, linea in enumerate(lineas, start=1):
        if re.fullmatch(regex, linea.strip(), re.DOTALL | re.VERBOSE):
            line_status_tree.insert("", tk.END, values=(linea.strip(), "Correcto"))
        else:
            line_status_tree.insert("", tk.END, values=(linea.strip(), "Incorrecto"))



# Función para validar el código
def validate_code():
    code = text_input.get("1.0", tk.END).strip()  # Obtener el texto del área de entrada y eliminar espacios en blanco
    lineas = code.split('\n')
    output_label.config(text="", fg="green")  # Limpiar mensaje anterior
    line_status_tree.delete(*line_status_tree.get_children())  # Limpiar la tabla de líneas y estados

# Expresiones regulares para validar el código C básico
    regex_declaration = r'^(int|float|char)\s+\w+\s*=\s*.*;$'  # Validación de declaraciones
    regex_assignment = r'^\s*\w+\s*=\s*.*;$'  # Validación de asignaciones
    regex_if = r'^\s*if\s*\(.*\)\s*{\s*$'  # Validación de if
    regex_else = r'^\s*else\s*{\s*$'  # Validación de else
    regex_while = r'^\s*while\s*\(.*\)\s*{\s*$'  # Validación de while
    regex_for = r'^\s*for\s*\(.*\)\s*{\s*$'  # Validación de for
    regex_brace_close = r'^\s*}\s*$'  # Validación de cierre de llaves
    regex_increment = r'^\s*\w+\s*\+\+\s*;$'  # Validación de incremento
    regex_decrement = r'^\s*\w+\s*--\s*;$'    # Validación de decremento


    # Contador de llaves
    open_braces = 0
    lines = code.splitlines()

    # Validar cada línea y agregar resultados a la tabla
    for i, line in enumerate(lines, start=1):
        line = line.strip()

        if re.match(regex_declaration, line):
            line_status_tree.insert("", tk.END, values=(line, "Correcto"))
        elif re.match(regex_assignment, line):
            line_status_tree.insert("", tk.END, values=(line, "Correcto"))
        elif re.match(regex_if, line):
            open_braces += 1
            line_status_tree.insert("", tk.END, values=(line, "Correcto"))
        elif re.match(regex_else, line):
            line_status_tree.insert("", tk.END, values=(line, "Correcto"))
        elif re.match(regex_while, line):
            open_braces += 1
            line_status_tree.insert("", tk.END, values=(line, "Correcto"))
        elif re.match(regex_for, line):
            open_braces += 1
            line_status_tree.insert("", tk.END, values=(line, "Correcto"))
        elif re.match(regex_increment, line):
            line_status_tree.insert("", tk.END, values=(line, "Correcto"))
        elif re.match(regex_decrement, line):
            line_status_tree.insert("", tk.END, values=(line, "Correcto"))
        elif re.match(regex_brace_close, line):
            if open_braces > 0:
                open_braces -= 1
                line_status_tree.insert("", tk.END, values=(line, "Correcto"))
            else:
                line_status_tree.insert("", tk.END, values=(line, "Incorrecto"))
        else:
            line_status_tree.insert("", tk.END, values=(line, "Incorrecto"))

    # Validar si quedan llaves abiertas al final
    if open_braces > 0:
        output_label.config(text="Error: Faltan llaves de cierre", fg="red")

# Función para el botón "Analizar"
def analizar():
    cadena = text_input.get("1.0", tk.END).strip()  # Obtener el texto del usuario
    lexico = analizador_lexico(cadena)  # Analizar la cadena
    tree.delete(*tree.get_children())  # Limpiar la tabla de lexemas
    line_status_tree.delete(*line_status_tree.get_children())  # Limpiar la tabla de líneas y estados

    # Mostrar los resultados del análisis léxico
    for lexema in lexico:
        text_output.insert(tk.END, f"{lexema}\n")
        tree.insert("", tk.END, values=(lexema.tipo, lexema.valor, lexema.descripcion))

# Crear la ventana principal
root = tk.Tk()
root.title("Analizador Léxico")

# Área de entrada para el código
text_input = scrolledtext.ScrolledText(root, width=60, height=20)
text_input.pack()

# Botón para analizar el código
analyze_button = tk.Button(root, text="Analizar", command=analizar)
analyze_button.pack()

# Botón para validar el código
validate_button = tk.Button(root, text="Validar Código C", command=validate_code)
validate_button.pack()

# Etiqueta de salida
output_label = tk.Label(root, text="", fg="green")
output_label.pack()

# Área de salida para mostrar los resultados del análisis
text_output = scrolledtext.ScrolledText(root, width=60, height=10)
text_output.pack()

# Tabla para mostrar los lexemas (ajustada)
tree = ttk.Treeview(root, columns=("Tipo", "Valor", "Descripción"), show="headings", height=5)
tree.heading("Tipo", text="Tipo")
tree.heading("Valor", text="Valor")
tree.heading("Descripción", text="Descripción")
tree.pack()

# Tabla para mostrar el número de línea y estado
line_status_tree = ttk.Treeview(root, columns=("Línea", "Estado"), show="headings", height=5)
line_status_tree.heading("Línea", text="Línea")
line_status_tree.heading("Estado", text="Estado")
line_status_tree.pack()

# Iniciar el bucle de la aplicación
root.mainloop()
