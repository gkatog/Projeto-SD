<h1 align="center">Projeto de Sistemas Distribuídos</h1>

### Integrantes

- Gabriel Kato Gomes - 12021BCC037
- Lucas Daniel Cunha - 12021BCC038

### Requisitos

- [x] Implementação de hash locais (dicionários)
- [x] Implementação de clientes e servidores
- [x] API devidamente tratada (casos de erros/exceções)
- [x] Testes automatizados
- [x] Múltiplos clientes e servidores
- [x] Implementação do Pub-Sub (localhost 127.0.0.1 e porta TCP 1883)

### Estrutura de arquivos

Dentro da pasta __src__ estão todos os arquivos necessários para execução do projeto e os testes automatizado.
Já na pasta principal do projeto estão os arquivos necessários para executar os códigos dentro da pasta __src__
e o arquivo de dependências do projeto.

### Intalação e execução

Clone o repositório do projeto:

```bash
git clone https://github.com/gkatog/Projeto-SD.git
```

Intale todas as dependências necessárias:

```bash
cd Trabalho_de_SD
chmod +x compile.sh
./compile.sh
```

Inicialize o mosquitto, servidores e clientes:

```bash
mosquitto -v
./admin-server.sh <porta1>
./mat-server.sh   <porta1>
./admin-client.sh <porta2>
./mat-client.sh   <porta2>
```

Utilização: Para utilização dos servidores é feita por meio dos clientes,
será necessário utilizar a linha de comando criada nos clientes. São simples
CLI para escolha da opção de um número válido para exercutar alguma opração,
também (para alguns casos) será necessário informar alguns dados para
inserção, alteração, etc.

### Link dos vídeos

[Video da parte 1](colocar_o_link)
