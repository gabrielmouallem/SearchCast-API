import hashlib
import re
from typing import Any, List


def format_text_to_double_quotes(text: str):
    words = text.split()
    formatted_string = " ".join(['"{}"'.format(word) for word in words])
    return formatted_string


def generate_unique_id(my_dict):
    # Concatenate relevant attributes
    video = my_dict["video"]
    concatenated_string = (
        f"{my_dict['text']}_{my_dict['start']}_{my_dict['duration']}_{video['videoId']}"
    )

    # Hash the concatenated string
    hashed_value = hashlib.md5(concatenated_string.encode()).hexdigest()

    return hashed_value


def extract_video_id(url: str):
    # Define the regular expression pattern to extract the video ID
    pattern = re.compile(
        r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    )

    # Use the pattern to search for the video ID in the URL
    match = pattern.search(url)

    # If a match is found, return the video ID, otherwise return None
    if match:
        return match.group(1)
    else:
        return None
