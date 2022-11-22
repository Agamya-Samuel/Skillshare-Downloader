import os
import requests
from dotenv import load_dotenv


try:
    DL_LINKS_MASTER_MONGODB_URL = os.getenv('DL_LINKS_MASTER_MONGODB_URL')
    DL_LINKS_MASTER_MONGODB_DATABASE_NAME = os.getenv('DL_LINKS_MASTER_MONGODB_DATABASE_NAME')
    DL_LINKS_MASTER_MONGODB_COLLECTION_NAME = os.getenv('DL_LINKS_MASTER_MONGODB_COLLECTION_NAME')

    # Everything Else DB
    EVERYTHING_ELSE_MONGODB_URL = os.getenv('EVERYTHING_ELSE_MONGODB_URL')
    EVERYTHING_ELSE_MONGODB_DATABASE_NAME = os.getenv('EVERYTHING_ELSE_MONGODB_DATABASE_NAME')
    EVERYTHING_ELSE_MONGODB_COLLECTION_NAME = os.getenv('EVERYTHING_ELSE_MONGODB_COLLECTION_NAME')

    # Bot related
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    PIXELDRAIN_API = os.getenv('PIXELDRAIN_API')
    ANONFILE_TOKEN = os.getenv('ANONFILE_TOKEN')
    SKILLSHARE_COOKIE = os.getenv('SKILLSHARE_COOKIE')

    if (
            (len(DL_LINKS_MASTER_MONGODB_URL) != 0) and 
            (len(DL_LINKS_MASTER_MONGODB_DATABASE_NAME) != 0) and 
            (len(DL_LINKS_MASTER_MONGODB_COLLECTION_NAME) != 0) and
            
            # Everything Else DB
            (len(EVERYTHING_ELSE_MONGODB_URL) != 0) and
            (len(EVERYTHING_ELSE_MONGODB_DATABASE_NAME) != 0) and
            (len(EVERYTHING_ELSE_MONGODB_COLLECTION_NAME) != 0) and

            # Bot related
            (len(BOT_TOKEN) != 0) and
            (len(PIXELDRAIN_API) != 0) and
            (len(ANONFILE_TOKEN) != 0) and
            (len(SKILLSHARE_COOKIE) != 0)
        ):
        raise TypeError

    else:
        print("config vars loaded Successfully.")

except TypeError:
    
    try:
        CONFIG_FILE_URL = os.getenv('CONFIG_FILE_URL')
        config_res = requests.request("GET", CONFIG_FILE_URL)
        print(f"Fetching config.env from: {CONFIG_FILE_URL}")
        if config_res.status_code == 200:
            print("Nice, config.env downloaded Successfully!!")
            with open('config.env', 'wb+') as f:
                f.write(config_res.content)
            load_dotenv('config.env', override=True)
            DL_LINKS_MASTER_MONGODB_URL = os.getenv('DL_LINKS_MASTER_MONGODB_URL')
            DL_LINKS_MASTER_MONGODB_DATABASE_NAME = os.getenv('DL_LINKS_MASTER_MONGODB_DATABASE_NAME')
            DL_LINKS_MASTER_MONGODB_COLLECTION_NAME = os.getenv('DL_LINKS_MASTER_MONGODB_COLLECTION_NAME')

            # Everything Else DB
            EVERYTHING_ELSE_MONGODB_URL = os.getenv('EVERYTHING_ELSE_MONGODB_URL')
            EVERYTHING_ELSE_MONGODB_DATABASE_NAME = os.getenv('EVERYTHING_ELSE_MONGODB_DATABASE_NAME')
            EVERYTHING_ELSE_MONGODB_COLLECTION_NAME = os.getenv('EVERYTHING_ELSE_MONGODB_COLLECTION_NAME')
            
            # Bot related
            BOT_TOKEN = os.getenv('BOT_TOKEN')
            PIXELDRAIN_API = os.getenv('PIXELDRAIN_API')
            ANONFILE_TOKEN = os.getenv('ANONFILE_TOKEN')
            SKILLSHARE_COOKIE = os.getenv('SKILLSHARE_COOKIE')

        else:
            print(f"Failed to download config.env {config_res.status_code}")
            raise Exception
    
    except Exception as e:
        print(f"Error: {e}")
        
        try:
            load_dotenv('config.env', override=True)
            print("Loading config.env from local")
            DL_LINKS_MASTER_MONGODB_URL = os.getenv('DL_LINKS_MASTER_MONGODB_URL')
            DL_LINKS_MASTER_MONGODB_DATABASE_NAME = os.getenv('DL_LINKS_MASTER_MONGODB_DATABASE_NAME')
            DL_LINKS_MASTER_MONGODB_COLLECTION_NAME = os.getenv('DL_LINKS_MASTER_MONGODB_COLLECTION_NAME')

            # Everything Else DB
            EVERYTHING_ELSE_MONGODB_URL = os.getenv('EVERYTHING_ELSE_MONGODB_URL')
            EVERYTHING_ELSE_MONGODB_DATABASE_NAME = os.getenv('EVERYTHING_ELSE_MONGODB_DATABASE_NAME')
            EVERYTHING_ELSE_MONGODB_COLLECTION_NAME = os.getenv('EVERYTHING_ELSE_MONGODB_COLLECTION_NAME')

            # Bot related
            BOT_TOKEN = os.getenv('BOT_TOKEN')
            PIXELDRAIN_API = os.getenv('PIXELDRAIN_API')
            ANONFILE_TOKEN = os.getenv('ANONFILE_TOKEN')
            SKILLSHARE_COOKIE = os.getenv('SKILLSHARE_COOKIE')

        except:
            print("config.env not found in local")
print(f"{DL_LINKS_MASTER_MONGODB_URL = }")
print(f"{DL_LINKS_MASTER_MONGODB_DATABASE_NAME = }")
print(f"{DL_LINKS_MASTER_MONGODB_COLLECTION_NAME = }")

# Everything Else DB
print(f"{EVERYTHING_ELSE_MONGODB_URL = }")
print(f"{EVERYTHING_ELSE_MONGODB_DATABASE_NAME = }")
print(f"{EVERYTHING_ELSE_MONGODB_COLLECTION_NAME = }")

# Bot related
print(f'{BOT_TOKEN = }')
print(f'{PIXELDRAIN_API = }')
print(f'{ANONFILE_TOKEN = }')
print(f'{SKILLSHARE_COOKIE = }')