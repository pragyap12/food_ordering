from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from watson_developer_cloud import ConversationV1
# from flask import Flask, render_template, request, send_from_directory
import json
import sqlite3

# app = Flask(__name__)
# print('hey')

context = None
user_contact_num = None


# print('hey1')


def error_callback(error):
    print(error)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    print('Received /start command')

    update.message.reply_text('Hey!Welcome to hotel bhuvan')


def help(bot, update):
    print('Received /help command')
    update.message.reply_text('Help!')


def message(bot, update):
    print('Received an update')
    global context

    conversation = ConversationV1(username='ad3b47a3-f07b-4d4e-98c1-0df7f02bfa68',  # TODO
                                  password='3aamChI0W1HU',  # TODO
                                  version='2018-02-16')

    print(conversation)
    print(type(context))
    print(context)

    print('hello' + update.message.text)

    # get response from watson
    response = conversation.message(
        workspace_id='d3c60545-4cd6-48d6-a853-ad2de1682988',  # TODO
        input={'text': update.message.text},
        context=context)
    # print('hello thw response is ::::::::::::::::;', response)
    s = 0

    num_intents = len(response['intents'])
    num_entities = len(response['entities'])

    if num_intents != 0  and response['intents'][0]['intent'] == 'get_menu':
        s = 1
        conn = sqlite3.connect('test1.db')
        c = conn.cursor()
        c.execute("SELECT * FROM menu")
        rows = c.fetchall()

        for row in rows:
            update.message.reply_text("Item: " + row[0] + "\t Price:" + str(row[1]))
        update.message.reply_text("select from above list only")
        conn.commit()
        conn.close()

    #if len(response['entities']) > 0 and response['entities'][0]['entity'] == 'sys-number':
        #if num_entities > 0:
            #user_contact_num = response['entities'][0]['value']
	     


    #if len(response['entities']) != 0  and response['entities'][0]['entity'] == 'sys-number':
     #   update.message.reply_text("Thank you")
    #print(json.dumps(response, indent=2))
    context = response['context']

    # c.execute("INSERT INTO address(address,pincode) VALUES(?,?)")
    # c.execute("SELECT * FROM address")
    # rows=c.fetchall()
    # for row in rows:
    # update.message.reply_text("Address: " + row[0] + "\t Pincode:" + str(row[1])

    # print(json.dumps(response, indent=2))

    # build response
    resp = ''
    for text in response['output']['text']:
        resp += text
    if s != 1:
        update.message.reply_text(resp)

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('586086802:AAGiRCLByS5JawrB1ER9WTtF6zcCYEjuhLM')  # TODO

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, message))

    dp.add_error_handler(error_callback)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
