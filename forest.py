from random import seed
from random import randrange
from csv import reader
from math import sqrt


def load_csv(filename):
    dataset = list()
    with open(filename,'r') as file:
        csv_reader = reader(file)
        for row in csv_reader :
            if not row:
                continue
            dataset.append(row)
    return dataset

def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

def str_column_to_int(dataset,column):
    class_values = list(row[-1]for row in dataset)
    unique = set(class_values)# removes the duplicate values
    lookup = dict()#just an empty dictionary
    for i,values in enumerate(unique):#the enumarate takes the index values of the unique
        lookup[values] = i#storing the index values
    for row in dataset:
        row[column] = lookup[row[column]]#replacing the actuall data by its index number to make the calucaltion easier
    return lookup

def cross_validation_split(dataset,n_folds):
    dataset_split = list()
    dataset_copy = list(dataset)
    fold_size = int(len(dataset)/n_folds)

    for i in range(n_folds):
        fold = list()
        while len(fold) < fold_size:
            index = randrange(len(dataset_copy))
            fold.append(dataset_copy.pop(index))
        dataset_split.append(fold)
    return dataset_split

def accuracy_metrics(actual,prediction):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == prediction[i]:
            correct+=1
    return correct/len(actual)*100.0

def evaluation_algorithm(dataset,algorithm,n_folds,*args):
    folds = cross_validation_split(dataset,n_folds)
    scores = list()
    
    for fold in folds:
        train_set = list(folds)
        train_set.remove(fold)
        train_set = sum(train_set,[])
        test_set = list()

        for row in fold:
            row_copy = list(row)
            test_set.append(row_copy)
            row_copy[-1] = None
        
        prediction = algorithm(train_set,test_set,*args)
        actual = [row[-1]for row in fold]
        accuracy = accuracy_metrics(actual,prediction)
        scores.append(accuracy)
    return scores


def test_split(index,boundary,dataset):
    left,right = list(),list()

    for row in dataset:
        if row[index]<boundary:
            left.append(row)
        else:
            right.append(row)
    return left,right

def gini_index(groups,classes):
    n_instances = float(sum(len(group)for group in groups))
    gini = 0.0

    for group in groups:
        size = len(group)
        if size == 0:
            continue
        scores = 0.0

        for class_val in classes:
            p = [row[-1]for row in group].count(class_val)/size
            scores += p*p
        gini +=(1.0-scores)*(size/n_instances)
    return gini

def get_split(dataset,n_features):
    class_values = list(set(row[-1]for row in dataset))
    b_index,b_scores,b_boundary,b_groups = 999,999,999,None
    features = list()

    while len(features) < n_features:
        index = randrange(len(dataset[0])-1)
        if index not in features:
            features.append(index)

    for index in features:
        for row in dataset:
            groups = test_split(index,row[index],dataset)
            gini = gini_index(groups,class_values)

            if gini<b_scores:
                b_index,b_scores,b_boundary,b_groups = index,gini,row[index],groups
    return{'index':b_index,'boundary':b_boundary,'group':b_groups}

def to_terminal(group):
    outcome = [row[-1]for row in group]
    return max(set(outcome),key=outcome.count)

def split(node,max_depth,n_features,min_size,depth):
    left,right = node['group']
    del(node['group'])

    if not left or not right:
        node['left']=node['right'] = to_terminal(left+right)
        return
    
    if depth >= max_depth:
        node['left'] = to_terminal(left)
        node['right'] = to_terminal(right)
        return
    
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
    else:
        node['left'] = get_split(left, n_features)          # ✅ build child node first
        split(node['left'], max_depth, n_features, min_size, depth+1)
    
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
    else:
        node['right'] = get_split(right, n_features)        # ✅ build child node first
        split(node['right'], max_depth, n_features, min_size, depth+1)
        

def build_tree(train,max_depth,min_size,n_features):
    root = get_split(train,n_features)
    split(root,max_depth,min_size,n_features,1)
    return root

def predict(node,row):
    if row[node['index']]<node['boundary']:
        if isinstance (node['left'],dict):
            return predict(node['left'],row)
        else:
            return node['left']
    else:
        if isinstance (node['right'],dict):
            return predict(node['right'],row)
        else:
            return node['right']
    

def sub_sample(dataset,ratio):
    sample = list()
    n_sample = round(len(dataset)*ratio)

    while len(sample)<n_sample:
        index = randrange(len(dataset))
        sample.append(dataset[index])
    return sample

def bagging_predict(trees,row):
    predictions = [predict(tree,row)for tree in trees]
    return max(set(predictions),key = predictions.count)

def random_forest(train,test,max_depth,min_size,sample_size,n_trees,n_features):
    trees = list()
    for i in range(n_trees):
        sample = sub_sample(train,sample_size)
        tree = build_tree(sample,max_depth,min_size,n_features)
        trees.append(tree)
    prediction = [bagging_predict(trees,row)for row in test]
    return(prediction)

seed(2)
filename = 'sonar.all-data'
dataset = load_csv(filename)

for i in range(len(dataset[0])-1):
    str_column_to_float(dataset,i)
str_column_to_int(dataset,len(dataset[0])-1)


n_folds = 5
max_depth = 10
min_size = 1
sample_size = 1.0
n_features = int(sqrt(len(dataset[0])-1))
for n_trees in [1,5,10]:
    scores = evaluation_algorithm(dataset,random_forest,n_folds,max_depth,min_size,sample_size,n_trees,n_features)
    print('Trees %d'%n_trees)
    print('Scores %s'%scores)
    print('Mean Accuracy %.3f%%'%(sum(scores)/float(len(scores))))
