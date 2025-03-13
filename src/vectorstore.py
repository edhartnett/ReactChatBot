from chromadb import PersistentClient, EmbeddingFunction, Embeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import List
import json

MODEL_NAME = "NovaSearch/stella_en_1.5B_v5"
DB_PATH = "/home/ed/chroma_db"
FAQ_FILE_PATH = "./faq.json"
ALIENS_FILE_PATH = "./aliens.json"

class QuestionAnswerPairs:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

class AliensInfo:
    def __init__(self, name: str, home_system: str, description: str, details: str):
        self.name = name
        self.home_system = home_system
        self.description = description
        self.details = details

class CustomEmbeddingClass(EmbeddingFunction):
    def __init__(self, model_name: str):
        self.embedding_model = HuggingFaceEmbedding(model_name=MODEL_NAME)

    def __call__(self, input_texts: list[str]) -> Embeddings:
        return [self.embedding_model.get_text_embedding(text) for text in input_texts]

class UfoSiteVectorStore:
    def __init__(self):
        print("creating db...")
        db = PersistentClient(path=DB_PATH)
        custom_embedding_function = CustomEmbeddingClass(MODEL_NAME)
        print("creating collection for FAQ...")
        self.faq_collection = db.get_or_create_collection(name="faq", embedding_function=custom_embedding_function)
        if self.faq_collection.count() == 0:
            print("FAQ collection is empty, loading...")
            self._load_faq_collection(FAQ_FILE_PATH)
            print("collection loaded")
        else:
            print("FAQ collection already exists, skipping loading.")

        print("creating collection for aliens...")
        self.aliens_collection = db.get_or_create_collection(name="aliens", embedding_function=custom_embedding_function)
        if self.aliens_collection.count() == 0:
            print("Aliens collection is empty, loading...")
            self._load_aliens_collection(ALIENS_FILE_PATH)
            print("collection loaded")
        else:
            print("Aliens collection already exists, skipping loading.")

    def _load_faq_collection(self, faq_file_path: str):
        print("reading faq file...")
        with open(faq_file_path, "r") as f:
            faqs = json.load(f) 

        print("adding faqs to collection..." + str(len(faqs)))
        self.faq_collection.add(
            documents=[faq["question"] for faq in faqs] + [faq["answer"] for faq in faqs],
            ids=[str(i) for i in range(2 * len(faqs))],
            metadatas=faqs + faqs
        )
        print("faqs have been added to collection.")

    def _load_aliens_collection(self, aliens_file_path: str):
        print("reading aliens file...")
        with open(aliens_file_path, "r") as f:
            aliens = json.load(f) 

        print("adding aliens to collection..." + str(len(aliens)))
        self.aliens_collection.add(
            documents=[alien["details"] for alien in aliens],
            ids=[str(i) for i in range(len(aliens))],
            metadatas=aliens
        )
        print("aliens have been added to collection.")

    def query_faqs(self, query: str):
        return self.faq_collection.query(
            query_texts=[query],
            n_results=5
        )

    def query_aliens(self, query: str):
        return self.aliens_collection.query(
            query_texts=[query],
            n_results=5
        )

    def query_aliens(self, query: str):
        return self.aliens_collection.query(
            query_texts=[query],
            n_results=5
        )
        