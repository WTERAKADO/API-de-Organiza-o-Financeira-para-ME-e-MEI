#Criarbd.py
# Importando SQLite
import sqlite3 as lite

# Criando conexao
con = lite.connect('dados.db')
 
# criando tabela de Despesas
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Despesas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, subtraido_em DATE, valor DECIMAL)")

# criando tabela de categorias
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Categorias(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")

# criando tabela de Receitas
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL)") 
