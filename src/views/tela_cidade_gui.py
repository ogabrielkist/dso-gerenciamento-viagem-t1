import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI
from models.pais import Pais


class TelaCidadeGUI(TelaBaseGUI):
    def __init__(self, titulo: str = "Cidades"):
        super().__init__()
        self._titulo = titulo

    def le_opcao(self) -> str | None:
        layout = [
            [
                sg.Text(
                    f"Gerenciamento de {self._titulo}",
                    font=("Helvetica", 18),
                    justification="center",
                    expand_x=True,
                )
            ],
            [
                sg.Button(
                    f"Incluir {self._titulo[:-1] if self._titulo.endswith('s') else self._titulo}",
                    key="-INCLUIR-",
                    size=(20, 2),
                    pad=(5, 5),
                )
            ],
            [
                sg.Button(
                    f"Listar {self._titulo}", key="-LISTAR-", size=(20, 2), pad=(5, 5)
                )
            ],
            [
                sg.Button(
                    f"Editar {self._titulo[:-1] if self._titulo.endswith('s') else self._titulo}",
                    key="-EDITAR-",
                    size=(20, 2),
                    pad=(5, 5),
                )
            ],
            [
                sg.Button(
                    f"Excluir {self._titulo[:-1] if self._titulo.endswith('s') else self._titulo}",
                    key="-EXCLUIR-",
                    size=(20, 2),
                    pad=(5, 5),
                )
            ],
            [sg.VPush()],
            [sg.Button("Voltar", key="-VOLTAR-", size=(20, 2), pad=(5, (15, 5)))],
        ]

        window = sg.Window(
            "Menu Cidade", layout, element_justification="center", finalize=True
        )

        event, values = window.read()
        window.close()

        if event == sg.WIN_CLOSED:
            return "-VOLTAR-"

        return event

    def pega_dados_entidade(
        self, lista_paises: list[Pais], dados_atuais: dict = None
    ) -> dict | None:
        if not lista_paises:
            self.mostra_erro(
                "Não é possível adicionar uma cidade pois não há países cadastrados."
            )
            return None

        mapa_pais_obj = {pais.nome: pais for pais in lista_paises}
        nomes_paises = list(mapa_pais_obj.keys())
        nome_atual = dados_atuais["nome"] if dados_atuais else ""
        pais_atual_nome = dados_atuais["pais"].nome if dados_atuais else nomes_paises[0]

        item_label = self._titulo[:-1] if self._titulo.endswith("s") else self._titulo
        titulo_janela = (
            f"Editar {item_label}" if dados_atuais else f"Incluir Novo(a) {item_label}"
        )

        layout = [
            [sg.Text(titulo_janela, font=("Helvetica", 16))],
            [sg.Text("Nome:", size=(8, 1)), sg.Input(nome_atual, key="-NOME-")],
            [
                sg.Text("País:", size=(8, 1)),
                sg.Combo(
                    nomes_paises,
                    default_value=pais_atual_nome,
                    readonly=True,
                    key="-PAIS-",
                ),
            ],
            [sg.Button("OK", key="-OK-"), sg.Button("Cancelar", key="-CANCELAR-")],
        ]

        window = sg.Window(titulo_janela, layout, finalize=True)

        dados = None
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == "-CANCELAR-":
                break

            if event == "-OK-":
                if not values["-NOME-"]:
                    self.mostra_erro("O campo 'Nome' não pode estar vazio.")
                    continue

                nome_pais_selecionado = values["-PAIS-"]
                pais_obj_selecionado = mapa_pais_obj[nome_pais_selecionado]

                dados = {"nome": values["-NOME-"], "pais": pais_obj_selecionado}
                break

        window.close()

        return dados

    def mostra_lista_entidades(self, dados_lista: list):
        """
        Mostra TODAS as cidades em uma janela com uma tabela.
        """
        if not dados_lista:
            self.mostra_mensagem(
                "Aviso",
                f"Nenhum(a) {self._titulo[:-1] if self._titulo.endswith('s') else self._titulo} cadastrado(a).",
            )
            return

        headings = ["ID", "Nome", "País"]

        data = [[d["id"], d["nome"], d["pais"].nome] for d in dados_lista]

        layout = [
            [sg.Text("Lista de Cidades Cadastradas", font=("Helvetica", 16))],
            [
                sg.Table(
                    values=data,
                    headings=headings,
                    auto_size_columns=True,
                    justification="left",
                    num_rows=min(20, len(data)),
                    key="-TABELA-",
                )
            ],
            [sg.Button("OK", key="-OK-")],
        ]

        window = sg.Window("Listagem de Cidades", layout, finalize=True, resizable=True)
        window.read()
        window.close()

    def seleciona_entidade(self, dados_lista: list, titulo_janela: str) -> str | None:
        if not dados_lista:
            self.mostra_erro(
                f"Não há {self._titulo.lower()} cadastrados para selecionar."
            )
            return None

        headings = ["ID", "Nome", "País"]

        data = []
        id_lookup = []

        for d in dados_lista:
            data.append([d["id"], d["nome"], d["pais"].nome])
            id_lookup.append(d["id"])

        layout = [
            [sg.Text(titulo_janela, font=("Helvetica", 16))],
            [
                sg.Table(
                    values=data,
                    headings=headings,
                    auto_size_columns=True,
                    num_rows=min(15, len(data)),
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    enable_events=True,
                    key="-TABELA-",
                )
            ],
            [
                sg.Button("Confirmar", key="-OK-"),
                sg.Button("Cancelar", key="-CANCELAR-"),
            ],
        ]

        window = sg.Window(titulo_janela, layout, finalize=True)

        id_selecionado = None
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == "-CANCELAR-":
                break

            if event == "-OK-":
                if values["-TABELA-"]:
                    row_index = values["-TABELA-"][0]
                    id_selecionado = id_lookup[row_index]
                    break
                else:
                    self.mostra_erro("Por favor, selecione uma cidade da lista.")

        window.close()

        return id_selecionado
