from __future__ import division
from collections import Counter
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
    actual[i] = l
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
    crf[i] = l
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
    lstm[i] = l
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
    yamcha[i] = l
    i += 1

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


if "predictions.txt" not in os.listdir("."):
    print "writing to file"
    f = open("predictions.txt", "w")
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

f = open("results.txt", "w")

for tag in tags:
    false_positives = 0
    true_positives = 0
    false_negatives = 0
    true_negatives = 0
    for i in xrange(10):
        actual_list = actual[i]
        predicted_list = maximal[i]
        for j in xrange(len(actual_list)):
            entity = actual_list[j]
            predicted = predicted_list[j]
            if entity == tag:
                if predicted == tag:
                    true_positives += 1
                else:
                    false_negatives += 1
            else:
                if predicted == tag:
                    false_positives += 1
                else:
                    true_negatives += 1

    accuracy = (true_positives + true_negatives)/(true_positives +
                                                  true_negatives +
                                                  false_positives +
                                                  false_negatives)
    precision = true_positives/(true_positives + false_positives)
    recall = true_positives/(true_positives + false_negatives)
    f_score = (2 * precision * recall)/(precision + recall)
    f.write("for tag:{}, accuracy:{}, precision:{}, recall:{}, f_score:{}".
            format(tag, accuracy, precision, recall, f_score))
    f.write("\n")

f.close()
