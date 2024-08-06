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

CLIENT = OpenAI(api_key=OPENAI_KEY)
STORY_NAME = "original_big"

canvas = Canvas(1024, 1224, "Infinte Story")

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


def print_scene(scene_data, scene_key):     
    text = scene_data["text"]       # key error
    print(text)
    show_illustration(scene_key)        
    scene_choices = scene_data["choices"]

    for idx, choice in enumerate(scene_choices):
        choice_text = choice["text"]
        print(f"{idx + 1}.{choice_text}")

def get_new_scene(scene_key, example_scene, plot):
    print("[Suspenseful music plays as the story continues...]")
    prompt = f"""
Return the next scene of a story for key [scene key]. 
An example scene should be formatted in json like this: [example scene]. 
The main plot line of the story is [plot].
"""    
    
    chat_completion = CLIENT.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="gpt-3.5-turbo", # the GPT model to use
        response_format={"type": "json_object"} # we want our response in json format,
    )

    response_str = chat_completion.choices[0].message.content
    new_scene_data = json.loads(response_str)

    return new_scene_data


def show_illustration(scene_key):
    illustration_path = f"img/{STORY_NAME}/{scene_key}.png"
    if os.path.exists(illustration_path):
        canvas.clear()
        canvas.create_image(0, 0, illustration_path)
    else:
        canvas.clear()
        canvas.create_rectangle(0, 0, 1024, 1224, "black")


def main():
    print("infinite story")
    story_data = json.load(open(f"data/{STORY_NAME}.json"))
    # print(story_data)
    starter_key = 'start'
    current_scene = story_data["scenes"][starter_key]

    while True:
        choice_scene = get_valid_choice(current_scene)      #?
        choice_key = choice_scene["scene_key"]

        if choice_key not in story_data["scenes"]:
            # Get new scene from openAI
            new_scene = get_new_scene(choice_key, story_data["scenes"]["start"], story_data["plot"])
            story_data["scenes"][choice_key] = new_scene



        current_scene = story_data["scenes"][choice_key]



if __name__ == "__main__":
    main()
    