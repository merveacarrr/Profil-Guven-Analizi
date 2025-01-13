import os
import pandas as pd
from sklearn.naive_bayes import CategoricalNB
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Veriyi kategorik aralıklara ayırma fonksiyonları
def categorize_column(data, column_name, bins=4):
    data[column_name], bins_edges = pd.cut(data[column_name], bins=bins, retbins=True)
    data[column_name] = pd.Categorical(data[column_name]).codes
    return bins_edges

def recategorize_data(train_X, test_X):
    columns_to_bin = [
        'nums/length username',
        'fullname words',
        'nums/length fullname',
        'description length',
        '#posts',
        '#followers',
        '#follows'
    ]

    bins = {}
    for column in columns_to_bin:
        bins[column] = categorize_column(train_X, column)
        test_X[column] = pd.cut(test_X[column], bins=bins[column])
        test_X[column] = pd.Categorical(test_X[column]).codes

    return train_X, test_X

# Naive Bayes Sınıflandırıcı Sınıfı
class NBC:
    def __init__(self, train_X=None, train_y=None):
        self.train_X = train_X
        self.train_y = train_y
        self.model = CategoricalNB()

    def train_model(self):
        self.model.fit(self.train_X, self.train_y)

    def predict(self, test_X):
        return self.model.predict(test_X)

    def save_model(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        self.model = joblib.load(filename)

# Veri yükleme
train_df = pd.read_csv("C:/Users/Merve/Desktop/Bulut_proje/Bulut_proje11/datalar/train.csv")
test_df = pd.read_csv("C:/Users/Merve/Desktop/Bulut_proje/Bulut_proje11/datalar/test.csv")

train_X = train_df.drop("fake", axis=1)
train_y = train_df['fake']
test_X = test_df.drop("fake", axis=1)
test_y = test_df['fake']

# Veriyi kategorik aralıklara ayırma
train_X, test_X = recategorize_data(train_X, test_X)

# Model eğitimi
nbc = NBC(train_X, train_y)
nbc.train_model()
predictions = nbc.predict(test_X)

# Modeli kaydetme
model_path = "C:/Users/Merve/Desktop/Bulut_proje/Bulut_proje11/models/trained_model.joblib"
nbc.save_model(model_path)
"""
# Tahmin sonuçlarını inceleme
accuracy = accuracy_score(test_y, predictions)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Karışıklık Matrisi oluşturma
conf_matrix = confusion_matrix(test_y, predictions)

# Karışıklık Matrisini görselleştirme
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=['Fake', 'Not Fake'], yticklabels=['Fake', 'Not Fake'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
"""
# Eğitim ve test verilerini kaydetm
train_X.to_csv("C:/Users/Merve/Desktop/Bulut_proje/Bulut_proje11/datalar/train_processed.csv", index=False)
test_X.to_csv("C:/Users/Merve/Desktop/Bulut_proje/Bulut_proje11/datalar/test_processed.csv", index=False)