from flask import Flask, render_template, request, flash, session
import Orange
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the model
with open('./models/random_forest_1.pkcls', 'rb') as f:
    model1 = pickle.load(f)
with open('./models/random_forest_2.pkcls', 'rb') as f:
    model2 = pickle.load(f)
with open('./models/random_forest_3.pkcls', 'rb') as f:
    model3 = pickle.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # Get domain from the loaded model
        domain1 = model1.domain
        domain2 = model2.domain
        domain3 = model3.domain

        data = []
        data.append(int(request.form.get('adults')))
        data.append(int(request.form.get('lead_time')))
        data.append(float(request.form.get('price')))
        data.append(int(request.form.get('special_requests')))
        if request.form.get("market_segment_type") == "Corporate":
            data.append(1)
        else:
            data.append(0)
        data.append(request.form.get("p_not_c"))
        if int(request.form.get('car_parking_space')) >= 1:
            data.append(1)
        else:
            data.append(0)
        data.append(int(request.form.get("number_of_week_nights")))
        if request.form.get("market_segment_type") == "Complementary":
            data.append(1)
        else:
            data.append(0)
        # Create Orange data Table
        input_data1 = Orange.data.Table.from_list(domain1, [data])
        input_data2 = Orange.data.Table.from_list(domain2, [data])
        input_data3 = Orange.data.Table.from_list(domain3, [data])

        # Predict using the model (returns list of predictions)
        prediction1 = int(model1(input_data1)[0])
        prediction2 = int(model2(input_data2)[0])
        prediction3 = int(model3(input_data3)[0])
        result_score = 0

        result_score += prediction1 + prediction2 + prediction3

        if result_score >= 2:
            flash("Reservation Not Canceled", "success")
        else:
            flash("Reservation Canceled", "error")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
