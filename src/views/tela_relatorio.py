import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI


class TelaRelatorio(TelaBaseGUI):
    def le_opcao(self):
        layout = [
            [
                sg.Text(
                    "Relatórios",
                    font=("Helvetica", 18, "bold"),
                    justification="center",
                    expand_x=True,
                )
            ],
            [sg.Button("Destinos Mais Populares", key="-DESTINOS_POPULARES-", size=(30, 2))],
            [sg.Button("Destinos Mais Caros/Baratos", key="-DESTINOS_PRECO-", size=(30, 2))],
            [sg.Button("Passeios Mais Populares", key="-PASSEIOS_POPULARES-", size=(30, 2))],
            [sg.Button("Passeios Mais Caros/Baratos", key="-PASSEIOS_PRECO-", size=(30, 2))],
            [sg.VPush()],
            [sg.Button("Voltar", key="-VOLTAR-", size=(20, 2))],
        ]

        window = sg.Window("Relatórios", layout, finalize=True)
        event, _ = window.read()
        window.close()

        if event in (sg.WIN_CLOSED, "-VOLTAR-"):
            return "-VOLTAR-"
        return event

    def mostra_relatorio(self, titulo, headings, data):
        if not data:
            self.mostra_mensagem(titulo, "Sem dados para exibir.")
            return

        layout = [
            [sg.Text(titulo, font=("Helvetica", 16, "bold"))],
            [
                sg.Table(
                    values=data,
                    headings=headings,
                    auto_size_columns=True,
                    justification="left",
                    num_rows=min(20, len(data)),
                    key="-TABLE-",
                )
            ],
            [sg.Button("Fechar", key="-FECHAR-")],
        ]

        window = sg.Window(titulo, layout, finalize=True, resizable=True, modal=True)
        window.read()
        window.close()

    def mostra_relatorio_destinos(self, destinos):
        data = [[idx + 1, destino, visitas] for idx, (destino, visitas) in enumerate(destinos)]
        self.mostra_relatorio(
            "Destinos Mais Populares",
            ["Posição", "Destino", "Visitas"],
            data,
        )

    def mostra_relatorio_extremos(
        self,
        titulo,
        headings,
        caros,
        baratos,
        titulo_caros="Mais Caros",
        titulo_baratos="Mais Baratos",
    ):
        def tabela_dados(dados):
            if not dados:
                return [[sg.Text("Sem dados para exibir.")]]
            return [
                [
                    sg.Table(
                        values=dados,
                        headings=headings,
                        auto_size_columns=True,
                        justification="left",
                        num_rows=min(10, len(dados)),
                        key=f"-TABLE-{titulo}-{titulo_caros}-",
                    )
                ]
            ]

        layout = [
            [sg.Text(titulo, font=("Helvetica", 16, "bold"))],
            [
                sg.Frame(
                    titulo_caros,
                    tabela_dados(caros),
                    expand_x=True,
                    pad=(5, 5),
                ),
                sg.Frame(
                    titulo_baratos,
                    tabela_dados(baratos),
                    expand_x=True,
                    pad=(5, 5),
                ),
            ],
            [sg.Button("Fechar", key="-FECHAR-")],
        ]

        window = sg.Window(titulo, layout, finalize=True, modal=True, resizable=True)
        window.read()
        window.close()

    def mostra_relatorio_destinos_preco(self, caros, baratos):
        dados_caros = [
            [idx + 1, cidade, pais, f"{valor:.2f}"]
            for idx, (cidade, pais, valor) in enumerate(caros)
        ]
        dados_baratos = [
            [idx + 1, cidade, pais, f"{valor:.2f}"]
            for idx, (cidade, pais, valor) in enumerate(baratos)
        ]
        self.mostra_relatorio_extremos(
            "Destinos por Valor",
            ["Posição", "Cidade", "País", "Valor Médio (R$)"],
            dados_caros,
            dados_baratos,
        )

    def mostra_relatorio_passeios_populares(self, passeios):
        data = [[idx + 1, atracao, cidade, qtd] for idx, (atracao, cidade, qtd) in enumerate(passeios)]
        self.mostra_relatorio(
            "Passeios Mais Populares",
            ["Posição", "Passeio", "Cidade", "Participações"],
            data,
        )

    def mostra_relatorio_passeios_preco(self, caros, baratos):
        dados_caros = [
            [idx + 1, atracao, cidade, f"{valor:.2f}"]
            for idx, (atracao, cidade, valor) in enumerate(caros)
        ]
        dados_baratos = [
            [idx + 1, atracao, cidade, f"{valor:.2f}"]
            for idx, (atracao, cidade, valor) in enumerate(baratos)
        ]
        self.mostra_relatorio_extremos(
            "Passeios por Valor",
            ["Posição", "Passeio", "Cidade", "Valor (R$)"],
            dados_caros,
            dados_baratos,
        )
