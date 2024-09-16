import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Conectando ao banco de dados SQLite
conn = sqlite3.connect('academia.db')
cursor = conn.cursor()

# Criando a tabela de usuários (alunos) se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_nascimento TEXT NOT NULL,
    endereco TEXT NOT NULL,
    valor_mensalidade REAL NOT NULL,
    data_inscricao TEXT NOT NULL
)
''')

# Configuração da janela principal
root = tk.Tk()
root.title("Sistema de Gestão de Academia")

# Função para adicionar um novo aluno
def adicionar_aluno():
    nome = nome_entry.get()
    data_nascimento = nascimento_entry.get()
    endereco = endereco_entry.get()
    valor_mensalidade = mensalidade_entry.get()
    data_inscricao = inscricao_entry.get()

    if nome and data_nascimento and endereco and valor_mensalidade and data_inscricao:
        try:
            valor_mensalidade = float(valor_mensalidade)
            cursor.execute('''
                INSERT INTO alunos (nome, data_nascimento, endereco, valor_mensalidade, data_inscricao)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, data_nascimento, endereco, valor_mensalidade, data_inscricao))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Aluno {nome} adicionado com sucesso!")
            limpar_campos()
            visualizar_alunos()  # Atualiza a lista de alunos
        except ValueError:
            messagebox.showerror("Erro", "Valor da mensalidade deve ser numérico!")
    else:
        messagebox.showerror("Erro", "Preencha todos os campos.")

# Função para visualizar alunos
def visualizar_alunos():
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    for aluno in alunos:
        try:
            valor_mensalidade = float(aluno[4])  # Converter para float
            tree.insert('', 'end', values=(aluno[0], aluno[1], aluno[2], aluno[3], f"R$ {valor_mensalidade:.2f}", aluno[5]))
        except ValueError:
            tree.insert('', 'end', values=(aluno[0], aluno[1], aluno[2], aluno[3], aluno[4], aluno[5]))  # Caso o valor não seja numérico

# Função para carregar os dados de um aluno selecionado
def carregar_dados_aluno(event):
    try:
        selected_item = tree.selection()[0]
        aluno = tree.item(selected_item)['values']

        # Preenchendo os campos com os dados do aluno selecionado
        nome_entry.delete(0, tk.END)
        nome_entry.insert(0, aluno[1])

        nascimento_entry.delete(0, tk.END)
        nascimento_entry.insert(0, aluno[2])

        endereco_entry.delete(0, tk.END)
        endereco_entry.insert(0, aluno[3])

        mensalidade_entry.delete(0, tk.END)
        mensalidade_entry.insert(0, aluno[4].replace('R$ ', ''))  # Removendo o "R$" para exibir o valor numérico

        inscricao_entry.delete(0, tk.END)
        inscricao_entry.insert(0, aluno[5])

    except IndexError:
        messagebox.showerror("Erro", "Selecione um aluno válido.")

# Função para atualizar dados do aluno
def atualizar_aluno():
    try:
        selected_item = tree.selection()[0]
        aluno_id = tree.item(selected_item)['values'][0]

        novo_nome = nome_entry.get()
        novo_endereco = endereco_entry.get()
        novo_valor_mensalidade = mensalidade_entry.get()
        nova_data_inscricao = inscricao_entry.get()

        if novo_valor_mensalidade:
            novo_valor_mensalidade = float(novo_valor_mensalidade)

        cursor.execute('''
        UPDATE alunos
        SET nome=?, endereco=?, valor_mensalidade=?, data_inscricao=?
        WHERE id=?
        ''', (novo_nome, novo_endereco, novo_valor_mensalidade, nova_data_inscricao, aluno_id))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Aluno {novo_nome} atualizado com sucesso!")
        visualizar_alunos()
        limpar_campos()

    except IndexError:
        messagebox.showerror("Erro", "Selecione um aluno para atualizar.")
    except ValueError:
        messagebox.showerror("Erro", "Valor da mensalidade deve ser numérico!")

# Função para deletar aluno
def deletar_aluno():
    try:
        selected_item = tree.selection()[0]
        aluno_id = tree.item(selected_item)['values'][0]
        aluno_nome = tree.item(selected_item)['values'][1]  # Captura o nome do aluno

        cursor.execute("DELETE FROM alunos WHERE id=?", (aluno_id,))
        conn.commit()
        tree.delete(selected_item)

        messagebox.showinfo("Sucesso", f"Aluno {aluno_nome} deletado com sucesso!")
    except IndexError:
        messagebox.showerror("Erro", "Selecione um aluno para deletar.")

# Função para limpar os campos
def limpar_campos():
    nome_entry.delete(0, tk.END)
    nascimento_entry.delete(0, tk.END)
    endereco_entry.delete(0, tk.END)
    mensalidade_entry.delete(0, tk.END)
    inscricao_entry.delete(0, tk.END)

# Labels e entradas
tk.Label(root, text="Nome").grid(row=0, column=0, padx=10, pady=5, sticky='w')
nome_entry = tk.Entry(root, width=50)
nome_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

tk.Label(root, text="Data de Nascimento (YYYY-MM-DD)").grid(row=1, column=0, padx=10, pady=5, sticky='w')
nascimento_entry = tk.Entry(root, width=50)
nascimento_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

tk.Label(root, text="Endereço").grid(row=2, column=0, padx=10, pady=5, sticky='w')
endereco_entry = tk.Entry(root, width=50)
endereco_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

tk.Label(root, text="Mensalidade (R$)").grid(row=3, column=0, padx=10, pady=5, sticky='w')
mensalidade_entry = tk.Entry(root, width=50)
mensalidade_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

tk.Label(root, text="Data de Inscrição (YYYY-MM-DD)").grid(row=4, column=0, padx=10, pady=5, sticky='w')
inscricao_entry = tk.Entry(root, width=50)
inscricao_entry.grid(row=4, column=1, padx=10, pady=5, sticky='ew')

# Configuração dos botões
button_width = 15
button_height = 1
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=2, rowspan=6, padx=10, pady=10, sticky='ns')

tk.Button(button_frame, text="Adicionar Aluno", command=adicionar_aluno, width=button_width, height=button_height).pack(fill='x', pady=5)
tk.Button(button_frame, text="Atualizar Aluno", command=atualizar_aluno, width=button_width, height=button_height).pack(fill='x', pady=5)
tk.Button(button_frame, text="Visualizar Alunos", command=visualizar_alunos, width=button_width, height=button_height).pack(fill='x', pady=5)
tk.Button(button_frame, text="Deletar Aluno", command=deletar_aluno, width=button_width, height=button_height).pack(fill='x', pady=5)

# Tabela (Treeview)
cols = ('ID', 'Nome', 'Nascimento', 'Endereço', 'Mensalidade', 'Inscrição')
tree = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor='w')  # Ajustando a largura das colunas
tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Bind para carregar os dados quando um aluno for selecionado
tree.bind("<<TreeviewSelect>>", carregar_dados_aluno)

# Configurações de expansão
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(1, weight=1)

# Executando o sistema
root.mainloop()

# Fechando a conexão com o banco de dados
conn.close()
