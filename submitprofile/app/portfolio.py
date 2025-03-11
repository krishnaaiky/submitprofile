import pandas as pd
import chromadb
import uuid
import os

class Portfolio:
    def __init__(self, file_path="./app/resource/my_portfolio.csv"):
        #print("******** Start of Portfolio init ********")
        self.file_path = file_path
        #print(file_path)
        #print(os.getcwd())
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")
        #print("******** End of Portfolio init ********")
    def load_portfolio(self):
        #print("******** Start of load portfolio Streamlit ********")
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links":row["Links"]},
                                    ids=[str(uuid.uuid4())])
        #print("******** End of load portfolio Streamlit ********")
    def query_links(self,skills):
        #print("******** Start of query links return ********")
        return self.collection.query(query_texts=skills,n_results=2).get('metadatas',[])