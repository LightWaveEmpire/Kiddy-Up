#import spacy
from spacy.pipeline import EntityRuler
import json
from parent.utils import constants
import sys
from dateutil import parser as dupr
from django.utils import timezone

def extract_entities(otask, entities=None, debug=False) -> dict:
    """
    Returns some reference for an image based on the task description

    param: task_description: from the task details, will be used to identify the task image

    :return: a reference to an image to use for the child view

    """
    user_ents_raw = entities

    if user_ents_raw is None:
        user_ents_raw = json.dumps(constants.ENT_STRUCTURE)

    task = json.loads(json.dumps(constants.TASK_STRUCTURE))

    # nlp = spacy.load('en_core_web_lg')
    nlp = constants.NLP

    ents_ruler = EntityRuler(nlp, phrase_matcher_attr="LOWER", overwrite_ents=True)
    user_ents = json.loads(user_ents_raw)
    #remainder = otask

    for category in user_ents:
        MATCH_ID = category.upper()
        docs = []
        for item in user_ents[category]:
            docs.append(nlp(item))
        ents_ruler.phrase_matcher.add(MATCH_ID, docs)
    #    print(MATCH_ID, docs)

    try:
        nlp.add_pipe(ents_ruler)
    except ValueError:
        print("Entity Ruler not added: already exists", file=sys.stderr)

    doc = nlp(otask)

    task['description'] = task['name'] = str(otask)

    for ent in doc.ents:
        if debug:
            print(ent, ent.label_, file=sys.stderr)

        if ent.label_ == "CHILD":
            task['people'].append(ent.text)

        if ent.label_ == "PERSON":
            task['people'].append(ent.text)

        if ent.label_ == "WORK":
            task['location'] = ent.text

        if ent.label_ == "SCHOOL":
            task['location'] = ent.text

        if ent.label_ in ["GPE", "LOC", "ORG, FAC"]:
            task = extract_location(ent, task)

        if ent.label_ == "DATE":
            task = extract_date(ent, task)

#    for person in task['people']:
#        if person in user_ents['CHILD']:
#            desc = desc.replace(person, "").strip()
#            remainder = remainder.replace(person, "").strip()

    task['description'] = clean_description(task, user_ents["CHILD"])
#    print(task['name'], "84", file=sys.stderr)
    title = clean_title(task, user_ents["CHILD"])
#    print(task['name'], "86", file=sys.stderr)

    task['name'] = reportClosest(
        findClosest(constants.DEFAULT_TASKS, title,
                    findClosest(user_ents['RACT'], title))
    )

    if task['name'] == "Untitled Task":
        task['name'] = title[0:17]

        if task['name'].islower():
            task['name'] = title.title()[0:17]
        if len(title) > 17:
            task['name'] += "..."
            
    if task['date'] == "2752-02-29":
        task['date'] = timezone.localdate().isoformat()

    print(task, file=sys.stderr)
    #ABRACADABRA! When I put this here it works.
    return task


def reportClosest(current_top):
    #    print("\n", current_top, "\n", flush=True)
    try:
        return current_top[0]
    except TypeError:
        return None


def findClosest(list_of_golds, new_task, current_top=("Untitled Task", 0), strict=False, debug=False):

    nlp = constants.NLP
    threshold = .86 if strict else .8

    # parses new_task if necessary
    try:
        new_task.is_parsed
    except AttributeError:
        temp = nlp(new_task)
        new_task = temp

    task, score = ("", 0)
    if current_top is not None:
        if current_top[1] >= 0 and current_top[1] <= 1:
            task = current_top[0]
            score = current_top[1]

    for gold_task in list_of_golds:
        try:
            gold_task.is_parsed
        except AttributeError:
            temp = nlp(gold_task)
            gold_task = temp
        sim = new_task.similarity(gold_task)
        if debug:
            print(gold_task, ": ", sim, file=sys.stderr, flush=True)
        if strict and sim < threshold:
            pass
        elif sim > score:
            score = sim
            task = gold_task
    if score > threshold:
        current_top = (task, score)
    return current_top


def extract_location(entity, task):
    if entity.label_ == "GPE" or entity.label_ == "LOC":
        task['location'] = entity.text
        #print(ent.root.text, ent.root.dep_)
        task['name'] = task['name'].replace(entity.text, "").strip()
        if entity.root.head.pos_ == "ADP":
            task['name'] = task['name'].replace(entity.root.head.text, "", 1).strip()

    if entity.label_ == "ORG" or entity.label_ == "FAC":
        if entity.root.head.text in ["at", "in", "on"]:
            if task['location'] == "no location given":
                task['location'] = entity.text
                task['name'] = task['name'].replace(entity.text, "").strip()
                if entity.root.head.pos_ == "ADP":
                    task['name'] = task['name'].replace(entity.root.head.text, "", 1).strip()

    return (task)


def extract_date(entity, task):
    task['date'] = dupr.parse(entity.text).date().isoformat()
    # DEBUG: use to dummy out issues reading date.
    # task['date'] = constants.TASK_STRUCTURE['date']
    task['name'] = task['name'].replace(entity.text, "").strip()
    if entity.root.head.pos_ == "ADP":
        task['name'] = task['name'].replace(entity.root.head.text, "", 1).strip()

    return (task)


def clean_description(task, children):

    desc = task['description']

    for person in task['people']:
        if person in children:
            task['description'] = desc.replace(person, "").strip()
            desc = task['description']
            #print("desc - ", person, desc)

        #quick-and-dirty patch
        if desc.startswith("\'s"):
            desc = desc.replace("\'s", "", 1).strip()

    return desc


def clean_title(task, children):

    title = task['name']

    for person in task['people']:
        if person in children:
            task['name'] = title.replace(person, "").strip()
            title = task['name']
            #print("title - ", person, " -- ", title)

    #quick-and-dirty patch
    if title.startswith("\'s"):
        title = title.replace("\'s", "", 1).strip()

    return title
