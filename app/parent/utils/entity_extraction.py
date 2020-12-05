
import spacy
from spacy.pipeline import EntityRuler
import json
from django.conf import settings


def extract_entities(otask: str) -> dict:
    """
    Returns some reference for an image based on the task description

    param: task_description: from the task details, will be used to identify the task image

    :return: a reference to an image to use for the child view

    """

    user_ents_raw = '''{

        "CHILD": []
    ,
        "SCHOOL": []
    ,
        "WORK": []
    ,
        "RACT": []
        }'''

    task = {}
    task['name'] = "Untitled Task"
    task['description'] = ""
    task['people'] = []
    task['date'] = "12/02/2021"
    task['location'] = "no location given"


    # Question - Does this need to run each time or can we run it once somehow? Not sure what the delay is on running this line
    nlp = settings.NLP

    user_ents_ruler = EntityRuler(nlp, phrase_matcher_attr="LOWER", overwrite_ents=True)
    user_ents = json.loads(user_ents_raw)

    for category in user_ents:
        MATCH_ID = category.upper()
        docs = []
        for item in user_ents[category]:
            docs.append(nlp(item))
        user_ents_ruler.phrase_matcher.add(MATCH_ID, docs)
    #    print(MATCH_ID, docs)

    nlp.add_pipe(user_ents_ruler)

    doc = nlp(otask)

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
            task['name'] = task['description'] = ent.text

        if ent.label_ == "DATE":
            task['date'] = ent.text

            if task['name'] == "Untitled Task":

                headOfPrep = ent.root.head.head
                referencePoint = headOfPrep

                if headOfPrep.pos_ == "VERB":
                    for child in headOfPrep.children:
                        if child.dep_ == "dobj":
                            referencePoint = child

                if referencePoint is headOfPrep:
                    for token in headOfPrep.sent:
                        if token.dep_ == "nsubj":
                            referencePoint = token

                for chunk in referencePoint.sent.as_doc().noun_chunks:
                    if chunk.root.text == referencePoint.text:
                        # print(chunk.text, ent.text)
                        task['name'] = task['description'] = (chunk.text)

    return task

