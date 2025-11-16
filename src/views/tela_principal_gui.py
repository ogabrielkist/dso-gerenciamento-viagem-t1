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
        
        col1 = [
            [sg.Button("Gerenciar Pessoas", key=1, size=(30, 2))],
            [sg.Button("Gerenciar Paises", key=2, size=(30, 2))],
            [sg.Button("Gerenciar Cidades", key=3, size=(30, 2))],
            [sg.Button("Gerenciar Empresas De Transporte", key=4, size=(30, 2))],
            [sg.Button("Gerenciar Meios de Transporte", key=5, size=(30, 2))],
            [sg.Button("Gerenciar Passagens", key=6, size=(30, 2))],
        ]
        col2 = [
            [sg.Button("Gerenciar Passeios Turisticos", key=7, size=(30, 2))],
            [sg.Button("Gerenciar Itinerários de Viagem", key=8, size=(30, 2))],
            [sg.Button("Gerenciar Trechos de Viagem", key=9, size=(30, 2))],
            [sg.Button("Gerenciar Viagens", key=10, size=(30, 2))],
            [sg.Button("Gerencias Pagamentos", key=11, size=(30, 2))],
            [sg.Button("Relatórios", key=12, size=(30, 2))],
        ]
        layout = [
            [sg.Text("SISTEMA DE GERENCIAMENTO DE VIAGENS",
                     font=('Bookman Old Style', 20, 'bold'),
                     justification='center', 
                     expand_x=True,
                     pad=(10, (20, 10))
            )],
            [sg.Column(col1, pad=(10, 10)), 
             sg.Column(col2, pad=(10, 10))],
            [sg.VPush()],
            [sg.Button("Sair", key=0, size=(20, 2), button_color=('white', 'firebrick4'))]
        ]

        window = sg.Window("Menu Principal", 
                           layout, 
                           element_justification='center',
                           size=(700, 500),
                           finalize=True)
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return 0
        
        return event
