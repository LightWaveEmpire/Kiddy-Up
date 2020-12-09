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

TASK_STRUCTURE = {
    'name': "Untitled Task",
    'description': "",
    'people': [],
    'date': "2021-12-02",
    'location': "no location given"
}

#NLP = spacy.load('en_core_web_lg')
NLP = model.load()

DEFAULT_TASKS = [
    NLP("put away 1oys"),
    NLP("feed the cat"),
    NLP("feed the dog"),
    NLP("put laundry in the hamper"),
    NLP("make the bed"),
    NLP("clearthe table"),
    NLP("pull weeds"),
    NLP("water the plants"),
    NLP("put away dishes"),
    NLP("wash the dishes"),
    NLP("load the dishwasher"),
    NLP("empty the dishwasher"),
    NLP("set the table"),
    NLP("bring in the groceries"),
    NLP("sort the laundry"),
    NLP("match the socks"),
    NLP("wash the cat dishes"),
    NLP("wash the dog dishes"),
    NLP("sweep the floor"),
    NLP("rake the leaves"),
    NLP("clean room"),
    NLP("put away the groceries"),
    NLP("put away the dishes"),
    NLP("vacuum"),
    NLP("wipe table"),
    NLP("put away clothes"),
    NLP("walk dog"),
    NLP("bring trash"),
    NLP("wash clothes"),
    NLP("move laundry"),
    NLP("take out trash")
]
