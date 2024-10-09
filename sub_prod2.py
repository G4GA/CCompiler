import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog
import re

# Definición de gramática
grammar = {
    'S': ['D', 'B'],
    'D': ['int ID = E;', 'float ID = E;', 'char ID = E;', 'int ID;', 'float ID;', 'char ID;'],
    'B': ['if ( E ) { B } else { B }', 'while ( E ) { B }', 'for ( E ) { B }', 'INCREMENT;', 'DECREMENT;', ''],
    'E': ['ID', 'NUM', 'ID + E', 'ID - E', 'ID * E', 'ID / E'],
    'INCREMENT': ['ID++;'],
    'DECREMENT': ['ID--;']
}

# Tablas FIRST y FOLLOW
first = {
    'S': {'int', 'float', 'char', 'if', 'while', 'for', 'ID', 'NUM', 'INCREMENT', 'DECREMENT'},
    'D': {'int', 'float', 'char'},
    'B': {'if', 'while', 'for', 'ID', 'INCREMENT', 'DECREMENT', ''},
    'E': {'ID', 'NUM'},
    'INCREMENT': {'ID'},
    'DECREMENT': {'ID'}
}

follow = {
    'S': {'$'},
    'D': {'if', 'while', 'for', 'INCREMENT', 'DECREMENT', '$'},
    'B': {'$'},
    'E': {';', ')'},
    'INCREMENT': {'$'},
    'DECREMENT': {'$'}
}

# Función para validar el código C básico
def validate_code(code):
    # Expresiones regulares para validar el código C básico
    regex_declaration = r'^(int|float|char)\s+(\w+)\s*=\s*([^;]+);$'  # Validación de declaraciones
    regex_declaration_no_init = r'^(int|float|char)\s+(\w+);\s*$'  # Validación de declaraciones sin inicialización
    regex_assignment = r'^\s*(\w+)\s*=\s*([^;]+);$'  # Validación de asignaciones
    regex_if = r'^\s*if\s*\(.*\)\s*{\s*$'  # Validación de if
    regex_else = r'^\s*else\s*{\s*$'  # Validación de else
    regex_while = r'^\s*while\s*\(.*\)\s*{\s*$'  # Validación de while
    regex_for = r'^\s*for\s*\(.*\)\s*{\s*$'  # Validación de for
    regex_increment = r'^\s*(\w+)\s*\+\+\s*;$'  # Validación de incremento
    regex_decrement = r'^\s*(\w+)\s*--\s*;$'  # Validación de decremento
    regex_brace_close = r'^\s*}\s*$'  # Validación de cierre de llaves
    regex_variable_usage = r'\b\w+\b'  # Uso de variables en expresiones

    # Contador de llaves y conjunto de variables declaradas
    open_braces = 0
    declared_variables = set()
    lines = code.splitlines()

    # Validar cada línea y agregar resultados a la tabla
    for i, line in enumerate(lines, start=1):
        line = line.strip()

        if re.match(regex_declaration, line):
            var_name = re.match(regex_declaration, line).group(2)
            declared_variables.add(var_name)
            line_status_tree.insert("", tk.END, values=(line, "Correcto"))
        elif re.match(regex_declaration_no_init, line):
            var_name = re.match(regex_declaration_no_init, line).group(2)
            declared_variables.add(var_name)
            line_status_tree.insert("", tk.END, values=(line, "Correcto"))
        elif re.match(regex_assignment, line):
            assigned_variable = re.match(regex_assignment, line).group(1)
            expression = re.match(regex_assignment, line).group(2)
            variables_used = re.findall(regex_variable_usage, expression)
            error_found = False

            # Validar que la variable de asignación esté declarada
            if assigned_variable not in declared_variables:
                line_status_tree.insert("", tk.END, values=(line, f"Incorrecto: '{assigned_variable}' no está declarado"))
                continue

            # Validar el uso de variables no declaradas en la expresión
            for var in variables_used:
                if var not in declared_variables and not var.isdigit():  # Ignorar números
                    line_status_tree.insert("", tk.END, values=(line, f"Incorrecto: '{var}' no está declarado"))
                    error_found = True
                    break

            if not error_found:
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
    else:
        output_label.config(text="Código validado correctamente", fg="green")

# Función para el botón "Analizar"
def analizar():
    cadena = text_input.get("1.0", tk.END).strip()  # Obtener el texto del usuario
    line_status_tree.delete(*line_status_tree.get_children())  # Limpiar la tabla de líneas y estados

    validate_code(cadena)

# Función para abrir un archivo y analizar su contenido
def open_file():
    file_path = filedialog.askopenfilename(title="Seleccionar archivo")
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text_input.delete("1.0", tk.END)  # Limpiar el área de texto
            text_input.insert(tk.END, content)  # Insertar el contenido del archivo en el área de texto

# Crear la ventana principal
root = tk.Tk()
root.title("Analizador Léxico")

# Área de entrada para el código
text_input = scrolledtext.ScrolledText(root, width=60, height=20)
text_input.pack()

# Botón para abrir un archivo
open_file_button = tk.Button(root, text="Abrir Archivo", command=open_file)
open_file_button.pack()

# Botón para analizar el código
analyze_button = tk.Button(root, text="Analizar", command=analizar)
analyze_button.pack()

# Etiqueta de salida
output_label = tk.Label(root, text="", fg="green")
output_label.pack()

# Tabla para mostrar el número de línea y estado
line_status_tree = ttk.Treeview(root, columns=("Línea", "Estado"), show="headings", height=5)
line_status_tree.heading("Línea", text="Línea")
line_status_tree.heading("Estado", text="Estado")
line_status_tree.pack()

# Iniciar el bucle de la aplicación
root.mainloop()
