import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI


class TelaPrincipalGUI(TelaBaseGUI):

    def __init__(self):
        super().__init__()

    def mostrar_menu_principal(self):
        """
        Cria e exibe a janela do menu principal.
        Retorna a 'key' do botão que foi clicado.
        """

        button_style = dict(
            size=(30, 2),
            pad=(5, 5),
            button_color=("white", "#8B4513"),
            mouseover_colors=("white", "#A0522D"),
        )

        opcoes = [
            (1, "Gerenciar Pessoas"),
            (2, "Gerenciar Países"),
            (3, "Gerenciar Destinos"),
            (4, "Gerenciar Empresas de Transporte"),
            (5, "Gerenciar Meios de Transporte"),
            (6, "Gerenciar Passagens"),
            (7, "Gerenciar Trechos de Viagem"),
            (8, "Gerenciar Passeios Turísticos"),
            (9, "Gerenciar Pagamentos"),
            (10, "Compras de Pacotes de Viagem"),
            (11, "Gerenciar Itinerários de Viagem"),
            (12, "Relatórios"),
            (13, "Painel de Destinos"),
        ]

        lista_opcoes = [
            [
                sg.Button(
                    f"{codigo:02d}  -  {descricao}",
                    key=codigo,
                    **button_style,
                )
            ]
            for codigo, descricao in opcoes
        ]
        layout = [
            [
                sg.Text(
                    "SISTEMA DE GERENCIAMENTO DE VIAGENS",
                    font=("Bookman Old Style", 20, "bold"),
                    justification="center",
                    expand_x=True,
                    pad=(10, (20, 10)),
                )
            ],
            [
                sg.Column(
                    lista_opcoes,
                    scrollable=True,
                    vertical_scroll_only=True,
                    size=(460, 360),
                    pad=(10, 10),
                    sbar_trough_color="#c98258",
                    sbar_background_color="#8B4513",
                    key="-MENU-COL-",
                )
            ],
            [sg.VPush()],
            [
                sg.Button(
                    "Sair", key=0, size=(20, 2), button_color=("white", "firebrick4")
                )
            ],
        ]

        window = sg.Window(
            "Menu Principal",
            layout,
            element_justification="center",
            size=(700, 500),
            finalize=True,
        )

        event, values = window.read()
        window.close()

        if event == sg.WIN_CLOSED:
            return 0

        return event
