from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

# Ensure a folder for temporary .arff files exists
os.makedirs("temp", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # Collect form inputs
        adults = request.form['adults']
        weekend_nights = request.form['weekend_nights']
        meal = request.form['meal']
        room = request.form['room']
        price = request.form['price']

        # Construct .arff content
        arff_content = f"""@RELATION hotel_bookings

@ATTRIBUTE number_of_adults NUMERIC
@ATTRIBUTE number_of_weekend_nights NUMERIC
@ATTRIBUTE type_of_meal {{'Meal Plan 1','Meal Plan 2','Meal Plan 3','Not Selected'}}
@ATTRIBUTE room_type {{'Room_Type 1','Room_Type 2','Room_Type 3','Room_Type 4','Room_Type 5','Room_Type 6','Room_Type 7'}}
@ATTRIBUTE average_price NUMERIC
@ATTRIBUTE booking_status {{'Canceled','Not_Canceled'}}

@DATA
{adults},{weekend_nights},'{meal}','{room}',{price},?
"""

        # Save to file
        arff_path = "temp/input.arff"
        with open(arff_path, "w") as f:
            f.write(arff_content)

        # Run Weka prediction using full java path (no reliance on PATH env variable)
        cmd = f'"C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.7.6-hotspot\\bin\\java.exe" -cp ".;weka.jar" weka.classifiers.trees.J48 -l results.model -T "{arff_path}" -p 0'

        # Debug print info
        print("==== DEBUG INFO ====")
        print(f"ARFF path exists? {os.path.exists(arff_path)}")
        print(f"results.model exists? {os.path.exists('results.model')}")
        print(f"weka.jar exists? {os.path.exists('weka.jar')}")
        print(f"Full CMD: {cmd}")
        print("=====================")

        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in output.splitlines():
                if line.strip().startswith("1") and ":" in line:
                    result = line.split()[2]  # e.g., "Canceled" or "Not_Canceled"
                    break
        except subprocess.CalledProcessError as e:
            result = "Σφάλμα κατά την πρόβλεψη: " + str(e.output)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
