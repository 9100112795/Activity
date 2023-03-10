# -*- coding: utf-8 -*-
"""Personal_Loan(k) (2).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JDvKHVU--NHOzdV_a97IHkk-c52nILHt
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv('/home/4767b117/Personal Loan/Bank_data_CEA/Bank_Personal_Loan_Modelling.csv')

data.head()

data.tail()

data.describe(include='all')

data.shape

data.info()

data.isna().sum()

data.duplicated().sum()

"""

```
# This is formatted as code
```

NO missing and duplicate values!"""

data.describe()

data.columns

"""Dropping unnecessary columns Like ID and ZIP CODE"""

data.drop(['ID','ZIP Code'], axis=1, inplace= True)

data.corr()

data.nunique()

data.value_counts(['Personal Loan'], normalize=True)

data.value_counts(['Personal Loan'])

sns.countplot(x="Personal Loan", data=data)

"""Data is highly imbalanced majority of data belongs to class 0.
Imbalanced ratio is 90:10 i.e., Out of 5000 data 4520 are not opting for personal loan and 480 are opting for Personal loan!!
"""

data.columns

"""#### Filtering categorical and numeric columns

*   List item
*   List item


"""

cat= ['Family','Education','Securities Account', 'CD Account','Online', 'CreditCard']
data[cat]=data[cat].astype('category')

cat

num=['Age', 'Experience', 'Income','CCAvg', 'Mortgage']

num

data.dtypes

data.value_counts(['Online'])

data.value_counts(['Online'], normalize=True)

"""###EDA"""

sns.countplot(x="Online", data=data)
plt.show()

def dist_box(data):
 # function plots a combined graph for univariate analysis of continous variable 
 #to check spread, central tendency , dispersion and outliers  
    Name=data.name.upper()
    fig,(ax_box,ax_dis)  =plt.subplots(nrows=2,sharex=True,gridspec_kw = {"height_ratios": (.25, .75)},figsize=(8, 5))
    mean=data.mean()
    median=data.median()
    mode=data.mode().tolist()[0]
    sns.set_theme(style="white")
    fig.suptitle("SPREAD OF DATA FOR "+ Name  , fontsize=18, fontweight='bold')
    sns.boxplot(x=data,showmeans=True, orient='h',color="violet",ax=ax_box)
    ax_box.set(xlabel='')
     # just trying to make visualisation better. This will set background to white
    sns.despine(top=True,right=True,left=True) # to remove side line from graph
    sns.distplot(data,kde=False,color='blue',ax=ax_dis)
    ax_dis.axvline(mean, color='r', linestyle='--',linewidth=2)
    ax_dis.axvline(median, color='g', linestyle='-',linewidth=2)
    ax_dis.axvline(mode, color='y', linestyle='-',linewidth=2)
    plt.legend({'Mean':mean,'Median':median,'Mode':mode})

#select all quantitative columns for checking the spread
list_col=  ['Age','Experience','Income','CCAvg','Mortgage']
for i in range(len(list_col)):
    dist_box(data[list_col[i]])

"""Observations

1. Age and experience both has same distrubtion with spike at 5
2. Income is right skewed and has some outlier on higher side which can be clipped.
3. Average montly credit is right skewed and has lot of outliers on higher side which can be clipped.
4. Mortgage is mostly 0 . but is right skewed and has lot of outlier on higher side which can be clipped!

##### Outlier detection
"""

data[num].describe()
Q1=data[num].quantile(0.25)
Q3=data[num].quantile(0.75)
IQR=Q3-Q1
IQR
((data[num]<(Q1-1.5*IQR)) | (data[num]>(Q3+1.5*IQR))).any()

"""Income, CCAvg and Mortgage have outliers!"""

q1=data['Income'].quantile(0.25)
q3=data['Income'].quantile(0.70)
iqr = q3-q1
filter1 = (data['Income']>=q1 - 1.5*iqr) & (data['Income']<=q3+1.5*iqr)
data=data.loc[filter1]

q1=data['CCAvg'].quantile(0.25)
q3=data['CCAvg'].quantile(0.70)
iqr = q3-q1
filter1 = (data['CCAvg']>=q1 - 1.5*iqr) & (data['CCAvg']<=q3+1.5*iqr)
data=data.loc[filter1]

q1=data['Mortgage'].quantile(0.25)
q3=data['Mortgage'].quantile(0.70)
iqr = q3-q1
filter1 = (data['Mortgage']>=q1 - 1.5*iqr) & (data['Mortgage']<=q3+1.5*iqr)
data=data.loc[filter1]

sns.heatmap(data[num].corr(),annot=True)

"""As we can see Age and experience are highly correlated!

### Creating Dummies
"""

data=pd.get_dummies(data, columns = cat)
data.head()

"""#### Data Prep"""

from sklearn.model_selection import train_test_split
X=data.drop(['Personal Loan'],axis=1)
y=data['Personal Loan']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=123)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.metrics import recall_score, classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import precision_recall_curve , auc , f1_score

RF=RandomForestClassifier()
RF.fit(X_train, y_train)
y_pred = RF.predict(X_test)
y_trains=RF.predict(X_train) 


print(accuracy_score(y_train, y_trains)*100)
print(accuracy_score(y_test, y_pred)*100)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(classification_report(y_train, y_trains))

fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred)

#create ROC curve
plt.plot(fpr,tpr)
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
auc = metrics.roc_auc_score(y_test, y_pred)
#create ROC curve
plt.plot(fpr,tpr,label="AUC="+str(auc))
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.legend(loc=4)
plt.show()

"""Feature Importances"""

importances = RF.feature_importances_
#Sort the feature importance in descending order
sorted_indices = np.argsort(importances)[::-1]
feat_labels = data.columns[1:]
for f in range(X_train.shape[1]):
    print("%2d) %-*s %f" % (f + 1, 30,
                            feat_labels[sorted_indices[f]],
                            importances[sorted_indices[f]]))

"""Logistic Model"""

logistic_model=LogisticRegression()
logistic_model.fit(X_train, y_train)
y_pred = logistic_model.predict(X_test)
y_trains=logistic_model.predict(X_train) 

print(accuracy_score(y_train, y_trains)*100)
print(accuracy_score(y_test, y_pred)*100)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(classification_report(y_train, y_trains))

fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred)

#create ROC curve
plt.plot(fpr,tpr)
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
auc = metrics.roc_auc_score(y_test, y_pred)
#create ROC curve
plt.plot(fpr,tpr,label="AUC="+str(auc))
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.legend(loc=4)
plt.show()

"""SVC MODEL"""

svc=SVC()
svc.fit(X_train, y_train)
y_pred = svc.predict(X_test)
print(svc.score(X_train,y_train)*100)
print(accuracy_score(y_test, y_pred)*100)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(classification_report(y_train, y_trains))

fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred)

#create ROC curve
plt.plot(fpr,tpr)
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
auc = metrics.roc_auc_score(y_test, y_pred)
#create ROC curve
plt.plot(fpr,tpr,label="AUC="+str(auc))
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.legend(loc=4)
plt.show()

import pickle

pickle_out = open("model.pkl","wb")
pickle.dump(model, pickle_out)
pickle_out.close()

model.predict([[2,3,1,4,5,6,8,7,9]])







