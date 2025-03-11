import streamlit as st
#from jsonschema.benchmarks.const_vs_enum import value
from langchain_community.document_loaders import WebBaseLoader
#from streamlit import markdown

from chains import Chain
from portfolio import Portfolio
from utils import clean_text
def create_streamlit_app(llm, portfolio, clean_text):
    #print("******** Start of Create Streamlit ********")
    st.title("Cold Email Generator")
    url_input = st.text_input("Enter a URL:",value="https://www.syneoshealth.com/careers/jobs/15549861-sr-clinical-research-associate-sr-cra-sponsor-dedicated-rare-disease-home-based-in-western-us")
    submit_button = st.button("Submit")
    #print("******** After Submit ********")
    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
           # print(data)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                #print(job)
                skills = job.get('skills',[])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An error occurred : {e}")
            ##st.code("Hello Hiring Manager, I am Kishankanth Yarramshetti", language='markdown')
    #print("******** End of Create Streamlit ********")
if __name__ == "__main__":
    #print("******** Start of MAIN Program ********")
    chain = Chain()
    #print("******** After Chain class-Main ********")
    portfolio = Portfolio()
    #print("******** After portfolio class ********")
    st.set_page_config(layout="wide", page_title="Cold Email Generator",page_icon="M")
    #print("******** After page config ********")
    create_streamlit_app(chain,portfolio,clean_text)
    #print("******** End of Main Create Streamlit ********")