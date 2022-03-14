import sys,fitz
import spacy
import re

from spacy import displacy
from spacy.matcher import Matcher



nlp = spacy.load("en_core_web_lg")
skills = "skills.jsonl"

ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.from_disk(skills)

patterns = [{"label": "EMAIL", "pattern": [{ "TEXT": { "REGEX" : "([^@|\s]+@[^@]+\.[^@|\s]+)"}}]},
            {"label": "MOBILE", "pattern": [{"TEXT": {"REGEX": "\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}" }}]}
            ]

ruler.add_patterns(patterns)

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME', [pattern], on_match=None)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text


def convertToText(fname):
	doc = fitz.open(fname)
	text = ""
	for page in doc:
		text = text + str(page.get_text())
	
	tx = " ".join(text.split("\n"))
	return tx



text = convertToText('./resume1.pdf')
doc = nlp(text)

name = extract_name(text)
print("-------")
print(name)
print("-------")

displacy.render(doc, style="ent", jupyter=True)

dict = {}
skills = []

i = 0

for ent in doc.ents:
	if ent.label_ == "PERSON" and i==0:
		dict['PERSON'] = ent.text
		i = i+1
	if ent.label_ == "EMAIL":
		dict["EMAIL"] = ent.text
	if ent.label_ == "MOBILE":
		dict['MOBILE'] = ent.text
	if ent.label_ == "SKILL":
		skills.append(ent.text)


skills = [i.capitalize() for i in set([i.lower() for i in skills])]
dict["SKILLS"] = skills 


print(dict)