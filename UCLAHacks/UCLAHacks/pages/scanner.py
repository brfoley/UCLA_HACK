
from UCLAHacks.templates import template
import reflex as rx
import json
import csv

def button_style(selected):
    return {
        "padding": "10px 15px",
        "color": "white",
        "border-radius": "5px",
        "border": "none",
        "font-weight": "bold",
        "cursor": "pointer",
        "background-color": rx.cond(selected, "#007bff", "#0056b3")
    }

class InputState(rx.State):
    height: str = ""
    weight: str = ""
    age: str = ""
    image: bool = False
    sex: str = ""
    name: str = ""
    shoulderWidth = ""
    hipWidth = ""

    def update_height(self, value):
        self.height = value

    def update_weight(self, value):
        self.weight = value

    def update_age(self, value):
        self.age = value
    
    def male(self):
        self.sex = "Male"

    def female(self):
        self.sex = "Female"

    def update_image(self, file):
        self.image = file
    
    def updateName(self, value):
        self.name=value
    
    def updateShoulderWidth(self, value):
        self.shoulderWidth = value
    
    def updateHipWidth(self,value):
        self.hipWidth = value
    
    
    def convertToJson(self):
        
                # Initialize variables to store the values
        right_shoulder_x = None
        left_shoulder_x = None
        right_hip_x = None
        left_hip_x = None

        # Open the CSV file and read its contents
        with open('/Users/brandonfoley/Documents/UCLAHacks/UCLAHacks/data.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check the dataPoint and assign values accordingly
                if row['dataPoint'] == 'RightShoulder':
                    right_shoulder_x = int(row['x'])
                elif row['dataPoint'] == 'LeftShoulder':
                    left_shoulder_x = int(row['x'])
                elif row['dataPoint'] == 'RightHip':
                    right_hip_x = int(row['x'])
                elif row['dataPoint'] == 'LeftHip':
                    left_hip_x = int(row['x'])
                
        CmPerPixel = int(self.height)/350
        print("CM per pixels are: " + str(CmPerPixel))
        self.shoulderWidth = (left_shoulder_x-right_shoulder_x)*CmPerPixel
        print("The width of your shoulders is: " + str(self.shoulderWidth*CmPerPixel))
        self.hipWidth = (left_hip_x-right_hip_x)*CmPerPixel
        print("The width of your hips is: " + str(self.hipWidth*CmPerPixel))
        
        
        data = {
            "name": self.name,
            "weight": self.weight,
            "height": self.height,
            "age": self.age,
            "sex": self.sex,
            "shoulder_width": self.shoulderWidth,
            "hip_width": self.hipWidth,
            "bmi": float(int(self.weight) / (pow((int(self.height) / 100),2))),
            "shoulder_hip_ratio": (int(self.shoulderWidth)/int(self.hipWidth))
        }
        
        # Convert dictionary to JSON string
        json_string = json.dumps(data, indent=4)
        
        # Write JSON string to a file
        with open('/Users/brandonfoley/Documents/UCLAHacks/UCLAHacks/data.json', 'w') as json_file:
            json_file.write(json_string)
        


def measurements():
    return rx.vstack(
        rx.hstack(
            rx.text("Name (F/L): ", align="right", width="20%"),
            rx.text_area(placeholder="First Last", width="90%", on_change=InputState.update_height),
            spacing="3"
        ),
        
        rx.hstack(
            rx.text("Height (cm): ", align="right", width="20%"),
            rx.text_area(placeholder="e.g., 180", width="80%", on_change=InputState.update_height),
            spacing="3"
        ),
        
        rx.hstack(
            rx.text("Weight (kg): ", align="right", width="20%"),
            rx.text_area(placeholder="e.g., 75", width="80%", on_change=InputState.update_weight),
            spacing="3"
        ),
        
        rx.hstack(
            rx.text("Age (years): ", align="right", width="20%"),   
            rx.text_area(placeholder="e.g., 29", width="80%", on_change=InputState.update_age),
            spacing="3"
        ),
    )

def sex():
    return rx.flex(
        rx.button(
            rx.cond(InputState.sex == "Male", "Male - Selected", "Male"),
            style=button_style(InputState.sex == "Male"),
            on_click=InputState.male,
        ),
        rx.button(
            rx.cond(InputState.sex == "Female", "Female - Selected", "Female"),
            style={"background-color": rx.cond(InputState.sex == "Female", "#dc3545", "#c82333")},  # Similarly for the female button
            on_click=InputState.female,
        ),
        spacing="3",
    )

"""
def image_upload():
    return rx.fragment(
        rx.upload(rx.text("Upload files"), rx.icon(tag="upload")),
        rx.button(on_submit=InputState.image),
        spacing="3",
    )
"""

@template(route="/scanner", title="Scanner")
def scanner() -> rx.Component:
    """The scanner page.

    Returns:
        The UI for the scanner page.
    """

    sex_section = sex()
    measurements_section = measurements()
    #upload_section = image_upload()
    camera_button = rx.link("Open Camera", href="/camera", style={"padding": "10px 15px", "background-color": "blue", "color": "white", "text-decoration": "none", "border-radius": "5px"})

    return rx.vstack(
        rx.heading("Welcome to the Body Scanner", size="6", align="center"),
        rx.text("Please enter your measurements below:", align="center"),

        measurements_section,
        sex_section,
        #upload_section,
        camera_button,

        rx.button(
            "Submit",
            color_scheme="green",
            on_click=[InputState.convertToJson, rx.window_alert(f"Saving Data: Height - {InputState.height}, Weight - {InputState.weight}, Age - {InputState.age}, Sex - {InputState.sex}"), rx.redirect("/")]
        )
    )

