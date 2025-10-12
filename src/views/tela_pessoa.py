from views.tela_base import TelaBase


class TelaPessoa(TelaBase):
    def le_opcao(self):
        opcoes = {1: "Incluir", 2: "Listar", 3: "Excluir", 4: "Editar"}
        self.tela_opcoes("PESSOAS", opcoes)
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_entidade(self, dados_atuais=None):
        self.limpar_tela()
        print("\n-------- DADOS PESSOA --------")

        nome_atual = dados_atuais["nome"] if dados_atuais else ""
        celular_atual = dados_atuais["celular"] if dados_atuais else ""
        identificacao_atual = dados_atuais["identificacao"] if dados_atuais else ""
        idade_atual = dados_atuais["idade"] if dados_atuais else ""

        nome = input(f"Nome [{nome_atual}]: ") or nome_atual
        celular = input(f"Celular [{celular_atual}]: ") or celular_atual
        identificacao = (
            input(f"Identificação (CPF) [{identificacao_atual}]: ")
            or identificacao_atual
        )
        idade_input = input(f"Idade [{idade_atual}]: ") or str(idade_atual)
        idade = int(idade_input)

        return {
            "nome": nome,
            "celular": celular,
            "identificacao": identificacao,
            "idade": idade,
        }

    def mostra_entidade(self, dados_pessoa):
        print("ID:", dados_pessoa["id"])
        print("Nome:", dados_pessoa["nome"])
        print("Identificação:", dados_pessoa["identificacao"])
        print("Idade:", dados_pessoa["idade"])
        print("Celular:", dados_pessoa["celular"])
        print("--------------------")

    def seleciona_entidade(self):
        id = input("ID da pessoa que deseja selecionar: ")
        return id
