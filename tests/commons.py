import uuid
from datetime import datetime, timezone
from pathlib import Path

from dateutil.parser import isoparse

SOURCE = Path(__file__).parent.parent / 'src'


class InMemoryHvacClient:
    """
    This is in-memory mock for hvac.Client. This implementation should be
    enough for our purposes because i cannot find a lib that can do that
    """
    __data = {}

    def __init__(self, url=None, token=None, *args, **kwargs):
        class Container: pass

        self.secrets = Container()
        self.secrets.kv = Container()
        self.secrets.kv.v2 = Container()
        self.secrets.kv.v2.read_secret_version = self._read_secret_version
        self.secrets.kv.v2.create_or_update_secret = self._create_or_update_secret
        self.secrets.kv.v2.update_metadata = self._update_metadata
        self.secrets.kv.v2.delete_metadata_and_all_versions = self._delete_metadata_and_all_versions
        self.sys = Container()
        self.sys.enable_secrets_engine = self._enable_secret_engine
        self.sys.list_mounted_secrets_engines = self._list_mounted_secrets_engines

    @classmethod
    def reset(cls):
        cls.__data.clear()

    def is_authenticated(self):
        return True

    @staticmethod
    def _dt():
        return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    def _create_or_update_secret(self, path, secret, cas=None,
                                 mount_point='secret'):
        dt = self._dt()
        self.__class__.__data[(path, mount_point)] = (secret, dt)
        return {
            'request_id': str(uuid.uuid4()),
            'lease_id': '', 'renewable': False, 'lease_duration': 0,
            'data': {
                'data': secret,
                'metadata': {
                    'created_time': dt,
                    'custom_metadata': None, 'deletion_time': '',
                    'destroyed': False, 'version': 1
                }
            },
            'wrap_info': None,
            'warnings': None,
            'auth': None,
            'mount_type': mount_point
        }

    def _update_metadata(self, path, *args, **kwargs):
        pass

    def _read_secret_version(self, path, mount_point='secret'):
        item = self.__class__.__data.get((path, mount_point))
        if not item:
            from hvac.exceptions import InvalidPath
            raise InvalidPath
        return {
            'request_id': str(uuid.uuid4()),
            'lease_id': '', 'renewable': False, 'lease_duration': 0,
            'data': {
                'data': item[0],
                'metadata': {
                    'created_time': item[1],
                    'custom_metadata': None,
                    'deletion_time': '',
                    'destroyed': False, 'version': 1
                }
            },
            'wrap_info': None,
            'warnings': None, 'auth': None, 'mount_type': mount_point
        }

    def _delete_metadata_and_all_versions(self, path, mount_point='secret'):
        self.__class__.__data.pop((path, mount_point), None)
        return True

    def _enable_secret_engine(self, *args, **kwargs):
        pass

    def _list_mounted_secrets_engines(self):
        return ['secrets', 'kv']


def valid_isoformat(d):
    if not d: return False
    try:
        isoparse(d)
        return True
    except ValueError:
        return False
