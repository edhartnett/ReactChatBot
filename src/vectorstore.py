from chromadb import Client, PersistentClient
from typing import List
import json

#MODEL_NAME = "NovaSearch/stella_en_1.5B_v5"
DB_PATH = "/home/ed/chroma_db"
FAQ_FILE_PATH = "./data/faq.json"
ALIENS_FILE_PATH = "./data/alien_races.json"

class UfoSiteVectorStore:
    def __init__(self):
        print("creating db...")
        self.db = PersistentClient(path=DB_PATH)
        #self.db = Client()
        #custom_embedding_function = CustomEmbeddingClass(MODEL_NAME)
        print("creating collection for FAQ...")
        self.faq_collection = self.db.get_or_create_collection(name="faq")
        if self.faq_collection.count() == 0:
            print("FAQ collection is empty, loading...")
            self._load_faq_collection(FAQ_FILE_PATH)
            print("collection loaded")
        else:
            print("FAQ collection already exists, skipping loading.")

        print("creating collection for aliens...")
        #self.aliens_collection = self.db.get_or_create_collection(name="aliens", embedding_function=custom_embedding_function)
        self.aliens_collection = self.db.get_or_create_collection(name="aliens")
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
            print(faqs)

        print("adding faqs to collection..." + str(len(faqs)))
        self.faq_collection.add(
            documents=[faq["question"] + faq["answer"] for faq in faqs],
            ids=[str(i) for i in range(len(faqs))]
        )
        print("faqs have been added to collection.")

    def _load_aliens_collection(self, aliens_file_path: str):
        print("reading aliens file...")
        with open(aliens_file_path, "r") as f:
            aliens = json.load(f) 
            print(aliens)

        print("adding aliens to collection..." + str(len(aliens)))
        self.aliens_collection.add(
            documents=[
                f"{alien['name']} home_system: {alien['home_system']} description: {alien['description']} trade goods: {alien['trade_goods']} art forms: {alien['art_forms']} details: {alien['details']}"
                for alien in aliens
            ],
            ids=[str(i) for i in range(len(aliens))]
        )
        print("aliens have been added to collection.")

    def query_faqs(self, query: str):
        print("querying faqs..." + query)
        print(self.faq_collection.count())
        results = self.faq_collection.query(
            query_texts=[query],
            n_results=1
        )
        print(results)
        return results

    def query_aliens(self, query: str):
        return self.aliens_collection.query(
            query_texts=[query],
            n_results=1
        )
    
    def reset(self):
        print("resetting...")
        self.db.reset()

# vector_store = UfoSiteVectorStore()
# ret_col = vector_store.db.get_collection("faq")
# results = vector_store.query_faqs("What is the Tectonic Strain Theory (TST)?")
# print(results)
# results = vector_store.query_faqs("What is a Qwqa?")
# print(results)
# results = vector_store.query_faqs("What is a aaaa?")
# print(results)