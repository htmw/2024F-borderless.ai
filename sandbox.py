from sentence_transformers import SentenceTransformer
import logging
from pinecone import Pinecone

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the model
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

pinecone_api_key = "06b354bc-e1b7-4a4f-aac7-1dd8ff4b941b"
index_name = "immigration-vectors-index"

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

# Wait for Pinecone index to be ready
while not pc.describe_index(index_name).status['ready']:
    logging.info("Waiting for Pinecone index to be ready...")

index = pc.Index(index_name)
logging.info("Pinecone index is ready.")

# Function to query Pinecone index with a given query
def query_pinecone(query):
    # Encode the query using SentenceTransformer
    query_vector = model.encode(query).tolist()
    logging.info(f"Query: {query}")

    # Perform the query on Pinecone
    response = index.query(vector=query_vector, top_k=5, include_metadata=True)
    
    # Return the results
    results = []
    for match in response['matches']:
        results.append({
            "document_id": match['metadata']['document_id'],
            "segment_index": match['metadata']['segment_index'],
            "segment_text": match['metadata']['segment_text'],
            "similarity_score": match['score']
        })
    
    return results


# import numpy as np
# import firebase_admin
# from firebase_admin import credentials, firestore
# from nltk import sent_tokenize
# from sentence_transformers import SentenceTransformer
# from pinecone import Pinecone
# import logging
# from torch.utils.data import DataLoader, Dataset

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Firebase and Pinecone configuration
# firebase_config = {
#     "type": "service_account",
#     "apiKey": "AIzaSyDQlZ5U-o9aj3OXcLNTI-k_t8ufpI9JqXo",
#     "authDomain": "borderlessai-filestore.firebaseapp.com",
#     "projectId": "borderlessai-filestore",
#     "private_key_id": "08bbb04a664a5443c921f633ffbd964f6126cf7c",
#     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDMcV/PwQUH6eFV\nwL/0zmWV0xEBGLfE1Tg00DIJvZU4aPM/g15hdAj2eYqB8zZ4GwgdO60m/0qQ8+nc\nEz6bTOa92JcleC637YiPARDbtTvxRuNX1+oF1DJRIesHhofncP7wJtci68DjdQuZ\nYb5sKCH5nTHtrs6AeSlDVfndIxpQWZfUsDkk2+CAabOSfErtJwfuaoQpHq91QCCd\npcUcj8Xnm+u2oTnDF+Z+jpGNFMUCxhx3+7V1PkUyoeg3c3LkcUaMxEal/j+c+aQJ\nb4l3zht0UDLo3VVeV8hTu0oKyi3B5YGoBwlGgj5jAdaTwyz1LfYVb0IxmzHT7iRi\ni1lWVQ9xAgMBAAECggEAFc1dZ11xOOfTNP7qOaQtJy4sGQ7WwjHu3Yr6WxmRqUNf\n9Xz/+qqSLh7GC5exTluroNp1W7xL6mtonCSdP5iS3toTPFa1vL2jG4UElDmem9tw\ncTTAa0C24PoaA2JwadkeBuRNexbjKh6YTxIiaYxaGzGNWoiS0xaYtOqdS9zreHf0\nsH9ihpU4lahZXO4HdelvH1XKZNqENGgs3sIawVbsjM+nSt0LUVGERMw3ViCRuCoy\nQoCb+WhJE46S5U5EIzISX6bW1oefHEPgZTqtGYEQUm0NvDqIoXO5TdMbcXafM1wQ\nj8h2mlAaiCF0q+oUkOamExldsNyqZAkhPUJl9dxYlQKBgQDpJ+tEF31/mU3Mel5T\nMtHPJCBYYrCgft8j62+/2W2oQBg7nsIqdZt4wug8yqBBf2ZtMvEYUrLdtougm9tN\ntufqGGGNesyu3HTg3FErQvWW0CfCdz78NSblrMJCyyML+fnnxxw1heGNVkBZNVzr\nFe0B2gMu/4AYqu3E0VzUrOnEnwKBgQDgeUQrOkj7JuHrE5jqugsxgm1FgG9pXZXe\nhCtXvAVK+V9r3wLEMzFH9P4y+Z8xLlMIN0YU8p/TU4PSCHyCv37T6XGvxzddsgOV\nmxzkCsoqereBk2rRAu/ze0Ji6Px9ZAX6Emby29ExrqgKMZMcN9n0Ryn3pHLQwW6n\nMvw384Ih7wKBgGnhyQO5LzL9KcmMYL2jvIg3PcElwFSCiU9EohEb6qKXyOl6ZW7m\nzd3/lXvWAQT9mERK+BY1qCjrt2kOnn8iaxtySwr3E3DtiN587xeYZvNAQG4dvSrH\n8Iwo8mdm3NmZghXx5CuiSxXmb36Tr0jLQkCvAvca7M9HAId7FI84n0i9AoGAJ2SA\nlwlyd0i6itN0mXSutDCMVo8UfiwjOdp99LaVQzQCD98iECZftp4C4hU2X54eiimR\nDeoKLD7SulAs8ZEDg9LK1asjRzkPMfj3l/lgwxWoEIA7VZSrYVI3Mz5p2ONtvRXv\npRz4WDyrVqaeh2wxvpGihsgAMixP692hr3v3UVcCgYAk3kDVRV36iaMPXwbqKycU\n4QntYw/w/pAkY6xHlnYLk0jtSUtliZEAVYQweojWc1poVkQfJTgsa+Lh/jfb1SFh\n5c3WgxxwQ30gq8+TRCJe0hcxGv+ls6hi3//yUGwVcU+zvqOLAQcy6nI3oTCI3sOU\nVMXFpoVTaNOAOYEk/go9uA==\n-----END PRIVATE KEY-----\n",
#     "client_email": "firebase-adminsdk-njswn@borderlessai-filestore.iam.gserviceaccount.com",
#     "client_id": "101159615520864016018",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-njswn%40borderlessai-filestore.iam.gserviceaccount.com",
#     "storageBucket": "borderlessai-filestore.appspot.com",
# }

# pinecone_api_key = "06b354bc-e1b7-4a4f-aac7-1dd8ff4b941b"
# index_name = "immigration-vectors-index"

# # Global variable to hold the model in each subprocess
# model = None

# # Model initialization for each worker
# def initialize_model():
#     global model
#     if model is None:
#         logging.info("Loading Sentence Transformer model in subprocess.")
#         model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

# # Dataset and DataLoader for efficient batching
# class TextDataset(Dataset):
#     def __init__(self, segments):
#         self.segments = segments

#     def __len__(self):
#         return len(self.segments)

#     def __getitem__(self, idx):
#         return self.segments[idx]

# def embed_segments(segments):
#     """Embed a batch of text segments."""
#     if model is None:
#         initialize_model()
#     return model.encode(segments)

# import re

# def process_document(doc_id, document_text, index):
#     """Process each document by segmenting, cleaning, embedding, and upserting to Pinecone."""
#     # Tokenize into segments
#     segments = sent_tokenize(document_text)
#     cleaned_segments = []

#     # Clean each segment
#     for segment in segments:
#         # 1. Strip extra whitespace and newlines
#         cleaned_text = segment.replace('\n', ' ').strip()
        
#         # 2. Remove metadata-like text patterns (e.g., "[ 123 ]")
#         cleaned_text = re.sub(r'\[\s*\d+\s*\]', '', cleaned_text)
        
#         # 3. Filter out short or empty segments
#         if len(cleaned_text) > 5:  # adjust length threshold as needed
#             cleaned_segments.append(cleaned_text)
    
#     # Prepare dataset for embedding
#     dataset = TextDataset(cleaned_segments)
#     dataloader = DataLoader(dataset, batch_size=64, shuffle=False)

#     # Embed and upsert each batch of cleaned segments
#     for batch in dataloader:
#         embeddings = embed_segments(batch)
#         vectors = []
#         for i, (embedding, segment) in enumerate(zip(embeddings, batch)):
#             vectors.append({
#                 "id": f"doc_{doc_id}_seg_{i}",
#                 "values": embedding.tolist(),
#                 "metadata": {
#                     "document_id": doc_id,
#                     "segment_index": i,
#                     "segment_text": segment
#                 }
#             })

#         logging.info(f"Upserting {len(vectors)} vectors for document ID {doc_id}")
#         upsert_to_pinecone(index, vectors)
#         logging.info(f"Successfully upserted {len(vectors)} vectors for document ID {doc_id}")

# def upsert_to_pinecone(index, vectors):
#     """Upsert vectors to Pinecone."""
#     index.upsert(vectors)
#     logging.info(f"Upserted batch of {len(vectors)} vectors to Pinecone.")

# if __name__ == "__main__":
#     # Initialize Firebase and Pinecone connections in the main process
#     cred = credentials.Certificate(firebase_config)
#     firebase_admin.initialize_app(cred, {
#         'storageBucket': 'borderlessai-filestore.appspot.com',
#         "projectId": "borderlessai-filestore"
#     })
#     db = firestore.client()
#     logging.info("Fetching document text data from Firestore.")
#     docs = db.collection("documents").stream()
#     document_texts = [(i, doc.to_dict().get("extracted_text", "")) for i, doc in enumerate(docs)]
#     logging.info(f"Retrieved {len(document_texts)} documents from Firestore.")

#     pc = Pinecone(api_key=pinecone_api_key)
#     while not pc.describe_index(index_name).status['ready']:
#         logging.info("Waiting for Pinecone index to be ready...")
#     index = pc.Index(index_name)
#     logging.info("Pinecone index is ready.")

#     # Process documents sequentially for debugging
#     for doc_id, text in document_texts:
#         logging.info(f"Processing document ID {doc_id}")
#         process_document(doc_id, text, index)

# # import os
# # import tempfile
# # from datetime import datetime
# # from pathlib import Path
# # import firebase_admin
# # from firebase_admin import credentials, firestore, storage
# # import pdfplumber
# # import pandas as pd
# # from bs4 import BeautifulSoup
# # import csv
# # import yaml
# # from docx import Document

# # # # Firebase configuration
# # firebase_config = {
# #     "type": "service_account",
# #     "apiKey": "AIzaSyDQlZ5U-o9aj3OXcLNTI-k_t8ufpI9JqXo",
# #     "authDomain": "borderlessai-filestore.firebaseapp.com",
# #     "projectId": "borderlessai-filestore",
# #     "private_key_id": "08bbb04a664a5443c921f633ffbd964f6126cf7c",
# #     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDMcV/PwQUH6eFV\nwL/0zmWV0xEBGLfE1Tg00DIJvZU4aPM/g15hdAj2eYqB8zZ4GwgdO60m/0qQ8+nc\nEz6bTOa92JcleC637YiPARDbtTvxRuNX1+oF1DJRIesHhofncP7wJtci68DjdQuZ\nYb5sKCH5nTHtrs6AeSlDVfndIxpQWZfUsDkk2+CAabOSfErtJwfuaoQpHq91QCCd\npcUcj8Xnm+u2oTnDF+Z+jpGNFMUCxhx3+7V1PkUyoeg3c3LkcUaMxEal/j+c+aQJ\nb4l3zht0UDLo3VVeV8hTu0oKyi3B5YGoBwlGgj5jAdaTwyz1LfYVb0IxmzHT7iRi\ni1lWVQ9xAgMBAAECggEAFc1dZ11xOOfTNP7qOaQtJy4sGQ7WwjHu3Yr6WxmRqUNf\n9Xz/+qqSLh7GC5exTluroNp1W7xL6mtonCSdP5iS3toTPFa1vL2jG4UElDmem9tw\ncTTAa0C24PoaA2JwadkeBuRNexbjKh6YTxIiaYxaGzGNWoiS0xaYtOqdS9zreHf0\nsH9ihpU4lahZXO4HdelvH1XKZNqENGgs3sIawVbsjM+nSt0LUVGERMw3ViCRuCoy\nQoCb+WhJE46S5U5EIzISX6bW1oefHEPgZTqtGYEQUm0NvDqIoXO5TdMbcXafM1wQ\nj8h2mlAaiCF0q+oUkOamExldsNyqZAkhPUJl9dxYlQKBgQDpJ+tEF31/mU3Mel5T\nMtHPJCBYYrCgft8j62+/2W2oQBg7nsIqdZt4wug8yqBBf2ZtMvEYUrLdtougm9tN\ntufqGGGNesyu3HTg3FErQvWW0CfCdz78NSblrMJCyyML+fnnxxw1heGNVkBZNVzr\nFe0B2gMu/4AYqu3E0VzUrOnEnwKBgQDgeUQrOkj7JuHrE5jqugsxgm1FgG9pXZXe\nhCtXvAVK+V9r3wLEMzFH9P4y+Z8xLlMIN0YU8p/TU4PSCHyCv37T6XGvxzddsgOV\nmxzkCsoqereBk2rRAu/ze0Ji6Px9ZAX6Emby29ExrqgKMZMcN9n0Ryn3pHLQwW6n\nMvw384Ih7wKBgGnhyQO5LzL9KcmMYL2jvIg3PcElwFSCiU9EohEb6qKXyOl6ZW7m\nzd3/lXvWAQT9mERK+BY1qCjrt2kOnn8iaxtySwr3E3DtiN587xeYZvNAQG4dvSrH\n8Iwo8mdm3NmZghXx5CuiSxXmb36Tr0jLQkCvAvca7M9HAId7FI84n0i9AoGAJ2SA\nlwlyd0i6itN0mXSutDCMVo8UfiwjOdp99LaVQzQCD98iECZftp4C4hU2X54eiimR\nDeoKLD7SulAs8ZEDg9LK1asjRzkPMfj3l/lgwxWoEIA7VZSrYVI3Mz5p2ONtvRXv\npRz4WDyrVqaeh2wxvpGihsgAMixP692hr3v3UVcCgYAk3kDVRV36iaMPXwbqKycU\n4QntYw/w/pAkY6xHlnYLk0jtSUtliZEAVYQweojWc1poVkQfJTgsa+Lh/jfb1SFh\n5c3WgxxwQ30gq8+TRCJe0hcxGv+ls6hi3//yUGwVcU+zvqOLAQcy6nI3oTCI3sOU\nVMXFpoVTaNOAOYEk/go9uA==\n-----END PRIVATE KEY-----\n",
# #     "client_email": "firebase-adminsdk-njswn@borderlessai-filestore.iam.gserviceaccount.com",
# #     "client_id": "101159615520864016018",
# #     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
# #     "token_uri": "https://oauth2.googleapis.com/token",
# #     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
# #     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-njswn%40borderlessai-filestore.iam.gserviceaccount.com",
# #     "storageBucket": "borderlessai-filestore.appspot.com",
# # }

# # cred = credentials.Certificate(firebase_config)
# # firebase_admin.initialize_app(cred, {
# #     'storageBucket': 'borderlessai-filestore.appspot.com',
# #     "projectId": "borderlessai-filestore"
# # })
# # bucket = storage.bucket()
# # db = firestore.client()

# # MAX_FIRESTORE_TEXT_SIZE = 1048487  # Firestore field size limit in bytes

# # # Utility functions for logging processed files
# # def get_processed_files():
# #     """Retrieve a set of already processed files."""
# #     return set(Path("processed_files_log.txt").read_text().splitlines()) if Path("processed_files_log.txt").exists() else set()

# # def log_processed_file(file_name):
# #     """Log processed files to avoid re-processing them."""
# #     with open("processed_files_log.txt", 'a') as f:
# #         f.write(file_name + '\n')

# # # Core processing functions
# # def download_and_process_files(blobs, tags=[]):
# #     """Download each file from Firebase Storage, extract its text, and store it in Firestore."""
# #     print(f"\nProcessing folder with tags: {tags}")
# #     processed_files = get_processed_files()

# #     with tempfile.TemporaryDirectory() as temp_dir:
# #         for blob in blobs:
# #             file_name = Path(blob.name).name
# #             if file_name in processed_files or not file_name:
# #                 print(f"Skipping {file_name} as it has been processed or is empty.")
# #                 continue

# #             file_path = download_file(blob, temp_dir, file_name)
# #             extracted_text = extract_text_based_on_file_type(file_path)
# #             if extracted_text:
# #                 store_text_in_firestore(file_name, extracted_text, tags)
# #                 log_processed_file(file_name)

# #     print(f"Finished processing folder with tags: {tags}")

# # def download_file(blob, temp_dir, file_name):
# #     """Download a file from Firebase Storage."""
# #     file_path = Path(temp_dir) / file_name
# #     blob.download_to_filename(file_path)
# #     print(f"Downloaded {file_name}")
# #     return file_path

# # def extract_text_based_on_file_type(file_path):
# #     """Extract text from various file types, skipping .xls, .xlsx, and .csv files."""
# #     extension = file_path.suffix.lower()
    
# #     # Skip .xls, .xlsx, and .csv files
# #     if extension in [".xls", ".xlsx", ".csv"]:
# #         print(f"Skipping {file_path.name} (file type is excluded from processing).")
# #         return None  # Skip processing
    
# #     if extension == ".pdf":
# #         return extract_text_from_pdf(file_path)
# #     elif extension in [".html", ".htm"]:
# #         return extract_text_from_html(file_path.read_text(encoding='utf-8'))
# #     elif extension in [".yaml", ".yml"]:
# #         return extract_text_from_yaml(file_path)
# #     elif extension == ".docx":
# #         return extract_text_from_docx(file_path)
# #     else:
# #         print(f"Unsupported file type for {file_path.name}")
# #         return None

# # # Text extraction methods for each file type
# # def extract_text_from_pdf(pdf_file):
# #     with pdfplumber.open(pdf_file) as pdf:
# #         return "\n".join(page.extract_text() or '' for page in pdf.pages)

# # def extract_text_from_excel(excel_file):
# #     csv_text = ""
# #     with pd.ExcelFile(excel_file) as xls:
# #         for sheet_name in xls.sheet_names:
# #             csv_text += f"Sheet: {sheet_name}\n" + pd.read_excel(xls, sheet_name).to_csv(index=False) + "\n"
# #     return csv_text

# # def extract_text_from_html(html_content):
# #     return clean_html_content(BeautifulSoup(html_content, "html.parser"))

# # def clean_html_content(soup):
# #     main_content = soup.find("main") or soup.find("article") or soup.find("div", class_="content") or soup.body or soup
# #     for tag in main_content(["header", "footer", "nav", "aside", "script", "style"]):
# #         tag.decompose()
# #     return main_content.get_text(separator="\n").strip()

# # def extract_text_from_csv(csv_file):
# #     with open(csv_file, mode='r', encoding='utf-8') as file:
# #         return "\n".join(', '.join(row) for row in csv.reader(file))

# # def extract_text_from_yaml(yaml_file):
# #     with open(yaml_file, mode='r', encoding='utf-8') as file:
# #         return yaml.dump(yaml.safe_load(file))

# # def extract_text_from_docx(docx_file):
# #     return "\n".join(paragraph.text for paragraph in Document(docx_file).paragraphs)

# # # Firestore storage method
# # def store_text_in_firestore(file_name, extracted_text, tags):
# #     """Stores extracted text in Firestore, truncating and storing full text in Firebase Storage if necessary."""
# #     if len(extracted_text.encode('utf-8')) > MAX_FIRESTORE_TEXT_SIZE:
# #         # Truncate and upload full text to Firebase Storage
# #         full_text_url = upload_full_text_to_storage(file_name, extracted_text)
# #         truncated_text = extracted_text[:MAX_FIRESTORE_TEXT_SIZE // 2] + "\n[Full text available in Firebase Storage]"
# #         data = {"title": file_name, "extracted_text": truncated_text, "full_text_url": full_text_url, "tags": tags, "date_added": datetime.now()}
# #     else:
# #         data = {"title": file_name, "extracted_text": extracted_text, "tags": tags, "date_added": datetime.now()}

# #     db.collection("documents").add(data)
# #     print(f"Document {file_name} stored successfully in Firestore.")

# # def upload_full_text_to_storage(file_name, text):
# #     """Uploads full text to Firebase Storage when Firestore's field size limit is exceeded."""
# #     blob = bucket.blob(f"extracted_texts/{file_name}.txt")
# #     blob.upload_from_string(text)
# #     print(f"Full text for {file_name} uploaded to Firebase Storage.")
# #     return blob.public_url

# # # Define and process blob groups with specific tags
# # blob_groups = {
# #     "admissions": "ADMISSIONS",
# #     "data": "DATA",
# #     "gen_context": "GEN_CONTEXT",
# #     "legal": "LEGAL",
# #     "policy": "POLICY",
# #     "report": "REPORT",
# #     "university": "UNIVERSITY"
# # }

# # for tag, prefix in blob_groups.items():
# #     blobs = bucket.list_blobs(prefix=prefix)
# #     download_and_process_files(blobs, tags=[tag])
