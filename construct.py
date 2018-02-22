# coding=utf-8
wordVectors = {}
with open("./wordvectors.txt") as f:
    for line in f:
        words = line.split(" ")
        wordVectors[words[0]] = words[1:-1]
print wordVectors["వీరు"]
