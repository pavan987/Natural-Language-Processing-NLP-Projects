import distsim
def n_best_accuracy(n, strings):
    total = len(strings)
    count = 0
    for line in strings:
        items = line.strip().split(" ")
        w1=word_to_vec_dict[items[0].strip()]
        w2=word_to_vec_dict[items[1].strip()]
        w3=items[2].strip()
        w4=word_to_vec_dict[items[3].strip()]
        ret = distsim.show_nearest(word_to_vec_dict,
                            w1-w2+w4,
                            set([items[0].strip(), items[1].strip(), items[3].strip()]),
                            distsim.cossim_dense)
        for i in range(n):
            if w3 == ret[i][0]:
                count+=1
                break
    return count*100.0/total


lines = open("word-test.v3.txt").readlines()
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")

groups = {}
groupname = ""
for line in lines:
    if ":" in line:
        groupname = line[2:].strip()
    else:
        if groupname != "":
            if groupname in groups:
                groups[groupname].append(line)
            else:
                groups[groupname]=[line]

for groupname in groups:
    print groupname
    print "1-best - ", n_best_accuracy(1, groups[groupname])
    print "5-best - ", n_best_accuracy(5, groups[groupname])
    print "10-best - ", n_best_accuracy(10, groups[groupname])
