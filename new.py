import locale
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, ConversationalRetrievalChain

class myAiBot:
    def __init__(self, google_api_key):
        # Set preferred encoding to UTF-8
        locale.getpreferredencoding = lambda: "UTF-8"
        # Google API key for Gemini
        self.google_api_key = google_api_key
        # Instantiate Google Gemini model
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=self.google_api_key, 
                                          convert_system_message_to_human=True, temperature=0.5, 
                                          top_p=0.9, top_k=40)
        # Define a chat prompt template
        self.prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
        {context}
        Question: {input}""")

        
        # Define output parser
        self.output_parser = StrOutputParser()
        self.result = None

    def load_documents_from_website(self, url):
        """Load documents from a website."""
        loader = WebBaseLoader(url)
        return loader.load()

    def initialize_embeddings(self):
        """Initialize HuggingFace embeddings."""
        return HuggingFaceEmbeddings()

    def split_documents_and_create_vector_store(self, docs, embeddings):
        """Split documents and create vector store using FAISS."""
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        return FAISS.from_documents(documents, embeddings)

    def create_document_chain_for_retrieval(self):
        """Create a document chain for retrieval."""
        return create_stuff_documents_chain(self.llm, self.prompt)

    def create_retrieval_chain_with_vector_retriever(self, vector):
        """Create a retrieval chain with vector retriever."""
        retriever = vector.as_retriever()
        document_chain = self.create_document_chain_for_retrieval()
        return create_retrieval_chain(retriever, document_chain)

    def create_conversational_retrieval_chain(self, vector):
        """Create a conversational retrieval chain."""
        retriever = vector.as_retriever()
        retrieval_chain = self.create_retrieval_chain_with_vector_retriever(vector)
        return ConversationalRetrievalChain.from_llm(self.llm, retriever, return_source_documents=True)

    def start_conversation(self,query,url):
        """Start conversation loop."""
        
        docs = self.load_documents_from_website(url)
        embeddings = self.initialize_embeddings()
        vector = self.split_documents_and_create_vector_store(docs, embeddings)
        qa_chain = self.create_conversational_retrieval_chain(vector)
        
        global result

        chat_history = []
        query
        result = qa_chain({'question': query, 'chat_history': chat_history})
        answer = result['answer']
        print('Answer: ' + result['answer'] + '\n')
        chat_history.append((query, result['answer']))
            
        return answer
# Usage:
if __name__ == "__main__":
    GOOGLE_API_KEY = 'AIzaSyC9u1gjP_ZyGDuyYkv5gnkkOyaDX50aR7U'
    ai_bot = myAiBot(GOOGLE_API_KEY)
    ai_bot.start_conversation()
