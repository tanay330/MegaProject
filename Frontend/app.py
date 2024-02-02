from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/options')
def options():
    return render_template('options.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('options.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('options.html', error='No selected file')

    # Process the uploaded file (example: read CSV data into a list of dictionaries)
    result = process_uploaded_file(file)

    # Render the result page with the processed data
    return render_template('result.html', result=result)

"""def process_uploaded_file(file):
    # Add your processing logic here
    # Example: Read the CSV file and return a list of dictionaries
    result = []
    for line in file:
        # Process each line of the CSV file (example assumes a CSV with two columns)
        columns = line.strip().split(',')
        result.append({'column1': columns[0], 'column2': columns[1]})
    return result"""
def process_uploaded_file(file):
    result = []
    
    # Assuming UTF-8 encoding, change it if your CSV file has a different encoding
    for line_bytes in file:
        line = line_bytes.decode('utf-8')
        # Process each line of the CSV file (example assumes a CSV with two columns)
        columns = line.strip().split(',')
        result.append({'column1': columns[0], 'column2': columns[1],'column3' :columns[2],'column4':columns[3],'column5':columns[4]})
    
    return result


if __name__ == '__main__':
    app.run(debug=True)
