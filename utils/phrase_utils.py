from utils import wildcards
import hashlib
def init_PhraseSet(client, phrases, project_number, project_id, wildcards_config):
	wildcards_config = ["select_word", "move_word"]
	wildcard_terms =  sum([wildcards.wildcardsdict[wildcard] for wildcard in wildcards_config], [])
	phraseset_string = "-".join(["-".join(phrase.split(" ")) for phrase in sorted(phrases + wildcard_terms)]).lower()
	phraseset_id = str(int(hashlib.sha256(phraseset_string.encode()).hexdigest(), 16) % 10**8)
	print(phraseset_id)
	print(phraseset_string)

	try:
		response = client.get_phrase_set({"name": f"projects/{project_number}/locations/global/phraseSets/{phraseset_id}"})
		print("existing phrase set found, loading...")
		return response
	except Exception as e:
		if "404 Resource" in str(e):	
			print("creating new phrase set...")
			values = set()
			for phrase in sorted(phrases):
				split_phrase = phrase.split(" ")
				for word in range(len(split_phrase)):
					values.add(split_phrase[word])
					values.add(" ".join(split_phrase[:word + 1]))
			for term in wildcard_terms:
				values.add(term)

			print(values)
			json_phrases = [{"value": term} for term in values]
			client.create_phrase_set({
			    "parent": f"projects/{project_id}/locations/global",
			    "phrase_set_id": phraseset_id,
			    "phrase_set": {
			        "boost": 10,
			        "phrases": json_phrases,
			    }})
			return client.get_phrase_set({"name": f"projects/{project_number}/locations/global/phraseSets/{phraseset_id}"})