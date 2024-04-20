import os
import threading
from time import sleep
from clienteAdministrativo import PortalAdministrativoCliente
from clienteMatricula import PortalMatriculaCliente
from servidorAdministrativo import run_server as run_admin_server
from servidorMatricula import run_server as run_matricula_server

# Configurações de porta para servidores e clientes
ADMIN_SERVER_PORTS = [50051, 50052]
MATRICULA_SERVER_PORTS = [60061, 60062]

def start_servers():
    # Inicializa os servidores administrativos em threads separadas
    admin_server_threads = []
    for port in ADMIN_SERVER_PORTS:
        thread = threading.Thread(target=run_admin_server, args=(port,))
        admin_server_threads.append(thread)
        thread.start()

    # Inicializa os servidores de matrícula em threads separadas
    matricula_server_threads = []
    for port in MATRICULA_SERVER_PORTS:
        thread = threading.Thread(target=run_matricula_server, args=(port,))
        matricula_server_threads.append(thread)
        thread.start()

    return admin_server_threads, matricula_server_threads

def perform_admin_operations(client):
    # Simula operações de administração

    # Caso de sucesso: Adicionar novo aluno
    client.novoAluno('12345', 'Rafael')
    sleep(2)

    # Caso de falha (aluno inexistente): Editar aluno
    client.editaAluno('99999', 'Nome Inválido')
    sleep(2)

    # Caso de sucesso: Obter todos os professores
    client.obtemTodosProfessores()
    sleep(2)

    # Caso de falha (disciplina inexistente): Remover disciplina
    client.removeDisciplina('disciplina123')
    sleep(2)

def perform_matricula_operations(client):
    # Simula operações de matrícula

    # Caso de sucesso: Adicionar professor
    client.adicionaProfessor('gbc011', '09876')
    sleep(2)

    # Caso de falha (professor já adicionado): Adicionar professor novamente
    client.adicionaProfessor('gbc011', '12345')
    sleep(2)

    # Caso de sucesso: Obter disciplinas de um aluno
    client.obtemDisciplinasAluno('12345')
    sleep(2)

    # Caso de falha (aluno inexistente): Obter disciplinas de aluno inexistente
    client.obtemDisciplinasAluno('99999')
    sleep(2)

if __name__ == "__main__":
    # Inicia os servidores em threads separadas
    admin_threads, matricula_threads = start_servers()

    # Inicializa os clientes administrativos e de matrícula
    admin_clients = [PortalAdministrativoCliente(port) for port in ADMIN_SERVER_PORTS]
    matricula_clients = [PortalMatriculaCliente(port) for port in MATRICULA_SERVER_PORTS]

    # Realiza operações de administração em clientes administrativos
    for client in admin_clients:
        threading.Thread(target=perform_admin_operations, args=(client,)).start()

    # Realiza operações de matrícula em clientes de matrícula
    for client in matricula_clients:
        threading.Thread(target=perform_matricula_operations, args=(client,)).start()

    # Aguarda a conclusão das threads dos servidores
    for thread in admin_threads:
        thread.join()
    for thread in matricula_threads:
        thread.join()
