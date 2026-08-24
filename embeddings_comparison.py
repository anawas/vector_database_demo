# source: https://medium.com/@nitinprodduturi/using-postgresql-as-a-vector-database-for-rag-retrieval-augmented-generation-c62cfebd9560
# make sure the PostgreSQL is running. Use the docker compose file.
# This example dooes not use any cloud services. All embeddings are calculated and stored locally.
from sentence_transformers import SentenceTransformer
import db
import embeddings
from psycopg2 import sql

conn = db.get_connection()
cur = conn.cursor()

docs = [
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
    "PostgreSQL is an open-source relational database.",
    "RAG combines retrieval and generation for better answers.",
    "pgvector adds vector search capabilities to Postgres."
]

similarity_fn_names = ["cosine", "dot", "euclidean", "manhattan"]

table_name = "documents"
attribute_name = "embedding"
print(f"Creating embeddings with similarity function 'euclidean'")
embedding: list[list[float]] = embeddings.get_embeddings(docs)
# Use ::vector cast for the embedding
print(f"Inserting into table {table_name}")
for doc, embed in zip(docs, embedding):
    cur.execute(
        sql.SQL("INSERT INTO {table} (content, {attr_name}) VALUES (%s, %s::vector)")
        .format(table=sql.Identifier(table_name), attr_name=sql.Identifier(attribute_name)), (doc, embed))
conn.commit()

cur.close()
conn.close()

