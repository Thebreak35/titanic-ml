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


with open('train.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for line in reader:
		training_data.append(line)

print(unique_vals(training_data, header[1]))