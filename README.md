# Belief-Networks-Hidden-Markov-Models
Fall 2025 CS 362/562

Give an example of a word which was correctly spelled by the user, but which was incorrectly
“corrected” by the algorithm. Why did this happen?

- "yell" incorrectly corrected to lell. 'y' has a very low probability of starting the word off in training data aspell.txt. 'l' on the other hand has a much higher probablity due to the number of 'l' words in the aspell.txt.

Give an example of a word which was incorrectly spelled by the user, but which was still
incorrectly “corrected” by the algorithm. Why did this happen?
- "thier" incorrectly corrected to "thier" should be their. the emissions probablility favors self emissions and the algorithm saw them as pausible sequence and and left them as is.

Give an example of a word which was incorrectly spelled by the user, and was correctly corrected
by the algorithm. Why was this one correctly corrected, while the previous two were not?
How might the overall algorithm’s performance differ in the “real world” if that training dataset is
taken from real typos collected from the internet, versus synthetic typos (programmatically
generated)?
- "ths" incorrectly corrected to "the". transition from 'h' to 'e' has a high probability than 'h' to 's', and 'h' to 's' is an uncommon sequence which led to the correction.
- real life example for typos would be key adjecent typos when one accidentally hit and a key next to the one they intended. 