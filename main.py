from engine.basic_engine import BasicEngine
import core.config as config

keys_basic=config.keys_basic
responses_basic=config.responses_basic

engine_basic=BasicEngine(keys_basic,responses_basic)

running=True

while running:
  msg=input('You: ').lower().strip()
  
  category,response=engine_basic.get_responses(msg)
  
  print(f"Bot: {response}\n")
  
  if category=="farewell":
    running=False
  