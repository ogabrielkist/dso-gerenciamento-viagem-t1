import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI


class TelaDestinosGUI(TelaBaseGUI):
    def le_opcao(self, paises: list, cidades: list) -> str:
        dados_paises = [
            [pais.nome, len(pais.cidades)]
            for pais in paises
        ]
        dados_cidades = [
            [cidade.nome, cidade.pais.nome]
            for cidade in cidades
        ]

        layout = [
            [
                sg.Text(
                    "Painel de Destinos",
                    font=("Helvetica", 18, "bold"),
                    justification="center",
                    expand_x=True,
                )
            ],
            [
                sg.Frame(
                    "Países",
                    [
                        [
                            sg.Table(
                                values=dados_paises,
                                headings=["País", "Qtd. Cidades"],
                                num_rows=min(10, len(dados_paises)),
                                auto_size_columns=True,
                                key="-TBL_PAISES-",
                            )
                        ]
                    ],
                    expand_x=True,
                ),
                sg.Frame(
                    "Cidades",
                    [
                        [
                            sg.Table(
                                values=dados_cidades,
                                headings=["Cidade", "País"],
                                num_rows=min(10, len(dados_cidades)),
                                auto_size_columns=True,
                                key="-TBL_CIDADES-",
                            )
                        ]
                    ],
                    expand_x=True,
                ),
            ],
            [
                sg.Button("Gerenciar Países", key="-GERENCIAR_PAISES-", size=(20, 2)),
                sg.Button("Gerenciar Cidades", key="-GERENCIAR_CIDADES-", size=(20, 2)),
            ],
            [sg.Button("Voltar", key="-VOLTAR-", size=(20, 2))],
        ]

        window = sg.Window("Destinos", layout, finalize=True, resizable=True)
        event, _ = window.read()
        window.close()

        if event in (sg.WIN_CLOSED, "-VOLTAR-"):
            return "-VOLTAR-"
        return event

