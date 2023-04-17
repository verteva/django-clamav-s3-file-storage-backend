from typing import Optional
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import pyclamd

from clamav_s3_storage_backend.exceptions import ClamAvScanFailed


class ClamAvS3Boto3Storage(S3Boto3Storage):
    """Storage backend that scans the file for viruses prior to uploading."""

    def _save(self, name, content):
        virus_scan_result_msg = self._run_virus_scan(content)
        virus_scan_passed = virus_scan_result_msg is None

        if virus_scan_passed:
            return super()._save(name, content)
        else:
            raise ClamAvScanFailed(
                f"Not uploading file. Virus scan failed. Message: {virus_scan_result_msg}"
            )

    def _run_virus_scan(self, content) -> Optional[str]:
        """Scan the provided filelike content

        Args:
            content (filelike): Content to scan

        Returns:
            Optional[str]: None if scan passed. Error message if scan failed.
        """
        kwargs = {}

        try:
            connection_settings = settings.CLAMD_CONNECTION
        except AttributeError:
            pass
        else:
            host = connection_settings.get("host")
            port = connection_settings.get("port")
            timeout = connection_settings.get("timeout")

            if port:
                kwargs["port"] = port
            if host:
                kwargs["host"] = host
            if timeout:
                kwargs["timeout"] = timeout

        client = pyclamd.ClamdNetworkSocket(**kwargs)
        scan_result_msg = client.scan_stream(content)
        content.seek(0) 
        return scan_result_msg
