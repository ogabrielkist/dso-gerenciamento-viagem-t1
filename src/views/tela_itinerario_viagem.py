from datetime import datetime
import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI


class TelaItinerarioViagem(TelaBaseGUI):
    def __init__(self):
        super().__init__()
        self._controlador_passeio = None

    def set_controlador_passeio(self, controlador_passeio):
        self._controlador_passeio = controlador_passeio

    def le_opcao(self):
        layout = [
            [
                sg.Text(
                    "Itinerários de Viagem",
                    font=("Helvetica", 18, "bold"),
                    justification="center",
                    expand_x=True,
                )
            ],
            [sg.Button("Incluir", key="-INCLUIR-", size=(25, 2))],
            [sg.Button("Listar", key="-LISTAR-", size=(25, 2))],
            [sg.Button("Editar", key="-EDITAR-", size=(25, 2))],
            [sg.Button("Excluir", key="-EXCLUIR-", size=(25, 2))],
            [sg.Button("Gerenciar Passeios", key="-PASSEIOS-", size=(25, 2))],
            [sg.VPush()],
            [sg.Button("Voltar", key="-VOLTAR-", size=(25, 2))],
        ]
        window = sg.Window("Itinerários", layout, finalize=True)
        event, _ = window.read()
        window.close()
        if event in (sg.WIN_CLOSED, "-VOLTAR-"):
            return "-VOLTAR-"
        return event

    def pega_dados_entidade(self, dados_atuais=None):
        data_atual = dados_atuais["data"].strftime("%Y-%m-%d") if dados_atuais else ""
        titulo = "Editar Itinerário" if dados_atuais else "Novo Itinerário"
        layout = [
            [sg.Text(titulo, font=("Helvetica", 16))],
            [
                sg.Text("Data (YYYY-MM-DD):", size=(20, 1)),
                sg.Input(default_text=data_atual, key="-DATA-"),
            ],
            [sg.Button("Salvar", key="-SALVAR-"), sg.Button("Cancelar", key="-CANCELAR-")],
        ]

        window = sg.Window(titulo, layout, finalize=True)
        dados = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break
            if event == "-SALVAR-":
                try:
                    data = datetime.strptime(values["-DATA-"], "%Y-%m-%d").date()
                    dados = {"data": data}
                    break
                except ValueError:
                    self.mostra_erro("Data inválida. Utilize o formato YYYY-MM-DD.")

        window.close()
        return dados

    def mostra_lista_entidades(self, dados_lista):
        if not dados_lista:
            self.mostra_mensagem("Itinerários", "Nenhum itinerário cadastrado.")
            return

        headings = ["ID", "Data", "Passeios"]

        data = []
        for d in dados_lista:
            passeios = d.get("passeios", [])
            if passeios:
                nomes = ", ".join(p.atracao_turistica for p in passeios)
                descricao = f"{len(passeios)} ({nomes})"
            else:
                descricao = "0"

            data.append([d["id"], d["data"].strftime("%d/%m/%Y"), descricao])

        self.mostra_lista("Itinerários", headings, data)

    def seleciona_entidade(self, dados_lista, titulo_janela):
        if not dados_lista:
            self.mostra_erro("Nenhum itinerário cadastrado.")
            return None

        headings = ["ID", "Data"]
        data = []
        id_lookup = []
        for d in dados_lista:
            data.append([d["id"], d["data"].strftime("%d/%m/%Y")])
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
                    key="-TABLE-",
                )
            ],
            [sg.Button("Selecionar", key="-OK-"), sg.Button("Cancelar", key="-CANCELAR-")],
        ]

        window = sg.Window(titulo_janela, layout, finalize=True)
        selecionado = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break
            if event == "-OK-":
                if values["-TABLE-"]:
                    selecionado = id_lookup[values["-TABLE-"][0]]
                    break
                self.mostra_erro("Selecione um itinerário.")

        window.close()
        return selecionado

    def gerenciar_passeios(self, itinerario):
        if self._controlador_passeio is None:
            self.mostra_erro("Controlador de passeios não configurado.")
            return

        def formatar(passeio):
            return f"{passeio.atracao_turistica} ({passeio.cidade.nome}) - {passeio.horario_inicio.strftime('%H:%M')}"

        while True:
            disponiveis = [
                p
                for p in self._controlador_passeio.get_entidades()
                if p not in itinerario.passeios
            ]
            mapa_disponiveis = {formatar(p): p for p in disponiveis}
            mapa_atuais = {formatar(p): p for p in itinerario.passeios}

            layout = [
                [
                    sg.Text(
                        f"Passeios do dia {itinerario.data.strftime('%d/%m/%Y')}",
                        font=("Helvetica", 16),
                    )
                ],
                [
                    sg.Frame(
                        "No Itinerário",
                        [
                            [
                                sg.Listbox(
                                    values=list(mapa_atuais.keys()),
                                    size=(40, 10),
                                    key="-ATUAIS-",
                                )
                            ]
                        ],
                        expand_x=True,
                    ),
                    sg.Frame(
                        "Disponíveis",
                        [
                            [
                                sg.Listbox(
                                    values=list(mapa_disponiveis.keys()),
                                    size=(40, 10),
                                    key="-DISPONIVEIS-",
                                )
                            ]
                        ],
                        expand_x=True,
                    ),
                ],
                [
                    sg.Button("Adicionar", key="-ADICIONAR-"),
                    sg.Button("Remover", key="-REMOVER-"),
                    sg.Button("Fechar", key="-FECHAR-"),
                ],
            ]

            window = sg.Window("Gerenciar Passeios", layout, finalize=True, modal=True)
            event, values = window.read()
            window.close()

            if event in (sg.WIN_CLOSED, "-FECHAR-"):
                break
            if event == "-ADICIONAR-":
                selecionado = values["-DISPONIVEIS-"]
                if selecionado:
                    itinerario.incluir_passeio(mapa_disponiveis[selecionado[0]])
                    self.mostra_sucesso("Passeio adicionado.")
                else:
                    self.mostra_erro("Escolha um passeio disponível.")
            if event == "-REMOVER-":
                selecionado = values["-ATUAIS-"]
                if selecionado:
                    itinerario.excluir_passeio(mapa_atuais[selecionado[0]])
                    self.mostra_sucesso("Passeio removido.")
                else:
                    self.mostra_erro("Escolha um passeio para remover.")
