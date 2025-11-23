from datetime import datetime
import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI


class TelaViagem(TelaBaseGUI):
    def __init__(self):
        super().__init__()
        self._controlador_itinerario = None

    def set_controlador_itinerario(self, controlador_itinerario):
        self._controlador_itinerario = controlador_itinerario

    def le_opcao(self):
        layout = [
            [
                sg.Text(
                    "Compras de Pacotes de Viagem",
                    font=("Helvetica", 18, "bold"),
                    justification="center",
                    expand_x=True,
                )
            ],
            [sg.Button("Incluir", key="-INCLUIR-", size=(25, 2))],
            [sg.Button("Listar", key="-LISTAR-", size=(25, 2))],
            [sg.Button("Editar", key="-EDITAR-", size=(25, 2))],
            [sg.Button("Excluir", key="-EXCLUIR-", size=(25, 2))],
            [sg.Button("Gerenciar Itinerários", key="-ITINERARIOS-", size=(25, 2))],
            [sg.Button("Gerenciar Participantes", key="-PARTICIPANTES-", size=(25, 2))],
            [sg.VPush()],
            [sg.Button("Voltar", key="-VOLTAR-", size=(25, 2))],
        ]
        window = sg.Window("Pacotes de Viagem", layout, finalize=True)
        event, _ = window.read()
        window.close()

        if event in (sg.WIN_CLOSED, "-VOLTAR-"):
            return "-VOLTAR-"
        return event

    def pega_dados_entidade(self, dados_atuais=None):
        data_inicio = (
            dados_atuais["data_inicio"].strftime("%Y-%m-%d") if dados_atuais else ""
        )
        data_fim = dados_atuais["data_fim"].strftime("%Y-%m-%d") if dados_atuais else ""
        valor = f"{dados_atuais['valor_total_pacote']:.2f}" if dados_atuais else ""

        titulo = "Editar Pacote de Viagem" if dados_atuais else "Novo Pacote de Viagem"

        layout = [
            [sg.Text(titulo, font=("Helvetica", 16))],
            [
                sg.Text("Data Início (YYYY-MM-DD):", size=(25, 1)),
                sg.Input(default_text=data_inicio, key="-DATA_INICIO-"),
            ],
            [
                sg.Text("Data Fim (YYYY-MM-DD):", size=(25, 1)),
                sg.Input(default_text=data_fim, key="-DATA_FIM-"),
            ],
            [
                sg.Text("Valor Total do Pacote (R$):", size=(25, 1)),
                sg.Input(default_text=valor, key="-VALOR-"),
            ],
            [
                sg.Button("Salvar", key="-SALVAR-"),
                sg.Button("Cancelar", key="-CANCELAR-"),
            ],
        ]

        window = sg.Window(titulo, layout, finalize=True)
        dados = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break
            if event == "-SALVAR-":
                try:
                    data_inicio = datetime.strptime(
                        values["-DATA_INICIO-"], "%Y-%m-%d"
                    ).date()
                    data_fim = datetime.strptime(
                        values["-DATA_FIM-"], "%Y-%m-%d"
                    ).date()
                    valor_total = float(values["-VALOR-"])

                    dados = {
                        "data_inicio": data_inicio,
                        "data_fim": data_fim,
                        "valor_total_pacote": valor_total,
                    }
                    break
                except ValueError:
                    self.mostra_erro(
                        "Datas precisam estar no formato YYYY-MM-DD e o valor deve ser numérico."
                    )

        window.close()
        return dados

    def mostra_lista_entidades(self, dados_lista):
        if not dados_lista:
            self.mostra_mensagem("Pacotes", "Nenhuma viagem cadastrada.")
            return

        headings = [
            "ID",
            "Início",
            "Fim",
            "Valor (R$)",
            "Participantes",
            "Destinos",
        ]

        data = []
        for d in dados_lista:
            participantes = d.get("participantes", [])
            destinos = d.get("destinos_visitados", [])

            participantes_str = ""
            if participantes:
                nomes = ", ".join(p.nome for p in participantes)
                participantes_str = f"{len(participantes)} ({nomes})"
            else:
                participantes_str = "0"

            destinos_str = ""
            if destinos:
                cidades = ", ".join(c.nome for c in destinos)
                destinos_str = f"{len(destinos)} ({cidades})"
            else:
                destinos_str = "0"

            data.append(
                [
                    d["id"],
                    d["data_inicio"].strftime("%d/%m/%Y"),
                    d["data_fim"].strftime("%d/%m/%Y"),
                    f"{d['valor_total_pacote']:.2f}",
                    participantes_str,
                    destinos_str,
                ]
            )
        self.mostra_lista("Pacotes de Viagem", headings, data)

    def seleciona_entidade(self, dados_lista, titulo_janela):
        if not dados_lista:
            self.mostra_erro("Não há viagens cadastradas.")
            return None

        headings = ["ID", "Período", "Valor (R$)"]
        data = []
        id_lookup = []

        for d in dados_lista:
            periodo = (
                f"{d['data_inicio'].strftime('%d/%m/%Y')} - "
                f"{d['data_fim'].strftime('%d/%m/%Y')}"
            )
            data.append([d["id"], periodo, f"{d['valor_total_pacote']:.2f}"])
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
            [
                sg.Button("Selecionar", key="-OK-"),
                sg.Button("Cancelar", key="-CANCELAR-"),
            ],
        ]

        window = sg.Window(titulo_janela, layout, finalize=True)
        escolhido = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break
            if event == "-OK-":
                if values["-TABLE-"]:
                    escolhido = id_lookup[values["-TABLE-"][0]]
                    break
                self.mostra_erro("Selecione um item da lista.")

        window.close()
        return escolhido

    def gerenciar_itinerarios(self, viagem):
        if self._controlador_itinerario is None:
            self.mostra_erro("Controlador de itinerários não configurado.")
            return

        def formatar(itinerario):
            total = len(itinerario.passeios)
            if total:
                nomes = ", ".join(p.atracao_turistica for p in itinerario.passeios)
                return (
                    f"{itinerario.data.strftime('%d/%m/%Y')} - "
                    f"{total} passeios ({nomes})"
                )
            return f"{itinerario.data.strftime('%d/%m/%Y')} - 0 passeios"

        while True:
            itinerarios_disponiveis = [
                it
                for it in self._controlador_itinerario.get_entidades()
                if it not in viagem.itinerarios
            ]
            mapa_disponiveis = {formatar(it): it for it in itinerarios_disponiveis}
            mapa_atuais = {formatar(it): it for it in viagem.itinerarios}
            layout = [
                [
                    sg.Text(
                        f"Gerenciar Itinerários - Viagem {viagem.data_inicio.strftime('%d/%m/%Y')}",
                        font=("Helvetica", 16),
                    )
                ],
                [
                    sg.Frame(
                        "Itinerários na Viagem",
                        [
                            [
                                sg.Listbox(
                                    values=list(mapa_atuais.keys()),
                                    size=(40, 8),
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
                                    size=(40, 8),
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

            window = sg.Window(
                "Gerenciar Itinerários", layout, finalize=True, modal=True
            )
            event, values = window.read()
            window.close()

            if event in (sg.WIN_CLOSED, "-FECHAR-"):
                break
            if event == "-ADICIONAR-":
                selecionado = values["-DISPONIVEIS-"]
                if selecionado:
                    itinerario = mapa_disponiveis[selecionado[0]]
                    viagem.incluir_itinerario(itinerario)
                    self.mostra_sucesso("Itinerário adicionado.")
                else:
                    self.mostra_erro("Selecione um itinerário disponível.")
            if event == "-REMOVER-":
                selecionado = values["-ATUAIS-"]
                if selecionado:
                    itinerario = mapa_atuais[selecionado[0]]
                    viagem.excluir_itinerario(itinerario)
                    self.mostra_sucesso("Itinerário removido.")
                else:
                    self.mostra_erro("Selecione um itinerário para remover.")

    def gerenciar_participantes(self, viagem, todas_pessoas):
        if not todas_pessoas:
            self.mostra_erro("Não há pessoas cadastradas para incluir na viagem.")
            return

        def formatar(pessoa):
            return f"{pessoa.nome} ({pessoa.identificacao})"

        while True:
            participantes = viagem.participantes
            disponiveis = [p for p in todas_pessoas if p not in participantes]

            mapa_participantes = {formatar(p): p for p in participantes}
            mapa_disponiveis = {formatar(p): p for p in disponiveis}

            layout = [
                [
                    sg.Text(
                        f"Participantes da Viagem {viagem.data_inicio.strftime('%d/%m/%Y')}",
                        font=("Helvetica", 16),
                    )
                ],
                [
                    sg.Frame(
                        "Na Viagem",
                        [
                            [
                                sg.Listbox(
                                    values=list(mapa_participantes.keys()),
                                    size=(40, 10),
                                    key="-PARTICIPANTES-",
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

            window = sg.Window(
                "Gerenciar Participantes", layout, finalize=True, modal=True
            )
            event, values = window.read()
            window.close()

            if event in (sg.WIN_CLOSED, "-FECHAR-"):
                break
            if event == "-ADICIONAR-":
                selecionado = values["-DISPONIVEIS-"]
                if selecionado:
                    pessoa = mapa_disponiveis[selecionado[0]]
                    viagem.incluir_participante(pessoa)
                    self.mostra_sucesso("Participante adicionado.")
                else:
                    self.mostra_erro("Selecione uma pessoa disponível.")
            if event == "-REMOVER-":
                selecionado = values["-PARTICIPANTES-"]
                if selecionado:
                    pessoa = mapa_participantes[selecionado[0]]
                    viagem.excluir_participante(pessoa)
                    self.mostra_sucesso("Participante removido.")
                else:
                    self.mostra_erro("Selecione um participante para remover.")
