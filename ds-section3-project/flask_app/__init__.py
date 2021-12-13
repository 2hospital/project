import os
from flask import Flask, render_template, request


MODEL_FILEPATH = os.path.join(os.getcwd(),'all','model.pkl') 
app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html'), 200

@app.route('/result',methods =['POST','GET'])
def ml():

    import numpy as np

    if request.method == 'POST':
        result = request.form
        
        X_test = []

        for data in result.values():
            X_test.append(float(data))

        num = int(X_test[-1])

        X_test = X_test[:-1] + [0]*(num-1) + [1] + [0]*(12-num)
        X_test[4] = np.log(X_test[4])
        X_test[6] = np.log(X_test[6])
        X_test[7] = np.log(X_test[7])
        X_test = [X_test]

        import pickle
        model = None

        with open(MODEL_FILEPATH,'rb') as pickle_file:
            model = pickle.load(pickle_file)

        y_pred = model.predict(X_test)

        if y_pred < 0:
            predict = 0
        else:
            predict = int(np.e**y_pred)

        return render_template("result.html",result=predict,input=result), 200

if __name__ == "__main__":
    app.run(debug=True)