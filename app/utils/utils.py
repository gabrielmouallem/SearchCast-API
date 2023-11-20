import hashlib


def generate_unique_id(my_dict):
    # Concatenate relevant attributes
    concatenated_string = f"{my_dict['text']}_{my_dict['start']}_{my_dict['duration']}_{my_dict['videoId']}"

    # Hash the concatenated string
    hashed_value = hashlib.md5(concatenated_string.encode()).hexdigest()

    return hashed_value
