import os
import envs

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

os.environ["OPENAI_API_KEY"] = envs.APIKEY

def Basic(prompt, temp):
    # load the document and convert to vector embeddings
    loader = DirectoryLoader("data/", use_multithreading=True)
    index = VectorstoreIndexCreator().from_loaders([loader])

    return index.query(prompt, llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=temp))


def TechSTD(section_no, temp):
    loader = DirectoryLoader("data/", use_multithreading=True)
    index = VectorstoreIndexCreator().from_loaders([loader])
    
    prompt = f'Retrieve the exact content of section "{section_no}" and show it to me.'
    content = index.query(prompt, llm=ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=temp))

    prompt2 = f'''Data: {content}
     
Based on this data, Identify any language, wording or symantics issues and generate some recommendations as this is data from a technical standard/requirements file which needs precise wording so people don't get confused. Your output should include:

The Recommendation number (if there are more than 1 recommendations).

The section number.

The current language from that section.

The identified issue with the current language.

Suggested language or modification.

The goal is to provide clear, actionable wording and symantics to enhance the technical requirements within the document. Please generate a recommendation following this format. if you cant identify any issues return "No changed are needed for this section."'''

    return index.query(prompt2, llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=temp))