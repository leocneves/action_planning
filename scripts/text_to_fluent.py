#!/usr/bin/env python
import spacy
from pathlib import Path
import warnings
import sys
import os
import rospy
from std_msgs.msg import String, UInt8
import time
import os
from rosplan_knowledge_msgs.srv import *
from rosplan_knowledge_msgs.msg import *
from diagnostic_msgs.msg import KeyValue
# warnings.filterwarnings("ignore")


nlp = spacy.load('en_core_web_sm')


# phrase = 'Bring me some Snack from a seating.'
# phrase = 'I need my notebook'
# phrase = 'Move to the bench, move to the bookshelf, and move to the bar.'
# phrase = 'Move to the sidetable, grasp the Garlic sauce and bring it to the bookshelf.'
def callback(data):
    global srvKlgBase

    phrase = data.data
    doc = nlp(phrase)
    atf = {
        'bring':'OBJECT_GOAL',
        'place':'OBJECT_GOAL',
        'move':'ROBOT_GOAL',
        'grasp':'GRASP_OBJECT'
    }

    args_fluents = {
            'OBJECT_GOAL':['obj', 'waypont'],
            'ROBOT_GOAL':['waypont'],
            'GRASP_OBJECT':['obj']
    }

    fluents = []

    for i,token in enumerate(doc):
        if token.pos_ == 'VERB':
            prep = [x for x in token.children if x.dep_ == 'prep']
            dobj = [x for x in token.children if x.dep_ == 'dobj']
            adp = [x for x in token.children if x.pos_ == 'ADP']

            if (len(prep) > 0) and (len(dobj) > 0):
                pobj = [x for x in prep[0].children if x.dep_ == 'pobj']

                print('\tExtracted relation from text:',token.text, '->', dobj[0].text, '->', pobj[0].text)
                fluents.append(f'{atf[token.text.lower()]}({dobj[0].text}, {pobj[0].text})')
            elif (len(prep) > 0):
                pobj = [x for x in prep[0].children if x.dep_ == 'pobj']
                if len(pobj) > 0:

                    print('\tExtracted relation from text:',token.text, '->', pobj[0].text)
                    fluents.append(f'{atf[token.text.lower()]}({pobj[0].text})')
            elif (len(dobj) > 0) and (len(adp) > 0):
                if dobj[0].text.lower() == 'it':
                    dobj = [x for x in doc[:i] if x.dep_ == 'dobj']
                    adp_dobj = [x for x in adp[0].children if x.dep_ == 'pobj']

                    print('\tExtracted relation from text:',token.text, '->', dobj[0].text, '->', adp_dobj[0].text)
                    fluents.append(f'{atf[token.text.lower()]}({dobj[0].text}, {adp_dobj[0].text})')

                else:

                    print('\tExtracted relation from text:',token.text, '->', dobj[0].text, '->', adp_dobj[0].text)
                    fluents.append(f'{atf[token.text.lower()]}({dobj[0].text}, {pobj[0].text})')

            elif (len(dobj) > 0):
                if dobj[0].text.lower() == 'it':
                    dobj = [x for x in doc[:i] if x.dep_ == 'dobj']

                    print('\tExtracted relation from text:',token.text, '->', dobj[0].text)
                    fluents.append(f'{atf[token.text.lower()]}({dobj[0].text})')
                else:

                    print('\tExtracted relation from text:',token.text, '->', dobj[0].text)
                    fluents.append(f'{atf[token.text.lower()]}({dobj[0].text})')

    rospy.logwarn('FLUENTS: ' + str(fluents))

    srvKlgBase = rospy.ServiceProxy('/rosplan_knowledge_base/update', KnowledgeUpdateService)

    for fluent in fluents:

        f = fluent.split('(')[0]
        argsFluent = fluent.split('(')[1].replace(')', '').split(',')

        # Atualiza a base de conhecimento
        srv = KnowledgeItem()

        srv.knowledge_type = 1
        srv.initial_time = rospy.get_rostime()
        srv.is_negative = False
        srv.instance_type = "bool"
        srv.attribute_name = f

        aux = []
        for arg,val in zip(args_fluents[f], argsFluent):
            k = KeyValue()
            k.key = arg
            k.value = val
            aux.append(k)

        srv.values=aux

        try:
            x = srvKlgBase(KnowledgeUpdateServiceRequest.ADD_KNOWLEDGE, srv)
            print(f'Fluent {f} with args {argsFluent} updated!')
        except Exception as e:
            print("Service call failed: %s" % e)

def main():
    rospy.init_node('text_to_fluent', anonymous=True)

    # pub = rospy.Publisher('/kcl_rosplan/plan_graph', String, queue_size=10)
    rospy.Subscriber("/command", String, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    main()



# Converte para imagem
# output_path = Path("teste.svg")
# svg = spacy.displacy.render(doc, style='dep')
# with output_path.open("w", encoding="utf-8") as fh:
#     fh.write(svg)
