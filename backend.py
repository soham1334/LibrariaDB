import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from urllib.parse import quote_plus
from langchain.prompts import PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts import FewShotPromptTemplate
from few_shots import few_shots


os.environ["GOOGLE_API_KEY"] = st.secrets["database"]["GOOGLE_API_KEY"]
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest", google_api_key=os.environ["GOOGLE_API_KEY"])


db = SQLDatabase.from_uri(
    st.secrets["database"]["uri"]
)
#print(db.table_info)

embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')

from few_shots import few_shots

def clean_metadata(example):
    return {
        k: (
            ", ".join(str(item) for item in v) if isinstance(v, list)
            else str(v) if not isinstance(v, (str, int, float, bool, type(None)))
            else v
        )
        for k, v in example.items()
    }

cleaned_fewshots = [clean_metadata(example) for example in few_shots]



to_vectorize = [" ".join(str(example.values())) for example in cleaned_fewshots]
vectorstore = FAISS.from_texts(texts=to_vectorize, embedding=embeddings, metadatas=cleaned_fewshots)

example_selector = SemanticSimilarityExampleSelector(
    vectorstore = vectorstore,
    k=2,
)



example_prompt = PromptTemplate(
    input_variables = ['Question','SQLQuery','SQLResult','Answer'],
    template = "\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}\n",
)
    
template="""
You are an expert in translating natural language questions into SQL queries for a MySQL database.

Do not use any markdown formatting like ```sql or ```.
*when asked for all names return all the available names and dont use LIMIT.
name of book or bookname is same ,similary for author and others.
when asked for names always return their full names.
Only output the SQL query directly, nothing else.

Use the following user question:
{input}
"""
few_shot_prompt = FewShotPromptTemplate(
    example_selector = example_selector ,
    example_prompt = example_prompt,
    prefix = _mysql_prompt + template,
    suffix = PROMPT_SUFFIX,
    input_variables = ["input","table_info","top_k"],
)

ndb_chain = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    prompt=few_shot_prompt,
    return_direct=True,
    verbose=True
)


def Queries (question):
    response = ndb_chain.invoke({"query":question})
    prompt = """Just give clean answers like names or numbers.
            If more than one column is present, include column names too.
            Do not return values in quotation marks.
            If result/response is empty, answer appropriately according to the question (e.g., NO / Invalid / Not Applicable / None / etc)."""
    ans = llm.invoke(f"{question}: {response1} ({prompt})")
    return ans.content
