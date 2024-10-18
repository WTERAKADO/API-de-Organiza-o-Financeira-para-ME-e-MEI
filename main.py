from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox
import sqlite3

#importando Pillow -------------------------------------------------------------

from PIL import Image, ImageTk

#importando Barra de Progresso do Tkinter --------------------------------------

from tkinter.ttk import Progressbar

#importando Barra de Progresso do Matplotlib -----------------------------------

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#importando Funções de Calendário ----------------------------------------------

from tkcalendar import Calendar,DateEntry
from datetime import date

#importando Funções de View ----------------------------------------------------

from view import bar_valores, inserir_categoria, inserir_despesas, inserir_receitas,consultar_categorias,consultar_despesas,consultar_receitas,tabela,deletar_despesas,deletar_receitas,pie_valores,percentagem_valor

#cores -------------------------------------------------------------------------

co0 = "#2e2d2b"
co1 = "#feffff"
co2 = "#4fa882"
co3 = "#38576b"
co4 = "#403d3d"
co5 = "#e06636"
co6 = "#038cfc"
co7 = "#3fbfb9"
co8 = "#263238"
co9 = "#e9edf5"

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

#criando janela vazia ----------------------------------------------------------

janela = Tk()
janela.title()
janela.geometry('900x650')
janela.configure(background=co9)
janela.resizable(width=False, height=False)

style = ttk.Style(janela)
style.theme_use("clam")

#criando frames para divisao da tela -------------------------------------------

frameCima = Frame(janela, width=1043, height=50, bg=co1, relief="flat")
frameCima.grid(row=0,column=0)

frameMeio = Frame(janela, width=1043, height=361, bg=co1, pady=20, relief="raised")
frameMeio.grid(row=1,column=0, pady=1, padx=0, sticky=NSEW)

frameBaixo = Frame(janela, width=1043, height=300, bg=co1, relief="flat")
frameBaixo.grid(row=2,column=0, pady=0, padx=10, sticky=NSEW)

frame_gra_pie = Frame(frameMeio, width=580, height=250, bg=co2)
frame_gra_pie.place(x=415, y=5)

#Criando frames dentro do frame inferior -------------------------------------------

frame_renda = Frame(frameBaixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0,column=0)

frame_operacoes= Frame(frameBaixo, width=220, height=250, bg=co1)
frame_operacoes.grid(row=0,column=1, padx=5)

frame_configuracao= Frame(frameBaixo, width=220, height=250, bg=co1)
frame_configuracao.grid(row=0,column=2, padx=5)

# definindo tree como global -------------------------------------------------------

global tree

# função inserir categoria (despesas) -----------------------------------------------

def inserir_cat_global():
    nome = e_categoria.get()

    lista_inserir = [nome]

    for i in lista_inserir:
        if i =='':
            messagebox.showerror('Erro','Preencha os campos adequadamente!')
            return
    
    # passando para a funcao inserir despesas presente na view

    inserir_categoria(lista_inserir)

    messagebox.showinfo('Sucesso','Os dados foram inseridos com êxito')

    e_categoria.delete(0,'end')

    # Coletando os valores da categoria

    categoria_funcao = consultar_categorias()
    print(f"Categorias disponíveis: {categoria_funcao}")  # Para verificar o retorno

    categoria = []

    for i in categoria_funcao:
        categoria.append(i[1])

    # atualizando a lista de categorias

    combo_categoria_despesas['values'] = (categoria)


# função inserir receitas ------------------------------------------------------

def inserir_receita_global():
    nome = 'Receita'
    data = e_cal_receitas.get()
    valor = e_valor_receitas.get()
    
    lista_inserir = [nome, data, valor]

    print(f"Valores para inserir: {lista_inserir}")  # Adiciona o print para verificar

    for i in lista_inserir:
        if i =='':
            Message.showerror('Erro','Preencha os campos adequadamente!')
            return
        
    # chamando a função inserir receitas presente na view
    try:
        inserir_receitas(lista_inserir)
        messagebox.showinfo('Sucesso', 'Os dados foram inseridos com êxito')
    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao inserir receita: {e}')

    e_cal_receitas.delete(0,'end')
    e_valor_receitas.delete(0,'end')

    # atualizando dados
    mostrar_renda()
    percentagem()
    grafico_bar()
    resumo()
    grafico_pie()

# função inserir despesas ------------------------------------------------------

def inserir_despesa_global():
    nome = combo_categoria_despesas.get()
    data = e_cal_despesas.get()
    valor = e_valor_despesas.get()
   
    lista_inserir = [nome, data, valor]

    print(f"Valores para inserir: {lista_inserir}")  # Adiciona o print para verificar

    for i in lista_inserir:
        if i =='':
            Message.showerror('Erro','Preencha os campos adequadamente!')
            return
        
    # chamando a função inserir receitas presente na view
    try:
        inserir_despesas(lista_inserir)
        messagebox.showinfo('Sucesso', 'Os dados foram inseridos com êxito')
    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao inserir receita: {e}')

    combo_categoria_despesas.delete(0,'end')
    e_cal_despesas.delete(0,'end')
    e_valor_despesas.delete(0,'end')

    # atualizando dados
    mostrar_renda()
    percentagem()
    grafico_bar()
    resumo()
    grafico_pie()

#Trabalhando no frame cima - logo ----------------------------------------------

#acessando a imagem ------------------------------------------------------------

app_img = Image.open('financa.png')
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text=" API de Organização Financeira para MEI/ME", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verlag 20 bold'), bg=co1, fg=co4)
app_logo.place(x=0,y=0)

# função deletar

def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]

        if nome == 'Receita':
            deletar_receitas([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram excluídos com êxito')

        
            # atualizando dados
            mostrar_renda()
            percentagem()
            grafico_bar()
            resumo()
            grafico_pie()
        else:
            deletar_despesas([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram excluídos com êxito')

        
            # atualizando dados
            mostrar_renda()
            percentagem()
            grafico_bar()
            resumo()
            grafico_pie()

    except IndexError:
        messagebox.showerror('Erro', 'Selecione na tabela qual dado deseja excluir')


#Trabalhando no frame meio - gráficos ----------------------------------------------

#percentagem -----------------------------------------------------------------------

def percentagem():
    l_nome = Label(frameMeio, text="Porcentagem da Receita Disponível", height=1, anchor=NW, font=('Verlag 12'), bg=co1, fg=co4)
    l_nome.place(x=7,y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='#47D359')
    style.configure("TProgressbar", thickness=25)
    
    bar = Progressbar(frameMeio, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=10,y=35)
    bar['value'] = percentagem_valor()[0]

    valor = percentagem_valor()[0]

    l_percentagem = Label(frameMeio, text="{:,.2f}%".format(valor), height=1, anchor=NW, font=('Verlag 12'), bg=co1, fg=co4)
    l_percentagem.place(x=200,y=35)

#Gráficos de barras ------------------------------------------------------------

def grafico_bar():
    lista_categorias = ['Receitas','Despesas','Saldo']
    lista_valores = bar_valores()

    # faça figura e atribua objetos de eixo ------------------------------------
    figura = plt.Figure(figsize=(4.5, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    # ax.autoscale(enable=True, axis='both', tight=None)

    ax.bar(lista_categorias, lista_valores,  color=colors, width=0.9)
    # create a list to collect the plt.patches data

    c = 0
    # set individual bar lables using above list
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom', color='dimgrey')
        c += 1

    ax.set_xticks(range(len(lista_categorias)))
    ax.set_xticklabels(lista_categorias, fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)

#Sessão de Resumos Totais ------------------------------------------------------------

def resumo():
    valor = bar_valores()
    
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309,y=52)
    l_sumario = Label(frameMeio, text="Total Renda Mensal         ".upper(), anchor=NW, font=('Verlag 12'), bg=co1, fg='#6666FF')
    l_sumario.place(x=309,y=35)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[0]), anchor=NW, font=('Arial 12'), bg=co1, fg='#545454')
    l_sumario.place(x=309,y=70)

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309,y=132)
    l_sumario = Label(frameMeio, text="Total Despesas Mensais     ".upper(), anchor=NW, font=('Verlag 12'), bg=co1, fg='#6666FF')
    l_sumario.place(x=309,y=115)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[1]), anchor=NW, font=('Arial 12'), bg=co1, fg='#545454')
    l_sumario.place(x=309,y=150)


    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309,y=212)
    l_sumario = Label(frameMeio, text="Saldo                                        ".upper(), anchor=NW, font=('Verlag 12'), bg=co1, fg='#6666FF')
    l_sumario.place(x=309,y=195)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[2]), anchor=NW, font=('Arial 12'), bg=co1, fg='#545454')
    l_sumario.place(x=309,y=230)


#Gráfico de Pizza ------------------------------------------------------------

def grafico_pie():
    # faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]

    # only "explode" the 2nd slice (i.e. 'Hogs')

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().grid(row=0, column=0)

#Trabalhando Frame Inferior ------------------------------------------------------------

#Tabela Renda Mensal (Valores) --------------------------------------------------------

app_tabela = Label(frameMeio, text="Tabela de Receitas & Despesas", anchor=NW, font=('Verlag 12'), bg=co1, fg=co4)
app_tabela.place(x=5,y=309)

#Função para mostrar renda ------------------------------------------------------------

def mostrar_renda():
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    # Consulta os dados da tabela Receitas
    cursor.execute("SELECT * FROM Receitas")
    lista_receitas = cursor.fetchall()

    # Consulta os dados da tabela Despesas
    cursor.execute("SELECT * FROM Despesas")
    lista_despesas = cursor.fetchall()

    conn.close()

    # Combina receitas e despesas
    lista_itens = lista_receitas + lista_despesas

    # creating a treeview with dual scrollbars
    tabela_head = ['#Id','Categoria','Data','Valor']
    
    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")
    # vertical scrollbar
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    # horizontal scrollbar
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)

#Configurações Despesas --------------------------------------------------------

l_info = Label(frame_operacoes, text='      Inserir Novas Despesas', height=1, anchor=NW, font=('Verlag 10 bold'), bg=co1, fg=co4)
l_info.place(x=10,y=10)

# Configurações Despesas > Categorias --------------------------

l_categoria = Label(frame_operacoes, text='Categoria', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_categoria.place(x=10,y=40)

categoria_funcao = consultar_categorias()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1])

# Configurações Despesas > Categorias > Lista Suspensa ----------

combo_categoria_despesas = ttk.Combobox(frame_operacoes, width=10, font=('Ivy 10'))
combo_categoria_despesas['values'] = (categoria)
combo_categoria_despesas.place(x=115,y=41)

# despesas > data -----------------------------------------------

l_cal_despesas = Label(frame_operacoes, text="Data", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_despesas.place(x=10,y=70)

e_cal_despesas = DateEntry(frame_operacoes, width=12, background='darkblue', foreground='white',borderwidth=2, year=2024)
e_cal_despesas.place(x=115,y=71)

# despesas > valor -----------------------------------------------

l_valor_despesas = Label(frame_operacoes, text="Valor", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_despesas.place(x=10,y=100)

e_valor_despesas = Entry(frame_operacoes, width=14, justify=LEFT, relief=SOLID)
e_valor_despesas.place(x=115,y=101)

# despesas > botão adicionar -----------------------------------------------

img_add_despesas = Image.open('adicionar.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)

botao_inserir_despesas = Button(frame_operacoes, command=inserir_despesa_global, image=img_add_despesas, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg='#DAF6DE', fg=co0, overrelief=RIDGE)
botao_inserir_despesas.place(x=115,y=131)

# despesas > botão excluir -----------------------------------------------

l_excluir = Label(frame_operacoes, text="Excluir Seleção", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg='#CC0000')
l_excluir.place(x=10,y=190)

img_excluir_despesas = Image.open('excluir.png')
img_excluir_despesas = img_excluir_despesas.resize((17,17))
img_excluir_despesas = ImageTk.PhotoImage(img_excluir_despesas)

botao_excluir_despesas = Button(frame_operacoes, command=deletar_dados, image=img_excluir_despesas, text=" Excluir".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg='#FFE5E5', fg=co0, overrelief=RIDGE)
botao_excluir_despesas.place(x=115,y=190)

#Configurações Receitas --------------------------------------------------------

l_info = Label(frame_configuracao, text='        Inserir Novas Receitas', height=1, anchor=NW, font=('Verlag 10 bold'), bg=co1, fg=co4)
l_info.place(x=10,y=10)

# receitas > data -----------------------------------------------

l_cal_receitas = Label(frame_configuracao, text="Data", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_receitas.place(x=30,y=40)

e_cal_receitas = DateEntry(frame_configuracao, width=12, background='darkblue', foreground='white',borderwidth=2, year=2024)
e_cal_receitas.place(x=115,y=41)

# receitas > valor -----------------------------------------------

l_valor_receitas = Label(frame_configuracao, text="Valor", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_receitas.place(x=30,y=70)

e_valor_receitas = Entry(frame_configuracao, width=14, justify=LEFT, relief=SOLID)
e_valor_receitas.place(x=115,y=71)

# receitas > botão adicionar -----------------------------------------------

img_add_receitas = Image.open('adicionar.png')
img_add_receitas = img_add_receitas.resize((17,17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)

botao_inserir_receitas = Button(frame_configuracao, command=inserir_receita_global, image=img_add_receitas, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg='#DAF6DE', fg=co0, overrelief=RIDGE)
botao_inserir_receitas.place(x=115,y=101)

# Operação Nova Categoria

l_valor_receitas = Label(frame_configuracao, text="Categoria", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_receitas.place(x=30,y=160)

e_categoria = Entry(frame_configuracao, width=14, justify=LEFT, relief=SOLID)
e_categoria.place(x=115,y=160)

# Nova Categoria > botão adicionar -----------------------------------------------

img_add_categoria = Image.open('adicionar.png')
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)

botao_inserir_categoria = Button(frame_configuracao, command=inserir_cat_global, image=img_add_categoria, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg='#DAF6DE', fg=co0, overrelief=RIDGE)
botao_inserir_categoria.place(x=115,y=191)





percentagem()
grafico_bar()
resumo()
grafico_pie()
mostrar_renda()

janela.mainloop()
