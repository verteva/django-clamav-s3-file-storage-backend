# django-clamav-s3-file-storage-backend
An extension of storages.backends.s3boto3.S3Boto3Storage that scans files using ClamAV pre-upload.

## Prerequisites

The ``clamav-daemon`` must be running on the local machine.

## Installation

Standard python installation:
        python setup.py install    
... or install using pip:
        pip install django-clamav-s3-file-storage-backend

## Configuration

This storage backend is a drop in replacement for S3Boto3Storage.

## Tests

To run the tests, setup a virtualenv with the required packages (see `requirements.txt`) and then cd into the project directory and run `./runtests.sh`.

## Error handling

This storage backend will raise a `ClamAvScanFailed` exception if the scan failed. The file will not be uploaded in this case.

## Acknowledgements 

Boilerplate code copied from https://github.com/musashiXXX/django-clamav-upload .

