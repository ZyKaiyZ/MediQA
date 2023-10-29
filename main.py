from fastapi import FastAPI, HTTPException
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

class QuestionInput(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(question_input: QuestionInput):
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

    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())

    result = qa_chain({"query": question_input.question})
    
    return {"answer": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
