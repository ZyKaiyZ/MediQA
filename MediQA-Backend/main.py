from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from g4f import Provider, models
from langchain.llms.base import LLM
from langchain_g4f import G4FLLM
from langchain.document_loaders import TextLoader
from langchain.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

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
    question: str

class QuestionOutput(BaseModel):
    answer: str

# Initialize llm and vectorstore at the module level
llm = None
vectorstore = None

async def initialize_llm_and_vectorstore() -> None:
    global llm, vectorstore

    try:
        llm = G4FLLM(
            model=models.default,
            provider=Provider.Vercel,
        )

        # load the files
        loader = TextLoader("./output.txt")
        data = loader.load()

        # split text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
        all_splits = text_splitter.split_documents(data)

        # embeddings
        embedding = GPT4AllEmbeddings()

        vectorstore = Chroma.from_documents(documents=all_splits, embedding=embedding)

    except Exception as e:
        # Handle exceptions and raise an HTTPException with an appropriate status code
        raise HTTPException(status_code=500, detail="Error initializing LLM and Vectorstore")

@app.on_event("startup")
async def startup_event():
    await initialize_llm_and_vectorstore()

@app.post("/api/ask", response_model=QuestionOutput)
async def ask_question(question_input: QuestionInput):
    if llm is None or vectorstore is None:
        raise HTTPException(status_code=503, detail="LLM and Vectorstore not initialized")

    try:
        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())

        result = qa_chain({"query": question_input.question})
        
        return {"answer": result}

    except Exception as e:
        # Handle exceptions and raise an HTTPException with an appropriate status code
        raise HTTPException(status_code=500, detail="Error processing the question")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
