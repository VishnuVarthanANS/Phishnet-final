import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("Loading dataset...")

df = pd.read_csv("dataset.csv")
print("Rows:", len(df))

FEATURES = [
    "having_IP_Address",
    "URL_Length",
    "Shortining_Service",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "SSLfinal_State",
    "Request_URL",
    "URL_of_Anchor",
    "Submitting_to_email",
    "Abnormal_URL",
    "Redirect",
    "Iframe",
    "web_traffic",
    "Google_Index",
    "Statistical_report"
]


print("Preparing features...")
X = df[FEATURES]
y = df["Result"].replace(-1,0)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

print("Training model...")
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train,y_train)

print("Evaluating...")
pred = model.predict(X_test)
acc = accuracy_score(y_test,pred)

print("\nModel Accuracy:", acc)

joblib.dump(model,"model.pkl")
print("Model saved as model.pkl")
