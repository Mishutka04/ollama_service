from src.service.base import BaseService
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import hub
from langchain.chains import RetrievalQA
from langchain.schema import Document


# class ModelService(BaseService):
#     model = Model


class WebAnalysisService(BaseService):
    """
    Сервис для анализа веб-страниц с использованием LangChain и Ollama
    """
    
    def __init__(self):
        # Инициализация LLM
        self.llm = Ollama(
            model="qwen2.5:1.5b",
            verbose=True,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            base_url="http://ollama:11434"  # Используем имя сервиса из docker-compose
        )
        
        # Загрузка промпта для RAG
        self.qa_chain_prompt = hub.pull("rlm/rag-prompt-llama")
    
    async def analyze_webpage(self, url: str):
        """
        Анализирует веб-страницу и возвращает её краткое содержание
        
        Args:
            url: URL веб-страницы для анализа
            
        Returns:
            dict: Результаты анализа
        """
        # Загрузка веб-страницы
        loader = WebBaseLoader(url)
        data = loader.load()
        
        # Разделение на чанки
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
        all_splits = text_splitter.split_documents(data)
        
        # Создание векторного хранилища
        vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=GPT4AllEmbeddings()
        )
        
        # Создание цепочки вопросов и ответов
        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": self.qa_chain_prompt},
        )
        
        # Формирование вопроса и получение ответа
        question = f"summarize what this blog is trying to say? {url}?"
        result = qa_chain({"query": question})
        
        return {
            "summary": result.get("result", ""),
            "chunks_count": len(all_splits),
            "documents_count": len(data)
        }


class TextAnalysisService(BaseService):
    """
    Сервис для анализа и поиска по текстовым документам с использованием RAG
    """
    
    def __init__(self):
        self.llm = Ollama(
            model="qwen2.5:1.5b",
            verbose=True,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            base_url="http://ollama:11434"
        )
        self.vectorstore = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=100
        )
    
    async def add_texts(self, texts: list[str]):
        """
        Добавляет тексты в векторное хранилище
        
        Args:
            texts: Список текстов для добавления
        """
        # Создаем документы из текстов используя правильный класс Document
        documents = [
            Document(
                page_content=text,
                metadata={"source": f"text_{i}"}
            ) for i, text in enumerate(texts)
        ]
        
        # Разбиваем на чанки
        splits = self.text_splitter.split_documents(documents)
        
        # Создаем или обновляем векторное хранилище
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=GPT4AllEmbeddings()
            )
        else:
            self.vectorstore.add_documents(splits)
    
    async def search(self, query: str, k: int = 3):
        """
        Поиск по добавленным текстам
        
        Args:
            query: Поисковый запрос
            k: Количество результатов
            
        Returns:
            dict: Результаты поиска
        """
        if self.vectorstore is None:
            raise ValueError("Нет добавленных текстов для поиска")
            
        # Создаем цепочку RAG
        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": k}),
            chain_type_kwargs={"prompt": hub.pull("rlm/rag-prompt-llama")},
        )
        
        # Получаем ответ
        result = qa_chain({"query": query})
        
        return {
            "answer": result.get("result", ""),
            "sources": result.get("source_documents", [])
        }

