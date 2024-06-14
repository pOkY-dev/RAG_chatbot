import pandas as pd
import pickle
from llama_index.core import VectorStoreIndex, Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Define the embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

def create_index(data_file, index_file):
    """
    Load rental data from an Excel file, create Document objects, and build an index.
    Save the index to disk using pickle.
    """
    # Load rental data from Excel
    rental_data = pd.read_excel(data_file)
    
    # Convert DataFrame directly to Document objects
    documents = [
        Document(text=str(row.to_dict()), metadata={"id": i})
        for i, row in rental_data.iterrows()
    ]

    # Create the index with the documents and the embedding model
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    
    # Save the index to disk using pickle
    with open(index_file, 'wb') as f:
        pickle.dump(index, f)

def load_index(index_file):
    """
    Load the index from disk using pickle.
    """
    with open(index_file, 'rb') as f:
        index = pickle.load(f)  
    return index

if __name__ == "__main__":
    data_file = 'data/merged_data_test_task.xlsx'
    index_file = 'rental_car_index.pkl'
    create_index(data_file, index_file)
