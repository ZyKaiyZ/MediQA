import os
import uvicorn
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

app = FastAPI()

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionInput(BaseModel):
    """Input for the question"""
    question: str

class QuestionOutput(BaseModel):
    """Output for the question"""
    query: str
    result: str

LLM = None
VECTORSTORE = None

async def initialize_llm_and_vectorstore() -> None:
    """Initialize the LLM and Vectorstore"""
    global LLM, VECTORSTORE

    try:
        load_dotenv()
        openai_model="gpt-3.5-turbo"
        openai_api_key = os.getenv("OPENAI_API_KEY")

        # load the files
        loader = TextLoader("./data.txt")
        data = loader.load()

        # split text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
        all_splits = text_splitter.split_documents(data)

        # embeddings
        embedding_model = "shibing624/text2vec-base-chinese"
        embedding = HuggingFaceEmbeddings(model_name=embedding_model)

        LLM = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model=openai_model)
        VECTORSTORE = Chroma.from_documents(documents=all_splits, embedding=embedding)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error initializing LLM and Vectorstore") from e

@app.on_event("startup")
async def startup_event() -> None:
    """Initialize the LLM and Vectorstore on startup"""
    await initialize_llm_and_vectorstore()

@app.post("/api/ask", response_model=QuestionOutput)
async def ask_question(question_input: QuestionInput) -> QuestionOutput:
    """Ask a question and get an answer"""
    if LLM is None or VECTORSTORE is None:
        raise HTTPException(status_code=503, detail="LLM and Vectorstore not initialized")

    try:
        qa_chain = RetrievalQA.from_chain_type(llm=LLM, chain_type="stuff", retriever=VECTORSTORE.as_retriever())
        
        result = qa_chain({"query": question_input.question})

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing the question") from e

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
