from bot.skillshare import (get_course_id, download_course_by_class_id)
from bot.db_handler import (Open_DB_Connection, is_duplicate, insert_document, find_document)
from bot.zipfiles import zip_folder
from bot.upload import upload_file
from bot.delete_data import delete

from bot import (DL_LINKS_MASTER_MONGODB_URL, DL_LINKS_MASTER_MONGODB_DATABASE_NAME, DL_LINKS_MASTER_MONGODB_COLLECTION_NAME)

import os

from telegram.ext import CommandHandler
from telegram.ext import Updater, MessageHandler, Filters

import logging

from telegram import Update
from telegram.ext import CallbackContext

from bot import (BOT_TOKEN)

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def this_function_does_everything(url, user_id):

    # Checks in DB if the Course_ID already exists or not
    with Open_DB_Connection(
        db_url=DL_LINKS_MASTER_MONGODB_URL,
        db_name=DL_LINKS_MASTER_MONGODB_DATABASE_NAME,
        db_collection_name=DL_LINKS_MASTER_MONGODB_COLLECTION_NAME
        ) as db:
        course_id = get_course_id(url = url)
        print(f'{course_id = }')
        collctn = db['collection']
        resp = is_duplicate(
            id = course_id,
            collection = collctn
            )
        print(f'{resp = }')
        
        # If Course_ID not found in DB, then Download the COURSE and add Links to the DB 
        if not resp:

            # Downloads the course, and saves in a Folder
            course_folder_path, course_title, teacher_name = download_course_by_class_id(course_id = course_id)
            
            
            # Zips the course Folder
            source_folder_path = os.path.join(course_folder_path, teacher_name)
            zip_fname = zip_folder(
                fname = course_id,
                archive_from = source_folder_path,
                archive_to = 'Skillshare'
                )
            print(f'{zip_fname = }')
            zip_file_path = os.path.join(course_folder_path, zip_fname)
            

            # Uploads the .Zip to respective File Servers
            anon_url, pd_url = upload_file(fpath=zip_file_path)


            # Deletes .Zip file and Course Folder from Local Disk
            # delete(fpath=zip_file_path, folder_path=course_folder_path)


            # Add the Downloaded Links to the DB
            insert_document(
                collection = collctn,
                id = course_id,
                url = url,
                name = course_title,
                user = user_id,
                anon = anon_url,
                pd = pd_url
                )
            

            # Returns Download Links to Callback functions
            return [anon_url, pd_url]


        # IF Course_ID already exists in the DB, just search the ID in DB and return back user the Downlaod Links
        else:
            cursor = find_document(
                collection = collctn,
                id = course_id
                )
            cursor = cursor[0]
            anon_url = cursor['anon']
            pd_url = cursor['pd']
            return [anon_url, pd_url]


# Callback functions
def start_callback(update, context):
    user_msg = context.args
    update.message.reply_text('Welcome to Skillshare DL Bot. Using this bot you can download Skillshare courses for Free !!!. Just send me any Skillshare course Link.')

def dl_callback(update, context):
    user_msg = context.args
    update.message.reply_text('Your Course is Downloading...')
    dl_link = str(update.message.text)
    user_id = update.effective_chat.id
    print(f'{user_id = }')

    # Replying back Download Links
    urls = this_function_does_everything(url=dl_link, user_id=user_id)
    msg = f'Anonfile Url = {urls[0]}\n'
    msg += f'Pixeldrain Url = {urls[1]}'
    update.message.reply_text(msg)
    

def dl_echo(update: Update, context: CallbackContext):
    user_msg = update.message.reply_text('Your Course is Downloading...')
    dl_link = str(update.message.text)
    user_id = update.effective_chat.id
    print(f'{user_id = }')
    
    # Replying back Download Links
    urls = this_function_does_everything(url=dl_link, user_id=user_id)
    msg = f'Anonfile Url = {urls[0]}\n'
    msg += f'Pixeldrain Url = {urls[1]}'
    update.message.reply_text(msg)


# Handlers
start_handler = CommandHandler('start', start_callback)
dl_handler = CommandHandler('dl', dl_callback)
dl_echo_handler = MessageHandler(Filters.text, dl_echo)


# adding Handlers to Dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(dl_handler)
dispatcher.add_handler(dl_echo_handler)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater.start_polling(drop_pending_updates=False)