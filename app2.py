import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime, date
import json, os, cv2
import sql, attend2
import operator as op

# Muda a seguinte variável para True para ignorar o login facial
skipFaceLogin = False

# IMPORTANTE!!!!
# </</</</
# />/>/>/>
# ID da câmara do utilizador
attend2.camID = 1

def add_cliente(root):
    def submit():
        client_name = entry_name.get()
        client_address = entry_address.get()
        client_nif = entry_nif.get()
        client_movel = entry_movel.get()
        client_email = entry_email.get()

        for container in [client_name, client_address, client_nif, client_movel, client_email]:
            if not container.strip() or container.isspace():
                messagebox.showwarning("Entrada inválida", "Todos os campos devem ser preenchidos.")
                return
        if op.countOf(client_email,'@') != 1 or op.countOf(client_email, '.') < 1:
            messagebox.showwarning("Entrada inválida", "O E-mail foi preenchido de forma incorreta")
            return
        elif len(client_nif) != 9:
            messagebox.showwarning("Entrada inválida", "O NIF deve conter 9 dígitos")
            return
        elif len(client_movel) != 9:
            messagebox.showwarning("Entrada inválida", "O telemóvel deve conter 9 dígitos")
            return

        if sql.newUser(client_name, client_address, client_nif, client_movel, client_email) == "":
            tk.messagebox.showinfo(title="Sucesso",message="Utilizador criado")
            add_client_window.destroy()
        else:
            tk.messagebox.showerror(title="Erro",message="Erro ao criar user ")

    def voltar():
        add_client_window.destroy()

    add_client_window = tk.Toplevel(root)
    add_client_window.title("Adicionar Cliente")
    add_client_window.geometry("400x300")

    tk.Label(add_client_window, text="Nome").grid(row=0, column=0,padx=1, pady=1)
    entry_name = tk.Entry(add_client_window)
    entry_name.grid(row=0, column=1, padx=1, pady=1)

    tk.Label(add_client_window, text="Endereço").grid(row=1, column=0,padx=1, pady=1)
    entry_address = tk.Entry(add_client_window)
    entry_address.grid(row=1, column=1,padx=1, pady=1)

    tk.Label(add_client_window, text="NIF").grid(row=2, column=0,padx=1, pady=1)
    entry_nif = tk.Entry(add_client_window)
    entry_nif.grid(row=2, column=1,padx=1, pady=1)

    tk.Label(add_client_window, text="Telemóvel").grid(row=3, column=0,padx=1, pady=1)
    entry_movel = tk.Entry(add_client_window)
    entry_movel.grid(row=3, column=1,padx=1, pady=1)

    tk.Label(add_client_window, text="Email").grid(row=4, column=0)
    entry_email = tk.Entry(add_client_window)
    entry_email.grid(row=4, column=1,padx=1, pady=1)

    button_submit = tk.Button(add_client_window, text="Adicionar", command=submit,padx=1, pady=1)
    button_submit.grid(row=5, column=1, columnspan=2)

    button_voltar = tk.Button(add_client_window, text="Voltar", command=voltar,padx=1, pady=1)
    button_voltar.grid(row=6, column=1, columnspan=2)

# Função para procurar cliente pelo nome
def search_cliente_by_name(root):
    search_window = tk.Toplevel(root)
    search_window.title("Buscar Cliente por Nome")
    search_window.geometry("1350x300")

    def buscar():
        name = entry_name.get()
            # se o nome estiver vazio, buscar todos os users
        if not name.strip() or name.isspace(): clientes = sql.fetchAllUsers()
        else: clientes = sql.fetchUserFromName(name)
        selected = []

        for i in tree.get_children():
            tree.delete(i)

        for cliente in clientes:
            active = lambda client: "Ativo" if bool(client[7]) else "Inativo"
            tree.insert('', tk.END, values=(cliente[0], cliente[1], cliente[2], cliente[3], cliente[4], cliente[6], active(cliente)))

        if not clientes:
            messagebox.showwarning("Cliente Não Encontrado", "Nenhum cliente encontrado com o nome fornecido.",
                                   parent=search_window)
    def apagar():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Nenhum Cliente Selecionado", "Por favor, selecione um cliente para apagar.")
            return 1

        client = tree.selection()
        id_cliente = tree.item(client, 'values')[0]

        if sql.deleteUser(id_cliente) == 0:
            messagebox.showinfo("Sucesso","Cliente eliminado")
            search_window.destroy()
            return 0
        else:
            messagebox.showerror("Erro","Erro ao eliminar cliente")
            return 2

    def toggle():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Nenhum Cliente Selecionado", "Por favor, selecione um cliente para ativar/desativar.")
            return 1

        client = (tree.item(tree.selection(),'values'))
        #print(client)
        id_cliente = int(client[0])
        active = lambda obj: True if obj[6].lower() == "ativo" else False
      #  print(f'{id_cliente}/{active(client)}')


        if sql.toggleUser(id_cliente,active(client)) == 0:
            if(active(client)): messagebox.showinfo("Sucesso", "Cliente desativado")
            else: messagebox.showinfo("Sucesso", "Cliente ativado")
            buscar() # Reload de Todos
            return 0
        else:
            messagebox.showerror("Erro", "Erro ao ativar/desativar cliente")
            return 2

    def editar():
        client = tree.item(tree.selection(), 'values')
        check = lambda activ: True if activ.lower() == "ativo" else False
        if not client:
            messagebox.showerror("Erro","Nenhum cliente selecionado")
            return 1
        #print(tree.item(client,'values'))
        id_cliente = int(client[0])

        editClient(root, id_cliente)

    def voltar():
        search_window.destroy()

    tk.Label(search_window, text="Nome do cliente:").grid(row=1, column=0)
    entry_name = tk.Entry(search_window)
    entry_name.grid(row=1, column=1)

    button_buscar = tk.Button(search_window, text="Buscar", command=buscar)
    button_buscar.grid(row=0, column=2)

    button_voltar = tk.Button(search_window, text="Voltar", command=voltar)
    button_voltar.grid(row=0, column=3)

    button_delete = tk.Button(search_window, text="Apagar", command=apagar)
    button_delete.grid(row=1, column=2)

    button_edit = tk.Button(search_window, text="Editar", command=editar)
    button_edit.grid(row=1, column=3)

    button_toggle = tk.Button(search_window, text="Ativar / Desativar", command=toggle)
    button_toggle.grid(row=2, column=2, pady=2)


    columns = ('ID', 'Nome', 'Endereço', 'NIF', 'Telemóvel', 'Email', 'Ativo')
    tree = ttk.Treeview(search_window, columns=columns, show='headings')

    for col in columns: tree.heading(col, text=col)

    tree.grid(row=3, column=0, columnspan=4, pady=10, sticky='nsew')

    for i in range(8): search_window.grid_columnconfigure(i, weight=1)

    buscar()  # Load Automático


    def editClient(root, id):
        edit_window = tk.Toplevel(search_window)
        edit_window.title("Editar cliente")
        edit_window.geometry("400x400")
        messagebox.showinfo("Aviso","Preencha apenas os campos que quer editar.")

        tk.Label(edit_window, text="Nome:").grid(row=0, column=0,padx=2,pady=2)
        name_entry = tk.Entry(edit_window)
        name_entry.grid(row=0, column=1,padx=2,pady=2)

        tk.Label(edit_window, text="NIF:").grid(row=1, column=0,padx=2,pady=2)
        nif_entry = tk.Entry(edit_window)
        nif_entry.grid(row=1, column=1,padx=2,pady=2)

        tk.Label(edit_window, text="Morada:").grid(row=2, column=0,padx=2,pady=2)
        address_entry = tk.Entry(edit_window)
        address_text = tk.Text(edit_window, width=30, height=5)
        address_entry.grid(row=2, column=1,padx=2,pady=2)

        tk.Label(edit_window, text="Telemóvel:").grid(row=3, column=0,padx=2,pady=2)
        phone_entry = tk.Entry(edit_window)
        phone_entry.grid(row=3, column=1,padx=2,pady=2)

        tk.Label(edit_window, text="E-Mail:").grid(row=4, column=0)
        email_entry = tk.Entry(edit_window)
        email_entry.grid(row=4, column=1,padx=2,pady=2)


        def submit():
            trueValues = []
            args = []
            possibilities = ['nome','nif','morada','phone','email']
            values = [name_entry.get(), nif_entry.get(), address_entry.get(), phone_entry.get(), email_entry.get()]

            for i in range(0,5):
                # A string é só espaço
                if not values[i].strip() or values[i].isspace(): continue
                elif i == 1 or i == 3:
                    if len(values[i]) != 9:
                        if i == 1: messagebox.showwarning("Erro","O NIF deve conter 9 dígitos")
                        else: messagebox.showwarning("Erro", "O telemóvel deve conter 9 dígitos")
                        return
                elif i == 4:
                    if op.countOf(values[4],'@') != 1:
                        messagebox.showwarning("Erro","O E-mail foi inserido de forma incorreta")
                        return
                args.append(possibilities[i])
                trueValues.append(values[i])

            if len(trueValues) == 0: messagebox.showwarning("Preenchimento","Não preencheu nenhum campo.")
            elif sql.editUser(args, trueValues, id) == 0:
                messagebox.showinfo("Sucesso","Utilizador editado\n(Não se esqueça de atualizar a tabela clicando em 'Buscar')")
                edit_window.destroy()
            else:
                messagebox.showerror("Erro","Erro ao editar utilizador")
                edit_window.destroy()

        def cancel():
            edit_window.destroy()
            return 3 # interrupted

        tk.Button(edit_window, text="Submit", command=submit).grid(row=6, column=0, columnspan=2)
        tk.Button(edit_window, text="Cancel", command=cancel).grid(row=7, column=0, columnspan=2)

    #master.wait_window(edit_window)

# Função principal para gerir clientes
def manage_clientes(root):
    response = messagebox.askyesnocancel("Gestão de Clientes", "Selecione \"Sim\" para criar um cliente.\nSelecione \"Não\" para gerir os existentes", parent=root)
    if response:  # Se a resposta for "Sim"
        add_cliente(root)
    elif response is False:  # Se a resposta for "Não"
        search_cliente_by_name(root)

def flowers(root):
    ans = messagebox.askyesnocancel("Escolha","Clique em \"sim\" para criar uma flor nova\nClique em \"não\" para gerir as flores existentes", parent=root)


    def manager_flowers(root):
        mg_flower_window = tk.Toplevel(root)
        mg_flower_window.geometry("1020x400")
        mg_flower_window.title("Gerir Flores")


        columns = ('ID', 'Nome', 'Preço', 'Ativo', 'Criação')
        tree = ttk.Treeview(mg_flower_window, columns=columns, show='headings')

        for col in columns: tree.heading(col, text=col)

        tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')



        def search():
            flores = sql.fetchAllFlowers()

            for i in tree.get_children():
                tree.delete(i)

            for flor in flores:
                active = lambda obj: "Ativo" if bool(obj[3]) else "Inativo"
                tree.insert('', tk.END, values=(int(flor[0]),flor[1],flor[2], active(flor), flor[4]))

        def back(): mg_flower_window.destroy()

        def delete():
            if not tree.selection(): # nada foi selecionado
                messagebox.showwarning("Selecione primeiro","Não selecionou uma flor")
                return

            id = int(tree.item(tree.selection(), 'values')[0])


            if sql.deleteFlower(id) == 0:
                messagebox.showinfo("Sucesso","Flor eliminada")
                search() # refresh
            else:
                messagebox.showerror("Erro","Erro ao eliminar flor")
                search() # refresh

        def toggle():
            if not tree.selection(): # nada foi selecionado
                messagebox.showwarning("Selecione primeiro","Não selecionou uma flor")
                return

            selected = tree.item(tree.selection(), 'values')

            check = lambda obj: True if obj[3].lower() == "ativo" else False
            id = selected[0]
            active = check(selected)

            if sql.toggleFlower(id,active) == 0:
                if active: messagebox.showinfo("Sucesso","Flor desativada")
                else: messagebox.showinfo("Sucesso","Flor ativada")
                search() # refresh
            else:
                messagebox.showerror("Erro","Erro ao eliminar flor")
                search() # refresh


        search() # Auto-Load

        tk.Button(mg_flower_window, text="Eliminar Selecionado", command=delete).grid(row=6, column=0, columnspan=2,pady=2)
        tk.Button(mg_flower_window, text="Ativar/Desativar Selecionado", command=toggle).grid(row=7, column=0, columnspan=2, pady=2)
        tk.Button(mg_flower_window, text="Voltar", command=back).grid(row=8, column=0, columnspan=2,pady=2)



    def new_flower(root):
        new_flower_window = tk.Toplevel(root)
        new_flower_window.geometry("259x124")
        new_flower_window.title("Nova Flor")

        tk.Label(new_flower_window, text="Nome da Flor:").grid(row=0, column=0)
        entry_name = tk.Entry(new_flower_window)
        entry_name.grid(row=0, column=1,pady=2)

        tk.Label(new_flower_window, text="Preço").grid(row=1, column=0)
        entry_price = tk.Entry(new_flower_window)
        entry_price.grid(row=1, column=1,pady=2)

        def submit():
            if sql.newFlower(entry_name.get(),entry_price.get()) == 0:
                messagebox.showinfo("Sucesso","Flor criada")
                new_flower_window.destroy()
            else: messagebox.showerror("Erro","Erro ao criar flor")


        def voltar(): new_flower_window.destroy()

        button_submit = tk.Button(new_flower_window, text="Adicionar", command=submit)
        button_submit.grid(row=2, column=0, columnspan=2,pady=2)

        button_voltar = tk.Button(new_flower_window, text="Voltar", command=voltar)
        button_voltar.grid(row=3, column=0, columnspan=2,pady=2)

    if ans: new_flower(root)
    elif ans is False: manager_flowers(root)





class Venda:
    def __init__(self, cli, produto, valor, data, especial):
        self.cli = cli
        #self.nome = nome
        #self.nif = nif
        self.produto = produto
        self.valor = valor
        self.data = data
        self.especial = especial

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Registro de Vendas e Pagamento")
        self.geometry("400x400")

        self.vendas = []


        if skipFaceLogin: self.create_widgets()
        else: self.face_login()

    def face_login(self):
        result = attend2.faceAuth()
        wrongs = 0
        wrongLimit = 2
        while True:
            if result is True:
                self.create_widgets()
                break
            elif result is False and wrongs < wrongLimit:
                tk.messagebox.showwarning(title="Incorreto",message="A face detetada não corresponde!")
                wrongs += 1
                cv2.destroyAllWindows()
                result = attend2.faceAuth() # limpar cache / temporarios
                # se não o fizer, a camara vai disparar continuamente depois da mensagem
            elif result is False and wrongs >= wrongLimit:
                tk.messagebox.showerror(title="Login abortado",message="Demasiadas tentativas incorretas")
                cv2.destroyAllWindows()
                exit(0)
            else: pass

    def manage_sales(self):
        self.mg_sales = tk.Toplevel(self)
        self.geometry = ("400x400")
        self.title("Gestão e Consulta de Vendas")
        def voltar(): self.mg_sales.destroy()

        columns = ('ID', 'Cliente', 'Flor', 'Flor(ID)', 'Cliente(ID)', 'Preço', 'Especial','Data')
        self.tree = ttk.Treeview(self.mg_sales, columns=columns, show='headings')
        self.tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        for col in columns: self.tree.heading(col, text=col)

        def load():
            vendas = sql.fetchAllSales()
            checkUser = lambda obj: f'{obj}' if obj is not None else "<Cliente Eliminado>" # "cliente eliminado" se user for NULL
            checkID = lambda obj: f'{str(obj)}' if obj is not None else "N/A"
            isSpecial = lambda obj: "Especial" if bool(obj) else "Normal"
            dateConv = lambda stamp: datetime.strftime(stamp, '%d-%m-%y')

            for i in self.tree.get_children(): self.tree.delete(i)

            for venda in vendas:
                self.tree.insert('', tk.END, values=(
                    venda[0], checkUser(venda[1]), venda[2], venda[3], checkID(venda[4]), venda[5], isSpecial(venda[6]), dateConv(venda[7])))

        def erase():
            if not self.tree.selection():
                messagebox.showwarning("Selecione","Não selecionou uma venda para apagar")
                return 1

            selection = self.tree.item(self.tree.selection(), "values")
            if sql.deleteSale(int(selection[0])) == 0:
                messagebox.showinfo("Sucesso","Venda eliminada com sucesso")
                load()
            else: messagebox.showerror("Erro","Erro ao eliminar venda")


        self.button_del = tk.Button(self.mg_sales, text="Eliminar selecionado", command=erase)
        self.button_del.grid(row=2, column=0, columnspan=2,pady=2)

        self.button_voltar = tk.Button(self.mg_sales, text="Voltar", command=voltar)
        self.button_voltar.grid(row=3, column=0, columnspan=2,pady=2)

        load() # Auto Load

    def create_widgets(self):
        # Botão para gerir clientes
        self.btn_clientes = ttk.Button(self, text="Clientes", command=lambda: manage_clientes(self))
        self.btn_clientes.pack(pady=10)

        # Botão para abrir o formulário de vendas
        self.btn_vendas = ttk.Button(self, text="Vendas", command=self.checkVenda)
        self.btn_vendas.pack(pady=10)

        # Botão para abrir o formulário de pagamento
        self.btn_pagamento = ttk.Button(self, text="Pagamento", command=self.choosePay)
        self.btn_pagamento.pack(pady=10)

        self.btn_flores = ttk.Button(self, text="Flores", command=lambda: flowers(self)).pack(pady=10)

        self.btn_quit = ttk.Button(self, text="Log Out", command=self.log_out).pack(pady=10)

    def log_out(self):
        App.destroy(self)
        self.face_login()

    def checkVenda(self):
        ans = messagebox.askyesnocancel("Criar/editar","Selecione \"Sim\" para criar vendas\nSelecione \"não\" para consultar vendas")
        if ans: self.open_venda_form()
        elif ans is False: self.manage_sales()
        #elif ans is None: pass

    def choosePay(self):
        ans = messagebox.askyesnocancel("Pagamentos","Escolha \"Sim\" para criar um novo pagamento\nEscolha \"Não\" para gerir os pagamentos")
        if ans: self.open_pagamento_window()
        elif ans is False: self.payments_manager()
    def open_venda_form(self):
        # Criando o formulário de vendas
        self.venda_window = tk.Toplevel(self)
        self.venda_window.title("Adicionar Venda")
        self.venda_window.geometry("400x550")

        # NCliente
        self.lbl_nome = ttk.Label(self.venda_window, text="ID Cliente:")
        self.lbl_nome.grid(column=0, row=1, padx=10, pady=5)
        self.entry_cli = ttk.Entry(self.venda_window)
        self.entry_cli.grid(column=1, row=1, padx=10, pady=5)

        # Produto
        self.lbl_produto = ttk.Label(self.venda_window, text="ID Produto:")
        self.lbl_produto.grid(column=0, row=3, padx=10, pady=5)
        self.entry_produto = ttk.Entry(self.venda_window)
        self.entry_produto.grid(column=1, row=3, padx=10, pady=5)

        # Valor Venda
        self.lbl_valor = ttk.Label(self.venda_window, text="Valor Venda:")
        self.lbl_valor.grid(column=0, row=4, padx=10, pady=5)
        self.entry_valor = ttk.Entry(self.venda_window)
        self.entry_valor.grid(column=1, row=4, padx=10, pady=5)

        # Data Venda
        self.lbl_data = ttk.Label(self.venda_window, text="Data Venda:")
        self.lbl_data.grid(column=0, row=5, padx=10, pady=5)
        self.entry_data = DateEntry(self.venda_window, date_pattern='dd/MM/yyyy', locale='pt_BR')
        self.entry_data.grid(column=1, row=5, padx=10, pady=5)

        # Checkbox Especial
        self.especial_var = tk.BooleanVar()
        self.checkbox_especial = ttk.Checkbutton(self.venda_window, text="Especial", variable=self.especial_var)
        self.checkbox_especial.grid(column=0, row=6, columnspan=2, padx=10, pady=5)

        # Botão para adicionar a venda
        self.btn_add_venda = ttk.Button(self.venda_window, text="Adicionar Venda", command=self.add_venda)
        self.btn_add_venda.grid(column=0, row=7, columnspan=2, pady=10)

        # Botão de Voltar
        self.btn_voltar_venda = ttk.Button(self.venda_window, text="Voltar", command=self.venda_window.destroy)
        self.btn_voltar_venda.grid(column=0, row=8, columnspan=2, pady=10)

        # Lista de Vendas
        self.list_vendas = tk.Listbox(self.venda_window)
        self.list_vendas.grid(column=0, row=9, columnspan=2, padx=10, pady=10, sticky='nsew')

    def add_venda(self):
        try:
            cli = int(self.entry_cli.get())
            #nome = self.entry_nome.get()
            #nif = self.entry_nif.get()
            produto = int(self.entry_produto.get())
            valor = float(self.entry_valor.get())
            data = self.entry_data.get_date().strftime('%Y-%m-%d')
            especial = self.especial_var.get()
            if sql.checkUserActive(cli) == 0:
                messagebox.showerror("User Inválido","O utilizador selecionado está inativo")
                return
            elif sql.checkFlowerActive(produto) == 0:
                messagebox.showerror("Produto inválido","O produto selecionado encontra-se inativo")
                return

            out = sql.newSale(cli, produto, valor, data, especial)
            if out == 0:
                venda = Venda(cli, produto, valor, data, especial)
                self.vendas.append(venda)

                self.list_vendas.insert(tk.END,
                                        f"Cliente {venda.cli} - {venda.produto} - {venda.valor:.2f} - {venda.data} - {'Especial' if venda.especial else 'Normal'}")
            else: raise ValueError() # Acionar except ValueError

            self.clear_venda_entries()

        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao adicionar venda: {e}\nVerifique se os IDs estão corretos")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def clear_venda_entries(self):
        self.entry_cli.delete(0, tk.END)
        # self.entry_nome.delete(0, tk.END)
        # self.entry_nif.delete(0, tk.END)
        self.entry_produto.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.entry_data.set_date(date.today())
        self.especial_var.set(False)

    def payments_manager(self):
        self.pay_mgr = tk.Toplevel(self)
        self.pay_mgr.title("Gestor de Pagamentos")
        self.pay_mgr.geometry("1018x400")
        def cancel(): self.pay_mgr.destroy()


        columns = ('ID', 'ID Venda', 'Valor', 'Liquidado', 'Data')
        self.tree = ttk.Treeview(self.pay_mgr, columns=columns, show='headings')
        self.tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        for col in columns: self.tree.heading(col, text=col)

        def load():
            payments = sql.fetchPayments()
            yes_or_no = lambda obj: "Sim" if bool(obj[3]) else "Não"
            datecorrector = lambda data: datetime.strftime(data[4], '%d-%m-%y')

            for i in self.tree.get_children(): self.tree.delete(i) # limpar a tabela antes de acrescentar dados

            for payment in payments:
                self.tree.insert('', tk.END, values=(
                    int(payment[0]), int(payment[1]), float(payment[2]), yes_or_no(payment), datecorrector(payment) ))

        def erase():
            if not self.tree.selection: messagebox.showwarning("Selecione","Não selecionou nenhum pagamento")
            else:
                selection = self.tree.item(self.tree.selection(), "values")
                if sql.deletePayment(int(selection[0])) == 0:
                    messagebox.showinfo("Sucesso","Pagamento Eliminado")
                    load()

                else: messagebox.showerror("Erro","Erro na execução.")


        self.button_del = tk.Button(self.pay_mgr, text="Eliminar selecionado", command=erase)
        self.button_del.grid(row=2, column=0, columnspan=2,pady=2)

        self.button_voltar = tk.Button(self.pay_mgr, text="Voltar", command=cancel)
        self.button_voltar.grid(row=3, column=0, columnspan=2,pady=2)

        load() # Auto load


    def open_pagamento_window(self):
        # Criando a janela de pagamento
        self.pagamento_window = tk.Toplevel(self)
        self.pagamento_window.title("Detalhes do Pagamento")
        self.pagamento_window.geometry("300x250")

        # Labels e Entradas
        tk.Label(self.pagamento_window, text="ID de Venda:").grid(row=0, column=0, padx=10, pady=5)
        self.nome_produto = tk.Entry(self.pagamento_window)
        self.nome_produto.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.pagamento_window, text="Data de Pagamento:").grid(row=1, column=0, padx=10, pady=5)
        self.data_pagamento = DateEntry(self.pagamento_window, date_pattern='dd/MM/yyyy', locale='pt_BR')
        self.data_pagamento.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.pagamento_window, text="Valor a Pagar:").grid(row=2, column=0, padx=10, pady=5)
        self.valor_frame = tk.Frame(self.pagamento_window)
        self.valor_frame.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.valor_a_pagar = ttk.Entry(self.valor_frame)
        self.valor_a_pagar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.valor_euro = tk.Label(self.valor_frame, text=" €")
        self.valor_euro.pack(side=tk.LEFT)

        # Checkboxes para valor liquidado ou não
        self.liquidado_var = tk.IntVar()
        self.nao_liquidado_var = tk.IntVar()

        self.checkbox_liquidado = tk.Checkbutton(self.pagamento_window, text="Liquidado", variable=self.liquidado_var, command=self.sync_checkboxes)
        self.checkbox_liquidado.grid(row=3, column=0, padx=10, pady=5)

        self.checkbox_nao_liquidado = tk.Checkbutton(self.pagamento_window, text="Não Liquidado", variable=self.nao_liquidado_var, command=self.sync_checkboxes)
        self.checkbox_nao_liquidado.grid(row=3, column=1, padx=10, pady=5)

        # Botão de Submissão
        self.submit_button = tk.Button(self.pagamento_window, text="Submeter", command=self.submit_pagamento)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Botão de Voltar
        self.btn_voltar_pagamento = ttk.Button(self.pagamento_window, text="Voltar", command=self.pagamento_window.destroy)
        self.btn_voltar_pagamento.grid(row=5, column=0, columnspan=2, pady=10)

    def sync_checkboxes(self):
        if self.liquidado_var.get() == 1:
            self.nao_liquidado_var.set(0)
        elif self.nao_liquidado_var.get() == 1:
            self.liquidado_var.set(0)

    def submit_pagamento(self):
        nome_produto = self.nome_produto.get()
        data_pagamento = self.data_pagamento.get_date()
        valor_a_pagar = self.valor_a_pagar.get()
        liquidado = self.liquidado_var.get()
        nao_liquidado = self.nao_liquidado_var.get()


        if not nome_produto or not data_pagamento or not valor_a_pagar:
            messagebox.showwarning("Campos Vazios", "Todos os campos devem ser preenchidos.")
            return
        elif liquidado == 0 and nao_liquidado == 0: # user esqueceu-se de preencher
            messagebox.showwarning("Liquidez","Selecione \"Liquidado\" ou \"Não Liquidado\" nas opções")
            return

        data_pagamento = datetime.strftime(data_pagamento, '%y-%m-%d') # Conversão da data
        status_pagamento = "Liquidado" if liquidado else "Não Liquidado"

        # # Aqui você pode fazer o processamento dos dados, como salvar em um banco de dados ou arquivo
        # messagebox.showinfo("Informações do Pagamento",
        #                     f"Produto: {nome_produto}\nData de Pagamento: {data_pagamento}\nValor: {valor_a_pagar}€\nStatus: {status_pagamento}")

        if sql.newPayment(int(nome_produto), float(valor_a_pagar), bool(liquidado), data_pagamento) == 0:
            messagebox.showinfo("Registado","Pagamento registado")
            self.pagamento_window.destroy()
            return 0
        else:
            messagebox.showerror("Erro","Falha ao registar pagamento")





if __name__ == "__main__":
    if sql.testConnection() == "":
        app = App()
        app.mainloop()

    else: messagebox.showerror("Falha no arranque","O sistema não conseguiu ligar ao servidor da base de dados.\nVerifique a ligação à internet e tente de novo")