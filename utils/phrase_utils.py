"""utility module for managing google cloud speech to text api PhraseSet generation/loading.
PhraseSets will bias the speech to text model towards certain words, e.g. "move" rather than "moose", which improves accuracy and speed.
phrases and wildcards to bias towards are specified in config.json
"""

from utils import wildcards
import hashlib

def init_PhraseSet(client, phrases, project_number, project_id, wildcards_config):

	# get a list of all relevant wildcard words
	wildcard_terms =  sum([wildcards.wildcardsdict[wildcard] for wildcard in wildcards_config], [])

	# generating a phraseset-specific string of all relevant terms as a way to tell whether two phrasesets are identical
	phraseset_string = "-".join(["-".join(phrase.split(" ")) for phrase in sorted(phrases + wildcard_terms)]).lower()

	# hashing that string into a shorter but still unique ID
	phraseset_id = str(int(hashlib.sha256(phraseset_string.encode()).hexdigest(), 16) % 10**8)
	print(phraseset_id) # debug
	print(phraseset_string) # debug

	try:
		# if we've already created this phraseset before, it'll be loaded and we don't need to create a new one
		response = client.get_phrase_set({"name": f"projects/{project_number}/locations/global/phraseSets/{phraseset_id}"})
		print("existing phrase set found, loading...")
		return response

	except Exception as e:
		# google cloud will raise an error if we try to load from a location that doesn't exist
		# meaning a phraseset with this ID doesn't exist and we need to create one
		if "404 Resource" in str(e):	
			print("creating new phrase set...")
			values = set()

			for phrase in sorted(phrases):
				split_phrase = phrase.split(" ")

				# we add individual words in the phrase as well as the phrase itself
				# e.g. "rotate", "that", "rotate that"
				for word in range(len(split_phrase)):
					values.add(split_phrase[word])
					values.add(" ".join(split_phrase[:word + 1]))
			# adding wildcard words
			for term in wildcard_terms:
				values.add(term)

			print(values) # debug

			# creating the new phraseset
			json_phrases = [{"value": term} for term in values]
			client.create_phrase_set({
			    "parent": f"projects/{project_id}/locations/global",
			    "phrase_set_id": phraseset_id,
			    "phrase_set": {
			        "boost": 10,
			        "phrases": json_phrases,
			    }})
			return client.get_phrase_set({"name": f"projects/{project_number}/locations/global/phraseSets/{phraseset_id}"})