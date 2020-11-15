import spacy
from spacy.pipeline import EntityRuler
import json

nlp = spacy.load("en_core_web_sm")
ruler = EntityRuler(nlp, phrase_matcher_attr="LOWER", overwrite_ents=True)


traci_ents_raw = '''{

        "child": ["bethany", "james", "emma sue"]
    ,

        "school": ["germanna community college", "old dominion university"]
    ,

        "work": ["national counseling group", "anthem insurance"]
    ,

        "ract": ["raid", "recitation", "kiddy-up meeting", "therapy", "staff meeting"]
}'''

user_ents = json.loads(traci_ents_raw)


# the code works, but we're not gonna wannna run it every time.
# look into serializing.

for category in user_ents:
    MATCH_ID = category.upper()
    docs = []
    for item in user_ents[category]:
        docs.append(nlp(item))
    ruler.phrase_matcher.add(MATCH_ID, docs)
#    print(MATCH_ID, docs)

nlp.add_pipe(ruler)


doc = nlp("emma sue has kiddy-up meeting tomorrow at old dominion university")


ents = [(ent.text, ent.label_) for ent in doc.ents]
print(ents)
