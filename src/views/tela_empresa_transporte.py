from views.tela_base import TelaBase


class TelaEmpresaTransporte(TelaBase):
    def le_opcao(self):
        opcoes = {1: "Incluir", 2: "Listar", 3: "Excluir", 4: "Editar"}
        self.tela_opcoes("EMPRESAS DE TRANSPORTE", opcoes)
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_entidade(self, dados_atuais=None):
        self.limpar_tela()
        print("\n-------- DADOS EMPRESA DE TRANSPORTE --------")

        nome_atual = dados_atuais["nome"] if dados_atuais else ""
        cnpj_atual = dados_atuais["cnpj"] if dados_atuais else ""
        telefone_atual = dados_atuais["telefone"] if dados_atuais else ""

        nome = input(f"Nome da empresa [{nome_atual}]: ") or nome_atual
        cnpj = input(f"CNPJ [{cnpj_atual}]: ") or cnpj_atual
        telefone = input(f"Telefone [{telefone_atual}]: ") or telefone_atual

        return {
            "nome": nome,
            "cnpj": cnpj,
            "telefone": telefone,
        }

    def mostra_entidade(self, dados_empresa):
        print("ID:", dados_empresa["id"])
        print("Nome:", dados_empresa["nome"])
        print("CNPJ:", dados_empresa["cnpj"])
        print("Telefone:", dados_empresa["telefone"])
        print("--------------------")

    def seleciona_entidade(self):
        id = input("ID da empresa que deseja selecionar: ")
        return id
