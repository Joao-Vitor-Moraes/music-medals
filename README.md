🏅 Music Medals
Uma aplicação web full-stack que analisa seu histórico do Last.fm e transforma seus hábitos musicais em um "Quadro de Medalhas" competitivo, mostrando seus artistas, álbuns e músicas mais ouvidos ao longo do último ano.

(Dica: Tire um screenshot da sua aplicação final e substitua o link acima para mostrar seu trabalho!)

✨ Funcionalidades
Quadro de Medalhas Detalhado: Gera um ranking para Artistas, Álbuns e Músicas baseado em suas posições no Top 5 de cada um dos últimos 12 meses.
Cache Inteligente: Resultados para usuários já pesquisados são carregados instantaneamente para uma melhor experiência do usuário e menor carga no servidor.
Busca por Usuário: Permite que qualquer pessoa gere um quadro de medalhas para qualquer usuário do Last.fm.
⚠️ Limitações e Desvantagens
É importante notar algumas características de performance desta aplicação:

Tempo de Processamento Inicial: A primeira vez que um usuário é analisado, a aplicação precisa buscar e processar dados de 12 meses de histórico do Last.fm. Este processo é intensivo e pode levar de 30 segundos a mais de 1 minuto, dependendo do volume de músicas do usuário e da velocidade da API do Last.fm.
Atualização do Cache: Para garantir uma performance rápida em visitas futuras, os resultados são salvos em um cache com validade de 24 horas. Isso significa que qualquer mudança nos hábitos musicais de um usuário só será refletida no ranking após esse período de 1 dia, quando os dados forem reprocessados.
🛠️ Tecnologias Utilizadas
Este projeto foi construído utilizando uma arquitetura moderna com backend e frontend desacoplados.

Backend
Python
Django (para a estrutura da API)
Pylast (para comunicação com a API do Last.fm)
Django Caching (utilizando o backend de banco de dados)
Concurrent.futures (para paralelização de chamadas de API)
Frontend
React
Next.js (para a estrutura, renderização e otimizações)
Tailwind CSS (para estilização e design responsivo)
🚀 Como Rodar Localmente
Para rodar este projeto na sua máquina, siga os passos abaixo.

Pré-requisitos
Python 3.10+
Node.js e npm
Uma conta de API do Last.fm para obter suas chaves.
1. Clonando o Repositório
Bash

git clone https://github.com/Joao-Vitor-Moraes/music-medals.git
cd music-medals
(Lembre-se de substituir pela URL do seu repositório)

2. Configurando o Backend (Django)
Crie e ative o ambiente virtual:

Bash

# Na raiz do projeto
python -m venv venv

# No Windows
.\venv\Scripts\activate

# No macOS/Linux
source venv/bin/activate
Crie o arquivo requirements.txt e instale as dependências:
(Este passo é importante para que outros possam instalar as dependências corretas)

Bash

pip freeze > requirements.txt
pip install -r requirements.txt
(Você só precisa fazer isso uma vez. Depois, salve e commite o arquivo requirements.txt gerado).

Configure as Variáveis de Ambiente:

Crie um arquivo chamado .env na raiz do projeto.
Adicione suas chaves da API do Last.fm dentro dele:
Ini, TOML

LASTFM_API_KEY="SUA_CHAVE_DE_API_AQUI"
LASTFM_SHARED_SECRET="SEU_SEGREDO_COMPARTILHADO_AQUI"
Prepare o Banco de Dados:

Bash

python manage.py migrate
python manage.py createcachetable
Inicie o servidor do backend:

Bash

# Deve rodar em http://localhost:8000
python manage.py runserver
3. Configurando o Frontend (Next.js)
Abra um novo terminal.

Navegue até a pasta frontend e instale as dependências:

Bash

cd frontend
npm install
Inicie o servidor de desenvolvimento:

Bash

# Deve rodar em http://localhost:3000
npm run dev
Após seguir estes passos, abra seu navegador e acesse http://localhost:3000 para ver a aplicação funcionando!
