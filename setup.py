from setuptools import setup

setup(
    name='django-clamav-s3-file-storage-backend',
    version='0.0.01',
    packages=['clamav_s3_storage_backend'],
    url='https://github.com/nano/django-clamav-s3-file-storage-backend',
    download_url='https://github.com/nano/django-clamav-s3-file-storage-backend/tarball/0.0.1',
    license='LICENSE.txt',
    author='Edward Ong',
    author_email='edward.ong@nano.com.au',
    description='An extension of storages.backends.s3boto3.S3Boto3Storage that scans files using ClamAV pre-upload.',
    long_description='README.md',
    install_requires=[
        'Django < 4.0.0,>=3.0.0',
        'pyClamd==0.4.0',
        'django-storages==1.13.2',
        'boto3 > 1.20.*',
    ],
    keywords='clamav django storage s3 backend'
)
