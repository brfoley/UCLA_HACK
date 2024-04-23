from UCLAHacks.templates import ThemeState, template

import reflex as rx
import pandas as pd
import json

import google.generativeai as genai
GOOGLE_API_KEY = "AIzaSyAFPS-aQ5MN58IEk5Y8sDmqbAtT7mRu3Hc"

class AIState(rx.State):
    is_program_loaded: bool = False
    
    def Generate_Prompt(self):
        self.is_program_loaded = False

        """
        At the command line, only need to run once to install the package via pip:

        $ pip install google-generativeai
        """

        from pathlib import Path

        genai.configure(api_key=GOOGLE_API_KEY)

        """
        At the command line, only need to run once to install the package via pip:

        $ pip install google-generativeai
        """

                
        # Set up the model
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        with open('../UCLAHacks/UCLAHacks/data.json', 'r') as file:
            data = json.load(file)
        
        system_instruction = "Personal Trainer Prompt:\n\nexample person: (Name:Harlan    BMI:24.6 ,Shoulder/Hip Ratio: 1.19, Goals:Weight loss, Experince: beginner, time availability:  4 says to workout, equipment access: weights 15-30lbs, problems: none )\n\nWhat I need you to do is take the goals, experience, time availability, equipment access, preferred exercise modularites, problems, BMI and Shoulder/Hip Ratio of this person. Goals should be used to determine the best way to approach the schedule. for typical goals, weightloss/cutting is supposed to have more cardio, bulking/muscle gain is more strength training, etc. Experince is used as a starting point of where to start the user. Time availability should be used to incorporate rest days.  Equipment access should lead to what types of exercises they can do along with the weights that they are able to use. With the preferred exercise modularites this determines what type of exercises should be preformed, however this may not always be possible due to the goals of the user. Problems should let us know things to avoid and types of exercises to avoid at the moment or permanently depending on the problem. BMI is up to your interpretation. Shoulder/Hip ratio tells us how in shape they are and the higher it is the more \"snatched\"  or skinny they are and for most women this is the goals and this is commonly associated with goals of weightloss/cutting as well. If the number is one or under this means the person is overweight and most likely needs to lose weight. With this information determine a good workout split for this person as well as what would fit their needs best. This plan should be progressible and to be able to fulfil their goals in the long run. Based off this data create this 7-day workoutplan, include: exercises, sets, reps, rest time, rpe/%1rm for strength training. If there is a rest day at any time in the workout plan instead of making all the fields blank, please fill them with empty strings, inside exercises please fill out one of each parts with empty strings. Return the workout plan in a JSON format. it should look like as follows:\n{\n  \"Day 1\": {\n    \"Focus\": \"Upper Body Push (Strength)\",\n    \"Exercises\": [\n      {\n        \"Name\": \"Barbell Bench Press\",\n        \"Sets\": 3,\n        \"Reps\": 8,\n        \"Rest\": \"2 minutes\",\n        \"Intensity\": \"75% 1RM\" \n      },\netc..."

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                    generation_config=generation_config,
                                    system_instruction=system_instruction,
                                    safety_settings=safety_settings)

        prompt_parts = [
        "BMI:{bmi} \nShoulder/hip ratio:{shoulder_hip_ratio}\ngoals:{goals} \nexperience:{experince}\ntime availability:{time} \nequipment access:{access} \npreferred exercise modularites:{preference} \nproblems: {problems}",
        ]

        response = model.generate_content(prompt_parts)
        print(response.text)
        
        workout_plan = json.loads(response.text)
        
        with open('../UCLAHacks/UCLAHacks/output.json', 'w') as f:
            json.dump(workout_plan, f, indent=4)
            
        self.is_program_loaded = True
        

@template(route="/Program", title="Program")
def Program() -> rx.Component:
    
    # Return all the day components stacked vertically
    return rx.vstack(
        rx.heading("AI Program", size="6", align="center", style={"width": "100%"}),
        rx.button("Generate Program", color_scheme="blue", on_click=AIState.Generate_Prompt),
        rx.text("Click generate program and wait around a minute for your custom workout plan!"),
        rx.cond(
            AIState.is_program_loaded,
            rx.button("Click here to see program", color_scheme="blue", on_click=rx.redirect("/Schedule"))
        ),
        # need to output workout plan here
        spacing="5",
        style={"width": "100%"},
        align="center",
    )