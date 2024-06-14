import pickle
import torch
from transformers import BartTokenizer, BartForConditionalGeneration
from langchain_community.vectorstores import Chroma

# Load BART model and tokenizer
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')

def load_index(index_file):
    """
    Load the index from disk using pickle.
    """
    with open(index_file, 'rb') as f:
        index = pickle.load(f)
    return index

def query_index(query, index, top_k=5):
    """
    Query the Chroma index to retrieve relevant documents.
    """
    response = index.similarity_search(query, k=top_k)
    return response

def format_response(response):
    """
    Format the retrieved documents into a structured response.
    """
    results = []
    for item in response:
        doc = item.metadata
        car_info = {
            'Brand': doc.get('Brand', 'N/A'),
            'Model': doc.get('Model', 'N/A'),
            'Body Style': doc.get('Body Style', 'N/A'),
            'Price (1-3 days)': doc.get(r'if 1-3 days\\ euro per day', 'N/A'),
            'Location': doc.get('Locations', 'N/A'),
            'Contact': doc.get('Contact person', 'N/A')
        }
        formatted_info = ', '.join(f'{key}: {value}' for key, value in car_info.items())
        results.append(formatted_info)
    return "\n".join(results)

def generate_response(retrieved_data, user_query):
    """
    Generate a response using the BART model based on the retrieved data and user query.
    """
    prompt = f"""
    You are a rental car agent. A user has asked the following question: "{user_query}"

    Based on the following car rental data:
    {retrieved_data}

    Provide a helpful and friendly response to the user as a car rental agent.
    """
    
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=150)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def handle_complex_queries(query, index_file='rental_car_index.pkl'):
    """
    Handle complex queries by retrieving and formatting data, then generating a response.
    """
    index = load_index(index_file)
    retrieved_data = query_index(query, index)
    formatted_data = format_response(retrieved_data)
    generated_response = generate_response(formatted_data, query)
    return generated_response

def handle_sequential_queries(queries, index_file='rental_car_index.pkl'):
    """
    Handle a sequence of queries by storing context and managing state between queries.
    """
    index = load_index(index_file)
    all_results = []
    for query in queries:
        retrieved_data = query_index(query, index)
        formatted_data = format_response(retrieved_data)
        all_results.append(formatted_data)
    return all_results

def get_lowest_priced_cars(index_file='rental_car_index.pkl', locations=None, num_cars=3):
    """
    Retrieve the lowest priced cars from specified locations.
    """
    index = load_index(index_file)

    if locations:
        location_query = ' OR '.join([f"Locations:{location}" for location in locations])
        retrieved_data = query_index(location_query, index, top_k=len(index.documents))
    else:
        retrieved_data = query_index('', index, top_k=len(index.documents))

    cars = [
        {
            "Brand": item.metadata['Brand'],
            "Model": item.metadata['Model'],
            "Price": item.metadata['if 1-3 days\\ euro per day'],
            "Location": item.metadata['Locations']
        }
        for item in retrieved_data
    ]

    sorted_cars = sorted(cars, key=lambda x: x['Price'])
    lowest_priced_cars = sorted_cars[:num_cars]
    return lowest_priced_cars
