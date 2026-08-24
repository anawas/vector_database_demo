from sentence_transformers import SentenceTransformer
from typing import Literal

def get_embeddings(document: list[str], similarity_function: Literal["cosine", "dot", "euclidean", "manhattan"]="euclidean") -> list[list[float]]:
    # we can select the similarity function from 'cosine', 'dot', 'euclidean', and 'manhattan'
    transformer = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2",
                                      cache_folder="model_cache",
                                      local_files_only=True,
                                      similarity_fn_name=similarity_function)
    return transformer.encode(document).tolist()
