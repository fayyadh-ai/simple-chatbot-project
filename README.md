# Simple Ruled-based chatbot(Python OOP)
A modular chatbot built using OOP principles and JSON keywords matching

## Features
- Keyword-based responses matching
- Modular engine architecture
- JSON-driven data system
- Exit detection by category(farewell)

## Project Structure
- Core/ -> Configuration
- Data/ -> JSON data sets
- Engine/ -> Chatbot engine logic
- main.py -> entry point

## How It Works
1. User input is received in main.py
2. Input is passed to Engine.get_response()
3. Engine matches keywords from JSON data
4. If matched random response is returned
5. If category is "farewell",the program exits

## How To Run
python main.py

## Roadmap
- Add film recomendation mode
- Implement state handling
- improve keyword matching precision
