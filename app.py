from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def show_csv_data():
    data = []
    with open('salesforce_leads_data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return render_template('csv_template.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
