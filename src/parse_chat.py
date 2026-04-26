import sys
import regex as re
import json
from datetime import datetime

file_name = sys.argv[1]
## USARE WITH INVECE DI FILEHANLDER?
file_handler = open(file_name, mode = "r", encoding = "UTF-8")

# IGNORO LE PRIME DUE RIGHE
file_handler.readline()
file_handler.readline()


all_conversations = []
new_conversation = []

for line in file_handler:
	# TODO Cambiare check di inizio conversazione, se ci sono righe vuote si blocca
	if re.match(r"^.{1,3}\s\d{2}/\d{2}/\d{4}$", line):
		## NUOVA CONVERSAZIONE
		if len(new_conversation) > 0:
			all_conversations.append(new_conversation)
		new_conversation = []
		print(new_conversation)

	else:
		new_conversation.append(line)

# ULTIMA CONVERSAZIONE CHE POTREBBE NON FINIRE CON RIGA VUOTA
if len(new_conversation) > 0:
	all_conversations.append(new_conversation)

participants = set()

data = {
	"medium": "LINE",
	"participants": [],
	"interactions": []
}

msg_id = 0

for conversation in all_conversations:
	# msg_id = 0 # SE VUOI INIZIALIZZARE PER OGNI CONVERSAZIONE
	interaction_data = {
		"date": "",
		"time": "",
		"messages": []
	}
	# PROBLEMA : SE C'è MESSAGGIO CON SPAZIO VUOTO E NON TROVA UNA DATA SI BLOCCA
	date = conversation[0].split()[1].strip()

	interaction_data["date"] = date

	conv_data = conversation[1:]

	new_message = {
		"offset": 0,
		"user": "",
		"text": []
	}

	first_time = 0
	for line in conv_data:

		# NUOVO MESSAGGIO
		if re.match(r"^\d\d:\d\d\t.*", line):
			if len(new_message["text"]) > 0:
				if len(new_message["text"]) > 1:
					new_message["text"] = " ".join(new_message["text"])[1:-1]
				else:
					new_message["text"] = new_message["text"][0]

				new_message["id"] = msg_id
				msg_id += 1
				interaction_data["messages"].append(new_message)

			split_line = line.strip().split("\t")
			time = split_line[0]
			parsed_time = datetime.strptime(time, "%H:%M")
			if first_time == 0:
				first_time = parsed_time
				interaction_data["time"] = time

			person = split_line[1]
			participants.add(person)
			# participants.add(transform_into_anonymous(person))


			offset = (parsed_time-first_time).seconds // 60
			new_message = {
				"offset": f"{offset//60:02d}:{offset%60:02d}",
				"user": person,
				"text": [split_line[2].strip()]
			}
		else:
			new_message["text"].append(line.strip())

	if len(new_message["text"]) > 0:
		if len(new_message["text"]) > 1:
			new_message["text"] = " ".join(new_message["text"])[1:-1]
		else:
			new_message["text"] = new_message["text"][0]
		interaction_data["messages"].append(new_message)

	# interaction_data["time"] = first_time
	new_message["id"] = msg_id
	msg_id += 1
	data["interactions"].append(interaction_data)

data["participants"] = list(participants)

with open(sys.argv[2], "w", encoding="utf-8") as file_handler_output:
	print(json.dumps(data, indent=4, ensure_ascii=False), file=file_handler_output)