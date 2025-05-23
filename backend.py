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

# These debug prints are good to keep for initial data check
st.write("--- Debugging Few Shots ---")
st.write(f"Number of few_shots examples: {len(few_shots)}")
if few_shots:
    st.write("First raw few_shot example:")
    st.json(few_shots[0])
st.write(f"Number of cleaned_fewshots examples: {len(cleaned_fewshots)}")
if cleaned_fewshots:
    st.write("First cleaned_fewshot example:")
    st.json(cleaned_fewshots[0])
    st.write("Keys in first cleaned_fewshot example:", cleaned_fewshots[0].keys())
st.write("--- End Debugging Few Shots ---")


to_vectorize = [" ".join(str(example.values())) for example in cleaned_fewshots]
vectorstore = FAISS.from_texts(texts=to_vectorize, embedding=embeddings, metadatas=cleaned_fewshots)

example_selector = SemanticSimilarityExampleSelector(
    vectorstore = vectorstore,
    k=2,
)

# --- CORRECTED & ENHANCED DEBUG PRINTS FOR SELECTED EXAMPLES ---
st.write("--- Debugging Selected Examples (from example_selector) ---")
try:
    # We need a dummy query to make select_examples work without a full chain run
    # This will simulate how the example_selector picks examples based on an input query.
    selected_examples_for_debug = example_selector.select_examples({"query": "How many books are there?"})
    st.write(f"Number of selected examples: {len(selected_examples_for_debug)}")
    if selected_examples_for_debug:
        st.write("Selected examples from ExampleSelector:")
        for i, ex in enumerate(selected_examples_for_debug):
            st.write(f"Selected example {i}:")
            st.json(ex)
            st.write(f"Keys in selected example {i}:", ex.keys())
    else:
        st.write("No examples were selected by example_selector.")
except Exception as e:
    st.error(f"Error selecting examples for debug: {e}")
st.write("--- End Debugging Selected Examples ---")
# --- END ENHANCED DEBUG PRINTS ---

example_prompt = PromptTemplate(
    input_variables = ['Question','SQLQuery','SQLResult','Answer'],
    template = "\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}\n",
)
    
template="""
You are an expert in translating natural language questions into SQL queries for a MySQL database.

Do not use any markdown formatting like ```sql or ```.
when asked to give all names return all the available names.
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
    ans = llm.invoke(f"{question}: {response} (just give me clean answer like names or numbers. dont give anything else")
    return ans.content
