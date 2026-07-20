# Machinelearning_projects
This just a repo of what i learned from books and personal project 



Premier_league(version1):
  This is my first project.
  I got this data set from https://www.kaggle.com/datasets/saife245/english-premier-league/data?select=final_dataset.csv.This project just predicts the result of the   matches before the actual match.
  My target   varible is FTR(FullTimeResult), this dataset was designed for sports betting so it had a lot of betting related      data so i dropped them all and other columns that were not required.
  After dropping   all the columns my features were HomeTeam,AwayTeam,FTR(y).
  I used the 18-19,19/20,20-21 as the training dataset and used 21-22 as test dataset. I converted the HomeTeam and AwayTeam columns into numbers using label encoding.
  This was a classification problem so i used a RandomForestClassifier. The model's accuracy was ~0.41.
  Next steps: implement rolling features to improve accuracy


Titanic V1:
  First submission.Used RandomForestClassifie. 
  Features:Basic Preprocessing,Onehot encoding
  Kaggle Public score:0.75119

Titanic V2:
  Added Evaluation metrics.
  Precision:0.738
  Recall:0.716
  f1_score:0.727
  ROC-AUC
  Confusion Metrics
  Threshold Tuning

Cancer:
  I used the sklearn's breast cancer dataset and used logistic regression on it this is very simple project.

heart_disease:
  This is a simple svc which predicts whether a person has heart disease or not i used rbf kernel and the C was 1.0. The accuracy was 0.85, precision was 0.83, recall was 0.86 and the f1 score was 0.84.

bank_note.py
 This project uses the bank note authentication dataset and i build the decision tree from the scratch with the help of this blog https://machinelearningmastery.com/implement-decision-tree-algorithm-scratch-python/ 

Forest.py
  This project uses the sonar dataset from https://archive.ics.uci.edu/dataset/151/connectionist+bench+sonar+mines+vs+rocks and i build this random forest from scratch with the help of this blog 
  https://machinelearningmastery.com/implement-random-forest-scratch-python/
