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

def main():
    print("infinite story")
    story_data = json.load(open(f"data/{STORY_NAME}.json"))
    print(story_data)



if __name__ == "__main__":
    main()
    