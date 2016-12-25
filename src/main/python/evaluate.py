import os

os.chdir("target")

def evaluate(resultFileName):
    file = open(resultFileName, "r", encoding = "utf-8")
    result = file.read()
    file.close()

    lines = result.split('\n')
    predictPositive = 0
    positive = 0
    truePositive = 0
    for line in lines:
        words = line.split("\t")
        if (len(words) == 7):
            if (words[5] != "OTHER"):
                if (words[5] == words[6]):
                    truePositive += 1
                positive += 1
            if (words[6] != "OTHER"):
                predictPositive += 1

    recall = truePositive / positive
    precision = truePositive / predictPositive
    f1 = (2 * precision * recall) / (precision + recall)
    return precision, recall, f1


def main(args):
    precision, recall, f1 = evaluate("result")
    import datetime
    dateStr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log = "precision: %.5f\nrecall:%.5f\nf1 score:%.5f\n"% (precision, recall, f1)
    log = "\n".join(["\n", dateStr, log])
    logFile = open("log", "a")
    logFile.write(log)
    logFile.close()
    print(log)
    return 0

main("result")
