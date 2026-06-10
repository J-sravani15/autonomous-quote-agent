import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# load dataset
df = pd.read_excel("Autonomous QUOTE AGENTS data set.xlsx")

# remove useless columns
df = df.drop(columns=[
    "Quote_Num",
    "Agent_Num",
    "Q_Creation_DT",
    "Q_Valid_DT",
    "Policy_Bind_DT"
])

# convert target variable
df["Policy_Bind"] = df["Policy_Bind"].map({"Yes":1,"No":0})

# convert categorical columns
categorical_cols = df.select_dtypes(include=["object"]).columns

encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

# split data
X = df.drop("Policy_Bind",axis=1)
y = df["Policy_Bind"]

X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.2,random_state=42
)

# train model
model = RandomForestClassifier()

model.fit(X_train,y_train)

# save model
joblib.dump(model,"conversion_model.pkl")

print("Model trained and saved")