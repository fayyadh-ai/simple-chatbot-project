import sys
import time

def typing_print(text,delay=0.15):
  words=str(text).split(" ")
  for i,word in enumerate(words):
    sys.stdout.write(word)
    sys.stdout.flush()
    if i<len(words) -1:
      sys.stdout.write(" ")
      sys.stdout.flush()
    time.sleep(delay)
  print()
  
def typing_debug_print(text,delay=0.05):
  words=str(text).split(" ")
  for i,word in enumerate(words):
    sys.stdout.write(word)
    sys.stdout.flush()
    if i<len(words) -1:
      sys.stdout.write(" ")
      sys.stdout.flush()
    time.sleep(delay)
  print()