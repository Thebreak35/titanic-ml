import csv
import pprint as pp

training_data = []
header = [	
	'PassengerId',
	'Pclass',
	'Name',
	'Sex',
	'Age',
	'SibSp',
	'Parch',
	'Ticket',
	'Fare',
	'Cabin',
	'Embarked',
	'Survived']


def unique_vals(rows, col):
	return set([row[col] for row in rows])

def is_numeric(value):
	return isinstance(value, int) or isinstance(value, float)

def class_counts(rows):
    counts = {}
    for row in rows:
    	label = row[11]
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

def gini(rows): #impurity
	counts = class_counts(rows)
	impurity = 1
	for lbl in counts:
		prob_of_lbl = counts[lbl] / float(len(rows))
		impurity -= prob_of_lbl**2

	return impurity

def info_gain(left, right, current_uncertainty):
	p = float(len(left)) / (len(left) + len(right))

	return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

def find_best_split(rows):
	best_gain = 0
	best_question = None
	current_uncertainty = gini(rows)
	n_features = len(rows[0]) - 1

	for col in range(n_features):
		values = set([row[col] for row in rows])

		for val in values:
			question = Question(col, val)
			true_rows, false_rows = partition(rows, question)

			if len(true_rows) == 0 or len(false_rows) == 0:
				continue

			gain = info_gain(true_rows, false_rows, current_uncertainty)
 
			if gain >= best_gain:
				best_gain, best_question = gain, question

	return best_gain, best_question

def build_tree(rows):
	gain, question = find_best_split(rows)

	if gain == 0:
		return Leaf(rows)

	true_rows, false_rows = partition(rows, question)
	true_branch = build_tree(true_rows)
	false_branch = build_tree(false_rows)

	return Decision_Node(question, true_branch, false_branch)

def print_tree(node, spacing=" "):
	if isinstance(node, Leaf):
		print(spacing + "Predict", node.predictions)
		return

	print(spacing + str(node.question))
	
	print (spacing + '--> True:')
	print_tree(node.true_branch, spacing + "  ")

	print (spacing + '--> False:')
	print_tree(node.false_branch, spacing + "  ")

def classify(rows, node):
	if isinstance(node, Leaf):
		return node.predictions

	if node.question.match(rows):
		return classify(rows, node.true_branch)
	else:
		return classify(rows, node.false_branch)

def print_leaf(counts):
    """A nicer way to print the predictions at a leaf."""
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


class Question:
	def __init__(self, column, value):
		self.column = column
		self.value = value

	def showValue(self):
		return self.value

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


class Leaf:
	def __init__(self, rows):
		self.predictions = class_counts(rows)


class Decision_Node:
	def __init__(self,question,true_branch,false_branch):
		self.question = question
		self.true_branch = true_branch
		self.false_branch = false_branch




dum = []


intData = [
	header[0],
	header[1],
	header[5],
	header[6],
	header[11]]

floatData = [header[8],header[4]]
with open('train.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for line in reader:
		dum = []
		for i in header:
			if i in intData and line[i] != '':
				line[i] = int(line[i])
			elif i in floatData and line[i] != '':
				line[i] = float(line[i])
			dum.append(line[i])
		training_data.append(dum)



# pp.pprint(training_data)

# pp.pprint(class_counts(training_data))
# pp.pprint(unique_vals(training_data, 5))
# pp.pprint(Question(4,'fmale'))

# q = Question(4, 'male')
# example = training_data[3]
# print(q)
# print(example)
# print(q.match(example))

# true_rows, false_rows = partition(training_data, Question(4, 'male'))
# print(true_rows,' ',false_rows)

# print(gini(training_data))

# current_uncertainty = gini(training_data)
# print(current_uncertainty)

# print(Question(4, 'fmale'))
# true_rows, false_rows = partition(training_data, Question(4, 'female'))
# print(info_gain(true_rows, false_rows, current_uncertainty))

# best_gain, best_question = find_best_split(training_data)
# pp.pprint(best_question)
# pp.pprint(best_gain)

# pp.pprint(class_counts(training_data))

mytree = build_tree(training_data)
# print_tree(mytree)
# print(classify(training_data[0], mytree))
# print(print_leaf(classify(training_data[1], mytree)))

header = [	'PassengerId',
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

intData = [	header[0],
			header[1],
			header[5],
			header[6]]
floatData = [	header[8],
				header[4]]
test_data = []
with open('test.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for line in reader:
		dum = []
		for i in header:
			if i in intData and line[i] != '':
				line[i] = int(line[i])
			elif i in floatData and line[i] != '':
				line[i] = float(line[i])
			dum.append(line[i])
		test_data.append(dum)


with open('answer.csv', mode='w') as ans:
	ans = csv.writer(ans, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	ans.writerow(['PassengerId', 'Survived'])
	predict = []
	for row in test_data:
		# print(row)
		pass_id = row[0]
		s = classify(row, mytree)
		a = s.keys()
		predict = [pass_id, a[0]]
		ans.writerow(predict)
