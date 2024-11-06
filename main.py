from fastapi import FastAPI, File, UploadFile, HTTPException
from azure.ai.formrecognizer.aio import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Retrieve environment variables
endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

if not endpoint or not key:
    raise ValueError("Please set the AZURE_FORM_RECOGNIZER_ENDPOINT and AZURE_FORM_RECOGNIZER_KEY environment variables in the .env file.")


@app.post("/extract-layout")
async def extract_layout(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png", "image/tiff"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Supported types: PDF, JPEG, PNG, TIFF.")

    try:
        contents = await file.read()

        # Initialize the client within an async context manager
        async with DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        ) as document_analysis_client:

            poller = await document_analysis_client.begin_analyze_document(
                model_id="prebuilt-layout", document=contents
            )
            result = await poller.result()

        # Analyze whether the document contains handwritten content.
        if any([style.is_handwritten for style in result.styles]):
            print("Document contains handwritten content")
        else:
            print("Document does not contain handwritten content")

        table_data = []

        for page in result.pages:
            # Check for tables in the page
            if not page.tables:
                continue

            page_info = {
                "page_number": page.page_number,
                "width": page.width,
                "height": page.height,
                "unit": page.unit,
                "tables": []
            }

            # Extract tables
            for table in result.tables:
                for region in table.bounding_regions:
                    if region.page_number == page.page_number:
                        table_info = {
                            "row_count": table.row_count,
                            "column_count": table.column_count,
                            "cells": [],
                            "bounding_box": [[point.x, point.y] for point in region.polygon]
                        }
                        for cell in table.cells:
                            if cell.bounding_regions[0].page_number == page.page_number:
                                cell_info = {
                                    "content": cell.content,
                                    "row_index": cell.row_index,
                                    "column_index": cell.column_index,
                                    "row_span": cell.row_span,
                                    "column_span": cell.column_span,
                                    "bounding_box": [[point.x, point.y] for region in cell.bounding_regions for point in region.polygon]
                                }
                                table_info["cells"].append(cell_info)
                        page_info["tables"].append(table_info)
                        break  # Avoid duplicate entries

            table_data.append(page_info)

        return {
                "tables": table_data,
                }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
