import sys
import json
import spacy
import pathlib
# from spacy_conll import init_parser

## AGGIUNTO ALTRIMENTI PRODUCEVA UN FILE IN UTF-16 LE CHE NON RISULTAVA LEGGIBILE
sys.stdout.reconfigure(encoding='utf-8')

# nlp = init_parser("ja",
#                 "udpipe",
# 				include_headers=True)

nlp = spacy.load("ja_core_news_sm")

file_input = pathlib.Path(sys.argv[1])
## AGGIUNTO PERCHé data = json.load(sys.argv[1]) NON FUNZIONAVA
with open(file_input, "r", encoding="utf-8") as f:
	data = json.load(f)


conversazioni = data["interactions"]

## AGGIUNTO ALTRIMENTI PRODUCEVA UN FILE IN UTF-16 LE CHE NON RISULTAVA LEGGIBILE
with open("prova_annotation.conllu", "w", encoding="utf-8") as out:
	for conv in conversazioni:
		orig_filename = f"{file_input.stem}.{conv['date'].replace('/','.')}"
		for message in conv["messages"]:

			## TODO: qui ci vuole una funzione che decide se quel messaggio è da parsare o meno.
			## Es. "[Messaggio Vocale]" non è da parsare, "[Sticker]" nemmeno...
			## TODO: gestire spazi speciali

			doc = nlp(message["text"])

			for sent_i, sent in enumerate(doc.sents):

				## USATO OUT.WRITE INVECE DI PRINT ALTRIMENTI STAMPAVA SUL TERMINALE
				out.write(f"# sent_id = {orig_filename}_{message['id']}_{sent_i}\n")
				out.write(f"# text = {sent.text}\n")
				for token in sent :
					head_id = token.head.i+1
					deprel = token.dep_
					tok_id = token.i+1

					morph = str(token.morph)
					if len(morph.strip()) == 0:
						morph = "_"
					if head_id == tok_id:
						head_id = 0
						deprel = 'root'
					out.write(f"{token.i+1}\t{token.text}\t{token.lemma_}\t{token.pos_}\t{token.tag_}\t_\t{head_id}\t{deprel}\t_\t{morph}\n")

				out.write(f"\n")