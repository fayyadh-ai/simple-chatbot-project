STOPWORDS = {
  "the", "a", "an", "from", "me", "give",
  "now", "please", "maybe", "okay", "and", "to"
}

def clean_tokens(tokens):
  return [t for t in tokens if t not in STOPWORDS]