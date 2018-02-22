
fp = open("temp_predictions.txt").readlines()

fp2 = open("mod_predictions.txt").readlines()

for i in xrange(len(fp)):
    line_pred = fp2[i].strip()
    line_mod = fp[i].strip()
    if line_pred.startswith("for"):
        continue
    else:
        word_pred = line_pred.split("\t")
        word_mod = line_mod.split("\t")
        if word_mod[4] != word_pred[4]:
            print word_pred, word_mod
