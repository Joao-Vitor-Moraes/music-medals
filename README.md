# 🏅 Music Medals

Uma aplicação web que analisa seu histórico do Last.fm e transforma seus dados em um Quadro de Medalhas, mostrando seus artistas, álbuns e músicas mais ouvidos ao longo do último ano.

## ✨ Funcionalidades

  - **Quadro de Medalhas Detalhado:** Gera um ranking para artistas, álbuns e músicas baseado em suas posições no top 5 de cada um dos últimos 12 meses.
  - **Cache Inteligente:** Resultados para usuários já pesquisados são carregados instantaneamente para uma melhor experiência do usuário e menor carga no servidor.
  - **Busca por Usuário:** Permite que qualquer pessoa gere um quadro de medalhas para qualquer usuário do Last.fm.

## ⚠️ Limitações e Desvantagens

É importante notar algumas características de performance desta aplicação:

  - **Tempo de Processamento Inicial:** A primeira vez que um usuário é analisado, a aplicação precisa buscar e processar dados de 12 meses de histórico do Last.fm. Este processo é intensivo e pode levar de **30 segundos a mais de 1 minuto**, dependendo do volume de músicas do usuário e da velocidade da API do Last.fm.
  - **Atualização do Cache:** Para garantir uma performance rápida em visitas futuras, os resultados são salvos em um cache com validade de 24 horas. Isso significa que qualquer mudança nos hábitos musicais de um usuário só será refletida no ranking **após esse período de 1 dia**, quando os dados forem reprocessados.

## 🛠️ Tecnologias Utilizadas

#### **Backend**

  - **Python**
  - **Django** (para a estrutura da API)
  - **Pylast** (para comunicação com a API do Last.fm)
  - **Django Caching** (utilizando o backend de banco de dados)
  - **Concurrent.futures** (para paralelização de chamadas de API)

#### **Frontend**

  - **React**
  - **Next.js** (para a estrutura, renderização e otimizações)
  - **Tailwind CSS** (para estilização e design responsivo)

## 🚀 Como Rodar Localmente

Para rodar este projeto na sua máquina, siga os passos abaixo.

### Pré-requisitos

  - Python 3.10+
  - Node.js e npm
  - Uma conta de API do Last.fm para obter suas chaves.

### 1\. Clonando o Repositório

```bash
git clone https://github.com/Joao-Vitor-Moraes/music-medals.git
cd music-medals
```

### 2\. Configurando o Backend (Django)

1.  **Crie e ative o ambiente virtual:**

    ```bash
    # Na raiz do projeto
    python -m venv venv

    # No Windows
    .\venv\Scripts\activate

    # No macOS/Linux
    source venv/bin/activate
    ```

2.  **Crie o arquivo `requirements.txt` e instale as dependências:**
    *(Este passo é importante para que outros possam instalar as dependências corretas)*

    ```bash
    pip freeze > requirements.txt
    pip install -r requirements.txt
    ```

    *(Você só precisa fazer isso uma vez. Depois, salve e commite o arquivo `requirements.txt` gerado).*

3.  **Configure as Variáveis de Ambiente:**

      * Crie um arquivo chamado `.env` na raiz do projeto.
      * Adicione suas chaves da API do Last.fm dentro dele:
        ```ini
        LASTFM_API_KEY="SUA_CHAVE_DE_API_AQUI"
        LASTFM_SHARED_SECRET="SEU_SEGREDO_COMPARTILHADO_AQUI"
        ```

4.  **Prepare o Banco de Dados:**

    ```bash
    python manage.py migrate
    python manage.py createcachetable
    ```

5.  **Inicie o servidor do backend:**

    ```bash
    # Deve rodar em http://localhost:8000
    python manage.py runserver
    ```

### 3\. Configurando o Frontend (Next.js)

1.  **Abra um novo terminal.**

2.  **Navegue até a pasta `frontend` e instale as dependências:**

    ```bash
    cd frontend
    npm install
    ```

3.  **Inicie o servidor de desenvolvimento:**

    ```bash
    # Deve rodar em http://localhost:3000
    npm run dev
    ```

Após seguir estes passos, abra seu navegador e acesse **`http://localhost:3000`** para ver a aplicação funcionando\!

-----

Criado por **João Vitor Moraes**.
