import json, os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel, Field

load_dotenv()
class Item(BaseModel):
    category: str
    name: str
    size: str
    qty: int = 1
    toppings: List[str] = []

class OrderDraft(BaseModel):
    items: List[Item] = Field(default_factory=list)
    service: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

def openAI_chat(messages, model="gpt-3.5-turbo"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
        return
    elif not api_key.startswith("sk-proj-"):
        print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
        return
    elif api_key.strip() != api_key:
        print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
        return 
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


def extract_order(utterance: str, menu_text: str) -> OrderDraft:
    from prompts import EXTRACTION_SYSTEM, EXTRACTION_USER_TEMPLATE
    user = EXTRACTION_USER_TEMPLATE.format(menu_text=menu_text, utterance=utterance)
    out = openAI_chat([
        {"role":"system","content":EXTRACTION_SYSTEM},
        {"role":"user","content":user}
    ])
    data = json.loads(out.strip())
    return OrderDraft(**data)