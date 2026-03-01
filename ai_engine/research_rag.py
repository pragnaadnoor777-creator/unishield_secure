import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

# 1. Setup Data Ingestion
# Documents in 'data/' should have metadata tags like 'department'
def load_secure_index(directory_path="./university_data"):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        # Create a dummy file if the folder is empty
        with open(f"{directory_path}/sample.txt", "w") as f:
            f.write("Quantum Physics Lab Report: Restricted to Physics Dept.")
    
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index

# 2. Secure Query Engine with Role-Based Access Control (RBAC)
def secure_query(index, user_query, user_dept):
    # Metadata Filtering: The AI "filters first, then searches" [cite: 88]
    filters = MetadataFilters(
        filters=[ExactMatchFilter(key="department", value=user_dept)]
    )
    
    query_engine = index.as_query_engine(filters=filters)
    response = query_engine.query(user_query)
    return response

# 3. Execution Logic
if __name__ == "__main__":
    # Initialize the index
    university_index = load_secure_index()
    
    # Example: A Physics student asking a question
    print("User: 'Tell me about the latest lab reports.'")
    print("System Role: Physics Student")
    
    answer = secure_query(university_index, "latest lab reports", "Physics")
    print(f"AI Response: {answer}")
