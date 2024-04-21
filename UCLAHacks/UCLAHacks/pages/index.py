"""The home page of the app."""

from UCLAHacks import styles
from UCLAHacks.templates import template
import reflex as rx

def introduction_text() -> rx.Component:
    """Component displaying introductory text about the system."""
    return rx.box(
        rx.text("Welcome to Your Personal Fitness Assistant!", size="6", align="center"),
        rx.text("We use advanced AI to analyze your body and provide customized workout plans.", align="center"),
        rx.text("Start by going to the Body Scanner to capture your body measurements.", align="center"),
        spacing="3",
        style={"width": "100%"},
        align="center"
    )


@template(route="/", title="Dashboard")
def index() -> rx.Component:
    return rx.vstack(
        rx.heading("Dashboard", size="6", align="center", style={"width": "100%"}),
        introduction_text(),
        spacing="5",
        style={"width": "100%"},
        align="center"
    )