from engine.basic_engine import BasicEngine
from engine.film_engine import FilmEngine
import core.config as config
from core.tokenziner import tokenize,tokens_to_string
from core.printer import typing_print,typing_debug_print
from utils.text_processing import clean_tokens

keys_basic=config.keys_basic
responses_basic=config.responses_basic

keys_film=config.keys_film
list_film=config.list_film
responses_film=config.responses_film

engine_basic=BasicEngine(keys_basic,responses_basic)
engine_film=FilmEngine(keys_film,list_film,responses_film)


running=True
debug_mode=False

engines=[
    engine_basic,
    engine_film
  ]

while running:
  raw=input('You : ')
  tokens=tokenize(raw)
  tokens=clean_tokens(tokens)
  msg=tokens_to_string(tokens)
  
  scores=[]

  for engine in engines:
    score=engine.get_score(msg)
    scores.append((engine,score))
  
  if debug_mode:
    print("")
    typing_debug_print(f"[DEBUG] tokens = {tokens}")
    
  if msg in["debug","debug on","debug off"]:
    if msg=="debug":
      debug_mode=not debug_mode
    elif msg=="debug on":
      debug_mode=True
    elif msg=="debug off":
      debug_mode=False
    status ="ON" if debug_mode else "OFF"
    typing_print(f"[DEBUG MODE {status}]")
    print()
    continue
  
  if debug_mode:
    for engine,score in scores:
      typing_debug_print(f"[DEBUG] {engine.name} score = {score}")
    
  best_engine,best_score=max(scores,key=lambda y:y[1])
  
  if best_score == 0:
    typing_print(f"Bot : Sorry I not understand \n")
    continue
  
  if debug_mode:
    intent=best_engine.get_intent_debug(msg)
    typing_debug_print(f"[DEBUG] engine = {best_engine.name}")
    typing_debug_print(f"[DEBUG] intent = {intent}")
    print("")
    
  result=best_engine.process_input(msg)
  if result["response"]:
    typing_print(f"Bot : {result["response"]} \n")
    
  if result["exit"]:
    running=False
    
  
   