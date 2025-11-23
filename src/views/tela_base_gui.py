import FreeSimpleGUI as sg
from abc import ABC


class TelaBaseGUI(ABC):
    def __init__(self):
        sg.theme("LightBrown6")
        sg.set_options(
            font=("Bookman Old Style", 12),
            button_color=("white", "#8B4513"),
            element_padding=(5, 5),
        )

    def limpar_tela(self):
        """
        Mantido por compatibilidade com telas antigas (sem efeito em GUI).
        """
        return

    def aguardar_enter(
        self, titulo="Continuar", mensagem="Clique em OK para prosseguir"
    ):
        """
        Exibe um popup modal apenas para aguardar confirmação do usuário.
        """
        sg.popup_ok(titulo, mensagem)

    def tela_opcoes(self, titulo, opcoes):
        """
        Oferece um seletor simples de opções. Usado apenas como fallback
        para fluxos herdados que ainda dependem de menu numérico.
        """
        coluna_botoes = [
            [
                sg.Button(
                    f"{codigo} - {descricao}",
                    key=codigo,
                    expand_x=True,
                    size=(30, 2),
                )
            ]
            for codigo, descricao in opcoes.items()
        ]

        layout = [
            [
                sg.Text(
                    titulo,
                    font=("Bookman Old Style", 18, "bold"),
                    justification="center",
                    expand_x=True,
                )
            ],
            [sg.Column(coluna_botoes)],
            [sg.Button("Voltar", key=0, size=(20, 1))],
        ]

        window = sg.Window(titulo, layout, finalize=True)
        event, _ = window.read()
        window.close()
        return event

    def cria_menu_de_botoes(self, titulo, botoes, key_voltar="-VOLTAR-"):
        """
        Constrói um menu genérico com botões grandes.
        Retorna a key clicada ou key_voltar caso a janela seja fechada.
        """
        layout_botoes = [
            [
                sg.Button(
                    label,
                    key=key,
                    expand_x=True,
                    size=(30, 2),
                    pad=(5, 5),
                )
            ]
            for key, label in botoes
        ]

        layout = [
            [
                sg.Text(
                    titulo,
                    font=("Bookman Old Style", 18, "bold"),
                    justification="center",
                    expand_x=True,
                    pad=(0, (0, 10)),
                )
            ],
            [sg.Column(layout_botoes, expand_x=True)],
            [
                sg.Button(
                    "Voltar",
                    key=key_voltar,
                    size=(20, 1),
                    pad=(5, (15, 5)),
                    button_color=("white", "firebrick3"),
                )
            ],
        ]

        window = sg.Window(
            titulo, layout, finalize=True, element_justification="center"
        )
        event, _ = window.read()
        window.close()

        if event in (None, sg.WIN_CLOSED):
            return key_voltar

        return event

    def mostra_erro(self, mensagem):
        """
        Exibe um popup de erro.
        """
        sg.popup_ok(
            mensagem,
            title="Erro",
            button_color=("white", "firebrick4"),
        )

    def mostra_mensagem(self, titulo, mensagem):
        """
        Exibe um popup genérico.
        """
        sg.popup(titulo, mensagem)
        return

    def mostra_sucesso(self, mensagem):
        """
        Pequeno helper para manter consistência semântica.
        """
        sg.popup_ok("Sucesso", mensagem)

    def mostra_lista(self, titulo, headings, data):
        """
        Exibe uma tabela em janela modal.
        """
        layout = [
            [sg.Text(titulo, font=("Bookman Old Style", 16, "bold"))],
            [
                sg.Table(
                    values=data,
                    headings=headings,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    num_rows=min(15, len(data)) if data else 1,
                    justification="left",
                    key="-TABLE-",
                    expand_x=True,
                    expand_y=True,
                )
            ],
            [sg.Button("Fechar", key="-OK-")],
        ]
        window = sg.Window(titulo, layout, finalize=True, resizable=True)
        window.read()
        window.close()

    def seleciona_em_tabela(self, titulo, headings, data, lookup):
        """
        Exibe uma tabela e retorna o valor associado ao índice selecionado.
        'data' deve ser uma lista de listas (linhas).
        'lookup' é uma lista paralela contendo o payload a ser retornado.
        """
        if not data:
            self.mostra_mensagem("Aviso", "Não há registros disponíveis para seleção.")
            return None

        layout = [
            [sg.Text(titulo, font=("Bookman Old Style", 16, "bold"))],
            [
                sg.Table(
                    values=data,
                    headings=headings,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    num_rows=min(15, len(data)),
                    justification="left",
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    enable_events=True,
                    key="-TABLE-",
                    expand_x=True,
                    expand_y=True,
                )
            ],
            [
                sg.Button("Confirmar", key="-OK-"),
                sg.Button("Cancelar", key="-CANCELAR-"),
            ],
        ]

        window = sg.Window(titulo, layout, finalize=True, resizable=True)
        selecionado = None

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break

            if event == "-OK-":
                if values["-TABLE-"]:
                    idx = values["-TABLE-"][0]
                    selecionado = lookup[idx]
                    break
                self.mostra_erro("Selecione uma linha antes de confirmar.")

        window.close()
        return selecionado
