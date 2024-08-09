import requests
import os

# Find all files available in https://data.pandonia-global-network.org/calibrationfiles/
url = 'https://data.pandonia-global-network.org/calibrationfiles/'
response = requests.get(url)

files = [url + file for file in response.text.split('href="')[1:] if file.endswith('.txt')]

# Download all files to a directory called 'calibration_files', create it if it doesn't exist
if not os.path.exists('calibration_files'):
    os.makedirs('calibration_files')
    
for file in files:
    filename = file.split('/')[-1]
    filepath = os.path.join('calibration_files', filename)
    response = requests.get(file)
    with open(filepath, 'wb') as f:
        f.write(response.content)
    




 