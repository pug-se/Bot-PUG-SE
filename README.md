# Bot-PUG-SE
É o bot do Telegram para a comunidade PUG-SE.

# Funcionalidades

# Como executar
1) Adicione as seguintes variáveis de ambiente:
    - TELEGRAM_KEY  (token do Telegram)
    - TELEGRAM_CHAT_ID (id do grupo onde o bot irá rodar)
2) Execute o comando ``python ./pugsebot/bot.py``

# Adicionando um novo comando
1) Crie um módulo na pasta commands/
2) Crie uma classe e herde da classe utils.Command
3) Inicialize super() os seguintes atributos:
    - name (nome do comando)
    - help (descrição geral do comando)
    - reply_function_name (nome da função do bot que será chamada no resultado da function)
    - schedule (função que descreve o schedule do comando)
    - function (código do seu comando)
4) Em functions/__init__.py, adicione .seuMódulo import SeuComandoClasse 
4) Em functions/__init__.py, adicione SeuComandoClasse() em command_list

# Testes
1) Adicione a variável de ambiente TELEGRAM_KEY_TEST (token do Telegram)
2) Execute o comando ``python ./pugsebot/tests.py``