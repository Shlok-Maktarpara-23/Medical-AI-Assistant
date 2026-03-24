# Taking user question → running AI chain → returning answer + sources

from logger import logger

def query_chain(chain,user_input:str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        result=chain.invoke(user_input)  # chain → your AI pipeline (from llm.py, i.e. RetrievalQA)
                                            # user_input → question asked by user
        response={
            "response":result["answer"],
            "sources":[doc.metadata.get("source","") for doc in result["source_documents"]]    # Extract sources
        }
        logger.debug(f"Chain response:{response}")
        return response
    except Exception as e:
        logger.exception("Error on query chain")
        raise

# Output (result) looks like:
# {
#     "result": "Diabetes is a condition...",
#     "source_documents": [Document1, Document2]
# }