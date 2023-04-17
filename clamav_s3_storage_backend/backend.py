from typing import Optional
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import pyclamd

from clamav_s3_storage_backend.exceptions import ClamAvScanFailed


class ClamAvS3Boto3Storage(S3Boto3Storage):
    """Storage backend that scans the file for viruses prior to uploading."""

    def _save(self, name, content):
        scan_result_msg = self._scan_content(content)
        scan_passed = scan_result_msg is None

        if scan_passed:
            return super()._save(name, content)
        else:
            raise ClamAvScanFailed(
                f"Not uploading file. Virus scan failed. Message: {scan_result_msg}"
            )

    def _scan_content(self, content) -> Optional[str]:
        """Scan the provided filelike content

        Args:
            content (filelike): Content to scan

        Returns:
            Optional[str]: None if scan passed. Error message if scan failed.
        """
        kwargs={}

        try:
            clamd_settings=settings.CLAMD_CONNECTION
        except AttributeError:
            pass
        else:

        
        
        
            host = clamd_settings.get('host')
            port = clamd_settings.get('port')
            timeout = clamd_settings.get('timeout')

            
            if port:
                kwargs['port'] = port
            if host:
                kwargs['host'] = host
            if timeout:
                kwargs['timeout'] = timeout

        
        clamd_client = pyclamd.ClamdNetworkSocket(**kwargs)
        scan_result_msg = clamd_client.scan_stream(content)
        return scan_result_msg
