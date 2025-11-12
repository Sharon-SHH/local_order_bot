EXTRACTION_SYSTEM = """You extract pizza orders to strict JSON.
- Only output JSON. No code fences, no text.
- Schema:
{"items":[{"category":"pizza|side|drink","name":"string","size":"small|medium|large|one_size","qty":int,"toppings":[ "string" ]}],"service":"pickup|delivery|null","address":"string|null","notes":"string|null"}
- If info missing, use null or sensible defaults (qty=1, toppings=[])."""

EXTRACTION_USER_TEMPLATE = """Menu:
{menu_text}

User said:
{utterance}

Return JSON ONLY."""
