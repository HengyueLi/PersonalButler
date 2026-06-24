import base64
import json
import os
import tempfile

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


class EncryptionAPI():
    _MAGIC = b"PERSONAL_BUTLER_V2\n"
    _FORMAT = "PersonalButler.encrypted-json"
    _VERSION = 2
    _SALT_SIZE = 16
    _NONCE_SIZE = 12
    _KEY_SIZE = 32
    _SCRYPT_N = 2 ** 15
    _SCRYPT_R = 8
    _SCRYPT_P = 1
    _MAX_SCRYPT_N = 2 ** 20

    @classmethod
    def IsUserNew(cls):
        # check if data exists.  return Ture if data is empty
        return not os.path.exists(cls.getDataSource())

    @staticmethod
    def getDataSource():
        return os.path.join(os.getcwd(), "profile.dat")

    def __init__(self, Password):
        self.Password = Password
        self.dataFile = self.getDataSource()
        self._db = None
        self._isconnected = False
        self._loaded_legacy = False

    def ResetPassword(self, Password):
        self._check_connected()
        self.Password = Password

    def getPassword(self) -> str:
        # Kept for the existing export/import page. The password is not stored
        # inside the encrypted data payload anymore.
        return self.Password

    def connect(self):
        if not os.path.exists(self.dataFile):
            self._db = self._new_db()
            self._isconnected = True
            return

        try:
            raw = self._read_file_bytes(self.dataFile)
            if raw.startswith(self._MAGIC):
                self._db = self._decrypt_v2(raw, self.Password)
                self._loaded_legacy = False
            else:
                raise ValueError('Unsupported data file format')
            self._normalize_db()
            self._isconnected = True
        except Exception:
            self._db = None
            self._isconnected = False

    def IsConnected(self):
        return self._isconnected

    def Save(self):
        self._check_connected()
        encrypted = self._encrypt_v2(self._db, self.Password)
        self._atomic_write(self.dataFile, encrypted)
        self._loaded_legacy = False

    def CreateTableIfNotExist(self, tableName, isSorted=False):
        # if isSorted, two keys named "key1" and "key2" is used to identify one item. These like (partition-key and sort-key)
        # if not, one key named "key1" is used to indentify one item, work as a primary-key
        self._check_connected()
        tables = self._tables()
        if tableName not in tables:
            tables[tableName] = {'isSorted': isSorted, 'data': {}}

    def DropTableIfExist(self, tableName):
        # delete table with all its data
        self._check_connected()
        self._tables().pop(tableName, None)

    def InsertIntoTable(self, tableName, data, key1, key2=None):
        # if key exist, update the item
        tbDict = self._get_table(tableName)
        isSorted = tbDict['isSorted']
        db = tbDict['data']
        if key2 is None:
            db[key1] = data
        else:
            if key1 not in db:
                db[key1] = {}
            db[key1][key2] = data

    def DeleteOneItemFromTable(self, tableName, key1, key2=None):
        tbDict = self._get_table(tableName)
        isSorted = tbDict['isSorted']
        db = tbDict['data']
        if isSorted:
            del db[key1][key2]
        else:
            del db[key1]

    def selectItems(self, tableName, key1, key2=None) -> list:
        # if only input key1, it is the primarykey, return list should contain only 1 item
        tbDict = self._get_table(tableName)
        isSorted = tbDict['isSorted']
        db = tbDict['data']
        if isSorted:
            if key2 is None:
                partition = db.get(key1, {})
                return [partition[key2] for key2 in partition]
            else:
                g = db.get(key1, {}).get(key2, None)
                return [g] if g is not None else []
        else:
            return [db[key1]]

    def SelectDistinctKey1(self, tableName) -> list:
        # use key1 (primary key) as filter
        # equally in sql: select DISTINCT key1 from tableName
        tbDict = self._get_table(tableName)
        db = tbDict['data']
        return list(db.keys())

    def getAllItems(self, tableName) -> list:
        # return list of data, data is dictionary
        tbDict = self._get_table(tableName)
        isSorted = tbDict['isSorted']
        db = tbDict['data']
        if isSorted:
            r = []
            for key1 in db:
                r += [db[key1][key2] for key2 in db[key1]]
            return r
        else:
            return [db[k] for k in db]

    @classmethod
    def _new_db(cls):
        return {'FILE_DB_CONFIG': {'version': cls._VERSION}, 'FILE_DB_TABLE': {}}

    def _normalize_db(self):
        if not isinstance(self._db, dict):
            raise ValueError('Invalid data file')
        if not isinstance(self._db.get('FILE_DB_CONFIG'), dict):
            raise ValueError('Invalid data file config')
        if not isinstance(self._db.get('FILE_DB_TABLE'), dict):
            raise ValueError('Invalid data file tables')

    def _tables(self):
        return self._db['FILE_DB_TABLE']

    def _get_table(self, tableName):
        self._check_connected()
        tbDict = self._tables().get(tableName, None)
        if tbDict is None:
            raise KeyError(tableName)
        return tbDict

    def _check_connected(self):
        if not self._isconnected or self._db is None:
            raise PermissionError('Data file is not connected.')

    @classmethod
    def _encrypt_v2(cls, data, password):
        salt = os.urandom(cls._SALT_SIZE)
        nonce = os.urandom(cls._NONCE_SIZE)
        header = {
            'format': cls._FORMAT,
            'version': cls._VERSION,
            'kdf': {
                'name': 'scrypt',
                'salt': cls._b64e(salt),
                'n': cls._SCRYPT_N,
                'r': cls._SCRYPT_R,
                'p': cls._SCRYPT_P,
                'length': cls._KEY_SIZE,
            },
            'cipher': {
                'name': 'AES-256-GCM',
                'nonce': cls._b64e(nonce),
            },
        }
        key = cls._derive_key(password, salt, cls._SCRYPT_N, cls._SCRYPT_R, cls._SCRYPT_P)
        aad = cls._canonical_json(header)
        plaintext = cls._canonical_json(data)
        ciphertext = AESGCM(key).encrypt(nonce, plaintext, aad)
        payload = {'header': header, 'ciphertext': cls._b64e(ciphertext)}
        return cls._MAGIC + cls._canonical_json(payload)

    @classmethod
    def _decrypt_v2(cls, raw, password):
        payload = json.loads(raw[len(cls._MAGIC):].decode('utf-8'))
        header = payload['header']
        cls._validate_header(header)
        kdf = header['kdf']
        cipher = header['cipher']
        salt = cls._b64d(kdf['salt'])
        nonce = cls._b64d(cipher['nonce'])
        ciphertext = cls._b64d(payload['ciphertext'])
        key = cls._derive_key(password, salt, kdf['n'], kdf['r'], kdf['p'])
        aad = cls._canonical_json(header)
        try:
            plaintext = AESGCM(key).decrypt(nonce, ciphertext, aad)
        except InvalidTag as exc:
            raise ValueError('Invalid password or corrupted data file') from exc
        return json.loads(plaintext.decode('utf-8'))

    @classmethod
    def _validate_header(cls, header):
        if header.get('format') != cls._FORMAT or header.get('version') != cls._VERSION:
            raise ValueError('Unsupported data file format')
        kdf = header.get('kdf', {})
        cipher = header.get('cipher', {})
        if kdf.get('name') != 'scrypt' or cipher.get('name') != 'AES-256-GCM':
            raise ValueError('Unsupported encryption settings')
        if kdf.get('length') != cls._KEY_SIZE:
            raise ValueError('Unsupported key size')
        n = kdf.get('n')
        r = kdf.get('r')
        p = kdf.get('p')
        if not isinstance(n, int) or n < 2 ** 14 or n > cls._MAX_SCRYPT_N or n & (n - 1):
            raise ValueError('Invalid scrypt N')
        if not isinstance(r, int) or r < 1 or r > 16:
            raise ValueError('Invalid scrypt r')
        if not isinstance(p, int) or p < 1 or p > 4:
            raise ValueError('Invalid scrypt p')
        salt = cls._b64d(kdf.get('salt', ''))
        nonce = cls._b64d(cipher.get('nonce', ''))
        if len(salt) < cls._SALT_SIZE or len(salt) > 64:
            raise ValueError('Invalid salt')
        if len(nonce) != cls._NONCE_SIZE:
            raise ValueError('Invalid nonce')

    @classmethod
    def _derive_key(cls, password, salt, n, r, p):
        kdf = Scrypt(salt=salt, length=cls._KEY_SIZE, n=n, r=r, p=p)
        return kdf.derive(password.encode('utf-8'))

    @staticmethod
    def _canonical_json(data):
        return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

    @staticmethod
    def _b64e(data):
        return base64.b64encode(data).decode('ascii')

    @staticmethod
    def _b64d(data):
        return base64.b64decode(data.encode('ascii'), validate=True)

    @staticmethod
    def _read_file_bytes(path):
        with open(path, 'rb') as f:
            return f.read()

    @classmethod
    def _atomic_write(cls, path, data):
        folder = os.path.dirname(os.path.abspath(path)) or os.getcwd()
        basename = os.path.basename(path)
        fd, tmp_path = tempfile.mkstemp(prefix='.' + basename + '.', suffix='.tmp', dir=folder)
        try:
            with os.fdopen(fd, 'wb') as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            try:
                os.chmod(tmp_path, 0o600)
            except OSError:
                pass
            os.replace(tmp_path, path)
            cls._fsync_dir(folder)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    @staticmethod
    def _fsync_dir(folder):
        flags = os.O_RDONLY
        if hasattr(os, 'O_DIRECTORY'):
            flags |= os.O_DIRECTORY
        try:
            fd = os.open(folder, flags)
        except OSError:
            return
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
