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

def class_counts(rows):
    counts = {}
    for row in rows:
        label = row[header[1]]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

class Question:
	def __init__(self, column, value):
		self.column = column
		self.value = value

	def match(self, example):
		val = example[self.column]
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

print(class_counts(training_data))
print(unique_vals(training_data, header[1]))
print(Question(4,'fmale'))

q = Question(4, 'male')
example = training_data[3][header[4]]
print(q)
print(example)
print(q.match(example))