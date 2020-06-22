# Bot-PUG-SE
É o bot do Telegram para a comunidade PUG-SE.

# Funcionalidades
- Schedule
- Cache
- ...

# Como executar
1) Adicione as seguintes variáveis de ambiente:
    - TELEGRAM_KEY  (token do Telegram)
    - TELEGRAM_CHAT_ID (id do grupo onde o bot irá rodar)
    - DATABASE_URL (opcional, URL de conexão com o banco de dados PostgreSQL)
2) Execute o comando ``python ./pugsebot/bot.py``

# Schedules
1) Configure uma base de dados
2) Defina a variável DATABASE_URL, que deve seguir o formato de url definido pelo <a href="https://docs.sqlalchemy.org/en/13/core/engines.html">SQLAlchemy</a>

# Adicionando um novo comando
1) Crie um módulo na pasta commands/
2) Crie uma classe e herde da classe utils.Command
3) Inicialize super() os seguintes atributos:
    - name (nome do comando)
    - help (descrição geral do comando)
    - reply_function_name (nome da função do bot que será chamada no resultado da function)
    - interval (intervalo em segundos para a execução agendada, use None se não quiser agendar)
    - expire, (duração em segundos da validade da cache, None se não quiser)
4) Implemente function (código do seu comando)

# Testes
1) Execute o comando ``./run_tests.sh`` (Linux) ou ``./run_tests.bat`` (Windows)
