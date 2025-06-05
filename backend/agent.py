from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

def get_retrieval_params(question: str) -> dict:
    """Dynamically tune parameters based on the query's type."""
    q_len = len(question.split())
    if "explain" in question.lower() or q_len > 12:
        return {
            "k": 8,
            "fetch_k": 25,
            "lambda_mult": 0.6
        }
    elif "list" in question.lower() or "examples" in question.lower():
        return {
            "k": 10,
            "fetch_k": 30,
            "lambda_mult": 0.7
        }
    else:
        return {
            "k": 4,
            "fetch_k": 10,
            "lambda_mult": 0.5
        }


def run_chain(transcript_text: str, question: str) -> str:
    # 1. Split transcript
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=200)
    chunks = splitter.create_documents([transcript_text])

    # 2. Create embeddings + vector store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # 3. Setup retriever with dynamic settings
    retrieval_params = get_retrieval_params(question)
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs=retrieval_params
    )

    # 4. Prompt Template
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are a knowledgeable and helpful assistant.

Use the CONTEXT from a YouTube transcript to answer the QUESTION thoroughly.

- Stick strictly to the context provided. Do not mention the word "transcript".
- If the answer isn't in the context, reply with "I don't know based on the given transcript."
- Return in clean, markdown-like format with **bold**, line breaks, and bullet points when helpful.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""
    )

    # 5. Run LLM chain
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    parser = StrOutputParser()

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(lambda docs: "\n\n".join([doc.page_content for doc in docs])),
        "question": RunnablePassthrough()
    })

    main_chain = parallel_chain | prompt | llm | parser

    return main_chain.invoke(question)
