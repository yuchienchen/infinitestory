import json

STORY_NAME = "original_small"

def main():
    print("infinite story")
    filename = "data/original_small.json"
    story_data = json.load(open(filename))
    # print(story_data.keys())
    scenes = story_data["scenes"]
    valid_keys = list(scenes.keys())
    print(valid_keys)

    for valid_key in valid_keys:
        scene_dict = scenes[valid_key]
        choices = scene_dict["choices"] 
        print(choices)



if __name__ == "__main__":
    main()