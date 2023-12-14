import os
from dotenv import load_dotenv


def setup():
    load_dotenv(dotenv_path=".env", verbose=True, override=True)

    env = os.environ.get("FLASK_ENV", "development")
    print(f"\n * API env: {env.upper()}\n")
    if env != "production":
        dotenv_path = f".env.{env}"
        load_dotenv(dotenv_path=dotenv_path, verbose=True, override=True)
    return env
