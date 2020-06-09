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
    - interval (intervalo em segundos para a execução agendada, use None se não quiser agendar)
4) Implemente function (código do seu comando)
5) Em commands/__init__.py, adicione .seuMódulo import SeuComandoClasse 
6) Em commands/__init__.py, adicione SeuComandoClasse() em command_list

# Testes
1) Execute o comando ``./run_tests.sh`` (Linux) ou ``./run_tests.bat`` (Windows)
