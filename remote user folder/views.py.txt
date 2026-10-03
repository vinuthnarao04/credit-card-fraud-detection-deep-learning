from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime

import pandas as pd

from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score


# Create your views here.
from Remote_User.models import ClientRegister_Model,detect_fraud_in_banking,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Detection_Of_Fraud_in_Banking_Status(request):
    if request.method == "POST":

        CID= request.POST.get('CID')
        CName= request.POST.get('CName')
        Gen= request.POST.get('Gen')
        Age= request.POST.get('Age')
        State= request.POST.get('State')
        City= request.POST.get('City')
        BB= request.POST.get('BB')
        AT= request.POST.get('AT')
        TID= request.POST.get('TID')
        TDate= request.POST.get('TDate')
        TTime= request.POST.get('TTime')
        TAmount= request.POST.get('TAmount')
        MID= request.POST.get('MID')
        TType= request.POST.get('TType')
        MCat= request.POST.get('MCat')
        ABal= request.POST.get('ABal')
        TDevice= request.POST.get('TDevice')
        TLoc= request.POST.get('TLoc')
        TCur= request.POST.get('TCur')
        TDesc= request.POST.get('TDesc')


        df = pd.read_csv('Datasets.csv',encoding='latin-1')
        df
        df.columns


        df['label'] = df.Is_Fraud.apply(lambda x: 1 if x == 1 else 0)
        df.head()

        cv = CountVectorizer()

        x = df['Customer_ID'].apply(str)
        y = df['label']

        cv = CountVectorizer()
        x = cv.fit_transform(x)

        print(x)
        print("Y")
        print(y)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Graph Neural Networks (GNN)")

        from sklearn.neural_network import MLPClassifier
        mlpc = MLPClassifier().fit(X_train, y_train)
        y_pred = mlpc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('MLPClassifier', mlpc))

        print("Decision Tree Classifier")
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        dtcpredict = dtc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, dtcpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, dtcpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, dtcpredict))
        models.append(('DecisionTreeClassifier', dtc))

        print("KNeighborsClassifier")
        from sklearn.neighbors import KNeighborsClassifier
        kn = KNeighborsClassifier()
        kn.fit(X_train, y_train)
        knpredict = kn.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, knpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, knpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, knpredict))
        models.append(('KNeighborsClassifier', kn))

        # SVM Model
        print("SVM")
        from sklearn import svm
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression
        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))


        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        CID1 = [CID]
        vector1 = cv.transform(CID1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if prediction == 0:
            val = 'Banking Fraud Not Found'
        elif prediction == 1:
            val = 'Banking Fraud Found'

        print(val)
        print(pred1)

        detect_fraud_in_banking.objects.create(
        CID=CID,
        CName=CName,
        Gen=Gen,
        Age=Age,
        State=State,
        City=City,
        BB=BB,
        AT=AT,
        TID=TID,
        TDate=TDate,
        TTime=TTime,
        TAmount=TAmount,
        MID=MID,
        TType=TType,
        MCat=MCat,
        ABal=ABal,
        TDevice=TDevice,
        TLoc=TLoc,
        TCur=TCur,
        TDesc=TDesc,
        Prediction=val)

        return render(request, 'RUser/Detection_Of_Fraud_in_Banking_Status.html',{'objs': val})
    return render(request, 'RUser/Detection_Of_Fraud_in_Banking_Status.html')



