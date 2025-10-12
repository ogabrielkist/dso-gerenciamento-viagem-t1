from views.tela_base import TelaBase


class TelaPais(TelaBase):
    def le_opcao(self):
        opcoes = {1: "Incluir", 2: "Listar", 3: "Excluir", 4: "Editar"}
        self.tela_opcoes("PAÍSES", opcoes)
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_entidade(self, dados_atuais=None):
        self.limpar_tela()
        print("\n-------- DADOS PAÍS --------")

        nome_atual = dados_atuais["nome"] if dados_atuais else ""
        nome = input(f"Nome do país [{nome_atual}]: ") or nome_atual

        return {
            "nome": nome,
        }

    def mostra_entidade(self, dados_pais):
        print("ID:", dados_pais["id"])
        print("Nome:", dados_pais["nome"])
        print("--------------------")

    def seleciona_entidade(self):
        id = input("ID do país que deseja selecionar: ")
        return id
