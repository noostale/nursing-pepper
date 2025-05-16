# -*- coding: utf-8 -*-
from __future__ import print_function

from modim.ws_client import ModimWSClient
from modim.interaction_manager import InteractionManager as im
from rdflib import Graph, Namespace, URIRef, RDF, Literal
import time

# Main interaction function
def interaction():
    
    # Use HTTP-based namespace
    EX = Namespace("http://example.org/robot_kb#")

    # Function to generate a person URI based on distance
    def person_uri_from_distance(d):
        return URIRef("http://example.org/robot_kb#person_%.2f" % d)
    
    # Load or initialize RDF graph
    graph = Graph()
    graph.bind("robot_kb", EX)
    try:
        graph.parse("../people_graph.ttl", format="turtle")
    except Exception:
        pass

    # Initialize the interaction manager
    im.init()
    time.sleep(1)

    # Simulate sonar input
    front = raw_input('Enter sonar distance (each distance represents a person): ')
    try:
        front_val = float(front)
    except ValueError:
        print("Invalid input for distance.")

    print('front:', front_val)

    # Determine the person URI
    person_uri = person_uri_from_distance(front_val)

    # Check if we already know this person
    name_literal = graph.value(person_uri, EX.hasName)
    if name_literal:
        # Known person
        name = unicode(name_literal)
        im.executeModality('TEXT', 'Hello, %s, I remember you!' % name)
        im.executeModality('TTS', 'Hello, %s, I remember you!' % name)
    else:
        # New visitor
        im.executeModality('TTS', 'Hello visitor, I have never seen you. What is your name?')
        im.executeModality('TEXT', 'Hello visitor, I have never seen you. What is your name?')
        name = raw_input('Please enter your name: ')
        im.simulate_human_say(name)
        im.executeModality('TEXT', 'Hello, %s, I will remember you next time.' % name)
        im.executeModality('TTS', 'Hi, %s, I will remember you next time.' % name)
        # Add new person to the graph
        graph.add((person_uri, RDF.type, EX.Person)) # This single person is of type 'Person'
        graph.add((person_uri, EX.hasName, Literal(name))) # This person has a name 'name'

    # Continue with interaction options
    choice = im.ask('welcome')
    im.executeModality('TEXT', 'Are you ready, %s? Select one of the options below!' % name)

    if choice == 'quiz':
        # Quiz flow
        answers = [im.ask('questions/question%d' % i) for i in range(1, 8)]
        score_map = {
            'poor': 1, 'fair': 2, 'good': 3, 'very_good': 4, 'excellent': 5,
            'very_much': 1, 'moderately': 2, 'a_little': 3, 'not_at_all': 4,
            'severe': 1, 'moderate': 2, 'slight': 3, 'none': 4,
            'never': 1, 'rarely': 2, 'sometimes': 3, 'often': 4, 'always': 5,
            'unable': 1, 'a_lot_of_difficulty': 2, 'some_difficulty': 3, 'no_difficulty': 4,
            'yes_regularly': 4, 'extremely': 1, 'quite_a_bit': 2
        }
        score = sum(score_map.get(ans, 0) for ans in answers)

        def classify(total):
            if total <= 12:
                return 'score_poor'
            elif total <= 18:
                return 'score_fair'
            elif total <= 24:
                return 'score_good'
            elif total <= 30:
                return 'score_very_good'
            else:
                return 'score_excellent'

        wellbeing = classify(score)
        im.execute(wellbeing)

        graph.set((person_uri, EX.hasScore, Literal(score))) # This person has a score of x
        graph.set((person_uri, EX.hasWellbeing, Literal(wellbeing))) # This person has a wellbeing of x

    elif choice == 'reflexes_test':
        im.ask('reflexes_test', 1)
        
        total_time = 0.0
        for i in range(10):
            print('Test #%d: Press Enter to simulate touching the robot\'s hand...' % (i + 1))
            start_time = time.time()
            raw_input()
            im.simulate_hand_touch(left=False, value=1.0)
            im.simulate_hand_touch(left=True, value=1.0)
            reflex_time = time.time() - start_time
            print('Time for test #%d: %.3fs' % (i + 1, reflex_time))
            total_time += reflex_time

        avg_reflex_time = total_time / 10.0
        print('Average reflex time: %.3fs' % avg_reflex_time)
        
        im.executeModality('TEXT', 'Your average reflex time is %.3fs' % avg_reflex_time)
        im.executeModality('TTS', 'Your average reflex time is %.3fs' % avg_reflex_time)

        graph.set((person_uri, EX.hasReflexTime, Literal(avg_reflex_time))) # This person has a reflex time of x

    elif choice == 'memory_test':
        for i in range(1, 6):
            im.ask('memory/image_memory_show_%d' % i, 1)
            time.sleep(3)

        correct_sequence = ['dolphin', 'horse', 'cat', 'dog', 'bear']
        user_answers = [unicode(im.ask('memory/text_memory_recall_%d' % i)) for i in range(1, 6)]

        memory_score = sum(1 for ua, correct in zip(user_answers, correct_sequence) if ua == correct)
        print('Memory test score: %d/5' % memory_score)

        feedback_map = {5: 'excellent_memory', 4: 'very_good_memory', 3: 'good_memory',
                        2: 'fair_memory', 1: 'poor_memory', 0: 'no_memory'}
        im.execute(feedback_map[memory_score])

        graph.set((person_uri, EX.hasMemoryScore, Literal(memory_score))) # This person has a memory score of x

    graph.serialize(destination='../people_graph.ttl', format='turtle')
    im.init()

if __name__ == '__main__':
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)
    mws.run_interaction(interaction)
