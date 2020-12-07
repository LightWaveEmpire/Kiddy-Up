#import spacy
from spacy.pipeline import EntityRuler
import json
import constants
# from django.conf import settings


def extract_entities(otask, entities=None, nlp=None) -> dict:
    """
    Returns some reference for an image based on the task description

    param: task_description: from the task details, will be used to identify the task image

    :return: a reference to an image to use for the child view

    """
    if entities is None:
        user_ents_raw = json.dumps(constants.ENT_STRUCTURE)
    else:
        user_ents_raw = entities

    task = {}
    task['name'] = "Untitled Task"
    task['description'] = ""
    task['people'] = []
    task['date'] = "12/02/2021"
    task['location'] = "no location given"

    # Question - Does this need to run each time or can we run it once somehow? Not sure what the delay is on running this line
    # nlp = settings.NLP
    if nlp is None:
        # nlp = spacy.load('en_core_web_lg')
        nlp = constants.NLP

    #this is not how constants are supposed to work
    ents_ruler = EntityRuler(nlp, phrase_matcher_attr="LOWER", overwrite_ents=True)
    user_ents = json.loads(user_ents_raw)
    remainder = otask

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
        pass

    doc = nlp(otask)

    task['description'] = str(otask)

    for ent in doc.ents:

        if ent.label_ == "CHILD":
            task['people'].append(ent.text)

        if ent.label_ == "PERSON":
            task['people'].append(ent.text)

        if ent.label_ == "WORK":
            task['location'] = ent.text

        if ent.label_ == "SCHOOL":
            task['location'] = ent.text

        # this is shoddy and needs tweaking
        if ent.label_ == "GPE":
            task['location'] = ent.text

        if ent.label_ == "RACT":
            task['name'] = ent.text

        if ent.label_ == "DATE":
            task['date'] = ent.text

    for person in task['people']:
        if person in user_ents['CHILD']:
            remainder = remainder.replace(person, "").strip()

    task['description'] = remainder

    task['name'] = reportClosest(
        findClosest(constants.DEFAULT_TASKS, remainder,
                    findClosest(user_ents['RACT'], remainder))
    )

    if task['name'] is None:
        try:
            task['name'] = remainder.title()[0:17]
            if len(remainder) > 18:
                task['name'] += "..."
        except IndexError:
            task['name'] = remainder.title()
#    if task['name'] == "Untitled Task":
#        for ent in doc.ents:
#
#            headOfPrep = ent.root.head.head
#            referencePoint = headOfPrep
#
#            if headOfPrep.pos_ == "VERB":
#                for child in headOfPrep.children:
#                    if child.dep_ == "dobj":
#                        referencePoint = child
#
#            if referencePoint is headOfPrep:
#                for token in headOfPrep.sent:
#                    if token.dep_ == "nsubj":
#                        referencePoint = token
#
#            for chunk in referencePoint.sent.as_doc().noun_chunks:
#                if chunk.root.text == referencePoint.text:
#                    # print(chunk.text, ent.text)
#                    task['name'] = (chunk.text)

    print("/n", task, "\n", flush=True)
    return task


def reportClosest(current_top):
    try:
        return current_top[0]
    except TypeError:
        return None


def findClosest(list_of_golds, new_task, current_top=("", 0), nlp=None):

    if nlp is None:
        # nlp = spacy.load('en_core_web_lg')
        nlp = constants.NLP

    try:
        new_task.is_parsed
    except AttributeError:
        temp = nlp(new_task)
        new_task = temp

    task = " "
    score = 0
    if current_top is not None:
        if current_top[1] >= 0 and current_top[1] < 1:
            task = current_top[0]
            score = current_top[1]

    for gold_task in list_of_golds:
        sim = new_task.similarity(gold_task)
        # print(gold_task, ": ", sim, file=sys.stderr)
        if sim > score:
            score = sim
            task = gold_task
    if score > .8:
        return task, sim
    return None
