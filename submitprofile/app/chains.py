import os

#from langchain.chains.flare.prompts import PROMPT_TEMPLATE
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()
#os.getenv("GROQ_API_KEY")
#print("******** After Load environment ********")
class Chain:
  def __init__(self):
   # print("******** Init Chain Class ********")
    self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")
    #print("******** After Chain class ********")
  def extract_jobs(self, cleaned_text):
    #print("******** Start of extract jobs ********")
    prompt_extract = PromptTemplate.from_template(
      """
      ### SCRAPED TEXT FROM WEBSITE:
      {page_data}
      ### INSTRUCTION:
      The scraped text is from the career's page of a website.
      Your job is to extract the job postings and return them in JSON format containing the following keys: `role`,`experience`,`skills` and `description`.
      Only return the valid JSON.
      ### VALID JSON (NO PREAMBLE):
      """
    )
    chain_extract = prompt_extract | self.llm
    res = chain_extract.invoke(input={"page_data": cleaned_text})
    try:
      json_parser = JsonOutputParser()
      res = json_parser.parse(res.content)
    except OutputParserException:
      raise OutputParserException("context too big. Unable to parse jobs.")
    #print("******** Before return extract job ********")
    return res if isinstance(res, list) else [res]
  def write_mail(self, job, links):
    #print("******** Start of write mail ********")
    prompt_email = PromptTemplate.from_template(
      """
      ### JOB DESCRIPTION:
      {job_description}

      ### INSTRUCTION:
      You are Kishankanth Yarramshetti, a Senior Data scientist working in Dallas, TX area. 
      Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
      process optimization, cost reduction, and heightened overall efficiency. 
      Your job is to write a cold email to the client regarding the job mentioned above describing the capability of me 
      in fulfilling their needs.
      Also add the most relevant ones from the following links to showcase my portfolio: {link_list}
      Remember you are Kishankanth Yarramshetti, a Senior Data scientist.
      Do not provide a preamble.
      ### EMAIL(NO PREAMBLE)
      """
    )
    chain_email = prompt_email | self.llm
    res = chain_email.invoke({"job_description":str(job),"link_list":links})
    #print("******** before return of write email ********")
    return res.content

if __name__ == "__main__":
  #print("******** Start of Chain init ********")
  print(os.getenv("GROQ_API_KEY"))
  #print("******** End of Chain init ********")