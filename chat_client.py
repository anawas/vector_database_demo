from sentence_transformers import SentenceTransformer
import db
import embeddings

conn = db.get_connection()
cur = conn.cursor()

query = "Who is Alan Turing?"
embedding: list[list[float]] = embeddings.get_embeddings([query])
# Use ::vector cast for the query embedding
cur.execute("""
SELECT content, embedding <=> %s::vector AS distance 
FROM documents 
ORDER BY distance 
LIMIT 3""", (embedding[0],))

result = cur.fetchall()
for res in result:
    print(res)

cur.close()
conn.close()

