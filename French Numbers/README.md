# FST implementation of French Numbers from 1 to 1000

In the French language, Arabic numerals that we use in everyday can be spelled out just like they can in English. For example, the numeral 175 is written as one hundred seventy five in English and cent soixante quinze in French.

French is interesting because they have a mixture of a decimal (base 10) and vegesimal (base 20) system, created by committee to placate two different regions of French that used different systems.

You may want to consult an online reference, such as https://www.udemy.com/blog/french-numbers-1-1000/.

• Between 70–79 and 90–99, French numbers use a vegesimal base sys- tem. For everything else, it is base 10.
• Numbers ending in 21, 31, 41, 51, 61, and 71 have an “and”. For example, 21 is vingt et un (“twenty and one”)
• Numbers larger than 100 are written as x hundred. For example, 600 becomes six cent (“six hundred”).
• To make things simpler, we’ll say that 80 is quatre vingt (without an “s”) and 200 is deux cent (also without an “s”). We also do not want hyphens between number parts (so 17 becomes dix sept and not dix-sept ).

Construct an fst in nltk that can translate any given Arabic numeral into its corresponding French string. For the sake of convenience, you will only be given integer input less than 1000.

# Morphology

 If you take a look at tests.py, you can see some of the words we’re going to working with: pack, ice, frolic, pace, ace, traffic, lilac, lick. Our goal is to be able to generate things like ”spruced” (from ”spruce+d”) and ”picnicking” (from ”picnic+ed”) using regular expressions (which are magically transformed into finite state machines2).
