import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI
from models.pessoa import Pessoa
from models.trecho_viagem import TrechoViagem


class TelaPassagemGUI(TelaBaseGUI):
    def __init__(self):
        super().__init__()

    def le_opcao(self) -> str | None:
        layout = [
            [sg.Text("Gerenciamento de Passagens", font=("Helvetica", 18), justification='center', expand_x=True)],
            [sg.Button("Incluir Passagem", key='-INCLUIR-', size=(25, 2), pad=(5, 5))],
            [sg.Button("Listar Passagens", key='-LISTAR-', size=(25, 2), pad=(5, 5))],
            [sg.Button("Editar Passagem", key='-EDITAR-', size=(25, 2), pad=(5, 5))],
            [sg.Button("Excluir Passagem", key='-EXCLUIR-', size=(25, 2), pad=(5, 5))],
            [sg.Button("Confirmar Compra", key='-CONFIRMAR_COMPRA-', size=(25, 2), pad=(5, 5))],
            [sg.VPush()], 
            [sg.Button("Voltar", key='-VOLTAR-', size=(25, 2), pad=(5, (15, 5)))]
        ]
        
        window = sg.Window(
            "Menu Passagem", 
            layout, 
            element_justification='center', 
            finalize=True
        )
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return '-VOLTAR-'
            
        return event

    def pega_dados_entidade(self, lista_pessoas: list[Pessoa], lista_trechos: list[TrechoViagem], dados_atuais: dict = None) -> dict | None:
        if not lista_pessoas:
            self.mostra_erro("Não é possível adicionar uma passagem pois não há pessoas cadastradas.")
            return None
        if not lista_trechos:
            self.mostra_erro("Não é possível adicionar uma passagem pois não há trechos cadastrados.")
            return None

        mapa_pessoa_obj = {f"{p.nome} ({p.identificacao})": p for p in lista_pessoas}
        nomes_pessoas = list(mapa_pessoa_obj.keys())
        
        def format_trecho(t):
            return f"{t.local_origem} -> {t.local_destino} ({t.data.strftime('%d/%m %H:%M')})"
        
        mapa_trecho_obj = {format_trecho(t): t for t in lista_trechos}
        nomes_trechos = list(mapa_trecho_obj.keys())
        
        if dados_atuais:
            p_atual = dados_atuais['passageiro']
            t_atual = dados_atuais['trecho']
            r_atual = dados_atuais['responsavel_compra']
            
            passageiro_atual_str = f"{p_atual.nome} ({p_atual.identificacao})"
            trecho_atual_str = format_trecho(t_atual)
            responsavel_atual_str = f"{r_atual.nome} ({r_atual.identificacao})"
            titulo_janela = "Editar Passagem"
        else:
            passageiro_atual_str = nomes_pessoas[0]
            trecho_atual_str = nomes_trechos[0]
            responsavel_atual_str = nomes_pessoas[0]
            titulo_janela = "Incluir Nova Passagem"

        layout = [
            [sg.Text(titulo_janela, font=("Helvetica", 16))],
            [sg.Text("Passageiro:", size=(10, 1)), 
             sg.Combo(nomes_pessoas, default_value=passageiro_atual_str, readonly=True, key='-PASSAGEIRO-', size=(40, 1))],
            [sg.Text("Trecho:", size=(10, 1)),
             sg.Combo(nomes_trechos, default_value=trecho_atual_str, readonly=True, key='-TRECHO-', size=(40, 1))],
            [sg.Text("Responsável:", size=(10, 1)),
             sg.Combo(nomes_pessoas, default_value=responsavel_atual_str, readonly=True, key='-RESPONSAVEL-', size=(40, 1))],
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
                passageiro_obj = mapa_pessoa_obj[values['-PASSAGEIRO-']]
                trecho_obj = mapa_trecho_obj[values['-TRECHO-']]
                responsavel_obj = mapa_pessoa_obj[values['-RESPONSAVEL-']]

                dados = {
                    "passageiro": passageiro_obj,
                    "trecho": trecho_obj,
                    "responsavel_compra": responsavel_obj
                }
                break

        window.close()

        return dados

    def mostra_lista_entidades(self, dados_lista: list):
        if not dados_lista:
            self.mostra_mensagem("Aviso", "Nenhuma passagem cadastrada.")
            return

        headings = ["ID", "Passageiro", "Trecho", "Data", "Responsável", "Status"]
        
        data = []
        for d in dados_lista:
            status = "Comprada" if d["compra_efetuada"] else "Pendente"
            trecho_str = f"{d['trecho'].local_origem} -> {d['trecho'].local_destino}"
            data_str = d['trecho'].data.strftime('%d/%m/%Y %H:%M')
            data.append([
                d['id'],
                d['passageiro'].nome,
                trecho_str,
                data_str,
                d['responsavel_compra'].nome,
                status
            ])

        layout = [
            [sg.Text("Lista de Passagens Cadastradas", font=("Helvetica", 16))],
            [sg.Table(values=data,
                      headings=headings,
                      auto_size_columns=True,
                      justification='left',
                      num_rows=min(20, len(data)),
                      key='-TABELA-')],
            [sg.Button("OK", key='-OK-')]
        ]
        
        window = sg.Window("Listagem de Passagens", layout, finalize=True, resizable=True)
        window.read()
        window.close()

    def seleciona_entidade(self, dados_lista: list, titulo_janela: str) -> str | None:
        if not dados_lista:
            self.mostra_erro("Não há passagens cadastradas para selecionar.")
            return None

        headings = ["ID", "Passageiro", "Trecho", "Data", "Status"]
        data = []
        id_lookup = []
        for d in dados_lista:
            status = "Comprada" if d["compra_efetuada"] else "Pendente"
            trecho_str = f"{d['trecho'].local_origem} -> {d['trecho'].local_destino}"
            data_str = d['trecho'].data.strftime('%d/%m/%Y %H:%M')
            data.append([
                d['id'],
                d['passageiro'].nome,
                trecho_str,
                data_str,
                status
            ])
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
                    self.mostra_erro("Por favor, selecione uma passagem da lista.")

        window.close()

        return id_selecionado
