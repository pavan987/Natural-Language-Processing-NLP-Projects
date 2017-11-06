# Word Similarities

Implement cossim sparse(v1,v2) and cossim dense(v1,v2) in distsim.py to compute and display the cosine similarities between each pair of these words.

## Implement show nearest().

Given a dictionary of word-context vectors, the context vector of a particular query word w, the words you want to exclude in the responses (It should be the query word w in this question), and the similarity metric you want to use (it should be the cossim sparse function you just implemented), show nearest() finds the 10 words most similar to w. Display the similar words, and their similarity scores against the query word w.

## Implement n_best_accuracy

Use the file word-test.v3.txt to try your word2vec vectors out on eight different analogy tasks. The groups of relations are delimited by lines starting with a colon (:) and you should see these groups: capital, currency, city-in-state, family, adjective-to-adverb, comparative, superlative, and nationality-adjective.

For each of the eight relation groups, print the 1-best, 5-best, and 10-best accuracy of your vectors on the group. The n-best accuracy is the percentage of items for which the correct answer was in the top n vectors returned.
