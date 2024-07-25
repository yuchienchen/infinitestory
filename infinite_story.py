import json
from notopenai import NotOpenAI
from pprint import pprint
import requests
import os
from graphics import Canvas
from io import BytesIO
from PIL import Image, ImageTk

api_key_cs106a = "pineapple"
client = NotOpenAI(api_key="pineapple")

history = []
main_plot = "You are exploring a world. Almost every scene is normal, but if the hero explores enough of the normal parts (eg more than 10 scenes), they will slowly start to uncover the mysterious parts. Most of the tone is simply setting a beautiful and uplifting landscape filled with wonder."

canvas = Canvas(1024, 1224, "Infinte Story")

story_key = "original_big"
write_key = story_key
story_data = json.load(open(f'data/{story_key}.json'))

def main():
    current_scene = 'start'
    
    while True:
        next_scene = run_scene(current_scene, story_data)
        if next_scene is None:
            print("The end.")
            break
        else:
            current_scene = next_scene

def get_continuation():

    print("[Suspenseful music plays as the story continues...]")
    prompt = f"Return the next scene of a story. An example scene should be formatted in json this: f{story_data['start']}. The main plot line of the story is {main_plot}. Here is what has happened so far: {history}"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
    )
    json_response = chat_completion.choices[0].message.content
    return json.loads(json_response)
    

def run_scene(scene_key, story_data):
    if scene_key in story_data:
        scene_data = story_data[scene_key]
        return run_standard_scene(scene_data, scene_key)
    else:
        ai_scene = get_continuation()
        story_data[scene_key] = ai_scene
        json.dump(story_data, open(f'data/{write_key}.json', 'w'), indent=2)
        return run_standard_scene(ai_scene, scene_key)

    
def run_standard_scene(scene_data, scene_key):
    description = scene_data['text']

    print("")
    print(scene_data['text'])
    show_illustration(scene_key)

    history.append(f"scene_key:{scene_key}. summary: {scene_data['scene_summary']}")
    
    if 'choices' in scene_data:
        choices = scene_data['choices']
        for idx, choice in enumerate(choices):
            print(f"{idx+1}. {choice['text']}")
        
        selected_choice = get_choice(choices)
        next_scene_key = selected_choice['scene_key']
        choice_text = selected_choice['text']

        history.append(f"Hero: {choice_text}")
        return next_scene_key
    else:
        return None  
    
def show_illustration(scene_key):
    illustration_path = f"img/{story_key}/{scene_key}.png"
    if os.path.exists(illustration_path):
        canvas.clear()
        canvas.create_image(0, 0, illustration_path)
    else:
        canvas.clear()
        canvas.create_rectangle(0, 0, 1024, 1224, "black")
    
    
def get_choice(choices):
    choice = input("What do you choose? ")
    while not choice.isdigit() or int(choice) > len(choices):
        choice = input("Please enter a valid choice: ")
    if choice.isdigit():
        choice_index = int(choice) - 1
        selected_choice = choices[choice_index]
        return selected_choice



if __name__ == "__main__":
    main()
    