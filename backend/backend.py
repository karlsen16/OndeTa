import psycopg2
# user:adminondeta
# senha:admin
# db:ondeta_db

conn = psycopg2.connect(
    host="localhost",
    database="ondeta_db",
    user="adminondeta",
    password="admin"
)

cursor = conn.cursor()

def inserir(login, animal, local):
    cursor.execute(
        "INSERT INTO animais_perdidos (login, animal, local) VALUES (%s, %s, %s)",
        (login, animal, local)
    )
    conn.commit()
    print("Cadastro inserido!")


def listar():
    cursor.execute("SELECT * FROM animais_perdidos")
    registros = cursor.fetchall()

    for r in registros:
        print(r)


def atualizar(id, login, animal, local):
    cursor.execute(
        "UPDATE animais_perdidos SET login=%s, animal=%s, local=%s WHERE id=%s",
        (login, animal, local, id)
    )
    conn.commit()
    print("Cadastro atualizado!")


def deletar(id):
    cursor.execute(
        "DELETE FROM animais_perdidos WHERE id=%s",
        (id,)
    )
    conn.commit()
    print("Cadastro deletado!")


def menu():
    while True:
        print("\n1 - Inserir")
        print("2 - Listar")
        print("3 - Atualizar")
        print("4 - Deletar")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            login = input("Login: ")
            animal = input("Animal (gato/cachorro): ")
            local = input("Local: ")
            inserir(login, animal, local)

        elif opcao == "2":
            listar()

        elif opcao == "3":
            id = int(input("ID do cadastro: "))
            login = input("Novo login: ")
            animal = input("Animal (gato/cachorro): ")
            local = input("Local: ")
            atualizar(id, login, animal, local)

        elif opcao == "4":
            id = int(input("ID do cadastro: "))
            deletar(id)

        elif opcao == "0":
            break


menu()

cursor.close()
conn.close()