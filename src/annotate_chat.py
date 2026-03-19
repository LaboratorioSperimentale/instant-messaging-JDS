import sys
import json
import spacy

## AGGIUNTO ALTRIMENTI PRODUCEVA UN FILE IN UTF-16 LE CHE NON RISULTAVA LEGGIBILE
sys.stdout.reconfigure(encoding='utf-8')

nlp = spacy.load("ja_core_news_trf")

## AGGIUNTO PERCHé data = json.load(sys.argv[1]) NON FUNZIONAVA
with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = json.load(f)

conversazioni = data["interactions"]

## AGGIUNTO ALTRIMENTI PRODUCEVA UN FILE IN UTF-16 LE CHE NON RISULTAVA LEGGIBILE
with open("prova_annotation.txt", "w", encoding="utf-8") as out:
	for conv in conversazioni:
		for message in conv["messages"]:
			doc = nlp(message["text"])

			## USATO OUT.WRITE INVECE DI PRINT ALTRIMENTI STAMPAVA SUL TERMINALE
			out.write(doc.text + "\n")
			for token in doc :
				out.write(f"{token.text} {token.pos_} {token.dep_}\n")