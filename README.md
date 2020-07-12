# Bot-PUG-SE
É o bot do Telegram para a comunidade PUG-SE.
Este bot foi feito pela comunidade de Python PUG-SE para levar informações importantes sobre a linguagem Python e eventos da comunidade.
Para saber quais as funcionalidades do bot, execute o mesmo e digite ``/help``

# Funcionalidades
- Agendamento de comandos
- Cache de comandos
- Acesso ao banco de dados
- Comandos (descritos em /help)

# Como executar
1) Adicione as seguintes variáveis de ambiente:
    - TELEGRAM_KEY  (token do Telegram)
    - TELEGRAM_CHAT_ID (id do grupo onde o bot irá rodar)
    - DATABASE_URL (opcional, URL de conexão com o banco de dados PostgreSQL)
2) Execute o comando ``python ./pugsebot/bot.py``

# Schedules
1) Configure uma base de dados
2) Defina a variável DATABASE_URL, que deve seguir o formato de url definido pelo <a href="https://docs.sqlalchemy.org/en/13/core/engines.html">SQLAlchemy</a>

# Como ajudar no projeto: 
1) Crie um branch a partir do branch dev
2) Implemente suas alterações. 
3) Adicione os testes em tests.py (usamos este framework https://docs.python.org/3/library/unittest.html)
4) Rode o script de ``./run_tests.sh`` (Linux) ou ``./run_tests.bat`` (Windows)
5) Faça um Pull Request para o dev e aguarde revisão

# Adicionando um novo comando
1) Crie um módulo no package commands
2) Crie uma classe e herde da classe utils.command_base.CommandBase
3) Inicialize super() os seguintes atributos:
    - name (nome do comando)
    - help_text (descrição geral do comando)
    - reply_function_name (nome da função do bot que será chamada no resultado da function). São 4 modos possíveis:
        - reply_text: responde a mensagem de um usuário com uma mensagem de texto
        - reply_photo: responde a mensagem de um usuário com uma imagem
        - send_text: envia uma mensagem de texto para o grupo alvo (definido em TELEGRAM_CHAT_ID)
        - send_image: envia uma imagem para o grupo alvo (definido em TELEGRAM_CHAT_ID)
    - schedule_interval (intervalo em segundos para a execução agendada, use None se não quiser agendar)
        - devido ao hibernamento de dynos no Heroku, o comando pode não ser executado na hora exata. Porém, o dyno vai executar comandos com execução agendada quando o bot acordar (agendamentos repetidos serão ignorados)
    - expire (duração em segundos da validade da cache, opcional)
4) Implemente function (código do seu comando)
    - Caso precise guardar algo no banco, use as funções set_info, get_info e remove_info de utils.command_base.CommandBase
    - exemplos de módulos de funcionalidades podem ser observados dentro do package commands

# Testes
1) Execute o comando
