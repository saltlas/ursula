""" all logic relating to matching command "wildcards" to concrete words.
for example, a user may say "rotate that" or "rotate this", but both are the same command"""


select_words = ["that", "this"]
move_words = ["there", "here"]

wildcardsdict = {"select_word":select_words, "move_word":move_words}