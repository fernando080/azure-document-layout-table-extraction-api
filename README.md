# Azure Document Layout Table Extraction API

This FastAPI application provides an API endpoint to extract tables information from uploaded documents using Azure Form Recognizer's `prebuilt-layout` model.

**IMPORTANT**: The azure model is able to extract other layout components like text, images, and handwriting. This project is focused on extracting tables from documents. Feel free to modify the code and include other layout components.

## Table of Contents
- Features
- Prerequisites
- Installation
- Configuration
- Api Usage
- Additional Notes

## Features
- **Document Analysis**: Analyzes documents to extract layout information, including tables and their cells.
- **Handwritten Content Detection**: Identifies if the document contains handwritten content.
- **Supports Multiple File Types**: Accepts PDF, JPEG, PNG, and TIFF files.
- **Asynchronous Processing**: Utilizes asynchronous programming for efficient I/O operations.

## Prerequisites
- Python 3.11 or higher
- **Azure Account**
- **Azure Form Recognizer Endpoint and Key**
- **Internet Connection**: Required to access Azure services.

## Installation
1. Clone the repository:
   ```bash
    git clone https://github.com/yourusername/azure-document-layout-table-extraction-api.git
    cd azure-ocument-layout-extraction-api
    ```
2. Install the required dependencies (poetry):
   ```bash
    poetry install
    ```
3. Activate the virtual environment:
   ```bash
   poetry shell
   ```
   
## Configuration
Create a `.env` file in the root directory and add the following environment variables:
   ```bash
    AZURE_FORM_RECOGNIZER_ENDPOINT=<your_form_recognizer_endpoint>
    AZURE_FORM_RECOGNIZER_KEY=<your_form_recognizer_key>
   ```
   
## Running the Application
Use the dockerfile to build the image and run the container:
   ```bash
    docker build -t azure-doc-extraction-api .
    docker run -p 8000:8000 --env-file .env azure-doc-extraction-api
   ```

## API Usage
### Endpoint: `/extract-layout`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameters**:
  - `file`: File to be uploaded (PDF, JPEG)

### Response
- **Content-Type**: application/json
- **Response**: JSON object containing the extracted tables information and details.

## Additional Notes
- **Table Content**: The API uses Azure Form Recognizer's `prebuilt-layout` model to detect tables content in the document.
- **Asynchronous Processing**: The Azure Form Recognizer client is used within an asynchronous context manager to handle I/O-bound operations efficiently.
- **Azure Services Limitations**: Ensure that your Azure account has the necessary permissions and resources to use the Form Recognizer service.
- **Logging**: Modify the `print` statements to proper logging if deploying to a production environment.