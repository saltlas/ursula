""" all logic relating to matching command "wildcards" to concrete words.
for example, a user may say "rotate that" or "rotate this", but both are the same command"""


select_words = ["that", "this"]
put_words = ["there", "here"]
move_words = ["forward", "backward", "back"] + put_words
scale_words = ["up", "down"]
axes = ["x", "y", "z"]

wildcardsdict = {"select_word":select_words, "put_word":put_words, "move_word":move_words, "scale_word":scale_words, "axis_word":axes}