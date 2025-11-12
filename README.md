### Order chatbot
🧠 Local Order Bot

An AI-powered pizza ordering chatbot built with Python, Typer CLI, Pydantic, and OpenAI (or Ollama) for natural-language understanding.


**Install and start Ollama**
```
brew install ollama
ollama pull llama3.2:3b-instruct
ollama serve
```


### Example

(Documents) ➜  local-order-bot git:(main) ✗ python app.py
👋 Welcome to Local Order Bot! Type 'quit' to exit.

You: I'd like a small cheese pizza with mushrooms
|   qty | item         | toppings   |   $ |
|-------|--------------|------------|-----|
|     1 | small cheese | mushrooms  |   8 |
Pickup or delivery? [pickup]: 
Confirm order (total $8.00)? [y/N]: y
✅ Order placed. Thank you!

👋 Welcome to Local Order Bot! Type 'quit' to exit.

You: I'd like a small fries
|   qty | item        | toppings   |   $ |
|-------|-------------|------------|-----|
|     1 | small fries | -          | 3.5 |
Pickup or delivery? [pickup]: 
Confirm order (total $3.50)? [y/N]: N
You: I'd like a small coke

|   qty | item        | toppings   |   $ |
|-------|-------------|------------|-----|
|     1 | small fries | -          | 3.5 |
|     1 | small coke  | -          | 1   |
Confirm order (total $4.50)? [y/N]: y
✅ Order placed. Thank you!
 