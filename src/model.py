# src/model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib

def train_model(path='data/rfm_labeled.csv'):
    df = pd.read_csv(path)
    X = df[['Recency','Frequency','Monetary']]
    y = df['NextMonthPurchase']

    # train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    # scale features
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    # train logistic regression
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_s, y_train)

    # predictions
    y_pred = model.predict(X_test_s)
    y_proba = model.predict_proba(X_test_s)[:,1]

    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("ROC-AUC:", roc_auc_score(y_test, y_proba))

    # save model and scaler
    joblib.dump(model, 'model/logistic_model.joblib')
    joblib.dump(scaler, 'model/scaler.joblib')

if __name__ == "__main__":
    train_model()
