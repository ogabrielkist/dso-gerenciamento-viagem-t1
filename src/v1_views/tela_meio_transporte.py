from views.tela_base import TelaBase
from models.meio_transporte import TipoTransporte


class TelaMeioTransporte(TelaBase):
    def __init__(self):
        super().__init__()
        self._controlador_empresa = None

    def set_controlador_empresa(self, controlador_empresa):
        self._controlador_empresa = controlador_empresa

    def le_opcao(self):
        opcoes = {1: "Incluir", 2: "Listar", 3: "Excluir", 4: "Editar"}
        self.tela_opcoes("MEIOS DE TRANSPORTE", opcoes)
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_entidade(self, dados_atuais=None):
        self.limpar_tela()
        print("\n-------- DADOS MEIO DE TRANSPORTE --------")

        print("\nTipos de transporte disponíveis:")
        tipos = list(TipoTransporte)
        for i, tipo in enumerate(tipos, 1):
            print(f"{i} - {tipo.value}")

        tipo_atual = dados_atuais["tipo"] if dados_atuais else None
        tipo_atual_index = None
        if tipo_atual:
            for i, tipo in enumerate(tipos):
                if tipo == tipo_atual:
                    tipo_atual_index = i + 1
                    break

        if tipo_atual_index:
            print(f"Tipo atual: {tipo_atual_index} - {tipo_atual.value}")
            opcao_tipo_input = input(
                f"Escolha o tipo (número) [{tipo_atual_index}]: "
            ) or str(tipo_atual_index)
        else:
            opcao_tipo_input = input("Escolha o tipo (número): ")

        opcao_tipo = int(opcao_tipo_input) - 1
        if opcao_tipo < 0 or opcao_tipo >= len(tipos):
            raise ValueError("Opção de tipo inválida.")

        tipo_selecionado = tipos[opcao_tipo]

        print("\nEmpresas disponíveis:")
        empresas = self._controlador_empresa._entidades
        for i, empresa in enumerate(empresas, 1):
            print(f"{i} - {empresa.nome}")

        if not empresas:
            raise ValueError(
                "Nenhuma empresa cadastrada. Cadastre uma empresa primeiro."
            )

        empresa_atual = dados_atuais["empresa"] if dados_atuais else None
        empresa_atual_index = None
        if empresa_atual:
            for i, empresa in enumerate(empresas):
                if empresa.id == empresa_atual.id:
                    empresa_atual_index = i + 1
                    break

        if empresa_atual_index:
            print(f"Empresa atual: {empresa_atual_index} - {empresa_atual.nome}")
            opcao_empresa_input = input(
                f"Escolha a empresa (número) [{empresa_atual_index}]: "
            ) or str(empresa_atual_index)
        else:
            opcao_empresa_input = input("Escolha a empresa (número): ")

        opcao_empresa = int(opcao_empresa_input) - 1
        if opcao_empresa < 0 or opcao_empresa >= len(empresas):
            raise ValueError("Opção de empresa inválida.")

        empresa_selecionada = empresas[opcao_empresa]

        return {
            "tipo": tipo_selecionado,
            "empresa": empresa_selecionada,
        }

    def mostra_entidade(self, dados_meio_transporte):
        print("ID:", dados_meio_transporte["id"])
        print("Tipo:", dados_meio_transporte["tipo"].value)
        print("Empresa:", dados_meio_transporte["empresa"].nome)
        print("CNPJ:", dados_meio_transporte["empresa"].cnpj)
        print("--------------------")

    def seleciona_entidade(self):
        id = input("ID do meio de transporte que deseja selecionar: ")
        return id
