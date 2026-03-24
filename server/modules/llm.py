# # Creating a Question-Answer system (RAG pipeline) using an LLM + your medical documents

# from langchain_core.prompts import PromptTemplate
# from langchain.chains import RetrievalQA
# from langchain_groq import ChatGroq
# import os
# from dotenv import load_dotenv

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # Takes a retriever (your medical knowledge) and returns a working AI chain
# def get_llm_chain(retriever):
#     llm=ChatGroq(
#         groq_api_key=GROQ_API_KEY,
#         model_name='llama3-70b-8192'
#     )

#     prompt = PromptTemplate(
#         input_variables=["context", "question"],    # context → medical data from your documents, question → user query
#         template="""
#         You are **MediBot**, an AI-powered assistant trained to help users understand medical documents and health-related questions.

#         Your job is to provide clear, accurate, and helpful responses based **only on the provided context**.

#         ---

#         🔍 **Context**:
#         {context}

#         🙋‍♂️ **User Question**:
#         {question}

#         ---

#         💬 **Answer**:
#         - Respond in a calm, factual, and respectful tone.
#         - Use simple explanations when needed.
#         - If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents."
#         - Do NOT make up facts.
#         - Do NOT give medical advice or diagnoses.
#         """
#     )

#     return RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff", # All retrieved documents are “stuffed” into one prompt
#         retriever=retriever, # This comes from your vector database (FAISS, Chroma, etc.) and Sends it as context
#         chain_type_kwargs={"prompt": prompt},   # Sends it as context
#         return_source_documents=True    # This return answer
#     )

# modules/llm.py

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableMap
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_chain(retriever):
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name='llama-3.3-70b-versatile'
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
            You are **MediBot**, an AI-powered assistant trained to help users understand medical documents and health-related questions.

            Your job is to provide clear, accurate, and detailed responses based **only on the provided context**.

            ---

            🔍 **Context**:
            {context}

            🙋‍♂️ **User Question**:
            {question}

            ---

            💬 **Answer**:
            - Give a **thorough and complete** answer based on the context.
            - Use bullet points or numbered lists when explaining multiple items (e.g. types, symptoms, causes).
            - Include all relevant details found in the context — do NOT summarize too briefly.
            - Use simple explanations when needed.
            - If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents."
            - Do NOT make up facts.
            - Do NOT give medical advice or diagnoses.
        """
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        RunnableMap({
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
            "source_documents": retriever
        })
        | {
            "answer": (
                (lambda x: {"context": x["context"], "question": x["question"]})
                | prompt
                | llm
                | StrOutputParser()
            ),
            "source_documents": lambda x: x["source_documents"]
        }
    )

    return chain