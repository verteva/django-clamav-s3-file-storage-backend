# django-clamav-s3-file-storage-backend
An extension of `storages.backends.s3boto3.S3Boto3Storage` that scans files using ClamAV pre-upload.

## Prerequisites

A `clamav` server must be running and a connection available to the Django app.

## Installation

Standard python installation:
        `python setup.py install`
or install using pip:
        `pip install django-clamav-s3-file-storage-backend`.

## Configuration

This storage backend is a drop in replacement for `S3Boto3Storage`.

Connection parameters to the clamav server can be changed by setting the Django setting CLAMD_CONNECTION to a dictionary containing configuration parameters. Valid keys are 'host', 'port', and 'timeout'. All of these keys are optional.

```
CLAMD_CONNECTION = { 
    "host": "notarealhost",    
    "port": 1234,
    "timeout": 20,
}
```

If the CLAMD_CONNECTION setting is not defined, or one of the aforementioned keys is missing from the settings dictionary, fallback defaults are used. These defaults are defined here: https://github.com/duggan/pyclamd/blob/master/pyclamd.py#L574.

## Tests

To run the tests, setup a virtualenv with the required packages (see `requirements.txt`) and then cd into the project directory and run `./runtests.sh`.

## Error handling

This storage backend will raise a `ClamAvScanFailed` exception if the scan failed. The file will not be uploaded in this case.

## Acknowledgements 

Boilerplate code copied from https://github.com/musashiXXX/django-clamav-upload .
