#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from interaction_file import *
#import interaction_file
from interactionFiles import interactionGenerator
import interactionFiles as iaf
from memory_quiz import memory_quiz


interactionGenerator(memory_quiz(), 'memory/')
