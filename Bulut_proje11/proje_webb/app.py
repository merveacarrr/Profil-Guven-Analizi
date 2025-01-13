from flask import Flask, render_template, request
import pandas as pd
from Bulut_proje11.data_yükleme import NBC, recategorize_data
from Bulut_proje11.data_çekme import fetch_instagram_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        username = request.form['username']
        kullanıcı_verileri = fetch_instagram_data(username)

        if kullanıcı_verileri:
            user_df = pd.DataFrame([kullanıcı_verileri])
            model = NBC()
            model.load_model("C:/Users/Merve/Desktop/Bulut_proje/Bulut_proje11/models/trained_model.joblib")
            train_df = pd.read_csv("C:/Users/Merve/Desktop/Bulut_proje/Bulut_proje11/datalar/train.csv")
            train_X = train_df.drop("fake", axis=1)
            user_df, _ = recategorize_data(train_X, user_df)

            prediction = model.predict(user_df)[0]
            fake_percentage = prediction * 100
            real_percentage = 100 - fake_percentage

            return render_template('result.html', fake_percentage=fake_percentage, real_percentage=real_percentage, kullanıcı_verileri=kullanıcı_verileri)
        else:
            return render_template('index.html', error="Could not fetch data for the given username. Please try again.")

if __name__ == '__main__':
    app.run(debug=True)
