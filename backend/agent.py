from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

def run_chain(transcript_text: str, question: str) -> str:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript_text])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5}, search_type="mmr", search_score_threshold=0.7)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=""" You are a helpful assistant.
You will be given a context and a question. Use the context to answer the question in detail.
If the answer is not interpretable from context, say 'I don't know'.
context: {context}
question: {question}"""
    )

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    parser = StrOutputParser()

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(lambda docs: "\n\n".join([doc.page_content for doc in docs])),
        "question": RunnablePassthrough()
    })

    main_chain = parallel_chain | prompt | llm | parser
    return main_chain.invoke(question)
