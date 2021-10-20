active = {"indicative":("present", "imperfect", "future", "perfect", "pluperfect", "future perfect"),
          "subjunctive":("present", "imperfect", "perfect", "pluperfect"),
          "imperative":("present", "future"),
          "infinitive":("present", "future", "perfect")}

persons = ("1st", "2nd", "3rd")
numbers = ("singular", "plural")

for x in range(2):
    if x == 0:
        voice = "active"
    else:
        voice = "passive"
    for mood in active.keys():
        tenses = active[mood]
        for tense in tenses:
            for number in numbers:
                for person in persons:
                    print(f"{voice}, {mood}, {tense}, {person} person {number}")
