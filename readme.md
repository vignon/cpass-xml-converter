# CSV to XML Converter

This Flask application converts CSV files containing name and IP address pairs into a specific XML format for network device configuration.

## Features

- Simple web interface with two input methods:
  - Upload a CSV file
  - Enter name,IP pairs directly in a text box
- Customizable RADIUS and TACACS secrets (can be left blank)
- Automatic conversion to the required XML format
- Sample CSV file available for download
- Error handling for invalid inputs

## Installation

1. Clone this repository or download the files
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Project Structure

```
csv_to_xml_app/
│
├── app.py                # Main Flask application file
│
├── templates/
│   └── index.html        # HTML template for the web interface
│
├── requirements.txt      # Python dependencies
│
└── README.md             # This file
```

## Usage

1. Make sure your project structure is set up correctly with the app.py file at the root and the index.html file in a templates directory
2. Run the Flask application:
   ```
   python app.py
   ```
3. Open your web browser and navigate to `http://127.0.0.1:5000/`
4. Choose one of the input methods:

   **Method 1: Upload a CSV file**
   - Select a CSV file with the following format:
     ```
     name,ip_address
     example-01,1.1.10.10
     example-02,1.1.20.20
     ```
   - Optionally fill in the RADIUS and TACACS secrets (or leave blank)
   - Click the "Convert to XML" button

   **Method 2: Enter data manually**
   - Click on the "Enter Data Manually" tab
   - Type or paste your name,IP pairs in the text box (one per line):
     ```
     example-01,1.1.10.10
     example-02,1.1.20.20
     ```
   - Optionally fill in the RADIUS and TACACS secrets (or leave blank)
   - Click the "Convert to XML" button

5. The application will generate and download an XML file with the specified format

## Sample Output XML

If you enter custom secrets (for example, "MyRadiusSecret" and "MyTacacsSecret"):

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<TipsContents xmlns="http://www.avendasys.com/tipsapiDefs/1.0">
  <TipsHeader exportTime="Fri Feb 28 17:05:11 EST 2025" version="6.11"/>
  <NadClients>
    <NadClient description="" name="example-01" nadGroups="" coaPort="3799" radsecEnabled="false" coaCapable="true" vendorName="Cisco" tacacsSecret="MyTacacsSecret" radiusSecret="MyRadiusSecret" ipAddress="1.1.10.10"/>
    <NadClient description="" name="example-02" nadGroups="" coaPort="3799" radsecEnabled="false" coaCapable="true" vendorName="Cisco" tacacsSecret="MyTacacsSecret" radiusSecret="MyRadiusSecret" ipAddress="1.1.20.20"/>
  </NadClients>
</TipsContents>
```

If you leave the secrets blank:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<TipsContents xmlns="http://www.avendasys.com/tipsapiDefs/1.0">
  <TipsHeader exportTime="Fri Feb 28 17:05:11 EST 2025" version="6.11"/>
  <NadClients>
    <NadClient description="" name="example-01" nadGroups="" coaPort="3799" radsecEnabled="false" coaCapable="true" vendorName="Cisco" tacacsSecret="" radiusSecret="" ipAddress="1.1.10.10"/>
    <NadClient description="" name="example-02" nadGroups="" coaPort="3799" radsecEnabled="false" coaCapable="true" vendorName="Cisco" tacacsSecret="" radiusSecret="" ipAddress="1.1.20.20"/>
  </NadClients>
</TipsContents>
```

## Notes

- The application automatically handles the header row in the CSV if present
- The standard values for TACACS and RADIUS secrets are included automatically as "20t!ntt@k19"
- The current date and time will be used in the XML export timestamp
