from views.tela_base import TelaBase


class TelaCidade(TelaBase):
    def __init__(self):
        super().__init__()
        self._controlador_pais = None

    def set_controlador_pais(self, controlador_pais):
        self._controlador_pais = controlador_pais

    def le_opcao(self):
        opcoes = {1: "Incluir", 2: "Listar", 3: "Excluir", 4: "Editar"}
        self.tela_opcoes("CIDADES", opcoes)
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_entidade(self, dados_atuais=None):
        self.limpar_tela()
        print("\n-------- DADOS CIDADE --------")

        nome_atual = dados_atuais["nome"] if dados_atuais else ""
        nome = input(f"Nome da cidade [{nome_atual}]: ") or nome_atual

        print("\nPaíses disponíveis:")
        paises = self._controlador_pais._entidades
        for i, pais in enumerate(paises, 1):
            print(f"{i} - {pais.nome}")

        if not paises:
            raise ValueError("Nenhum país cadastrado. Cadastre um país primeiro.")

        pais_atual = dados_atuais["pais"] if dados_atuais else None
        pais_atual_index = None
        if pais_atual:
            for i, pais in enumerate(paises):
                if pais.id == pais_atual.id:
                    pais_atual_index = i + 1
                    break

        if pais_atual_index:
            print(f"País atual: {pais_atual_index} - {pais_atual.nome}")
            opcao_pais_input = input(
                f"Escolha o país (número) [{pais_atual_index}]: "
            ) or str(pais_atual_index)
        else:
            opcao_pais_input = input("Escolha o país (número): ")

        opcao_pais = int(opcao_pais_input) - 1
        if opcao_pais < 0 or opcao_pais >= len(paises):
            raise ValueError("Opção de país inválida.")

        pais_selecionado = paises[opcao_pais]

        return {
            "nome": nome,
            "pais": pais_selecionado,
        }

    def mostra_entidade(self, dados_cidade):
        print("ID:", dados_cidade["id"])
        print("Nome:", dados_cidade["nome"])
        print("País:", dados_cidade["pais"].nome)
        print("--------------------")

    def seleciona_entidade(self):
        id = input("ID da cidade que deseja selecionar: ")
        return id
