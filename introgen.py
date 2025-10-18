import os
import argparse
import json
import re
"""IntroGen orchestration: fetch LinkedIn info and produce recruiter-friendly
summaries and ice-breakers using an LLM.

Public API:
- fetch_person_data(name: str) -> dict

The returned dict has keys: summary_and_facts, interests, ice_breakers, profile_pic_url.
"""

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from thirdparties.linkedin import get_linkedin_data
from agents.linkedinLookUpAgent import lookup as linkedin_lookup_agent

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")


def _extract_json_from_text(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def fetch_person_data(name: str):
    """
    Returns a dict with keys:
      - summary_and_facts: {"summary": str, "facts": [str, str]}
      - interests: [str, ...]
      - ice_breakers: [str, ...]
      - profile_pic_url: str (may be empty)
    """
    # Small trace logs for local development (avoid printing secrets)

    linkedin_url = linkedin_lookup_agent(name=name)
    # print(f"linkedin url is {linkedin_url}")
    linkedin_info = get_linkedin_data(linkedin_url=linkedin_url, mock=False)

    json_prompt = """
        Given the following LinkedIn information about a person:

        {information}

        Produce a single valid JSON object (and only the JSON) with the following shape:

        {
        "summary_and_facts": {
            "summary": "<one-sentence short summary>",
            "facts": ["<interesting fact 1>", "<interesting fact 2>"]
        },
        "interests": ["<interest1>", "<interest2>", "..."],
        "ice_breakers": ["<ice breaker question 1>", "<ice breaker question 2>", "<ice breaker question 3>"],
        "profile_pic_url": "<absolute url to profile picture or empty string>"
        }

        Do not include any extra commentary or text. Ensure the JSON is valid.
    """

    prompt = PromptTemplate(input_variables=["information"], template=json_prompt)

    # prefer Google if key available, otherwise try Ollama (local)
    try:
        if api_key:
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
        else:
            llm = ChatOllama(model="llama3")
    except Exception:
        llm = ChatOllama(model="llama3")

    chain = prompt | llm | StrOutputParser()

    raw = chain.invoke({"information": linkedin_info})

    # try finalizing valid JSON
    try:
        data = json.loads(raw)
    except Exception:
        # attempt to extract a JSON object from surrounding text
        extracted = _extract_json_from_text(raw)
        try:
            data = json.loads(extracted)
        except Exception:
            # fallback: return a minimal safe structure with raw text included
            data = {
                "summary_and_facts": {"summary": "", "facts": []},
                "interests": [],
                "ice_breakers": [],
                "profile_pic_url": "",
                "raw": raw,
            }

    return data


if __name__ == "__main__":
    pass

