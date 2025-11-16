import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI
from models.empresa_transporte import EmpresaTransporte
from models.meio_transporte import TipoTransporte

class TelaMeioTransporteGUI(TelaBaseGUI):
    TIPOS_TRANSPORTE = [tipo.value for tipo in TipoTransporte]

    def __init__(self):
        super().__init__()

    def le_opcao(self) -> str | None:
        layout = [
            [sg.Text("Gerenciamento de Meios de Transporte", font=("Helvetica", 18), justification='center', expand_x=True)],
            [sg.Button("Incluir Meio de Transporte", key='-INCLUIR-', size=(25, 2), pad=(5, 5))],
            [sg.Button("Listar Meios de Transporte", key='-LISTAR-', size=(25, 2), pad=(5, 5))],
            [sg.Button("Editar Meio de Transporte", key='-EDITAR-', size=(25, 2), pad=(5, 5))],
            [sg.Button("Excluir Meio de Transporte", key='-EXCLUIR-', size=(25, 2), pad=(5, 5))],
            [sg.VPush()],
            [sg.Button("Voltar", key='-VOLTAR-', size=(25, 2), pad=(5, (15, 5)))]
        ]
        window = sg.Window(
            "Menu Meio de Transporte",
            layout,
            element_justification='center',
            finalize=True
        )
        event, values = window.read()
        window.close()
        if event == sg.WIN_CLOSED:
            return '-VOLTAR-'
        return event

    def pega_dados_entidade(self, lista_empresas: list[EmpresaTransporte], dados_atuais: dict = None) -> dict | None:
        if not lista_empresas:
            self.mostra_erro("Não é possível adicionar um meio de transporte pois não há empresas cadastradas.")
            return None

        mapa_empresa_obj = {emp.nome: emp for emp in lista_empresas}
        nomes_empresas = list(mapa_empresa_obj.keys())
        
        if dados_atuais:
            tipo_atual = dados_atuais['tipo']
            empresa_atual_nome = dados_atuais['empresa'].nome
            titulo_janela = "Editar Meio de Transporte"
        else:
            tipo_atual = self.TIPOS_TRANSPORTE[0]
            empresa_atual_nome = nomes_empresas[0]
            titulo_janela = "Incluir Novo Meio de Transporte"

        layout = [
            [sg.Text(titulo_janela, font=("Helvetica", 16))],
            [sg.Text("Tipo:", size=(8, 1)), 
             sg.Combo(self.TIPOS_TRANSPORTE, default_value=tipo_atual, readonly=True, key='-TIPO-')],
            [sg.Text("Empresa:", size=(8, 1)),
             sg.Combo(nomes_empresas, default_value=empresa_atual_nome, readonly=True, key='-EMPRESA-')],
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
                nome_empresa_selecionada = values['-EMPRESA-']
                empresa_obj_selecionada = mapa_empresa_obj[nome_empresa_selecionada]
                dados = {
                    "tipo": values['-TIPO-'],
                    "empresa": empresa_obj_selecionada
                }
                break

        window.close()

        return dados

    def mostra_lista_entidades(self, dados_lista: list):
        if not dados_lista:
            self.mostra_mensagem("Aviso", "Nenhum meio de transporte cadastrado.")
            return

        headings = ["ID", "Tipo", "Empresa"]
        data = [
            [d['id'], d['tipo'], d['empresa'].nome]
            for d in dados_lista
        ]
        layout = [
            [sg.Text("Lista de Meios de Transporte Cadastrados", font=("Helvetica", 16))],
            [sg.Table(values=data,
                      headings=headings,
                      auto_size_columns=True,
                      justification='left',
                      num_rows=min(20, len(data)),
                      key='-TABELA-')],
            [sg.Button("OK", key='-OK-')]
        ]
        window = sg.Window("Listagem de Meios de Transporte", layout, finalize=True, resizable=True)
        window.read()
        window.close()

    def seleciona_entidade(self, dados_lista: list, titulo_janela: str) -> str | None:
        if not dados_lista:
            self.mostra_erro("Não há meios de transporte cadastrados para selecionar.")
            return None

        headings = ["ID", "Tipo", "Empresa"]
        data = []
        id_lookup = []
        for d in dados_lista:
            data.append([d['id'], d['tipo'], d['empresa'].nome])
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
                    self.mostra_erro("Por favor, selecione um item da lista.")

        window.close()

        return id_selecionado
