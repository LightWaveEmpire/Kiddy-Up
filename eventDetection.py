# There's a bug in the algorithm-- it can't tell what to do with
# [multiple noun phrases with the same base] in the [same sentence] .
#
# fine:
# "Soccer practice on thurs. Football practice on september 8th"
# "Soccer practice now on thurs and ballet lesson on september 8th"
#
# problem:
# "Soccer practice on thurs and football practice on september 8th"
#
# This is because it can't tell the difference between "soccer practice"
# and "football practice", just that they're both "practice".
#
# So it reports both dates for both activities.
#
# I'm working on it.
#
# -- BJD

import spacy

nlp = spacy.load("en_core_web_lg")

# comment and uncomment these lines as you like to change the sample document
doc = nlp(" Our recruitment this year will occur from today, September 8th, to September 16th. ")
# doc = nlp("soccer practice is on thurs. football practice is on september 8th")
# doc = nlp("we will be selling cookies from september 8th to september 16th")

# Uncomment these lines to load a file for testing.
# You may need to alter the value of filename.
#filename = "sample.txt"
#infile = open(filename)
#doc = nlp(infile.read())
#infile.close()

# For each date in the source...
# find the most closely related noun or verb.
# This noun/verb is now the reference point.
for ent in doc.ents:
    if ent.label_ == "DATE":
        headOfPrep = ent.root.head.head
        referencePoint = headOfPrep

    # We expect an activity to be a noun phrase. So if our current
    # reference point is a verb, we need to find the relevant noun.

        # If our reference verb says that something was done to our noun,
        # we're looking for the object of that verb.
        # The object, a noun, will be our new reference point.
        if headOfPrep.pos_ == "VERB":
            for child in headOfPrep.children:
                if child.dep_ == "dobj":
                    referencePoint = child

        # This block will activate if:
        # 1. The reference verb had no object
        # 2. The reference verb says our noun "is" or "will be" something
        # 3. The reference point was already a noun
        #
        # Any of these conditions mean we're probably looking for
        # the subject of the sentence.
        # The subject, a noun, will be our new reference point.
        #
        # Note: in theory, the reference point should only be a noun if
        # the input had no verb, in which case the noun is already the
        # subject and this shouldn't change anything. If that turns out
        # not to be true... well, it won't be the only update I need to
        # make anyhow.
        if referencePoint is headOfPrep:
            for token in headOfPrep.sent:
                if token.dep_ == "nsubj":
                    referencePoint = token

        # Now that we're sure we have a good reference point, we just need
        # to find the noun phrase it's part of. Find all the noun phrases
        # in the sentence and check which one has our noun as a base.
        #
        # NOTE: this is where the bug is. I need to figure out how to look
        # for the noun phrase using *this instance* of the noun.
        for chunk in referencePoint.sent.as_doc().noun_chunks:
            if chunk.root.text == referencePoint.text:
                print(chunk.text, ent.text)
