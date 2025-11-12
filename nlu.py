import requests, json
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

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

def ollama_chat(messages, model="llama3:8b"):
    r = requests.post("http://localhost:11434/api/chat",
                      json={"model": model, "messages": messages, "stream": False})
    r.raise_for_status()
    return r.json()["message"]["content"]

def extract_order(utterance: str, menu_text: str) -> OrderDraft:
    from prompts import EXTRACTION_SYSTEM, EXTRACTION_USER_TEMPLATE
    user = EXTRACTION_USER_TEMPLATE.format(menu_text=menu_text, utterance=utterance)
    out = ollama_chat([
        {"role":"system","content":EXTRACTION_SYSTEM},
        {"role":"user","content":user}
    ])
    # model may add whitespace; ensure pure JSON
    data = json.loads(out.strip())
    return OrderDraft(**data)
