import re
import spacy
from nltk.corpus import stopwords

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
            'BE','B.E.','B.COM', 'B.E', 'BS', 'B.S','B.S.',
            'ME', 'M.E', 'M.E.', 'M.S','M.S.', 'MASTERS',
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]

def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]
    

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|!|,]', r'', tex)
            if tex in EDUCATION and tex not in STOPWORDS:
                index = resume_text.index(tex)
                
                text = resume_text[index:(index+200)]
            
                edu[tex] =  text 
                
            elif tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index ]
                

    # Extract year
    education = []
    for key in edu.keys():
        
        #print("first ",edu[key])
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        
        #print(year)
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
        print(education)

    return education
    

