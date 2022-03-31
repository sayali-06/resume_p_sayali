#organizzation
import spacy
nlp = spacy.load("en_core_web_sm")      

def extract_org(text):
    text = nlp(text)
    for word in text.ents:
        if word.label_ == "LOC":
            print(word.text,word.label_)

