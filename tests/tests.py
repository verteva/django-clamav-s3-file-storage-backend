import pyclamd
import tempfile
from django.test import TestCase
import clamav_s3_storage_backend
import clamav_s3_storage_backend.backend
from django.core.files import File
from unittest import mock

from clamav_s3_storage_backend.exceptions import ClamAvScanFailed

class ClamavS3Boto3StorageTests(TestCase):
    def setUp(self):
        self.storage = clamav_s3_storage_backend.backend.ClamAvS3Boto3Storage()
        self.storage._connections.connection = mock.MagicMock()
        self.cd = pyclamd.ClamdAgnostic()


    def test_file_with_virus(self):
        # create file (bytestring) with eicar flag
        with tempfile.NamedTemporaryFile() as file_with_virus:
            file_with_virus.write(self.cd.EICAR())
            file_with_virus.flush()
            file_with_virus.seek(0)

            with self.assertRaises(ClamAvScanFailed):
                self.storage.save('file/with/virus', file_with_virus)

    def test_file_without_virus(self):
        """
        Test saving a file
        """
        


        # create file (bytestring) with eicar flag
        name='file/with/no/virus'
        with tempfile.NamedTemporaryFile() as file_with_no_virus:
            file_content=b'This is not a virus'
            file_with_no_virus.write(file_content)
            file_with_no_virus.flush()
            file_with_no_virus.seek(0)
            self.storage.save(name, file_with_no_virus)
            self.storage.bucket.Object.assert_called_once_with(name)
                
            self.storage.bucket.Object.assert_called_once_with(name)

            obj = self.storage.bucket.Object.return_value
            blahfioe=File(file_with_no_virus)
            blahfioe.name=name
            self.assertEqual(obj.upload_fileobj.call_args[0][0].read(), file_content)
            