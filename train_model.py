import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

data = pd.read_csv('spam_emails.csv')

data.dropna(subset=['email', 'spam'], inplace=True)

if data['spam'].dtype == 'object':
    data['spam'] = data['spam'].apply(lambda x: 1 if x.lower() == 'spam' else 0)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(data['email'], data['spam'], test_size=0.2, random_state=42)

# Vector hóa văn bản
vectorizer = CountVectorizer()
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# Huấn luyện mô hình
model = MultinomialNB()
model.fit(X_train_vect, y_train)

# Đánh giá mô hình
y_pred = model.predict(X_test_vect)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(classification_report(y_test, y_pred))

# Lưu trữ mô hình và vectorizer
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

