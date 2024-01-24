import tkinter as tk
from tkinter import ttk, messagebox
import ply.lex as lex

tokens = [
    'PuntoComa',
    'ParentesisA',
    'ParentesisC',
    'LlaveA',
    'LlaveC',
    'Comilla',
    'Operador',
    'PalabrasReservadas',
    'Letra',
    'NUMBER',
    'Asignacion',
]

PalabrasReservadas = {
    'for': 'PalabrasReservadas',
    'fun': 'PalabrasReservadas',
    'if': 'PalabrasReservadas',
    'else': 'PalabrasReservadas',
    'int': 'PalabrasReservadas',
    'str': 'PalabrasReservadas',
}

tokens += list(PalabrasReservadas.values())

# Token patterns
t_PuntoComa = r';'
t_ParentesisA = r'\('
t_ParentesisC = r'\)'
t_LlaveA = r'\{'
t_LlaveC = r'\}'
t_Comilla = r'"'
t_Asignacion = r'/='
t_Operador = r'(>=|<=|==|!=|>|<|\++)'

def t_Letra(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = PalabrasReservadas.get(t.value, 'Letra')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    error_table.insert('', 'end', values=(f"Caracter no permitido '{t.value[0]}'",))
    t.lexer.skip(1)

lexer = lex.lex()

def check_code():
    # Limpia las tablas de tokens y errores
    token_table.delete(*token_table.get_children())
    error_table.delete(*error_table.get_children())

    # Obtiene el texto del usuario
    code = txt.get("1.0", tk.END).strip()
    if not code:
        messagebox.showinfo("Información", "No hay código para verificar.")
        return

    # Procesa el código con el analizador léxico
    lexer.input(code)
    try:
        for token in lexer:
            token_table.insert('', 'end', values=(token.type, token.value))
        # messagebox.showinfo("Información", "Análisis léxico completado sin errores.")
    except Exception as e:
        print("Error", str(e))
        # messagebox.showerror("Error", str(e))

# interfaz gráfica relacionada con el analizador léxico
root = tk.Tk()
root.title("Analizador Léxico")
root.configure(bg='lightgray')

main_frame = ttk.Frame(root, padding=10)
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Marco para el área de texto
text_frame = ttk.LabelFrame(main_frame, text="Código", padding=10)
text_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Área de texto dentro del marco
codigo = ''
txt = tk.Text(text_frame, width=40, height=15, bg='lightblue')  # Fondo azul claro para el área de texto
txt.pack(expand=True, fill="both")
txt.insert(tk.END, codigo)

# Botón para analizar
def on_enter(e):
    btn.config(bg='green', fg='white')

def on_leave(e):
    btn.config(bg='lightblue', fg='black')

btn = tk.Button(main_frame, text="Analizar", command=check_code, width=10, height=2, bg='lightblue', fg='black')
btn.grid(row=0, column=1, padx=10, pady=10)
btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)

style = ttk.Style()
style.theme_use("default")  # Usar tema por defecto como base

style.configure("Custom.Treeview", background="lightblue", fieldbackground="lightblue", foreground="black")
style.map("Custom.Treeview", background=[('selected', 'blue')], foreground=[('selected', 'white')])

# Marco para tokens
token_frame = ttk.LabelFrame(main_frame, text="Tokens", padding=10,)
token_frame.grid(row=1, column=0, padx=10, pady=10)

# Tabla de tokens
token_table = ttk.Treeview(token_frame, columns=('Type', 'Value'), show='headings', style="Custom.Treeview")
token_table.heading('Type', text='Token')
token_table.heading('Value', text='Valor')
token_table.pack()

# Marco para errores de sintaxis
error_frame = ttk.LabelFrame(main_frame, text="Caracteres no permitidos", padding=10)
error_frame.grid(row=1, column=1, padx=10, pady=10)  # Cambiar la posición del marco de errores

# Tabla de errores
error_table = ttk.Treeview(error_frame, columns=('Error',), show='headings', style="Custom.Treeview")
error_table.heading('Error', text='Mensaje de Error')
error_table.column('Error', width=200)
error_table.pack()

# Etiqueta para resultados
result_label = tk.Label(main_frame, text="", fg="red")
result_label.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
