from flask import Flask, request, render_template
import pickle
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        vect = vectorizer.transform(data).toarray()
        prediction = model.predict(vect)[0]
        
        feature_names = vectorizer.get_feature_names_out()
        keyword_indices = vect[0].nonzero()[0]
        keywords = [feature_names[i] for i in keyword_indices]

        result_text = "Đây là spam" if prediction == 1 else "Đây không phải là spam"

        return render_template('index.html', prediction=result_text, keywords=keywords, original_message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
