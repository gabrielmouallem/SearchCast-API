import hashlib
import re
from typing import Any, List

def paginate(items: List[Any], page: int, per_page: int) -> List[Any]:
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    return items[start_index:end_index]


def generate_unique_id(my_dict):
    # Concatenate relevant attributes
    concatenated_string = f"{my_dict['text']}_{my_dict['start']}_{my_dict['duration']}_{my_dict.video['videoId']}"

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
