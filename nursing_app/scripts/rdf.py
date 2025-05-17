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
        # Start interaction with a known person
        name = unicode(name_literal)
        im.executeModality('TEXT', 'Hello, %s, I remember you!' % name)
        im.executeModality('TTS', 'Hello, %s, I remember you!' % name)
        
        # Retrieve previous wellbeing score
        wellbeing_feedback = graph.value(person_uri, EX.hasWellbeingFeedback)
        reflex_feedback = graph.value(person_uri, EX.hasReflexFeedback)
        memory_feedback = graph.value(person_uri, EX.hasMemoryFeedback)
        
         # If wellbeing was poor or fair, ask if they feel better now
        if wellbeing_feedback in [Literal('score_poor'), Literal('score_fair')]:
            im.executeModality('TEXT', 'Last time, you reported not feeling great. Do you feel better today?')
            im.executeModality('TTS', 'Last time, you reported not feeling great. Do you feel better today?')
        elif wellbeing_feedback in [Literal('score_good'), Literal('score_very_good'), Literal('score_excellent')]:
            im.executeModality('TEXT', 'Great to see you again! Keep up the good wellbeing, %s!' % name)
            im.executeModality('TTS', 'Great to see you again! Keep up the good wellbeing, %s!' % name)
        
        # Reflex/memory encouragement
        if reflex_feedback in [Literal('poor_reflexes'), Literal('fair_reflexes')]:
            im.executeModality('TEXT', 'Your reflexes were a bit slow last time. Want to try again today?')
            im.executeModality('TTS', 'Your reflexes were a bit slow last time. Want to try again today?')

        if memory_feedback in [Literal('poor_memory'), Literal('no_memory'), Literal('fair_memory')]:
            im.executeModality('TEXT', 'Want to see if your memory has improved since last time?')
            im.executeModality('TTS', 'Want to see if your memory has improved since last time?')
    else:
        # Start interaction with a new person
        im.executeModality('TTS', 'Hello visitor, I have never seen you. What is your name?')
        im.executeModality('TEXT', 'Hello visitor, I have never seen you. What is your name?')
        
        # Simulate human saying their name
        name = raw_input('Please enter your name: ')
        im.simulate_human_say(name)
        
        # Make robot greet the new person
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
        answers_map = {
            'poor': 1, 'fair': 2, 'good': 3, 'very_good': 4, 'excellent': 5,
            'very_much': 1, 'moderately': 2, 'a_little': 3, 'not_at_all': 4,
            'severe': 1, 'moderate': 2, 'slight': 3, 'none': 4,
            'never': 1, 'rarely': 2, 'sometimes': 3, 'often': 4, 'always': 5,
            'unable': 1, 'a_lot_of_difficulty': 2, 'some_difficulty': 3, 'no_difficulty': 4,
            'yes_regularly': 4, 'extremely': 1, 'quite_a_bit': 2
        }
        total = sum(answers_map.get(ans, 0) for ans in answers)

        if total <= 12:
            score = 'score_poor'
        elif total <= 18:
            score = 'score_fair'
        elif total <= 24:
            score = 'score_good'
        elif total <= 30:
            score = 'score_very_good'
        else:
            score = 'score_excellent'

        im.execute(score)

        graph.set((person_uri, EX.hasScore, Literal(score))) # This person has a score of x
        graph.set((person_uri, EX.hasWellbeingFeedback, Literal(score))) # This person has a wellbeing of x

    elif choice == 'reflexes_test':
        im.ask('reflexes_test')
        
        total_time = 0.0
        for i in range(10):
            print('Test #%d: Press Enter to simulate touching the robot\'s hand...' % (i + 1))
            start_time = time.time()
            raw_input()
            
            # Simulate hand touch on both sides
            im.simulate_hand_touch(left=False, value=1.0)
            im.simulate_hand_touch(left=True, value=1.0)
            
            reflex_time = time.time() - start_time
            print('Time for test #%d: %.3fs' % (i + 1, reflex_time))
            total_time += reflex_time

        avg_reflex_time = total_time / 10.0
        print('Average reflex time: %.3fs' % avg_reflex_time)
        
        # Infer reflex score
        if avg_reflex_time < 0.5:
            reflex_score = 'excellent_reflexes'
        elif avg_reflex_time < 1.0:
            reflex_score = 'very_good_reflexes'
        elif avg_reflex_time < 1.5:
            reflex_score = 'good_reflexes'
        elif avg_reflex_time < 2.0:
            reflex_score = 'fair_reflexes'
        else:
            reflex_score = 'poor_reflexes'
        
        im.executeModality('TEXT', 'Your average reflex time is %.3fs' % avg_reflex_time)
        im.executeModality('TTS', 'Your average reflex time is %.3fs' % avg_reflex_time)
        time.sleep(1)
        
        graph.set((person_uri, EX.hasReflexTime, Literal(avg_reflex_time))) # This person has a reflex time of x
        graph.set((person_uri, EX.hasReflexFeedback, Literal(reflex_score))) # This person has a reflex score that classifies them as x

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
        im.executeModality('TEXT', 'Your memory score is %d out of 5' % memory_score)
        im.executeModality('TTS', 'Your memory score is %d out of 5' % memory_score)
        time.sleep(1)

        graph.set((person_uri, EX.hasMemoryScore, Literal(memory_score))) # This person has a memory score of x
        graph.set((person_uri, EX.hasMemoryFeedback, Literal(feedback_map[memory_score]))) # This person has a memory feedback of x

    graph.serialize(destination='../people_graph.ttl', format='turtle')
    im.init()

if __name__ == '__main__':
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)
    mws.run_interaction(interaction)
