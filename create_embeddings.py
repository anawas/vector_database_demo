# source: https://medium.com/@nitinprodduturi/using-postgresql-as-a-vector-database-for-rag-retrieval-augmented-generation-c62cfebd9560
# make sure the PostgreSQL is running. Use the docker compose file.
# This example dooes not use any cloud services. All embeddings are calculated and stored locally.
from sentence_transformers import SentenceTransformer
import db
import embeddings

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

embedding: list[list[float]] = embeddings.get_embeddings(docs)
# Use ::vector cast for the embedding
for doc, embed in zip(docs, embedding):
    print(doc, embed)
    cur.execute("INSERT INTO documents (content, embedding) VALUES (%s, %s::vector)", (doc, embed))
conn.commit()

cur.close()
conn.close()

