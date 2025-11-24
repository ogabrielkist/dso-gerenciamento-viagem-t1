from datetime import datetime
import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI


class TelaTrechoViagemGUI(TelaBaseGUI):
    def __init__(self):
        super().__init__()
        self._controlador_meio_transporte = None

    def set_controlador_meio_transporte(self, controlador_meio_transporte):
        self._controlador_meio_transporte = controlador_meio_transporte

    def le_opcao(self):
        layout = [
            [
                sg.Text(
                    "Trechos de Viagem",
                    font=("Helvetica", 18, "bold"),
                    justification="center",
                    expand_x=True,
                )
            ],
            [sg.Button("Incluir", key="-INCLUIR-", size=(25, 2))],
            [sg.Button("Listar", key="-LISTAR-", size=(25, 2))],
            [sg.Button("Editar", key="-EDITAR-", size=(25, 2))],
            [sg.Button("Excluir", key="-EXCLUIR-", size=(25, 2))],
            [sg.VPush()],
            [sg.Button("Voltar", key="-VOLTAR-", size=(25, 2))],
        ]
        window = sg.Window("Trechos de Viagem", layout, finalize=True)
        event, _ = window.read()
        window.close()
        if event in (sg.WIN_CLOSED, "-VOLTAR-"):
            return "-VOLTAR-"
        return event

    def pega_dados_entidade(self, dados_atuais=None):
        meios = (
            self._controlador_meio_transporte.get_entidades()
            if self._controlador_meio_transporte
            else []
        )
        if not meios:
            self.mostra_erro(
                "Cadastre pelo menos um meio de transporte antes de criar trechos."
            )
            return None

        mapa_meio = {
            f"{meio.tipo.value} - {meio.empresa.nome}": meio for meio in meios
        }
        meio_default = (
            f"{dados_atuais['meio_transporte'].tipo.value} - "
            f"{dados_atuais['meio_transporte'].empresa.nome}"
            if dados_atuais
            else next(iter(mapa_meio.keys()))
        )

        data_atual = (
            dados_atuais["data"].strftime("%Y-%m-%d %H:%M") if dados_atuais else ""
        )
        origem_atual = dados_atuais["local_origem"] if dados_atuais else ""
        destino_atual = dados_atuais["local_destino"] if dados_atuais else ""

        titulo = "Editar Trecho" if dados_atuais else "Novo Trecho"
        layout = [
            [sg.Text(titulo, font=("Helvetica", 16))],
            [
                sg.Text("Data e Hora (YYYY-MM-DD HH:MM):", size=(30, 1)),
                sg.Input(default_text=data_atual, key="-DATA-"),
            ],
            [
                sg.Text("Origem:", size=(30, 1)),
                sg.Input(default_text=origem_atual, key="-ORIGEM-"),
            ],
            [
                sg.Text("Destino:", size=(30, 1)),
                sg.Input(default_text=destino_atual, key="-DESTINO-"),
            ],
            [
                sg.Text("Meio de Transporte:", size=(30, 1)),
                sg.Combo(
                    list(mapa_meio.keys()),
                    default_value=meio_default,
                    readonly=True,
                    key="-MEIO-",
                ),
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
                    data = datetime.strptime(values["-DATA-"], "%Y-%m-%d %H:%M")
                    origem = values["-ORIGEM-"].strip()
                    destino = values["-DESTINO-"].strip()

                    if not origem or not destino:
                        raise ValueError("Origem e destino são obrigatórios.")

                    meio = mapa_meio[values["-MEIO-"]]
                    dados = {
                        "data": data,
                        "local_origem": origem,
                        "local_destino": destino,
                        "meio_transporte": meio,
                    }
                    break
                except ValueError as err:
                    self.mostra_erro(str(err))

        window.close()
        return dados

    def mostra_lista_entidades(self, dados_lista):
        if not dados_lista:
            self.mostra_mensagem("Trechos", "Nenhum trecho cadastrado.")
            return

        headings = ["ID", "Data", "Origem", "Destino", "Meio"]
        data = [
            [
                d["id"],
                d["data"].strftime("%d/%m/%Y %H:%M"),
                d["local_origem"],
                d["local_destino"],
                f"{d['meio_transporte'].tipo.value} - {d['meio_transporte'].empresa.nome}",
            ]
            for d in dados_lista
        ]
        self.mostra_lista("Trechos de Viagem", headings, data)

    def seleciona_entidade(self, dados_lista, titulo_janela):
        if not dados_lista:
            self.mostra_erro("Nenhum trecho cadastrado.")
            return None

        headings = ["ID", "Data", "Origem", "Destino"]
        data = []
        id_lookup = []
        for d in dados_lista:
            data.append(
                [
                    d["id"],
                    d["data"].strftime("%d/%m/%Y %H:%M"),
                    d["local_origem"],
                    d["local_destino"],
                ]
            )
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
                self.mostra_erro("Selecione um trecho.")

        window.close()
        return selecionado
