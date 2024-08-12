import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_calibration_files(limit=20):
    base_url = 'https://data.pandonia-global-network.org/calibrationfiles/'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    files = []
    for link in soup.select('a'):
        href = link.get('href')
        if href and href.endswith('.txt'):
            if 'disused' not in href:
                full_url = urljoin(base_url, href)
                files.append(full_url)
    
    return files[:limit]


def download_files(files):
    if not os.path.exists('calibration_files'):
        os.makedirs('calibration_files')
    
    for file in files:
        filename = file.split('/')[-1]
        filepath = os.path.join('calibration_files', filename)
        response = requests.get(file)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
        
if __name__ == "__main__":
    files_limit = int(input("Enter the number of files to download: "))
    files = get_calibration_files(files_limit)
    download_files(files)
    




 