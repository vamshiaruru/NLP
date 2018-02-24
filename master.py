from __future__ import division
from collections import Counter
from sklearn.metrics import precision_recall_fscore_support as score
import os


i = 0
actual = {}
for filename in sorted(os.listdir("./actual")):
    l = []
    with open("./actual/"+filename, "r") as f:
        for line in f:
            words = line.strip().split(" ")
            if len(words) != 1:
                l.append(words[2].strip())
    lo = []
    for tag in l:
        if tag == "O":
            lo.append(tag)
        else:
            lo.append(tag[2:])
    actual[i] = lo
    i += 1

i = 0
crf = {}
for filename in sorted(os.listdir("./CRF++")):
    l = []
    with open("./CRF++/"+filename, "r") as f:
        for line in f:
            words = line.strip().split("\t")
            if len(words) != 1:
                l.append(words[3].strip())
    lo = []
    for tag in l:
        if tag == "O":
            lo.append(tag)
        else:
            lo.append(tag[2:])
    crf[i] = lo
    i += 1

i = 0
lstm = {}
for filename in sorted(os.listdir("./LSTM CRF")):
    l = []
    with open("./LSTM CRF/"+filename, "r") as f:
        for line in f:
            words = line.strip().split(" ")
            if len(words) != 1:
                l.append(words[2].strip())
    lo = []
    for tag in l:
        if tag == "O":
            lo.append(tag)
        else:
            lo.append(tag[2:])
    lstm[i] = lo
    i += 1

i = 0
yamcha = {}
for filename in sorted(os.listdir("./YamCha")):
    l = []
    with open("./YamCha/"+filename, "r") as f:
        for line in f:
            line = str(line).strip()
            words = line.split("\t")
            if len(words) != 1:
                l.append(words[3].strip())
    lo = []
    for tag in l:
        if tag == "O":
            lo.append(tag)
        else:
            lo.append(tag[2:])
    yamcha[i] = lo
    i += 1

if "DT_data.txt" not in os.listdir("."):
    with open("DT_data.txt", "w") as fp:
        for i in xrange(10):
            a_list = actual[i]
            y_list = yamcha[i]
            l_list = lstm[i]
            c_list = crf[i]
            for j in xrange(len(a_list)):
                fp.write(c_list[j]+" "+y_list[j]+" "+l_list[j]+" "+a_list[j]+"\n")

maximal = {}
for i in xrange(10):
    l = []
    lstm_list = lstm[i]
    yamcha_list = yamcha[i]
    crf_list = crf[i]
    combined = zip(lstm_list, yamcha_list, crf_list)
    for j in combined:
        d = dict(Counter(j))
        key = d.values().index(max(d.values()))
        l.append(d.keys()[key])
    maximal[i] = l
    i += 1

tags = set()

for i in xrange(10):
    tags = tags.union(actual[i])


if "mod_predictions.txt" not in os.listdir("."):
    print "writing to file"
    f = open("mod_predictions.txt", "w")
    for j in xrange(10):
        f.write("for file {}: \n".format(j))
        for i in xrange(len(actual[j])):
            f.write(actual[j][i]+"\t"+maximal[j][i])
            if actual[j][i] == maximal[j][i]:
                f.write("\t\t\t true prediction")
            else:
                f.write("\t\t\t false prediction")
            f.write("\n")
    f.close()
output_data = []
actual_data = []
for i in xrange(10):
    output_data = output_data + maximal[i]
    actual_data = actual_data + actual[i]
precision, recall, fscore, support = score(output_data, actual_data)
tags = sorted(list(tags))
fp = open("simple_ensemble_results.txt", "w")
for i in xrange(len(tags)):
    fp.write("for the tag {}, precision {}, recall {}, fscore {}\n".format(
        tags[i], precision[i], recall[i], fscore[i]))
fp.close()