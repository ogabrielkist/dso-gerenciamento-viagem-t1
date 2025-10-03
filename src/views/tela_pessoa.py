class TelaPessoa:
    def tela_opcoes(self):
        print("\n-------- PESSOAS --------")
        print("Escolha a opção")
        print("1 - Incluir Pessoa")
        print("2 - Listar Pessoas")
        print("3 - Excluir Pessoa")
        print("0 - Retornar")

        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_pessoa(self):
        print("\n-------- DADOS PESSOA --------")
        nome = input("Nome: ")
        celular = input("Celular: ")
        identificacao = input("Identificação (CPF): ")
        idade = int(input("Idade: "))
        return {"nome": nome, "celular": celular, "identificacao": identificacao, "idade": idade}

    def mostra_pessoa(self, dados_pessoa):
        print("Nome:", dados_pessoa["nome"])
        print("Identificação:", dados_pessoa["identificacao"])
        print("Idade:", dados_pessoa["idade"])
        print("Celular:", dados_pessoa["celular"])
        print("--------------------")
    
    def seleciona_pessoa(self):
        identificacao = input("Identificação da pessoa que deseja selecionar: ")
        return identificacao

    def mostra_mensagem(self, msg):
        print(msg)
