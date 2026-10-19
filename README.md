# Spare Parts Automation

## Overview

A Python automation project for processing automotive spare parts supplier price lists and updating online listings.

The project automates a workflow that would otherwise require multiple manual steps, from retrieving supplier prices to generating and uploading the final XML file.

## Features

- Downloads supplier price lists from email
- Processes supplier data in Excel format
- Handles duplicate OEM part numbers by selecting the lowest available price
- Generates XML data for online listings
- Uploads the resulting file to Yandex Disk
- Runs the workflow from a single entry point

## Technologies

- Python
- Excel data processing
- XML parsing and generation
- Email automation
- API integration
- Yandex Disk

## How It Works

The entire workflow is launched by running `import_xml.py`.

The script coordinates the processing steps, reducing repetitive manual work and making the supplier price update process more consistent.

## Project Structure

- `import_xml.py` — main entry point for the automated workflow
- `download_email_prices.py` — retrieves supplier price lists from email
- `download_prices.py` — processes and retrieves price data
- `upload_yandex.py` — uploads the generated file to Yandex Disk

## Project Status

The project is under active development. Documentation and setup instructions will be expanded as the project evolves.