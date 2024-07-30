from enum import Enum
import hashlib
from pymongo import ASCENDING, DESCENDING
import re


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


def get_proper_user_data(user):
    new_user_data = {**user}
    if "password" in new_user_data:
        del new_user_data["password"]
    if "subscription" in user:
        plan = "month"
        interval = new_user_data["subscription"]["plan"]["interval"]
        interval_count = new_user_data["subscription"]["plan"]["interval_count"]

        if interval == "year":
            plan = "year"
        if interval == "month":
            if interval_count == 6:
                plan = "semester"

        return {
            **new_user_data,
            "subscription": {
                "current_period_end": new_user_data["subscription"][
                    "current_period_end"
                ],
                "cancel_at": new_user_data["subscription"]["cancel_at"],
                "plan": plan,
            },
        }
    return new_user_data


class OrderByOptions(Enum):
    PUBLISH_DATE_ASC = "video.publishDate.asc"
    PUBLISH_DATE_DESC = "video.publishDate.desc"
    VIEW_COUNT_ASC = "video.viewCount.asc"
    VIEW_COUNT_DESC = "video.viewCount.desc"


# Define the allowed order-by options using the enum directly
ALLOWED_ORDER_BY_OPTIONS = set(OrderByOptions)


def sanitize_and_convert_order_by(order_by_str):
    # Sanitize the input
    try:
        order_by_option = OrderByOptions(order_by_str)
    except ValueError:
        order_by_option = OrderByOptions.PUBLISH_DATE_ASC

    # Convert to pymongo format
    field, order = order_by_option.value.rsplit(".", 1)
    pymongo_order = ASCENDING if order == "asc" else DESCENDING

    return {field: pymongo_order}
