import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI
from models.utils.validadores import (
    formata_cpf,
    formata_telefone,
    normaliza_cpf,
    normaliza_telefone,
)


class TelaPessoaGUI(TelaBaseGUI):

    def __init__(self):
        super().__init__()

    def le_opcao(self) -> str | None:
        layout = [
            [
                sg.Text(
                    "Gerenciamento de Pessoas",
                    font=("Helvetica", 18),
                    justification="center",
                    expand_x=True,
                )
            ],
            [sg.Button("Incluir Pessoa", key="-INCLUIR-", size=(20, 2), pad=(5, 5))],
            [sg.Button("Listar Pessoas", key="-LISTAR-", size=(20, 2), pad=(5, 5))],
            [sg.Button("Editar Pessoa", key="-EDITAR-", size=(20, 2), pad=(5, 5))],
            [sg.Button("Excluir Pessoa", key="-EXCLUIR-", size=(20, 2), pad=(5, 5))],
            [sg.VPush()],
            [sg.Button("Voltar", key="-VOLTAR-", size=(20, 2), pad=(5, (15, 5)))],
        ]

        window = sg.Window(
            "Menu Pessoa", layout, element_justification="center", finalize=True
        )

        event, values = window.read()
        window.close()

        if event == sg.WIN_CLOSED:
            return "-VOLTAR-"

        return event

    def pega_dados_entidade(self, dados_atuais: dict = None) -> dict | None:
        nome = dados_atuais["nome"] if dados_atuais else ""
        celular = formata_telefone(dados_atuais["celular"]) if dados_atuais else ""
        identificacao = (
            formata_cpf(dados_atuais["identificacao"]) if dados_atuais else ""
        )
        idade = dados_atuais["idade"] if dados_atuais else ""

        titulo_janela = "Editar Pessoa" if dados_atuais else "Incluir Nova Pessoa"

        layout = [
            [sg.Text(titulo_janela, font=("Helvetica", 16))],
            [sg.Text("Nome:", size=(12, 1)), sg.Input(nome, key="-NOME-")],
            [sg.Text("Celular:", size=(12, 1)), sg.Input(celular, key="-CELULAR-")],
            [
                sg.Text("Identificação (CPF):", size=(12, 1)),
                sg.Input(identificacao, key="-ID-"),
            ],
            [sg.Text("Idade:", size=(12, 1)), sg.Input(idade, key="-IDADE-")],
            [sg.Button("OK", key="-OK-"), sg.Button("Cancelar", key="-CANCELAR-")],
        ]

        window = sg.Window(titulo_janela, layout, finalize=True)

        dados = None
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == "-CANCELAR-":
                break

            if event == "-OK-":
                try:
                    idade_int = int(values["-IDADE-"])
                    cpf_normalizado = normaliza_cpf(values["-ID-"])
                    celular_normalizado = normaliza_telefone(values["-CELULAR-"])

                    dados = {
                        "nome": values["-NOME-"],
                        "celular": celular_normalizado,
                        "identificacao": cpf_normalizado,
                        "idade": idade_int,
                    }

                    break

                except ValueError as err:
                    self.mostra_erro(str(err))
                except Exception as e:
                    self.mostra_erro(f"Erro ao processar dados: {e}")

        window.close()

        return dados

    def mostra_lista_entidades(self, dados_lista: list):
        if not dados_lista:
            self.mostra_mensagem("Aviso", "Nenhuma pessoa cadastrada.")
            return

        headings = ["ID", "Nome", "Celular", "Identificação (CPF)", "Idade"]

        data = [
            [
                d["id"],
                d["nome"],
                formata_telefone(d["celular"]),
                formata_cpf(d["identificacao"]),
                d["idade"],
            ]
            for d in dados_lista
        ]

        layout = [
            [sg.Text("Lista de Pessoas Cadastradas", font=("Helvetica", 16))],
            [
                sg.Table(
                    values=data,
                    headings=headings,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    num_rows=min(20, len(data)),
                    key="-TABELA-",
                )
            ],
            [sg.Button("OK", key="-OK-")],
        ]

        window = sg.Window("Listagem de Pessoas", layout, finalize=True, resizable=True)
        window.read()
        window.close()

    def seleciona_entidade(self, dados_lista: list, titulo_janela: str) -> str | None:
        if not dados_lista:
            self.mostra_erro("Não há pessoas cadastradas para selecionar.")
            return None

        headings = ["ID", "Nome", "Celular", "Identificação (CPF)", "Idade"]

        data = []
        id_lookup = []

        for d in dados_lista:
            data.append(
                [
                    d["id"],
                    d["nome"],
                    formata_telefone(d["celular"]),
                    formata_cpf(d["identificacao"]),
                    d["idade"],
                ]
            )
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
                    self.mostra_erro("Por favor, selecione uma pessoa da lista.")

        window.close()

        return id_selecionado
