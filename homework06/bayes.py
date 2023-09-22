from collections import defaultdict
from math import log

class NaiveBayesClassifier:

    def __init__(self, alpha = 1, tp = ['ham', 'spam']):
        self.classifier = defaultdict(lambda:0)
        self.d = 0
        self.alpha = alpha
        self.pPos = 0.5
        self.pNeg = 0.5
        self.tp = tp #type name [pos, neg]
        pass

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.classifier
        for i in range (len(X)):
            temp = X[i].split(' ')
            for j in temp:
                if(self.classifier[j, self.tp[0]] == 0 and self.classifier[j, self.tp[1]] == 0):
                    self.d += 1
                self.classifier['*', y[i]] += 1
                self.classifier[j, y[i]] += 1
        
        nPositive = self.classifier['*', self.tp[0]]
        nNegative = self.classifier['*', self.tp[1]]

        lst = list(self.classifier)
        for i in range(0, len(lst), 2):
            temp = lst[i][0]
            if temp != '*':
                self.classifier[temp, 'pPos'] = (self.classifier[temp, self.tp[0]] + self.alpha)/(self.classifier['*', self.tp[0]] + self.d * self.alpha)
                self.classifier[temp, 'pNeg'] = (self.classifier[temp, self.tp[1]] + self.alpha)/(self.classifier['*', self.tp[1]] + self.d * self.alpha)
        
        self.classifier = self.classifier
        pass

    def predict(self, X):
        sumP_pos = self.pPos
        sumP_neg = self.pNeg
        for j in X:
            pPos = self.classifier[j, 'pPos']
            pNeg = self.classifier[j, 'pNeg']
            if(pPos != 0):
                sumP_pos += log(pPos)
            if(pNeg != 0):
                sumP_neg += log(pNeg)
        if(sumP_pos > sumP_neg):
            return self.tp[0]
        else:
            return self.tp[1]

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        tr = 0
        fl = 0
        for i in range (len(X_test)):
            temp = X_test[i].split(' ')
            mType = self.predict(temp)
            if(mType == y_test[i]):
                tr+=1
            else:
                fl+=1
        return (tr / (tr + fl))
        pass

'''if __name__ == "__main__":
    with open("SMSSpamCollection") as f:
        data = list(csv.reader(f, delimiter="\t"))
    #print(len(data))

    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
    X = [clean(x).lower() for x in X]
    #print(X[:3])

    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
    #print(X_train[0], '\n', y_train[0])
    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    #model.predict(X_test)
    print(model.score(X_test, y_test))'''