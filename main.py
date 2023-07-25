from balaboba import Balaboba

bb = Balaboba()
text_types = bb.get_text_types(language="ru")

balaboba_style = 0

text_for_generation = "Понятие общества в современном мире выглядит "

text_after_generation = bb.balaboba(text_for_generation, text_type=text_types[balaboba_style])

print(text_after_generation)