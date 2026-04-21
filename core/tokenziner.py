def tokenize(raw):
  tokens=raw.lower().strip().split()
  return tokens
  
def tokens_to_string(tokens):
  return " ".join(tokens)