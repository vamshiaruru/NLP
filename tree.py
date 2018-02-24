from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support as score


mapping = {"LOC": 0,
           "MISC": 1,
           "O": 2,
           "ORG": 3,
           "PERSON": 4}

reverse_mapping = {0: "LOC",
                   1: "MISC",
                   2: "O",
                   3: "ORG",
                   4: "PERSON"}

with open("DT_data.txt") as fp:
    input_data = []
    output_data = []
    for line in fp:
        words = line.strip().split(" ")
        words = [mapping[word] for word in words]
        input_data.append(words[:3])
        output_data.append(words[3])


input_train, input_test, output_train, output_test = train_test_split(
        input_data, output_data, test_size=0.2, train_size=0.8)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(input_train, output_train)
output = clf.predict(input_test)
precision, recall, fscore, support = score(output_test, output)
fp = open("decision_tree_results.txt", "w")
for i in xrange(5):
    fp.write("for tag:{}, precision is {}, recall is {}, fscore is {}\n".format(
        reverse_mapping[i], precision[i], recall[i], fscore[i]))
fp.close()
