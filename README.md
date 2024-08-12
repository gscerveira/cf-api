# Pandora Calibration File API

This package aims to provide a simple API for parsing the contents of Pandora calibration files, storing it in a database, allowing for it to be queried through HTTP requests.

## How to Use the Package

### Installation

To install the package, you need to have Docker installed on your machine. You can get it [here](https://docs.docker.com/get-docker/).

### Running the Application

To start the application, you will first need to build the Docker image. Run the following command from the root folder of the project:

#### For Unix-like systems (Linux, macOS):
```bash
docker build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -t cf-api .
```

#### For Windows:
```powershell
docker build --build-arg USER_ID=1000 --build-arg GROUP_ID=1000 -t cf-api .
```

After successfully building the image, and before running the container, create a docker volume to store the database data:

```bash
docker volume create cf-api-data
```

Then, you can run the container with the following command:

```bash
docker run -p 8000:8000 -v cf-api-data:/cf-api/data cf-api
```

### Using the API

#### Parsing Calibration Files

Before querying the calibration data, you need to parse and store the calibration data. To do this, you need to send a POST request to the following endpoint:

Using curl (Unix-like systems):
```bash
curl -X POST http://localhost:8000/parse_calibration_files/
```

Using PowerShell (Windows):
```powershell
Invoke-WebRequest -Method POST -Uri http://localhost:8000/parse_calibration_files/
```

Note that this should only be done once.

#### Querying Calibration Data

To query the stored data, you can send a GET request to the following endpoint (the examples below also use curl):

- To get all the calibration files:

  curl:
  ```bash
  curl -X GET http://localhost:8000/calibration_files/
  ```
  PowerShell:
  ```powershell
  Invoke-WebRequest -Method GET -Uri http://localhost:8000/calibration_files/
  ```

- To filter by pandora_id:
  curl:
  ```bash
  curl -X GET http://localhost:8000/calibration_files/?pandora_id=101
  ```
  PowerShell:
  ```powershell
  Invoke-WebRequest -Method GET -Uri http://localhost:8000/calibration_files/?pandora_id=101
  ```

- To filter by spectrometer_id:
  curl:
  ```bash
  curl -X GET http://localhost:8000/calibration_files/?spectrometer_id=1
  ```
  PowerShell:
  ```powershell
  Invoke-WebRequest -Method GET -Uri http://localhost:8000/calibration_files/?spectrometer_id=1
  ```

- To filter by version:
  curl:
  ```bash
  curl -X GET http://localhost:8000/calibration_files/?version=1
  ```
  PowerShell:
  ```powershell
  Invoke-WebRequest -Method GET -Uri http://localhost:8000/calibration_files/?version=1
  ```

- To filter by validity_date:
  curl:
  ```bash
  curl -X GET http://localhost:8000/calibration_files/?validity_date=2023-06-20
  ```
  PowerShell:
  ```powershell
  Invoke-WebRequest -Method GET -Uri http://localhost:8000/calibration_files/?validity_date=2023-06-20
  ```

- To filter by key:
  curl:
  ```bash
  curl -X GET "http://localhost:8000/calibration_files/?key=Indices%20of%20warm%20pixels"
  ```
  PowerShell:
  ```powershell
  Invoke-WebRequest -Method GET -Uri "http://localhost:8000/calibration_files/?key=Indices%20of%20warm%20pixels"
  ```

- To combine multiple filters:
  curl:
  ```bash
  curl -X GET "http://localhost:8000/calibration_files/?pandora_id=101&version=1&key=Indices%20of%20warm%20pixels"
  ```
  PowerShell:
  ```powershell
  Invoke-WebRequest -Method GET -Uri "http://localhost:8000/calibration_files/?pandora_id=101&version=1&key=Indices%20of%20warm%20pixels"
  ```

Note: You can paste the URLs into your web browser to see the results.