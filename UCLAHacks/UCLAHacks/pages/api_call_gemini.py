import google.generativeai as genai
GOOGLE_API_KEY = "AIzaSyAFPS-aQ5MN58IEk5Y8sDmqbAtT7mRu3Hc"

def Generate_Prompt():

    """
    At the command line, only need to run once to install the package via pip:

    $ pip install google-generativeai
    """

    from pathlib import Path

    import google.generativeai as genai

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

    system_instruction = "Personal Trainer Prompt:\n\nexample person: (Name:Harlan\tBMI:30.5 Shoulder/Hip Ratio: 1.19)\n\nWhat I need you to do is take the BMI and Shoulder/Hip Ratio of this person. With this information match the BMI to what types of workout should be given, match the Ratio to what the workout split for the week will be. The lists list what workout type should be given based off of the BMI. They also list what muscle groups should be focused based on the Shoulder/Hip Ratio. Based off this data create this 5-day workoutplan, include: exercises, sets, reps, rest time, rpe/%1rm for strength training. Return the workout plan in JSON structure. \nLike this: \n\"Day 3\": {\n      \"Muscle Groups\": \"Legs and Shoulders\",\n      \"Workout Type\": \"Cardio/Strength Focused\",\n      \"Exercises\": [\n        {\n          \"Exercise Name\": \"Back Squat\",\n          \"Sets\": 5,\n          \"Reps\": 5,\n          \"Rest Time\": \"3 minutes\",\n          \"Intensity\": \"85% 1RM\"\n        },\n\n\n\n"

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                generation_config=generation_config,
                                system_instruction=system_instruction,
                                safety_settings=safety_settings)

    prompt_parts = [
    "muscle_groups = {\n  \"Ratio > 1.2\": \"Workout split = Back and Biceps/Chest and Triceps/Legs and Shoulders/Core \",\n  \"1.1 < Ratio < 1.2\": \"Workout split = Back/Shoulders and Arms/Legs/Chest and Core\",\n  \"Ratio < 1.1\": \"Workout split = Chest and Shoulders/Arms/Legs/Back\"\n}\n\nworkout_type = {\n  \"BMI > 25\": \"Cardio/Strength Focused\",\n  \"20 < BMI < 25\": \"Intense Workouts / Combination of Hypertrophy and Strength\",\n  \"BMI < 20\": \"Hypertrophy focused\"\n}",
    ]

    response = model.generate_content(prompt_parts)
    print(response.text)
        
Generate_Prompt()