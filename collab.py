import re
import requests
import sqlite3
import time

TELEGRAM_BOT_TOKEN = "<redacted>"
TELEGRAM_BOT_CHAT_ID = "<redacted>"

connection = sqlite3.connect("/root/collaborator.db")

cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS interactions (time_of_event TEXT, source_address TEXT, type_of_interaction TEXT, interaction_id TEXT)")
cursor.close() 

with open("/root/collaborator_output.txt") as input:
    for line in input:
        if 'containing interaction ID' in line:

            # print('[+]', 'Collaborator Interaction Detected')

            time_of_event = re.findall(': (.*) : Received ', line)[0]
            source_address = re.findall('from (.*) for', line)[0]
            type_of_interaction = re.findall('Received (.*) from', line)[0]
            interaction_id = re.findall('containing interaction IDs: (.*)', line)[0]

            # # Cleaning the output.. as it looks something like [81.134.100.21:61445] right now.
            # source_address = source_address.replace('[', '')
            # source_address = source_address.replace(']', '')
            # source_address = source_address.split(':')[0]

            # print('[ ]', "Time of Event:", time_of_event)
            # print('[ ]', 'Source Address:', source_address)
            # print('[ ]', 'Type of Interaction:', type_of_interaction)
            # print('[ ]', 'Interaction ID(s):', interaction_id)

            cursor = connection.cursor()
            rows = cursor.execute("SELECT * FROM interactions WHERE time_of_event = ? AND source_address = ? AND type_of_interaction = ? AND interaction_id = ?", (time_of_event, source_address, type_of_interaction, interaction_id)).fetchall()
            cursor.close() 

            if len(rows) == 0:

                print('[+]', 'Collaborator Interaction Detected')

                # print('[ ]', "Time of Event:", time_of_event)
                # print('[ ]', 'Source Address:', source_address)
                # print('[ ]', 'Type of Interaction:', type_of_interaction)
                # print('[ ]', 'Interaction ID(s):', interaction_id)

                cursor = connection.cursor()
                cursor.execute("INSERT INTO interactions (time_of_event, source_address, type_of_interaction, interaction_id) VALUES (?, ?, ?, ?)", (time_of_event, source_address, type_of_interaction, interaction_id))
                cursor.close() 

                url = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage'

                data = {
                    'chat_id': TELEGRAM_BOT_CHAT_ID,
                    'text': '*Collaborator Interaction Detected*' + '\n' + 
                            '*Time of Event:* ' + time_of_event + '\n' + 
                            '*Source Address:* ' + source_address + '\n' + 
                            '*Type of Interaction:* ' + type_of_interaction + '\n' + 
                            '*Interaction ID(s):* ' + interaction_id,
                    'parse_mode': 'Markdown'
                }

                x = requests.post(url, json = data)

                # print('[ ]', 'HTTP Status Code:', x.status_code)
                
                # In an attempt to stop spamming my phone!
                time.sleep(1)

# print("[ ]", "Total number of database rows changed:", connection.total_changes)
connection.commit()
