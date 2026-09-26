import sqlite3

conexao = sqlite3.connect('produtos.db')
cursor = conexao.cursor()

cursor.execute("""
    create table if not exists produtos (
        id integer primary key autoincrement,
        nome text not null,
        quantidade int,
        preco real
        )
""")
conexao.commit()

class Produtos:
    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def salvar(self):
        cursor.execute(
            "insert into produtos (nome, quantidade, preco) values (?, ?, ?)",
            (self.nome, self.quantidade, self.preco)
        )
        conexao.commit()

primeira_vez = True

while True:
    if not primeira_vez:
        print()
        cont = input(str('voce deseja continuar com o programa? [s/n]')).upper()
        if cont == 'N':
            print()
            print('ATE O PROXIMO PRODUTO!')
            break
        elif cont != 'S':
            print('Opção invalida')
            continue

    primeira_vez = False

    print('''
    Adicionar um novo produto          [1]
    Ver produtos existentes            [2]
    Alterar a quantidade de um produto [3]
    Deletar produto                    [4]
    Produtos com o estoque baixo       [5]
    Valor total em estoque             [6]
    '''))

    opcao = input(str('qual opção você deseja escolher? '))
    print() 
    if opcao == '1':
        nome = input('Digite o nome do produto: ')
        quantidade = float(input('Digite a quantidade de produtos: '))
        preco = float(input('Digite o valor do produto: '))
        produto = Produtos(nome, quantidade, preco)
        produto.salvar()
        print('Produto salvo')

    elif opcao == '2':
        cursor.execute("select * from produtos")
        resultado = cursor.fetchall()

        for produto in resultado:
            print(f"{produto[0]} - {produto[1]} - Qtd: {produto[2]} - Preço: R${produto[3]}")

    elif opcao == '3':
        qnt_alterar = input('Qual produto você deseja alterar a quantidade?')
        nova_qnt = float(input('Nova quantidade: '))

        cursor.execute(
            "update produtos SET quantidade = ? where nome = ?",
            (nova_qnt, qnt_alterar)
        )
        conexao.commit()
        print('quantidade atualizada!')

    elif opcao == '4':
        nome_apagar = input('Qual produto você deseja deletar? ')

        cursor.execute(
            "delete from produtos where nome = ?",
            (nome_apagar,)
        )
        conexao.commit()
        print()
        print('produto deletado!')

    elif opcao == '5':
        cursor.execute("select * from produtos where quantidade <= 5")
        resultado = cursor.fetchall()
        
        for produto in resultado:
            print(f"{produto[0]} - {produto[1]} - Qtd: {produto[2]} - Preço: R${produto[3]}")

    elif opcao == '6':
        cursor.execute("select * from produtos")
        resultado = cursor.fetchall()

        soma = 0
        for produto in resultado:
            total = produto[2] * produto[3]
            soma += total
            print(f'o valor total do estoque de {produto[1]} e de R${total}')
        print()
        print(f'o valor total do estoque e de R${soma}')

    elif opcao == 'delete':
        cursor.execute("delete from produtos")
        cursor.execute("delete from sqlite_sequence where name='produtos'")
        conexao.commit()
        print('Banco resetado!')

    else:
        print('Opção invalida!')

conexao.close()