import re
import string

def preprocess_text(text):
    #Convert to lowercase
    text = text.lower()
    
    #Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    #Remove numbers
    text = re.sub(r'\d+', '', text)
    
    #Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
