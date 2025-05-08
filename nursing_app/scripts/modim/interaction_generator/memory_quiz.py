#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

lang_tag = ('<*,*,it,*>','<*,*,es,*>','<*,*,en,*>')

# Image list
images = ['dolphin.jpg', 'horse.jpg', 'cat.jpg', 'dog.jpg', 'bear.jpg']
positions = ['first', 'second', 'third', 'fourth', 'fifth']
positions_it = ['prima', 'seconda', 'terza', 'quarta', 'quinta']
positions_es = ['primera', 'segunda', 'tercera', 'cuarta', 'quinta']

def presentation_actions():
    actions = []
    for i, image in enumerate(images):
        action = {
            'NAME': 'memory_show_%d' % (i + 1),
            'IMAGES': [(tag, image) for tag in lang_tag]
        }
        actions.append(action)
    return actions

def recall_actions():
    actions = []
    for i in range(5):
        correct = images[i]
        options = random.sample(images, 3)
        if correct not in options:
            options[random.randint(0, 2)] = correct

        # BUTTONS structure
        buttons = []
        for img in options:
            label = img.split('.')[0]
            values = [(tag, label) for tag in lang_tag]
            buttons.append((label, values))

        # TEXTS per language
        question_it = u"Qual e' stata la %s immagine?" % positions_it[i]
        question_es = u"Cual fue la %s imagen?" % positions_es[i]
        question_en = u"What was the %s image?" % positions[i]

        texts = zip(lang_tag, [question_it, question_es, question_en])

        action = {
            'NAME': 'memory_recall_%d' % (i + 1),
            'TEXTS': texts,
            'BUTTONS': buttons,
            'GRAMMARS': [(tag, '[LOAD_GRAMMAR] frame_memory') for tag in lang_tag]
        }

        actions.append(action)
    return actions

def memory_quiz():
    return presentation_actions() + recall_actions()
