# Importando SQLite
import sqlite3 as lite
import pandas as pd

# Criando conexao
con = lite.connect('dados.db')

#funções de inserir ------------------------------------------------------------------------

# Criando categorias
def inserir_categoria(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categorias (nome) VALUES (?)"
        cur.execute(query,i)

# Criando campo receitas
def inserir_receitas(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria, adicionado_em,valor) VALUES (?,?,?)"
        cur.execute(query,i)

# Criando campo despesas
def inserir_despesas(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Despesas (categoria, subtraido_em,valor) VALUES (?,?,?)"
        cur.execute(query,i)

#funções de deletar ------------------------------------------------------------------------

# deletar Receitas
def deletar_receitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id=?"
        cur.execute(query,i)

# deletar Despesas
def deletar_despesas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Despesas WHERE id=?"
        cur.execute(query,i)

#funções de consulta ------------------------------------------------------------------------

# consultar categorias
def consultar_categorias():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categorias")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    
    return lista_itens

# consultar receitas
def consultar_receitas():
    lista_receitas = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")
        linha = cur.fetchall()
        for l in linha:
            lista_receitas.append(l)
    
    return lista_receitas 

# consultar despesas
def consultar_despesas():
    lista_despesas = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Despesas")
        linha = cur.fetchall()
        for l in linha:
            lista_despesas.append(l)
    
    return lista_despesas

# função para dados da tabela ---------------------------------------------------------

def tabela():
    despesas = consultar_despesas()
    receitas = consultar_receitas()

    tabela_lista = []

    for i in despesas:
        tabela_lista.append(i)

    for i in receitas:
        tabela_lista.append(i)


# função para dados do gradico de barra------------------------------------------------
def bar_valores():
   
    # receitas totais---------------------
    receitas = consultar_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    # despesas totais---------------------
    despesas = consultar_despesas()
    despesas_lista = []

    for i in despesas:
        despesas_lista.append(i[3])

    despesa_total = sum(despesas_lista)

    # saldo total
    saldo_total = receita_total - despesa_total

    return [receita_total,despesa_total,saldo_total]

# função gráfico pizza---------------------------------------------------------------------
def pie_valores():
    despesas = consultar_despesas()
    tabela_lista = []

    for i in despesas:
        tabela_lista.append(i)

    dataframe = pd.DataFrame(tabela_lista, columns=['id','categoria','data','valor'])
    dataframe = dataframe.groupby('categoria')['valor'].sum()

    lista_valores = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)

    return([lista_categorias, lista_valores])


# função para dados da percentagem------------------------------------------------
def percentagem_valor():
   
    # receitas totais---------------------
    receitas = consultar_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    # despesas totais---------------------
    despesas = consultar_despesas()
    despesas_lista = []

    for i in despesas:
        despesas_lista.append(i[3])

    despesa_total = sum(despesas_lista)

    # percentagem total
    total = ((receita_total - despesa_total)/receita_total)*100

    return [total]
