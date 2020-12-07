#import spacy
import en_core_web_lg as model
#from spacy.pipeline import EntityRuler

# load any spaCy models that are installed
# this takes some time to load so doing it here and hopefully this improves performance

ENT_STRUCTURE = {
    "CHILD": [],
    "SCHOOL": [],
    "WORK": [],
    "RACT": []
}

#NLP = spacy.load('en_core_web_lg')
NLP = model.load()

DEFAULT_TASKS = [
    NLP("put away toys"),
    NLP("feed cat"),
    NLP("feed dog"),
    NLP("put laundry in hamper"),
    NLP("make bed"),
    NLP("clear table"),
    NLP("pull weeds"),
    NLP("water plants"),
    NLP("put away dishes"),
    NLP("wash dishes"),
    NLP("load dishwasher"),
    NLP("empty dishwasher"),
    NLP("help set table"),
    NLP("bring in groceries"),
    NLP("sort laundry"),
    NLP("match socks"),
    NLP("wash cat dishes"),
    NLP("wash dog dishes"),
    NLP("sweep floor"),
    NLP("rake leaves"),
    NLP("clean room"),
    NLP("put away groceries"),
    NLP("put away dishes"),
    NLP("vacuum"),
    NLP("wipe table"),
    NLP("put away clothes"),
    NLP("walk dog"),
    NLP("bring trash"),
    NLP("wash clothes"),
    NLP("move laundry"),
    NLP("take out trash")
]
