# Simple Rule-Based Chatbot (Python, OOP)

A modular chatbot built with object-oriented design and JSON-based keyword matching.
This project focuses on building a structured decision system rather than relying on complex AI models.

## Features

- Keyword-based intent detection using JSON rules
- Modular engine architecture (plug-and-play engines)
- Lightweight state handling (memory of previous inputs)
- Category-based exit detection (e.g. farewell intent)
- Extendable system for multiple domains (current: film,upcoming: life)

## Project Structure

core/     -> configuration and shared utilities  
data/     -> JSON datasets (keywords, responses)  
engine/   -> chatbot engines (film,upcoming: life)  
main.py   -> application entry point

## How It Works

1. User input is received in "main.py"
2. Input is passed to the selected engine
3. Engine parses input using keyword matching + scoring
4. System determines intent, genre, modifier, or context
5. Response is generated based on decision flow
6. State is updated for future interactions

## Example

User: give me top 5 action movies  
Bot: returns top 5 action films  

User: top 10  
Bot: uses previous genre (action) + new modifier  


## How To Run

python main.py


## Roadmap

- Add LifeEngine (habit tracking,scheduling)
- Improve intent prioritization logic
- Enhance keyword matching with scoring refinement
- Refactor decision system for better scalability

## Notes

This project is designed as a learning step toward building agent-based systems,
focusing on state management, decision logic, and modular architecture.