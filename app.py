# import requests
# import geocoder
import json
from retrying import retry
from flask import Flask, request, render_template
import location_obfuscation  # Import your script as a module
import kAnonymity

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        # Create an instance of the location_obfuscation class
        location_processor = location_obfuscation.location_obfuscation(float(latitude), float(longitude))
        resp = location_processor.get_location() 
        resp = json.loads(resp.text)
        exact_loc = resp["results"][1]["formatted_address"]
        print("exactLocation:" + exact_loc)
        obfuscated_area = location_processor.find_obfuscated_area()
        print("ob-area :" + obfuscated_area)
        return render_template('result.html', latitude = latitude, longitude= longitude, exact_loc=exact_loc, obfuscated_area=obfuscated_area)
    
    return render_template('index.html')

@app.route('/submitKAnonymity', methods=['GET', 'POST'])
def submitKAnonymity():
    if request.method == 'POST':
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        kValue = request.form.get('kValue')
        radius = request.form.get('radius')
        # Create an instance of the location_obfuscation class
        kAnon_processor = kAnonymity.kAnonymity(float(latitude), float(longitude), int(kValue), float(radius))
        resp = kAnon_processor.fetch_user_address_from_coordinates() 
        resp = json.loads(resp.text)
        exact_loc = resp["results"][1]["formatted_address"]
        dummyAddresses = kAnon_processor.generate_dummy_locations()
        return render_template('result-kAnon.html', exact_loc=exact_loc, dummyAddresses=dummyAddresses, 
                               latitude = latitude, longitude= longitude, radius = radius, kValue = kValue )
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
