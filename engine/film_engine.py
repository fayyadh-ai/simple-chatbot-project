import json
from core.config import ENCODING
import random

class FilmEngine:
  name="FilmEngine"
  
  def __init__(self,keys_film,list_film,response_film):
    self.keys=self.load_film(keys_film)
    self.list=self.load_film(list_film)
    self.response=self.load_film(response_film)
    self.state={
      "last_genre":[],
      "last_modifier":None,
      "last_intent":None
    }
    
    
  #====================================================/
  # ENTRY POINT
  #====================================================/
  
  def process_input(self,msg):
    
    parse=self.parse_message(msg)
    
    genre=parse["genre"]
    modifier=parse["modifier"] 
    intent=parse["intent"]
    context=parse["context"]
    
    if not genre:
      genre=self.state.get("last_genre",[])
      
    if not modifier:
      if intent:
        modifier=None
      else:
        modifier=self.state.get("last_modifier")
      
    if genre:
      if isinstance(genre,str):
        genre = [genre]
      self.state["last_genre"]=genre
      
    if modifier:
      if intent:
        intent=None
      self.state["last_modifier"]=modifier
      
    mode = self.decide_mode(genre,modifier,intent,context)
      
    match mode:
      case "single_genre":
        result =self.formatter_film(genre[0],modifier)
      case "multi_genre":
        result =self.formatter_multi_genre(genre,modifier)
      case "recommend_by_genre":
        result =self.recommend_by_genre(genre)
      case "recommend_all":
        result =self.recommend_all()
      case "fallback":
        genre_result=self.fallback_genre(msg)
        
        if genre_result:
          result = genre_result
        
        else :
          search_result=self.fallback_search(msg)
          result = search_result
      
    return {
      "response":result,
      "exit":False
    }
    
    
  #====================================================/
  # PARSING AND DETECTION
  #====================================================/
  
  def parse_message(self,msg):
    parse={
      "genre":[],
      "modifier":None,
      "intent":None,
      "context":None
    }
    genre_score={}
    
    for name,data in self.keys["genre"].items():
      score = 0
      keywords=data["keywords"]
      weight=data["score"]
      for k in keywords:
        if k in msg:
          score += weight
      if score >0:
        genre_score[name]=score
        
    if genre_score:
      sorted_genres =sorted(genre_score.items(),key = lambda x:x[1],reverse=True)
      parse["genre"]=[g[0] for g in sorted_genres[:2]]
            
    for category in ["modifier","intent","context"]:
      parse[category]=self.detect_category(msg,category)
            
    return parse
    
  def detect_category(self,msg,category):
    for name,data in self.keys[category].items():
      keywords=data["keywords"]
      for k in keywords:
        if k in msg:
          return name
    return None
    
  def decide_mode(self,genre,modifier,intent,context):
    
    if intent and context:
      if genre:
        return "recommend_by_genre"
      return "recommend_all"
        
    if genre:
      if len(genre)==1:
        return "single_genre"
      if len(genre)>1:
        return "multi_genre"
        
    else:
      return "fallback"
  
  
  #====================================================/
  # CORE
  #====================================================/
  
  def recommend_all(self):
    first_text,last_text=self.get_recommend_response()
    result=[]
    if first_text:
      result.append(first_text)
    
    for genre in self.list:
      result.append("")
      result.append(f"{genre.title()} Movies:")
      result.append("")
      films_list=self.list[genre][:3]
      
      for i,film in enumerate(films_list,1):
        result.append(f"{i}.{film['title']} ({film['year']}) | rating:{film['rating']}")
        
    if last_text:
      result.append("")
      result.append(last_text)
      
    return "\n".join(result)
    
  def recommend_by_genre(self,genre):

    if isinstance(genre,list):
      genre=genre[0]
      
    first_text,last_text=self.get_recommend_response(genre)
    
    result=[]
    if first_text:
      result.append(first_text)
      result.append("")
      
    recommend_film_genre=self.list[genre][:5]
    for i,film in enumerate(recommend_film_genre,1):
      result.append(f"{i}.{film['title']} ({film['year']}) | rating:{film['rating']}")
      
    if last_text:
      result.append("")
      result.append(last_text)
      
    return "\n".join(result)
  
  
  #====================================================/
  # FORMATTER
  #====================================================/
  
  def formatter_film(self,genre,modifier=None):
      
    first_text=self.get_first_text(genre,modifier)
    last_text=self.get_last_text(genre,modifier)
    list_film=self.get_film_list(genre,modifier)
    
    result=[]
    
    if first_text:
      result.append(first_text)
      result.append("")
      
    result.append(self.formatter_film_list(list_film))
      
    if last_text:
      result.append("")
      result.append(last_text)
      
    return "\n".join(result)
    
  def formatter_multi_genre(self,genre,modifier=None):
    first_text=self.get_first_text(None,modifier)
    genre_text = self.format_genre_list(genre)
    first_text = first_text.replace("{genre}", genre_text)
      
    last_text=self.get_last_text(None,modifier)
    
    result = []
    
    if first_text:
      result.append(first_text)
      result.append("")
      
    for g in genre:
      genre_display=g.replace("_"," ").title()
      
      result.append(f"{genre_display} Movies :")
        
      list_film=self.get_film_list(g,modifier)
        
      result.append("")
      result.append(self.formatter_film_list(list_film))
      result.append("")
      
    if last_text:
      result.append("")
      result.append(last_text)
      
    return "\n".join(result)
    
  def formatter_film_list(self,list_film):
    result = []
    
    for i, film in enumerate(list_film, 1):

      if isinstance(film, tuple):
        title,desc=film
        result.append( f"{i}. {title} ({desc['year']}) rating:{desc['rating']}")
      else:
          result.append (f"{i}. {film['title']} ({film['year']}) |  rating:{film['rating']}")
          
    return "\n".join(result)
    
  def format_genre_list(self, genres):
      
    genres=[g.replace("_"," ") for g in genres]
    
    if len(genres) == 1:
      return genres[0]
    elif len(genres) == 2:
      return " and ".join(genres)
    else:
      return ", ".join(genres[:-1]) + ", and " + genres[-1]
  
  
  #====================================================/
  # DATA ACCESS
  #====================================================/
  
  def get_first_text(self,genre=None,modifier=None):
    if modifier:
      data=self.response["modifier"][modifier]
    else:
      data=self.response["default"]
      
    first_text=random.choice(data["first"])
    
    if genre:
      genre_display = genre.replace("_", " ").title()
      first_text=first_text.format(genre=genre_display)
      
    return first_text
    
  def get_last_text(self,genre=None,modifier=None):
    if modifier:
      data=self.response["modifier"][modifier]
    else:
      data=self.response["default"]
      
    last_text=random.choice(data["last"])
    
    if genre:
      genre_display = genre.replace("_", " ").title()
      last_text=last_text.format(genre=genre_display)
      
    return last_text
    
  def get_film_list(self,genre,modifier=None):
    
    list_film = self.list[genre]
    
    if modifier == "rating":
      list_film = sorted(list_film, key=lambda x: x["rating"], reverse=True)
      
    elif modifier == "year":
      list_film = sorted(list_film, key=lambda x: x["year"], reverse=True)
    
    if modifier == "top_10":
      list_film = list_film[:10]
    else:
      list_film = list_film[:5]
    
    return list_film
    
  
  #====================================================/
  # RESPONSE BUILDER
  #====================================================/
  
  def get_recommend_response(self,genre=None):
    if genre:
      data=self.response["intent"]["recommend_by_genre"]
    else:
      data=self.response["intent"]["recommend_all"]
      
    first_text=random.choice(data["first"])
    last_text=random.choice(data["last"])
    
    if genre:
      genre_display = genre.replace("_", " ").title()
      first_text=first_text.format(genre=genre_display)
      last_text=last_text.format(genre=genre_display)
    return first_text,last_text
  
  
  #====================================================/
  # SCORING
  #====================================================/
  
  def get_score(self,tokens):
    keywords_score=self.keywords_score(tokens)
    title_score=self.title_score(tokens)
    
    return keywords_score + title_score
    
  def keywords_score(self,tokens):
    score=0
    for category in self.keys:
      for key_type,data in self.keys[category].items():
        keywords=data["keywords"]
        weight=data["score"]
        for k in keywords:
          if k in tokens:
              score += weight
              
    return score
    
  def title_score(self, tokens):
    score = 0
    msg_tokens = set(tokens)

    for genre in self.list:
      for film in self.list[genre]:
        title = film['title'] if isinstance(film, dict) else film
        film_tokens = set(title.lower().split())
          
        if msg_tokens & film_tokens:
          score += 2

    return score
  
  
  #====================================================/
  # FALLBACK
  #====================================================/
  
  def fallback_genre(self,msg):
    for genre in self.keys["genre"]:
      if genre in msg:
        return self.formatter_film(genre)
        
    return None
    
  def fallback_search(self,msg):
    result=[]
    for genre in self.list:
      for film in self.list[genre]:
        title=film["title"]
        if title.lower() in msg:
          result.append((genre,title))
          
    if not result:
      return None
      
    genre,title=result[0]
    result_text=f"I found these movie in {genre} \n\n"
    for i,(genre,title) in enumerate(result,1):
      result_text+=f"{i}.{title}"
    
    return result_text
  
  
  #====================================================/
  # DEBUG
  #====================================================/
  
  def get_intent_debug(self,msg):
    parse=self.parse_message(msg)
    
    genre=parse["genre"] or self.state.get("last_genre",[])
    modifier=parse["modifier"]
    intent=parse["intent"]
    context=parse["context"]
    
    if modifier and intent:
      intent=None
    
    if not modifier:
      if intent:
        modifier=None
      else:
        modifier=self.state.get("last_modifier")
    
    genre_text = self.format_genre_list(genre)
    
    mode = self.decide_mode(genre,modifier,intent,context)
    
    match mode:
      case "single_genre":
        return f"single_genre ({genre_text},{modifier})"
        
      case "multi_genre":
        return f"multi_genre ({genre_text},{modifier})"
        
      case "recommend_by_genre":
        return f"recommend_by_genre ({genre_text})"
        
      case "recommend_all":
        return "recommend_all"
        
      case "fallback":
        if self.fallback_genre(msg):
          return "fallback_genre"
          
        if self.fallback_search(msg):
          return "fallback_search"
          
    return "Unknown"
   
    
  #====================================================/
  # UTILS
  #====================================================/
      
  def load_film(self,path):
    with path.open("r",encoding=ENCODING) as file_path:
      return json.load(file_path)
      
  def is_follow_up(self,msg):
    words = msg.split()
    
    if len(words) <= 2:
      return True
    
    return False