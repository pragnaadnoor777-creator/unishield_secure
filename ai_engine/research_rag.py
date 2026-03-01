import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Force Local Embeddings for AMD Slingshot Privacy standards
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.llm = None # Set to None for pure retrieval testing

def load_secure_index(directory_path="./university_data"):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        with open(f"{directory_path}/physics_sample.txt", "w") as f:
            f.write("Quantum Physics Lab Report: Restricted to Physics Dept. Author: Dr. Bose.")
    
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index

def secure_query(index, query_str, dept):
    # In a full demo, we would add metadata filters here
    query_engine = index.as_query_engine()
    response = query_engine.query(query_str)
    return response