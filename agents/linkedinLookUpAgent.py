import os
import sys

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from tools.tools import get_profile_linkedin

load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")


def lookup(name: str) -> str:
    # llm = ChatOllama(model="llama3")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

    template = (
        "Given the full name {name_of_person}, return only the URL to "
        "their LinkedIn profile page. Respond with just the URL."
    )
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tool_for_agent = [
        Tool(
            name="Search LinkedIn profile",
            func=get_profile_linkedin,
            description="Finds a candidate's LinkedIn profile URL.",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tool_for_agent, prompt=react_prompt)

    agent_executor = AgentExecutor(
        agent=agent, tools=tool_for_agent, verbose=True, handle_parsing_errors=True
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]

    return linkedin_profile_url


if __name__ == "__main__":
    pass
