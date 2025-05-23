
#from langchain.llms import GooglePalm
import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from urllib.parse import quote_plus
from langchain.prompts import PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_community.vectorstores import Chroma
from langchain.vectorstores import FAISS
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX ,_mysql_prompt
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate


os.environ["GOOGLE_API_KEY"] = "AIzaSyAPWigmGbmoJfwxizaPfn_LA8nAHOM8oVk"

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
vectorstore = FAISS.from_texts(texts=to_vectorize, embedding=embeddings)
#vectorstore = Chroma.from_texts(to_vectorize ,embedding = embeddings,metadatas =cleaned_fewshots)
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
when asked to give all names return all the available names.
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
 ans = llm.invoke(f"{question}: {response} (just give me clean answer like names or numbers. dont give anything else")
 return ans.content

