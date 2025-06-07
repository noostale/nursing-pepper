# -*- coding: utf-8 -*-
from __future__ import print_function

from modim.ws_client import ModimWSClient
from modim.interaction_manager import InteractionManager as im
from rdflib import Graph, Namespace, URIRef, RDF, Literal
import time
import sys

# Redirect stderr to devnull to silence ALSA warnings
#sys.stderr = open(os.devnull, 'w')
        

# Main interaction function
def interaction():
    import os
    import sys
    from datetime import datetime


    def run_talk(im):
        """
        Enters a loop of “You: …” console input. 
        Sends each line to Gemini, prints “Nursing Pepper: …”,
        and speaks it via TTS. Typing 'exit' or 'quit' breaks out.
        """
        
                
        def get_gemini_response(user_input):
            import urllib2
            import json
            import os
            from dotenv import load_dotenv
            load_dotenv()  # Loads API_KEY from .env by default
            api_key = os.getenv("API_KEY")
            gemini_url = (
                "https://generativelanguage.googleapis.com/v1beta/models/"
                "gemini-2.0-flash:generateContent?key=" + api_key
            )

            # The “system instruction” for Nursing Pepper, lod from the file 
            # 'context'
            with open("../context", 'r') as f:
                system_instruction_text = f.read().strip()
                
            
            """
            Sends user_input to Gemini-2.0 and returns the reply text.
            """
            headers = {"Content-Type": "application/json"}
            data = {
                "system_instruction": {
                    "parts": [
                        {"text": system_instruction_text}
                    ]
                },
                "contents": [
                    {
                        "parts": [
                            {"text": user_input}
                        ]
                    }
                ]
            }
            json_data = json.dumps(data)
            request = urllib2.Request(gemini_url, data=json_data, headers=headers)

            try:
                response = urllib2.urlopen(request)
                response_data = response.read()
                result = json.loads(response_data)
                # Extract only the text part of the first candidate
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
                return answer.strip()
            except urllib2.HTTPError as e:
                error_message = e.read()
                return "HTTP error code: {} | {}".format(e.code, error_message)
            except Exception as e:
                return "Error: {}".format(str(e))

        
        im.executeModality('TTS', 'Hi! I am Nursing Pepper, your friendly robot nurse. How can I help you today?')
        im.executeModality('TEXT', 'Hi! I am Nursing Pepper, your friendly robot nurse. How can I help you today?')
        
        while True:
            try:
                #user_input = raw_input("You: ")  # type: ignore
                user_input = im.speech_to_text()
                print("You:", user_input)
            except EOFError:
                break

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting talk mode...")
                im.executeModality('TEXT', "Exiting talk mode.")
                im.executeModality('TTS', "Exiting talk mode.")
                break

            answer = get_gemini_response(user_input)
            print("Nursing Pepper:", answer)
            # Let the robot both display and speak the reply
            im.executeModality('TTS', answer)
            im.executeModality('TEXT', answer)
        
        
    def run_quiz(im, graph, person_uri, EX):
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

        graph.set((person_uri, EX.hasScore, Literal(score)))
        graph.set((person_uri, EX.hasWellbeingFeedback, Literal(score)))


    def run_reflex_test(im, graph, person_uri, EX):
        im.executeModality('TEXT', "Touch one of my hands as fast as you can!")

        total_time = 0.0
        for i in range(10):
            print('Test #%d: Press Enter to simulate touching the robot\'s hand...' % (i + 1))
            start_time = time.time()
            raw_input() # type: ignore

            im.simulate_hand_touch(left=False, value=1.0)
            im.simulate_hand_touch(left=True, value=1.0)

            reflex_time = time.time() - start_time
            print('Time for test #%d: %.3fs' % (i + 1, reflex_time))
            total_time += reflex_time

        avg_reflex_time = total_time / 10.0
        print('Average reflex time: %.3fs' % avg_reflex_time)

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

        graph.set((person_uri, EX.hasReflexTime, Literal(avg_reflex_time)))
        graph.set((person_uri, EX.hasReflexFeedback, Literal(reflex_score)))


    def run_memory_test(im, graph, person_uri, EX):
        for i in range(1, 6):
            im.ask('memory/image_memory_show_%d' % i, 1)
            time.sleep(3)

        correct_sequence = ['dolphin', 'horse', 'cat', 'dog', 'bear']
        user_answers = [unicode(im.ask('memory/text_memory_recall_%d' % i)) for i in range(1, 6)] # type: ignore

        memory_score = sum(1 for ua, correct in zip(user_answers, correct_sequence) if ua == correct)
        print('Memory test score: %d/5' % memory_score)

        feedback_map = {5: 'excellent_memory', 4: 'very_good_memory', 3: 'good_memory',
                        2: 'fair_memory', 1: 'poor_memory', 0: 'no_memory'}

        im.executeModality('TEXT', 'Your memory score is %d out of 5' % memory_score)
        im.executeModality('TTS', 'Your memory score is %d out of 5' % memory_score)
        time.sleep(1)

        graph.set((person_uri, EX.hasMemoryScore, Literal(memory_score)))
        graph.set((person_uri, EX.hasMemoryFeedback, Literal(feedback_map[memory_score])))



    EX = Namespace("http://example.org/robot_kb#")

    def person_uri_from_distance(d):
        return URIRef("http://example.org/robot_kb#person_%.2f" % d)

    graph = Graph()
    graph.bind("robot_kb", EX)
    try:
        graph.parse("../people_graph.ttl", format="turtle")
    except Exception:
        print("No previous graph found, starting fresh.")
        pass

    im.init()
    time.sleep(1)

    while True:
        front = raw_input('Enter sonar distance (each distance represents a person): ') # type: ignore
        try:
            front_val = float(front)
            break
        except ValueError:
            print("Invalid input. Please enter a valid numeric distance.")

    print('front:', front_val)

    person_uri = person_uri_from_distance(front_val)
    current_time = datetime.now().isoformat()

    last_seen = graph.value(person_uri, EX.lastInteractionDate)
    if last_seen:
        graph.set((person_uri, EX.previousInteractionDate, last_seen))

    graph.set((person_uri, EX.lastInteractionDate, Literal(current_time)))

    name_literal = graph.value(person_uri, EX.hasName)
    if name_literal:
        name = unicode(name_literal) # type: ignore
        im.executeModality('TEXT', 'Hello, %s, I remember you!' % name)
        im.executeModality('TTS', 'Hello, %s, I remember you!' % name)

        wellbeing_feedback = graph.value(person_uri, EX.hasWellbeingFeedback)
        reflex_feedback = graph.value(person_uri, EX.hasReflexFeedback)
        memory_feedback = graph.value(person_uri, EX.hasMemoryFeedback)
        
        # If last seen is more than 30 days ago, tell the user that is nice to see them again TODO

        if wellbeing_feedback in [Literal('score_poor'), Literal('score_fair')]:
            im.executeModality('TEXT', 'Last time, you reported not feeling great. Do you feel better today?')
            im.executeModality('TTS', 'Last time, you reported not feeling great. Do you feel better today?')
            
        elif wellbeing_feedback in [Literal('score_good'), Literal('score_very_good'), Literal('score_excellent')]:
            im.executeModality('TEXT', 'Great to see you again! Keep up the good wellbeing, %s!' % name)
            im.executeModality('TTS', 'Great to see you again! Keep up the good wellbeing, %s!' % name)

        if reflex_feedback in [Literal('poor_reflexes'), Literal('fair_reflexes')]:
            im.executeModality('TEXT', 'Your reflexes were a bit slow last time. Want to try again today?')
            im.executeModality('TTS', 'Your reflexes were a bit slow last time. Want to try again today?')

        if memory_feedback in [Literal('poor_memory'), Literal('no_memory'), Literal('fair_memory')]:
            im.executeModality('TEXT', 'Want to see if your memory has improved since last time?')
            im.executeModality('TTS', 'Want to see if your memory has improved since last time?')
    else:
        im.executeModality('TEXT', 'Hello visitor, I have never seen you. What is your name?')
        im.executeModality('TTS', 'Hello visitor, I have never seen you. What is your name?')
        #name = raw_input('Please enter your name: ') # type: ignore
        #im.simulate_human_say(name)
        name = im.speech_to_text()  # type: ignore
        im.executeModality('TEXT', 'Hi, %s, I will remember you next time.' % name)
        im.executeModality('TTS', 'Hi, %s, I will remember you next time.' % name)
        graph.add((person_uri, RDF.type, EX.Person))
        graph.add((person_uri, EX.hasName, Literal(name)))


    exit = False
    
    while not exit:
        
        im.executeModality('TEXT', 'Are you ready, %s? Select one of the options below!' % name)
        choice = im.ask('welcome')
        
        voice_command = im.speech_to_text()  # type: ignore
        
        if choice == 'quiz' or voice_command == 'quiz':
            run_quiz(im, graph, person_uri, EX)
        elif choice == 'reflexes_test':
            run_reflex_test(im, graph, person_uri, EX)
        elif choice == 'memory_test':
            run_memory_test(im, graph, person_uri, EX)
        elif choice == 'talk':
            run_talk(im)
        elif choice == 'exit':
            im.executeModality('TEXT', 'Goodbye, %s! See you next time!' % name)
            im.executeModality('TTS', 'Goodbye, %s! See you next time!' % name)
            exit = True

    graph.serialize(destination='../people_graph.ttl', format='turtle')
    im.init()


if __name__ == '__main__':
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)
    mws.run_interaction(interaction)


# Functions benchmark -> non legati al task, ma alle capacità del robot a prescindere (NON CAMBIANO MAI)
# Task benchmark -> applicazione specifica, valutazione degli achievement chiave del contesto specifico del robot (gamification) (cambiano in base al task)