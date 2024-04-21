from UCLAHacks.templates import ThemeState, template

import reflex as rx
import pandas as pd
import json

import subprocess
import google.generativeai as genai
GOOGLE_API_KEY = "AIzaSyAFPS-aQ5MN58IEk5Y8sDmqbAtT7mRu3Hc"

class AIState(rx.State):
    def generate_program(self):
        workout_plan = self.Generate_Prompt()
        with open('../UCLAHacks/UCLAHacks/output.json', 'w') as f:
            json.dump(workout_plan, f, indent=4)
    
    def Generate_Prompt(self):
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

        system_instruction = "Personal Trainer Prompt:\n\nPerson: (Name:{name}\tBMI:{bmi} Shoulder/Hip Ratio: {shoulder_hip_ratio})\n\nWhat I need you to do is take the BMI and Shoulder/Hip Ratio of this person. With this information match the BMI to what types of workout should be given, match the Ratio to what the workout split for the week will be. The lists list what workout type should be given based off of the BMI. They also list what muscle groups should be focused based on the Shoulder/Hip Ratio. Based off this data create this 5-day workoutplan, include: exercises, sets, reps, rest time, rpe/%1rm for strength training. Return the workout plan in JSON structure. \nLike this: \n\"Day 3\": {\n      \"Muscle Groups\": \"Legs and Shoulders\",\n      \"Workout Type\": \"Cardio/Strength Focused\",\n      \"Exercises\": [\n        {\n          \"Exercise Name\": \"Back Squat\",\n          \"Sets\": 5,\n          \"Reps\": 5,\n          \"Rest Time\": \"3 minutes\",\n          \"Intensity\": \"85% 1RM\"\n        },\n\n\n\n"

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                    generation_config=generation_config,
                                    system_instruction=system_instruction,
                                    safety_settings=safety_settings)

        prompt_parts = [
        "muscle_groups = {\n  \"Ratio > 1.2\": \"Workout split = Back and Biceps/Chest and Triceps/Legs and Shoulders/Core \",\n  \"1.1 < Ratio < 1.2\": \"Workout split = Back/Shoulders and Arms/Legs/Chest and Core\",\n  \"Ratio < 1.1\": \"Workout split = Chest and Shoulders/Arms/Legs/Back\"\n}\n\nworkout_type = {\n  \"BMI > 25\": \"Cardio/Strength Focused\",\n  \"20 < BMI < 25\": \"Intense Workouts / Combination of Hypertrophy and Strength\",\n  \"BMI < 20\": \"Hypertrophy focused\"\n}",
        ]

        response = model.generate_content(prompt_parts)
        
        workout_plan = json.loads(response.text)
        # Write the JSON response to a file
        # with open('../UCLAHacks/UCLAHacks/output.json', 'w') as f:
        #     json.dump(workout_plan, f, indent=4)

        # print("JSON response has been written to output.json file.")
        print(workout_plan)
        
        return workout_plan

@template(route="/Program", title="Program")
def Program() -> rx.Component:
    # Read the workout plan from the output.json file
    with open('../UCLAHacks/UCLAHacks/output.json', 'r') as file:
        workout_plan_list = json.load(file)
    
    # List to store the components for each day's workout plan
    day_components = []
    
    # Convert the list of workout plans into DataFrames for each day
    for workout_plan in workout_plan_list:
        for day, details in workout_plan.items():
            exercises = details['Exercises']
            # Create a DataFrame for the exercises
            df = pd.DataFrame(exercises)
            # Create a table for the exercises
            table = rx.data_table(
                data=df,
                pagination=True,
                search=False,
                sort=True
            )
            # Construct the title for the table (day and muscle group)
            title = f"{day}: {details['Muscle Groups']}"
            # Construct the component for this day's workout plan
            day_component = rx.vstack(
                rx.heading(title, size="5", align="center"),
                table,
                spacing="5",
                style={"width": "100%"},
                align="center",
            )
            # Append the day component to the list
            day_components.append(day_component)
    
    # Return all the day components stacked vertically
    return rx.vstack(
        rx.heading("AI Program", size="6", align="center", style={"width": "100%"}),
        rx.button("Generate Program", color_scheme="blue", on_click=AIState.generate_program),
        *day_components,
        spacing="5",
        style={"width": "100%"},
        align="center",
    )
