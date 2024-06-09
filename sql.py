import mysql.connector, io, os
from datetime import datetime
from PIL import Image

__h = "suricatingss.xyz"
__u = "pycharm"
__p = "QH!Wd2YFiL._Ghfv"
__d = "python_final"
def testConnection():
    try:
        mysql.connector.connect( host=__h, user=__u, password=__p, database=__d )
        return ""
    except Exception as ex: return f"Erro, {ex.args}"

def newUser(name, address, nif, phone, email):
    schema = mysql.connector.connect( host=__h, user=__u, password=__p, database=__d )
    query = ""
    with schema.cursor() as sqlcmd:
        query = "INSERT INTO clientes (nome,morada,nif,phone,email) VALUES (%s,%s,%s,%s,%s);"
        data = [name, address, nif, phone, email]
        try:
            sqlcmd.execute(query,data)
            schema.commit()
            return ""
        except Exception as ex:
            return f"Exception! {ex.args}"

def fetchLastID():
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)
    with schema.cursor() as cmd:
        query = "SELECT COUNT(id) FROM CLIENTES;"
        cmd.execute(query)
        return cmd.fetchone()[0]

def recordAuth(name):
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)
    query = f"INSERT INTO staff_records (name) VALUES ('{name}')"
    try:
        with schema.cursor() as cmd:
            cmd.execute(query)
            schema.commit()
        return ""
    except Exception as ex:
        print(ex.args)
        return f"{ex.args}"


def deleteUser(userID):
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)
    query = f"DELETE FROM clientes WHERE id = {userID};"
    try:
        with schema.cursor() as cmd:
            cmd.execute(query)
        schema.commit()
        return 0
    except: return 1

def fetchUserFromName(name):
    query = f"SELECT * FROM clientes WHERE nome REGEXP '{name}'"
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)
    try:
        with schema.cursor() as cmd:
            cmd.execute(query)
            return cmd.fetchall()
    except:
        return []

def fetchAllUsers():
    query = "SELECT * FROM clientes"
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)
    try:
        with schema.cursor() as cmd:
            cmd.execute(query)
            return cmd.fetchall()
    except:
        return []

def editUser(fields, values, id):
    # cód. erro
    # 0 - sucesso
    # 1 - argumentos
    # 2 - query
    if len(fields) != len(values): return 1 # cód erro argumentos
    query = "UPDATE clientes SET "
    for index in range(0, len(fields)):
        if index != 0: query += ", "
        # acrescentar vírgula no caso de não ser o primeiro argumento
        query += f"{fields[index]} = "
        if fields[index] == 'nif' or fields[index] == 'ativo' or fields[index] == 'phone': query += f"{values[index]}"
        else: query += f"'{values[index]}'"

    query += f" WHERE id = {id}"
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)
    #print(query)
    try:
        with schema.cursor() as cmd: cmd.execute(query)
        schema.commit()
        return 0
    except: return 2

def toggleUser(id, state):
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)
    state = not state  # inverter
    query = f"UPDATE clientes SET ativo = {state} WHERE id = {id}"

    with schema.cursor() as cmd:
        try:
            cmd.execute(query)
            schema.commit()
            return 0
        except:
            return 2

def fetchAllSales():
    query= ("SELECT compras.id, clientes.nome, flores.nome, compras.id_flor, compras.id_cliente, compras.valor, compras.especial, compras.data FROM compras"
            " LEFT JOIN clientes ON clientes.id = compras.id_cliente LEFT JOIN flores ON flores.id = compras.id_flor")

    with mysql.connector.connect(host=__h, user=__u, password=__p, database=__d) as schema:
        with schema.cursor() as cmd:
            try:
                cmd.execute(query)
                return cmd.fetchall()
            except: return []


def fetchAllFlowers():
    query = "SELECT * FROM flores"
    with mysql.connector.connect(host=__h, user=__u, password=__p, database=__d) as schema:
        with schema.cursor() as cmd:
            try:
                cmd.execute(query)
                return cmd.fetchall()
            except: return []


def fetchFilteredFlowers(name):
    query = f"SELECT * FROM flores WHERE name LIKE '{name}'"
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)

    with schema.cursor() as cmd:
        try:
            cmd.execute(query)
            return cmd.fetchall()
        except: return []

def fetchAllFlowers():
    query = "SELECT * FROM flores"
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)

    with schema.cursor() as cmd:
        try:
            cmd.execute(query)
            return cmd.fetchall()
        except: return []

def newSale(client, product, price,date, special):
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)

    query = ("INSERT INTO compras (id_cliente, id_flor, valor, especial, `data`) VALUES ("
             f"{client}, {product}, {price}, {special}, '{date}')")
    #print(query)

    with schema.cursor() as cmd:
        try:
            cmd.execute(query)
            schema.commit()
            return 0
        except: return 2

def fetchPayments():
    query = "SELECT * FROM pagamentos"
    with mysql.connector.connect(host=__h, user=__u, password=__p, database=__d) as schema:
        with schema.cursor() as cmd:
            try:
                cmd.execute(query)
                return cmd.fetchall()
            except: return []

def deletePayment(id):
    query = f"DELETE FROM pagamentos WHERE id = {id}"
    with mysql.connector.connect(host=__h, user=__u, password=__p, database=__d) as schema:
        with schema.cursor() as cmd:
            try:
                cmd.execute(query)
                schema.commit()
                return 0
            except:
                return 2

def newPayment(venda, preco, pago, data):
    query = "INSERT INTO pagamentos (id_venda, valor, pago, data) VALUES (%s,%s,%s,%s)"

    data = [venda, preco, pago, data]
    with mysql.connector.connect(host=__h, user=__u, password=__p, database=__d) as schema:
        with schema.cursor() as cmd:
            try:
                cmd.execute(query,data)
                schema.commit()
                return 0
            except:
                return 2


def newSale(cliente, prod, preco, data, special):
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)
    query = ("INSERT INTO compras (id_cliente, id_flor, valor, especial, data) "
             f"VALUES ({cliente},{prod},{preco},{special},'{data}')")

    with schema.cursor() as cmd:
        try:
            cmd.execute(query)
            schema.commit()
            return 0
        except: return 2

def deleteSale(id):
    query = f"DELETE FROM compras WHERE compras.id = {id}"
    with mysql.connector.connect(host=__h, user=__u, password=__p, database=__d) as schema:
        with schema.cursor() as cmd:
            try:
                cmd.execute(query)
                schema.commit()
                return 0
            except: return 2

def deleteFlower(id):
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)
    query = f"DELETE FROM flores WHERE flores.id = {id}"
    with schema.cursor() as cmd:
        try:
            cmd.execute(query)
            schema.commit()
            return 0
        except: return 2

def toggleFlower(id, state):
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)
    state = not state # inverter
    query = f"UPDATE flores SET ativo = {state} WHERE id = {id}"

    with schema.cursor() as cmd:
        try:
            cmd.execute(query)
            schema.commit()
            return 0
        except: return 2

def newFlower(name,price):
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)
    query = f"INSERT INTO flores (nome,preco) VALUES (%s,%s)"
    values = [name,price]

    with schema.cursor() as cmd:
        try:
            cmd.execute(query,values)
            schema.commit()
            return 0
        except: return 2

def checkUserActive(id):
    query = f"SELECT ativo FROM clientes WHERE id = {id}"
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)

    with schema.cursor() as cmd:
        try:
            cmd.execute(query)
            return int(cmd.fetchone()[0])
        except: return 2

def checkFlowerActive(id):
    query = f"SELECT ativo FROM flores WHERE id = {id}"
    schema = mysql.connector.connect(host=__h, user=__u, password=__p, database=__d)

    with schema.cursor() as cmd:
        try:
            cmd.execute(query)
            return int(cmd.fetchone()[0])
        except: return 2




if __name__ == "__main__":
    teste = testConnection()
    if teste == "": print("sucesso")
    else: print(teste)



