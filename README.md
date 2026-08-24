# Vector Database Demo

A minimal, fully local semantic-search example built with Python, PostgreSQL, and
[pgvector](https://github.com/pgvector/pgvector). It turns short documents into
vector embeddings with
[`sentence-transformers/all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2),
stores them in PostgreSQL, and retrieves the documents closest to a natural-language query.

No hosted embedding or vector-database service is required.

## How it works

1. `embeddings.py` loads the Sentence Transformer model and creates 384-dimensional embeddings.
2. `create_embeddings.py` embeds the sample documents and inserts them into PostgreSQL.
3. `chat_client.py` embeds a question and uses pgvector cosine distance to return the three closest documents.

## Requirements

- Python 3.14 or later (as declared in `pyproject.toml`)
- [uv](https://docs.astral.sh/uv/) for Python environment management
- Docker with Docker Compose

## Setup

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/<your-username>/vectordb-demo.git
   cd vectordb-demo
   ```

2. Install the Python dependencies:

   ```bash
   uv add sentence-transformers psycopg2-binary python-dotenv
   ```

3. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

   On PowerShell, use:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Set `DB_USER_PASSWORD` in `.env` to the same value as `POSTGRES_PASSWORD`
   in `docker-compose.yml`. The Compose file currently uses
   `yoursecretpassword`.

5. Start PostgreSQL with pgvector:

   ```bash
   docker compose up -d
   ```

6. Create the pgvector extension and the table used by the scripts:

   ```bash
   docker compose exec db psql -U postgres -d postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"
   docker compose exec db psql -U postgres -d postgres -c "CREATE TABLE IF NOT EXISTS documents (id BIGSERIAL PRIMARY KEY, content TEXT NOT NULL, embedding VECTOR(384) NOT NULL);"
   ```

## Usage

Insert the sample documents and their embeddings:

```bash
uv run python create_embeddings.py
```

Run the example similarity query (`Who is Alan Turing?`):

```bash
uv run python chat_client.py
```

The client prints the three most relevant stored documents together with their
cosine distances. Smaller distances indicate closer matches.

To try another query, edit the `query` value in `chat_client.py` and run the
script again.

`embeddings_comparison.py` is an alternate loading script that demonstrates
safe SQL identifier composition with `psycopg2.sql`:

```bash
uv run python embeddings_comparison.py
```

> **Note:** Each loading-script run inserts another copy of the sample documents.
> Clear the table with `TRUNCATE TABLE documents;` if you want to start over.

## Configuration

Database settings are read from `.env`:

| Variable | Default | Description |
| --- | --- | --- |
| `DB_NAME` | `postgres` | PostgreSQL database name |
| `DB_USER_NAME` | `postgres` | PostgreSQL user |
| `DB_USER_PASSWORD` | none | PostgreSQL password |
| `DB_HOST` | `localhost` | PostgreSQL host |

The embedding model is loaded from `model_cache` with `local_files_only=True`.
If the cache is not included in your clone, download the model once and place it
there, or temporarily remove `local_files_only=True` in `embeddings.py` to let
Sentence Transformers download it.

## Project structure

```text
.
|-- chat_client.py             # Runs a pgvector similarity search
|-- create_embeddings.py       # Embeds and inserts sample documents
|-- db.py                      # Creates the PostgreSQL connection
|-- docker-compose.yml         # Starts PostgreSQL with pgvector
|-- embeddings.py              # Loads the model and creates embeddings
|-- embeddings_comparison.py   # Alternate insertion example
|-- model_cache/               # Local Sentence Transformer model cache
|-- pyproject.toml             # Python project metadata
`-- .env.example               # Database configuration template
```

## Before publishing

Do not commit `.env`, `.venv`, IDE settings, Python cache files, or database
data. Model caches can also make a repository unnecessarily large; consider
excluding `model_cache/` and allowing the model to download during setup.

## License

No license has been selected yet. Add a `LICENSE` file before publishing if you
want others to be able to reuse or modify the project under explicit terms.
