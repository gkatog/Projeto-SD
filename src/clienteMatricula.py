import PortalDeMatricula_pb2_grpc
import PortalDeMatricula_pb2

import grpc
import sys


class PortalMatriculaCliente:
    def __init__(self, porta: int):
        self.porta = porta

    def adicionaProfessor(self, sigla_disciplina: str, siape_professor: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.porta}') as channel:
            stub = PortalDeMatricula_pb2_grpc.PortalMatriculaStub(channel)

            try:
                reply = stub.AdicionaProfessor(
                    PortalDeMatricula_pb2.DisciplinaPessoa(
                        disciplina=sigla_disciplina,
                        idPessoa=siape_professor
                    )
                )

                print()
                if reply.status != 1:
                    print('Professor adicionado com sucesso a disciplina')
                else:
                    print(f'{reply.msg}')
            except grpc.RpcError as e:
                print(f'adicionaProfessor: {e}')

    def removeProfessor(self, sigla_disciplina: str, siape_professor: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.porta}') as channel:
            stub = PortalDeMatricula_pb2_grpc.PortalMatriculaStub(channel)

            try:
                reply = stub.RemoveProfessor(
                    PortalDeMatricula_pb2.DisciplinaPessoa(
                        disciplina=sigla_disciplina,
                        idPessoa=siape_professor
                    )
                )

                print()
                if reply.status != 1:
                    print('Professor removido com sucesso')
                else:
                    print(f'{reply.msg}')
            except grpc.RpcError as e:
                print(f'removeProfessor: {e}')

    def adicionaAluno(self, sigla_disciplina: str, matricula_aluno: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.porta}') as channel:
            stub = PortalDeMatricula_pb2_grpc.PortalMatriculaStub(channel)

            try:
                reply = stub.AdicionaAluno(
                    PortalDeMatricula_pb2.DisciplinaPessoa(
                        disciplina=sigla_disciplina,
                        idPessoa=matricula_aluno
                    )
                )

                print()
                if reply.status != 1:
                    print('Aluno inserido com sucesso')
                else:
                    print(reply.msg)
            except grpc.RpcError as e:
                print(f'adicionaAluno: {e}')

    def removeAluno(self, sigla_disciplina: str, matricula_aluno: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.porta}') as channel:
            stub = PortalDeMatricula_pb2_grpc.PortalMatriculaStub(channel)

            try:
                reply = stub.RemoveAluno(
                    PortalDeMatricula_pb2.DisciplinaPessoa(
                        disciplina=sigla_disciplina,
                        idPessoa=matricula_aluno
                    )
                )

                print()
                if reply.status != 1:
                    print('Aluno removido com sucesso')
                else:
                    print(reply.msg)
            except grpc.RpcError as e:
                print(f'removeAluno: {e}')

    def detalheDisciplina(self, sigla_disciplina: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.porta}') as channel:
            stub = PortalDeMatricula_pb2_grpc.PortalMatriculaStub(channel)

            try:
                reply = stub.DetalhaDisciplina(
                    PortalDeMatricula_pb2.Identificador(
                        id=sigla_disciplina
                    )
                )

                print()
                if reply.disciplina.sigla == '' and reply.disciplina.nome == '':
                    print('Disciplina não encontrada ou sem dados')
                else:
                    print(reply)
            except grpc.RpcError as e:
                print(f'detalheDisciplina: {e}')

    def obtemDisciplinasProfessor(self, siape_professor: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.porta}') as channel:
            stub = PortalDeMatricula_pb2_grpc.PortalMatriculaStub(channel)

            try:
                replies = stub.ObtemDisciplinasProfessor(
                    PortalDeMatricula_pb2.Identificador(
                        id=siape_professor
                    )
                )

                print()
                print(f'Disciplinas do professor:')
                for disc in replies:
                    print(f'{disc.disciplina.sigla}: {disc.disciplina.nome} com {disc.disciplina.vagas} vaga(s)')
                    print(f'\t- {disc.professor.siape}: {disc.professor.nome}')
                    print(f'\tCom os alunos:')
                    for aluno in disc.alunos:
                        if aluno.matricula != '' and aluno.nome != '':
                            print(f'\t\t* {aluno.matricula}: {aluno.nome}')
            except grpc.RpcError as e:
                print(f'obtemDisciplinasProfessor: {e}')

    def obtemDisciplinasAluno(self, matricula_aluno: str) -> None:
        with grpc.insecure_channel(f'localhost:{self.porta}') as channel:
            stub = PortalDeMatricula_pb2_grpc.PortalMatriculaStub(channel)

            try:
                replies = stub.ObtemDisciplinasAluno(
                    PortalDeMatricula_pb2.Identificador(
                        id=matricula_aluno
                    )
                )

                print()
                print('Disciplinas do aluno:')
                for reply in replies:
                    print(f'{reply.disciplina.sigla}: {reply.disciplina.nome} com {reply.disciplina.vagas} vaga(s)')

                    if reply.professor.siape == '' and reply.professor.nome == '':
                        print(f'\t- Disciplina sem professor')
                    else:
                        print(f'\t- {reply.professor.siape}: {reply.professor.nome}')

                    print(f'\t- Com {reply.totalAlunos} aluno(s) na disciplina')
            except grpc.RpcError as e:
                print(f'obtemDisciplinasAluno: {e}')


def menu_opcoes() -> None:
    print()
    print('#' * 20)
    print('1 - Adiciona professor')
    print('2 - Remove professor')
    print('3 - Adiciona aluno')
    print('4 - Remove aluno')
    print('5 - Detalha disciplina')
    print('6 - Obtem disciplinas professores')
    print('7 - Obtem disciplina alunos')
    print('#' * 20)


def menu(PortalMat: PortalMatriculaCliente) -> None:
    while True:
        menu_opcoes()
        opcoes = int(input('Digite uma opção: '))

        match opcoes:
            case 1:
                sigla_disciplina = input('Digite a sigla da disciplina: ')
                siape_professor = input('Digite o siape do profesor: ')

                PortalMat.adicionaProfessor(sigla_disciplina, siape_professor)
            case 2:
                sigla_disciplina = input('Digite a sigla da disciplina: ')
                siape_professor = input('Digite o siape do profesor: ')

                PortalMat.removeProfessor(sigla_disciplina, siape_professor)
            case 3:
                sigla_disciplina = input('Digite a sigla da disciplina: ')
                matricula_aluno = input('Digite a matrícula do aluno: ')

                PortalMat.adicionaAluno(sigla_disciplina, matricula_aluno)
            case 4:
                sigla_disciplina = input('Digite a sigla da disciplina: ')
                matricula_aluno = input('Digite a matrícula do aluno: ')

                PortalMat.removeAluno(sigla_disciplina, matricula_aluno)
            case 5:
                sigla_disciplina = input('Digite a sigla da disciplina: ')

                PortalMat.detalheDisciplina(sigla_disciplina)
            case 6:
                siape_professor = input('Digite o siape do professor: ')

                PortalMat.obtemDisciplinasProfessor(siape_professor)
            case 7:
                matricula_aluno = input('Digite a matrícula do aluno: ')

                PortalMat.obtemDisciplinasAluno(matricula_aluno)
            case _:
                print('Digite uma entrada válida')


if __name__ == '__main__':
    try:
        porta = int(sys.argv[1])
    except Exception:
        porta = 50051

    Portal = PortalMatriculaCliente(porta)

    menu(Portal)
