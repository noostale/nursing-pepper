# -*- coding: utf-8 -*-

from modim.ws_client import ModimWSClient
from modim.interaction_manager import InteractionManager as im


# Virtual TTS code to be added so that you can hear a voice 
# even in simulated environment
"""
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
engine.setProperty('voice', 'us1')
engine.say("Hello, Marco. How are you today?")
engine.runAndWait()
"""

# Ideas:
# HRI
# 1. human reflexes test: speed with which the human can react to a a red light into screen and toch the robot's hand
# 2. human memory test: show a sequence of 5 images + text and ask the human to repeat them in the same order
# 3. if scored poorly, play a simple game with the human
# HRB
# 1. Add a quantitative computation and save the score of the human reflexes test
# 2. Add a quantitative computation and save the score of the human memory test
# 3. Add a quantitative computation and save the score of the simple game
# 4. Add a final human User Satisfaction questionnaire (1-5) on Ease of use, Naturalness of the robot’s speech/gestures and overall enjoyment
# 5. Other metrics: total time of the interaction

def interaction():
    import csv
    import time

    # Load CSV into a lookup dict (float key: string value)
    people = {}
    with open('database.csv', 'rb') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if len(row) >= 2:
                try:
                    people[float(row[0])] = row[1]
                except:
                    continue

    # Initialize the interaction manager
    im.init()

    # Simulate sonar input
    front = raw_input('Enter sonar distance (In this demo, each distance is a person): ')
    try:
        front_val = float(front)
    except ValueError:
        print("Invalid input for distance.")

    print('front:', front_val)

    # Simulate hand greeting the user
    im.greet_user_animation()


    if front_val in people:
        name = people[front_val]
        im.executeModality('TTS', 'Hello, %s, I remember you' % name)
    else:
        im.executeModality('TTS', 'Hello, visitor, I have never seen you, tell me your name')
        name = raw_input('Please enter your name (Will be speeched to the robot): ')
        
        im.simulate_human_say(name)
        im.executeModality('TTS', 'Hi, %s, I will remember you next time' % name)

    # Continue with the rest of the interaction
    choice = im.ask('welcome')
    
    if choice == "quiz":
        answers = [im.ask("questions/question%d" % i) for i in range(1, 8)]

        # Print all answers
        print(tuple(answers))
        
        option_score_mapping = {
            # question1 - 5 options
            "poor": 1,
            "fair": 2,
            "good": 3,
            "very_good": 4,
            "excellent": 5,

            # question2 - 4 options
            "very_much": 1,
            "moderately": 2,
            "a_little": 3,
            "not_at_all": 4,

            # question3 - 4 options
            "severe": 1,
            "moderate": 2,
            "slight": 3,
            "none": 4,

            # question4 - 5 options
            "never": 1,
            "rarely": 2,
            "sometimes": 3,
            "often": 4,
            "always": 5,

            # question5 - 4 options
            "unable": 1,
            "a_lot_of_difficulty": 2,
            "some_difficulty": 3,
            "no_difficulty": 4,

            # question6 - 4 options
            "never": 1,
            "rarely": 2,
            "sometimes": 3,
            "yes_regularly": 4,

            # question7 - 4 options
            "extremely": 1,
            "quite_a_bit": 2,
            "a_little": 3,
            "not_at_all": 4,

            # question8 - 5 options
            "never": 1,
            "rarely": 2,
            "sometimes": 3,
            "often": 4,
            "always": 5,
        }
        
        # Calculate the score
        score = 0
        for answer in answers:
            score += option_score_mapping[answer]

        
        # Print the score
        print("Total score: %d" % score)
        
        def classify_wellbeing(total_score):
            if total_score <= 12:
                return "score_poor"
            elif total_score <= 18:
                return "score_fair"
            elif total_score <= 24:
                return "score_good"
            elif total_score <= 30:
                return "score_very_good"
            else:
                return "score_excellent"
        
        # Classify the wellbeing based on the score
        wellbeing = classify_wellbeing(score)
        print("Wellbeing classification: %s" % wellbeing)
        
        # Execute the modality for the wellbeing classification
        im.execute(wellbeing)
        
        # add in the column "score" the result of the score
        with open('database.csv', 'ab') as f:
            writer = csv.writer(f)
            writer.writerow([front_val, name, score])
    if choice == "reflexes_test":
        
        im.ask("reflexes_test", 1)
        

        start_time = time.time()
        
        # Simulate the robot's hand touch (for idea 1, to implement the reflexes test)
        raw_input('Press Enter to simulate touching the robot\'s hand...')
        im.simulate_hand_touch(left=False, value=1.0)
        im.simulate_hand_touch(left=True, value=1.0)
        
        final_time = time.time() - start_time
        
        print("Time to toch my hand: %f" % final_time)
        
                


    im.init()


if __name__ == "__main__":
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)
    mws.run_interaction(interaction)
