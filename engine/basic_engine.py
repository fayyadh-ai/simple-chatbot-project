from core.config import ENCODING
import json
import random

class BasicEngine:
  name="BasicEngine"
  def __init__(self,keys_path,responses_path):
    self.keys=self.load_json(keys_path)
    self.responses=self.load_json(responses_path)
    
  def load_json(self,file_path):
    with file_path.open("r",encoding=ENCODING) as load:
      return json.load(load)
    
  def get_responses(self,msg):
    for category,keywords in self.keys.items():
      if any(k in msg for k in keywords):
        response=random.choice(self.responses[category])
        return category,response
    return None,None
    
  def get_score(self,tokens):
    score = 0
    for category,keywords in self.keys.items():
      for k in keywords:
        if k in tokens:
          score += 3
          
    return score
    
  def process_input(self,msg):
    category,response=self.get_responses(msg)
    return {
      "response":response,
      "exit":category=="farewell"
    }
      
  def get_intent_debug(self,msg):
    category,response=self.get_responses(msg)
    if category:
      return f"{category} | response_found"
    return "Unknown"