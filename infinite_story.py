import json
from notopenai import NotOpenAI
from pprint import pprint
import requests
import os
from graphics import Canvas
from io import BytesIO
from PIL import Image, ImageTk
from openai import OpenAI
from openaikey import OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)
STORY_NAME = "original_small"


def get_valid_choice(scene_data):
    print_scene(scene_data)
    amt_choice = len(scene_data["choices"])

    choice = input("What do you choose? ")

    # if it is a number
    # if it is above 0
    # if it is equal to or below the length of choices
    while not choice.isdigit() or int(choice) - 1 < 0 or int(choice) - 1 >= amt_choice:
        choice = input("Please enter a valid choice: ")

    valid_idx = int(choice) - 1
    valid_scene = scene_data["choices"][valid_idx]

    return valid_scene


def print_scene(scene_data):
    text = scene_data["text"]
    print(text)
    scene_choices = scene_data["choices"]

    for idx, choice in enumerate(scene_choices):
        choice_text = choice["text"]
        print(f"{idx + 1}.{choice_text}")


def main():
    print("infinite story")
    story_data = json.load(open(f"data/{STORY_NAME}.json"))
    # print(story_data)
    starter_key = 'start'
    current_scene = story_data["scenes"][starter_key]

    while True:
        choice_scene = get_valid_choice(current_scene)
        choice_key = choice_scene["scene_key"]
        current_scene = story_data["scenes"][choice_key]



if __name__ == "__main__":
    main()
    