import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI


class TelaEmpresaTransporteGUI(TelaBaseGUI):
    def __init__(self):
        super().__init__()

    def le_opcao(self) -> str | None:
        layout = [
            [sg.Text("Gerenciamento de Empresas", font=("Helvetica", 18), justification='center', expand_x=True)],
            [sg.Button("Incluir Empresa", key='-INCLUIR-', size=(20, 2), pad=(5, 5))],
            [sg.Button("Listar Empresas", key='-LISTAR-', size=(20, 2), pad=(5, 5))],
            [sg.Button("Editar Empresa", key='-EDITAR-', size=(20, 2), pad=(5, 5))],
            [sg.Button("Excluir Empresa", key='-EXCLUIR-', size=(20, 2), pad=(5, 5))],
            [sg.VPush()],
            [sg.Button("Voltar", key='-VOLTAR-', size=(20, 2), pad=(5, (15, 5)))]
        ]

        window = sg.Window(
            "Menu Empresa de Transporte",
            layout,
            element_justification='center',
            finalize=True
        )

        event, values = window.read()
        window.close()

        if event == sg.WIN_CLOSED:
            return '-VOLTAR-'

        return event

    def pega_dados_entidade(self, dados_atuais: dict = None) -> dict | None:
        nome = dados_atuais['nome'] if dados_atuais else ''
        cnpj = dados_atuais['cnpj'] if dados_atuais else ''
        telefone = dados_atuais['telefone'] if dados_atuais else ''

        titulo_janela = "Editar Empresa" if dados_atuais else "Incluir Nova Empresa"

        layout = [
            [sg.Text(titulo_janela, font=("Helvetica", 16))],
            [sg.Text("Nome:", size=(10, 1)), sg.Input(nome, key='-NOME-')],
            [sg.Text("CNPJ:", size=(10, 1)), sg.Input(cnpj, key='-CNPJ-')],
            [sg.Text("Telefone:", size=(10, 1)),
             sg.Input(telefone, key='-TELEFONE-')],
            [sg.Button("OK", key='-OK-'),
             sg.Button("Cancelar", key='-CANCELAR-')]
        ]

        window = sg.Window(titulo_janela, layout, finalize=True)

        dados = None
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == '-CANCELAR-':
                break

            if event == '-OK-':

                if not values['-NOME-'] or not values['-CNPJ-'] or not values['-TELEFONE-']:
                    self.mostra_erro("Todos os campos são obrigatórios.")
                    continue

                dados = {
                    "nome": values['-NOME-'],
                    "cnpj": values['-CNPJ-'],
                    "telefone": values['-TELEFONE-'],
                }
                break

        window.close()

        return dados

    def mostra_lista_entidades(self, dados_lista: list):
        if not dados_lista:
            self.mostra_mensagem("Aviso", "Nenhuma empresa cadastrada.")
            return

        headings = ["ID", "Nome", "CNPJ", "Telefone"]

        data = [
            [d['id'], d['nome'], d['cnpj'], d['telefone']]
            for d in dados_lista
        ]

        layout = [
            [sg.Text("Lista de Empresas Cadastradas", font=("Helvetica", 16))],
            [sg.Table(values=data,
                      headings=headings,
                      auto_size_columns=True,
                      justification='left',
                      num_rows=min(20, len(data)),
                      key='-TABELA-')],
            [sg.Button("OK", key='-OK-')]
        ]

        window = sg.Window("Listagem de Empresas", layout, finalize=True, resizable=True)
        window.read()
        window.close()

    def seleciona_entidade(self, dados_lista: list, titulo_janela: str) -> str | None:
        if not dados_lista:
            self.mostra_erro("Não há empresas cadastradas para selecionar.")
            return None

        headings = ["ID", "Nome", "CNPJ", "Telefone"]

        data = []
        id_lookup = []

        for d in dados_lista:
            data.append([d['id'], d['nome'], d['cnpj'], d['telefone']])
            id_lookup.append(d['id'])

        layout = [
            [sg.Text(titulo_janela, font=("Helvetica", 16))],
            [sg.Table(values=data,
                      headings=headings,
                      auto_size_columns=True,
                      num_rows=min(15, len(data)),
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                      enable_events=True,
                      key='-TABELA-')],
            [sg.Button("Confirmar", key='-OK-'),
             sg.Button("Cancelar", key='-CANCELAR-')]
        ]

        window = sg.Window(titulo_janela, layout, finalize=True)

        id_selecionado = None
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == '-CANCELAR-':
                break

            if event == '-OK-':
                if values['-TABELA-']:
                    row_index = values['-TABELA-'][0]
                    id_selecionado = id_lookup[row_index]
                    break
                else:
                    self.mostra_erro("Por favor, selecione uma empresa da lista.")

        window.close()

        return id_selecionado
