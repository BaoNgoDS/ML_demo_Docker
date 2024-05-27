# README

## Mô hình phân loại Spam bằng Python trên Docker

Hướng dẫn này sẽ giúp bạn triển khai mô hình phân loại spam bằng Python trên Docker. Chúng ta sẽ bắt đầu từ bước đầu tiên và đi qua từng bước chi tiết.

### Bước 1: Chuẩn bị Môi trường và Cài đặt Yêu cầu

1. **Tạo thư mục dự án**:
   - Tạo một thư mục mới cho dự án của bạn, ví dụ: `spam_classifier_demo`. Mở terminal và chạy lệnh:
     ```sh
     mkdir spam_classifier_demo
     cd spam_classifier_demo
     ```

### Bước 2: Tạo Dockerfile

1. **Tạo Dockerfile**:
   - Trong thư mục dự án `spam_classifier_demo`, tạo một file có tên `Dockerfile` và mở nó bằng một trình soạn thảo văn bản.
   - Thêm nội dung sau vào `Dockerfile`:
     ```Dockerfile
     FROM python:3.9-slim

     # Thiết lập thư mục làm việc
     WORKDIR /app

     # Sao chép các file yêu cầu vào thư mục làm việc
     COPY requirements.txt requirements.txt

     # Cài đặt các thư viện yêu cầu
     RUN pip install -r requirements.txt

     # Sao chép toàn bộ nội dung của thư mục dự án vào container
     COPY . .

     # Chạy lệnh để khởi động ứng dụng
     CMD ["python", "app.py"]
     ```

### Bước 3: Tạo file requirements.txt

1. **Tạo file requirements.txt**:
   - Trong thư mục `spam_classifier_demo`, tạo một file có tên `requirements.txt` và mở nó bằng trình soạn thảo văn bản.
   - Thêm các thư viện cần thiết vào file `requirements.txt`:
     ```txt
     flask
     sklearn
     pandas
     numpy
     ```

### Bước 4: Tạo ứng dụng Flask

1. **Tạo file app.py**:
   - Trong thư mục `spam_classifier_demo`, tạo một file có tên `app.py` và mở nó bằng trình soạn thảo văn bản.
   - Thêm nội dung sau vào `app.py`:
     ```python
     from flask import Flask, request, render_template
     import pickle

     app = Flask(__name__)

     # Tải mô hình và vectorizer đã huấn luyện
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
             prediction = model.predict(vect)
             return render_template('index.html', prediction=prediction[0])

     if __name__ == '__main__':
         app.run(host='0.0.0.0', port=5000)
     ```

### Bước 5: Tạo giao diện người dùng

1. **Tạo thư mục templates**:
   - Trong thư mục `spam_classifier_demo`, tạo một thư mục có tên `templates`.
     ```sh
     mkdir templates
     ```

2. **Tạo file index.html**:
   - Trong thư mục `templates`, tạo một file có tên `index.html` và mở nó bằng trình soạn thảo văn bản.
   - Thêm nội dung sau vào `index.html`:
     ```html
     <!DOCTYPE html>
     <html lang="en">
     <head>
         <meta charset="UTF-8">
         <meta name="viewport" content="width=device-width, initial-scale=1.0">
         <title>Spam Classifier</title>
     </head>
     <body>
         <h1>Spam Classifier</h1>
         <form action="/predict" method="post">
             <label for="message">Enter a message:</label><br><br>
             <textarea name="message" id="message" rows="4" cols="50"></textarea><br><br>
             <input type="submit" value="Predict">
         </form>
         {% if prediction %}
             <h2>Prediction: {{ prediction }}</h2>
         {% endif %}
     </body>
     </html>
     ```

### Bước 6: Huấn luyện mô hình và lưu trữ

1. **Tạo script huấn luyện mô hình**:
   - Trong thư mục `spam_classifier_demo`, tạo một file có tên `train_model.py` và mở nó bằng trình soạn thảo văn bản.
   - Thêm nội dung sau vào `train_model.py`:
     ```python
     from sklearn.feature_extraction.text import CountVectorizer
     from sklearn.naive_bayes import MultinomialNB
     import pandas as pd
     import pickle

     # Load dữ liệu
     data = pd.read_csv('spam.csv')
     X = data['text']
     y = data['label']

     # Vector hóa văn bản
     vectorizer = CountVectorizer()
     X = vectorizer.fit_transform(X)

     # Huấn luyện mô hình
     model = MultinomialNB()
     model.fit(X, y)

     # Lưu trữ mô hình và vectorizer
     pickle.dump(model, open('model.pkl', 'wb'))
     pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))
     ```

2. **Tạo file dữ liệu mẫu**:
   - Tạo một file CSV có tên `spam.csv` với nội dung ví dụ sau:
     ```csv
     text,label
     "Congratulations, you've won a free ticket!",spam
     "Hey, can we reschedule our meeting?",not spam
     ```

3. **Chạy script huấn luyện**:
   - Chạy script `train_model.py` để huấn luyện mô hình và lưu trữ:
     ```sh
     python train_model.py
     ```

### Bước 7: Xây dựng Docker Image và Chạy Container

1. **Xây dựng Docker Image**:
   - Mở terminal và chuyển đến thư mục dự án, sau đó chạy lệnh:
     ```sh
     docker build -t spam_classifier_demo .
     ```

2. **Chạy Docker Container**:
   - Chạy lệnh sau để khởi động container:
     ```sh
     docker run -p 5000:5000 spam_classifier_demo
     ```

### Bước 8: Truy cập ứng dụng

1. **Truy cập ứng dụng**:
   - Mở trình duyệt và truy cập `http://localhost:5000` để xem giao diện nhập câu và phân loại.
