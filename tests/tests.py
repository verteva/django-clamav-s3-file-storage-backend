from contextlib import contextmanager
import pyclamd
import tempfile
from django.test import TestCase, override_settings
import clamav_s3_storage_backend
import clamav_s3_storage_backend.backend
from unittest import mock

from clamav_s3_storage_backend.exceptions import ClamAvScanFailed


EICAR_BYTESTRING = None  # this will be overwritten during the test


@contextmanager
def safe_file():
    with tempfile.NamedTemporaryFile() as f:
        file_content = b"This is not a virus"
        f.write(file_content)
        f.flush()
        f.seek(0)
        yield f


@contextmanager
def eicar_test_file():
    # Creates an EICAR test file.
    # This file is used to test antivirus software.
    # create file (bytestring) with eicar flag

    with tempfile.NamedTemporaryFile() as f:
        f.write(EICAR_BYTESTRING)
        f.flush()
        f.seek(0)
        yield f


class ClamavS3Boto3StorageTests(TestCase):
    def setUp(self):
        self.storage = clamav_s3_storage_backend.backend.ClamAvS3Boto3Storage()
        self.storage._connections.connection = mock.MagicMock()
        self.cd = pyclamd.ClamdAgnostic()

        global EICAR_BYTESTRING
        EICAR_BYTESTRING = self.cd.EICAR()

    def test_file_with_virus(self):
        # create file (bytestring) with eicar flag
        with eicar_test_file() as f:
            with self.assertRaises(ClamAvScanFailed):
                self.storage.save("file/with/virus", f)

    def test_file_without_virus(self):
        """
        Test saving a file
        """

        name = "file/with/no/virus"
        with safe_file() as f:
            self.storage.save(name, f)
            self.storage.bucket.Object.assert_called_once_with(name)

    @override_settings(CLAMD_CONNECTION={"host": "notarealhost", "port": 1234})
    def test_bad_connection_parameters_result_in_connection_error(self):
        """Connection parameters to the ClamAV server shall be configurable through Django settings."""

        name = "file/with/no/virus"
        with safe_file() as f:
            with self.assertRaises(pyclamd.pyclamd.ConnectionError):
                self.storage.save(name, f)
