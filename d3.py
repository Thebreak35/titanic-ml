import csv

training_data = []
header = [	'PassengerId',
				'Survived',
				'Pclass',
				'Name',
				'Sex',
				'Age',
				'SibSp',
				'Parch',
				'Ticket',
				'Fare',
				'Cabin',
				'Embarked']


def unique_vals(rows, col):
	return set([row[col] for row in rows])

def is_numeric(value):
	return isinstance(value, int) or isinstance(value, float)

def class_counts(rows, i):
    counts = {}
    for row in rows:
        label = row[header[i]]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    
    return counts

def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    
    return true_rows, false_rows

def gini(rows, i): #impurity
	counts = class_counts(rows, i)
	impurity = 1
	for lbl in counts:
		prob_of_lbl = counts[lbl] / float(len(rows))
		impurity -= prob_of_lbl**2

	return impurity

class Question:
	def __init__(self, column, value):
		self.column = column
		self.value = value

	def showValue(self):
		return self.value

	def match(self, example):
		val = example[header[self.column]]
		if is_numeric(val):
			return val >= self.value
		else:
			return val == self.value

	def __repr__(self):
		condition = "=="
		if is_numeric(self.value):
			condition = ">="
		
		return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))

with open('train.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for line in reader:
		training_data.append(line)

print(class_counts(training_data, 3))
print(unique_vals(training_data, header[1]))
print(Question(4,'fmale'))

q = Question(4, 'male')
example = training_data[3]
print(q)
print(example)
print(q.match(example))

true_rows, false_rows = partition(training_data, Question(4, 'male'))
print(true_rows,' ',false_rows)

print(gini(training_data, 4))