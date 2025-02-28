from flask import Flask, request, Response, render_template
import csv
import io
import datetime
from xml.dom import minidom
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Determine input type
        input_type = request.form.get('input_type', 'file')
        
        try:
            # Process based on input type
            if input_type == 'file':
                # Check if a file was uploaded
                if 'file' not in request.files:
                    return render_template('index.html', error='No file part')
                
                file = request.files['file']
                
                if file.filename == '':
                    return render_template('index.html', error='No file selected')
                
                if not file.filename.endswith('.csv'):
                    return render_template('index.html', error='File must be a CSV')
                
                # Read the CSV file
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_data = list(csv.reader(stream))
                
                # Skip header row if present
                start_row = 1 if len(csv_data) > 1 and isinstance(csv_data[0][0], str) and csv_data[0][0].lower() == 'name' else 0
                csv_data = csv_data[start_row:]
                
            elif input_type == 'text':
                # Process text input
                text_data = request.form.get('text_data', '')
                
                if not text_data.strip():
                    return render_template('index.html', error='No data entered')
                
                # Parse the text data as CSV
                stream = io.StringIO(text_data, newline=None)
                csv_data = list(csv.reader(stream))
                
                # Check if first row is header and skip if needed
                if len(csv_data) > 1 and isinstance(csv_data[0][0], str) and csv_data[0][0].lower() == 'name':
                    csv_data = csv_data[1:]
            
            else:
                return render_template('index.html', error='Invalid input type')
            
            # Get secrets from form
            radius_secret = request.form.get('radius_secret', '')
            tacacs_secret = request.form.get('tacacs_secret', '')
            
            # Create XML structure
            root = ET.Element("TipsContents")
            root.set("xmlns", "http://www.avendasys.com/tipsapiDefs/1.0")
            
            # Add header
            header = ET.SubElement(root, "TipsHeader")
            current_time = datetime.datetime.now().strftime("%a %b %d %H:%M:%S EST %Y")
            header.set("exportTime", current_time)
            header.set("version", "6.11")
            
            # Add NadClients container
            nad_clients = ET.SubElement(root, "NadClients")
            
            # Flag to check if we have valid data
            has_valid_data = False
            
            # Add each NadClient from CSV data
            for row in csv_data:
                if len(row) >= 2:  # Ensure we have at least name and IP
                    name = row[0].strip()
                    ip_address = row[1].strip()
                    
                    if name and ip_address:  # Only process if both values exist
                        has_valid_data = True
                        nad_client = ET.SubElement(nad_clients, "NadClient")
                        nad_client.set("description", "")
                        nad_client.set("name", name)
                        nad_client.set("nadGroups", "")
                        nad_client.set("coaPort", "3799")
                        nad_client.set("radsecEnabled", "false")
                        nad_client.set("coaCapable", "true")
                        nad_client.set("vendorName", "Cisco")
                        nad_client.set("tacacsSecret", tacacs_secret)
                        nad_client.set("radiusSecret", radius_secret)
                        nad_client.set("ipAddress", ip_address)
            
            if not has_valid_data:
                return render_template('index.html', error='No valid name,IP pairs found in the input')
            
            # Convert to pretty-printed XML
            xml_str = ET.tostring(root, encoding='utf-8')
            dom = minidom.parseString(xml_str)
            pretty_xml = dom.toprettyxml(indent="  ")
            
            # Fix the XML declaration
            pretty_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + pretty_xml.split('\n', 1)[1]
            
            # Return XML as downloadable file
            response = Response(pretty_xml, mimetype='application/xml')
            response.headers.set('Content-Disposition', 'attachment', filename='output.xml')
            return response
                
        except Exception as e:
            return render_template('index.html', error=f'Error processing input: {str(e)}')
    
    return render_template('index.html')

@app.route('/sample', methods=['GET'])
def sample():
    sample_content = "name,ip_address\nexample-01,1.1.10.10\nexample-02,1.1.20.20"
    return Response(
        sample_content,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=sample.csv'}
    )

if __name__ == '__main__':
    app.run(debug=True)
