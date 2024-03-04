import PortalAdministrativo_pb2
import PortalAdministrativo_pb2_grpc

import grpc
import sys


class PortalAdministrativoCliente:
    def __init__(self, port: int):
        self.port = port

    def novoAluno(self, matricula: str, nome: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.NovoAluno(
                    PortalAdministrativo_pb2.Aluno(matricula=matricula, nome=nome)
                )

                print()
                if reply.status != 1:
                    print('Inserido com sucesso')
                else:
                    print(f'{reply.msg}')
            except grpc.RpcError as e:
                print(f'novoAluno: {e}')

    def editaAluno(self, matricula: str, nome: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.EditaAluno(
                    PortalAdministrativo_pb2.Aluno(matricula=matricula, nome=nome)
                )

                print()
                if reply.status != 1:
                    print('Alterado com sucesso')
                else:
                    print(f'{reply.msg}')
            except grpc.RpcError as e:
                print(f'editaAluno: {e}')

    def removeAluno(self, matricula: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.RemoveAluno(
                    PortalAdministrativo_pb2.Identificador(id=matricula)
                )

                print()
                if reply.status == 0:
                    print('Removeu com sucesso')
                else:
                    print(reply.msg)
            except grpc.RpcError as e:
                print(f'removeAluno: {e}')

    def obtemAluno(self, matricula: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.ObtemAluno(
                    PortalAdministrativo_pb2.Identificador(id=matricula)
                )

                print()
                if reply.nome != '' and reply.matricula != '':
                    print(f'{reply.matricula}: {reply.nome}')
                else:
                    print(f'Esse aluno não existe')
            except grpc.RpcError as e:
                print(f'obtemAluno: {e}')

    def obtemTodosAlunos(self) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                replies = stub.ObtemTodosAlunos(
                    PortalAdministrativo_pb2.Vazia()
                )

                print()
                print('Alunos:')
                for reply in replies:
                    print(f'{reply.matricula}: {reply.nome}')
            except grpc.RpcError as e:
                print(f'obtemTodosAlunos: {e}')

    def novoProfessor(self, siape: str, nome: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.NovoProfessor(
                    PortalAdministrativo_pb2.Professor(siape=siape, nome=nome)
                )

                print()
                if reply.status != 1:
                    print('Inserido com sucesso')
                else:
                    print(f'{reply.msg}')
            except grpc.RpcError as e:
                print(f'novoProfessor: {e}')

    def editaProfessor(self, siape: str, nome: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.EditaProfessor(
                    PortalAdministrativo_pb2.Professor(siape=siape, nome=nome)
                )

                print()
                if reply.status != 1:
                    print('Alterado com sucesso')
                else:
                    print(f'{reply.msg}')
            except grpc.RpcError as e:
                print(f'editaProfessor: {e}')

    def removeProfessor(self, siape: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.RemoveProfessor(
                    PortalAdministrativo_pb2.Identificador(id=siape)
                )

                print()
                if reply.status != 1:
                    print('Removido com sucesso')
                else:
                    print(reply.msg)
            except grpc.RpcError as e:
                print(f'removeProfessor: {e}')

    def obtemProfessor(self, siape: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.ObtemProfessor(
                    PortalAdministrativo_pb2.Identificador(id=siape)
                )

                print()
                if reply.nome != '' and reply.siape != '':
                    print(f'{reply.siape}: {reply.nome}')
                else:
                    print(f'Esse professor não existe')
            except grpc.RpcError as e:
                print(f'obtemProfessor: {e}')

    def obtemTodosProfessores(self) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                replies = stub.ObtemTodosProfessores(
                    PortalAdministrativo_pb2.Vazia()
                )

                print()
                print('Professores:')
                for reply in replies:
                    print(f'{reply.siape}: {reply.nome}')
            except grpc.RpcError as e:
                print(f'obtemTodosProfessores: {e}')

    def novaDisciplina(self, sigla: str, nome: str, vagas: int) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.NovaDisciplina(
                    PortalAdministrativo_pb2.Disciplina(
                        sigla=sigla,
                        nome=nome,
                        vagas=vagas
                    )
                )

                print()
                if reply.status != 1:
                    print('Inserido com sucesso')
                else:
                    print(f'{reply.msg}')
            except grpc.RpcError as e:
                print(f'novaDisciplina: {e}')

    def editaDisciplina(self, sigla: str, nome: str, vagas: int) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.EditaDisciplina(
                    PortalAdministrativo_pb2.Disciplina(
                        sigla=sigla,
                        nome=nome,
                        vagas=vagas
                    )
                )

                print()
                if reply.status != 1:
                    print('Alterado com sucesso')
                else:
                    print(f'{reply.msg}')
            except grpc.RpcError as e:
                print(f'editaDisciplina: {e}')

    def removeDisciplina(self, sigla: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.RemoveDisciplina(
                    PortalAdministrativo_pb2.Identificador(id=sigla)
                )

                print()
                if reply.status != 1:
                    print('Removido com sucesso')
                else:
                    print(reply.msg)
            except grpc.RpcError as e:
                print(f'removeDisciplina: {e}')

    def obtemDisciplina(self, sigla: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                reply = stub.ObtemDisciplina(
                    PortalAdministrativo_pb2.Identificador(id=sigla)
                )

                print()
                if reply.sigla != '' and reply.nome != '' and reply.vagas > 0:
                    print(f'{reply.sigla}: {reply.nome} com {reply.vagas} vaga(s)')
                else:
                    print(f'Essa disciplina não existe')
            except grpc.RpcError as e:
                print(f'obtemDisciplina: {e}')

    def obtemTodasDisciplinas(self) -> None:
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = PortalAdministrativo_pb2_grpc.PortalAdministrativoStub(channel)

            try:
                replies = stub.ObtemTodasDisciplinas(
                    PortalAdministrativo_pb2.Vazia()
                )

                print()
                print('Disciplinas:')
                for reply in replies:
                    print(f'{reply.sigla}: {reply.nome} com {reply.vagas} vagas')
            except grpc.RpcError as e:
                print(f'obtemTodasDisciplinas: {e}')


def menu_opcoes() -> None:
    print()
    print('#' * 20)
    print('1 - Novo Aluno')
    print('2 - Edita Aluno')
    print('3 - Remove Aluno')
    print('4 - Obtem Aluno')
    print('5 - Obtem todo alunos')
    print('6 - Novo professor')
    print('7 - Edita professor')
    print('8 - Remove professor')
    print('9 - Obtem professor')
    print('10 - Obtem todos professores')
    print('11 - Nova disciplina')
    print('12 - Edita disciplina')
    print('13 - Remove disciplina')
    print('14 - Obtem disciplina')
    print('15 - Obtem todas disciplinas')
    print('#' * 20)


def menu(porta: int) -> None:
    PortalAdm = PortalAdministrativoCliente(porta)

    print(f'Funcionando na porta: {porta}')

    while True:
        menu_opcoes()
        opcao = int(input('Digite uma opção: '))

        match opcao:
            case 1:
                matricula = input('Digite a matricula: ')
                nome = input('Digite o nome: ')

                PortalAdm.novoAluno(matricula, nome)
            case 2:
                matricula = input('Digite a matricula: ')
                nome = input('Digite o nome: ')

                PortalAdm.editaAluno(matricula, nome)
            case 3:
                matricula = input('Digite a matricula: ')

                PortalAdm.removeAluno(matricula)
            case 4:
                matricula = input('Digite a matricula: ')

                PortalAdm.obtemAluno(matricula)
            case 5:
                PortalAdm.obtemTodosAlunos()
            case 6:
                siape = input('Digite o siape: ')
                nome = input('Digite o nome: ')

                PortalAdm.novoProfessor(siape, nome)
            case 7:
                siape = input('Digite o siape: ')
                nome = input('Digite o nome: ')

                PortalAdm.editaProfessor(siape, nome)
            case 8:
                siape = input('Digite o siape: ')

                PortalAdm.removeProfessor(siape)
            case 9:
                siape = input('Digite o siape: ')

                PortalAdm.obtemProfessor(siape)
            case 10:
                PortalAdm.obtemTodosProfessores()
            case 11:
                sigla = input('Digite a sigla: ')
                nome = input('Digite o nome: ')
                vagas = int(input('Digite o número de vagas: '))

                PortalAdm.novaDisciplina(sigla, nome, vagas)
            case 12:
                sigla = input('Digite a sigla: ')
                nome = input('Digite o nome: ')
                vagas = int(input('Digite o número de vagas: '))

                PortalAdm.editaDisciplina(sigla, nome, vagas)
            case 13:
                sigla = input('Digite a sigla: ')

                PortalAdm.removeDisciplina(sigla)
            case 14:
                sigla = input('Digite a sigla: ')

                PortalAdm.obtemDisciplina(sigla)
            case 15:
                PortalAdm.obtemTodasDisciplinas()
            case _:
                print('Digite um valor válido')


if __name__ == '__main__':
    try:
        porta = int(sys.argv[1])
    except Exception:
        porta = 60061

    menu(porta)
