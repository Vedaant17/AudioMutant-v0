from langgraph import Graph, Node, Edge, Agent, Tool, Message
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas import MixSuggestion

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

parser = PydanticOutputParser(pydantic_object=MixSuggestion)

prompt = ChatPromptTemplate.from_template("""
You are a professional mix engineer.

Given the detected issue:
{issue}

Provide:
- Clear explanation
- Exact fix
- Plugin type to use

{format_instructions}
""")

def generate_mix_suggestion(issue: str):
    
    chain = prompt | llm | parser
    return chain.invoke({
        "issue": issue,
        "format_instructions": parser.get_format_instructions()
    })
