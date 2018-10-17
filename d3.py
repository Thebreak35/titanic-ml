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

print(unique_vals(training_data, header[1]))
print(Question(4,'fmale'))