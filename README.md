# PersonalButler

PersonalButler is a local-first personal information manager with a browser UI. It provides three core modules:

- **Password**: store password records as user-defined key-value pairs.
- **Relation**: manage contacts and notes about people.
- **Diary**: keep private diary entries.

The app runs locally as a Flask server and stores all application data in one encrypted file, `profile.dat`, in the current working directory. Decrypted data is kept in memory while the app is running and is not intentionally written to temporary plaintext files.

## Security Model

The default storage backend is implemented in `code/DataAPI/encryptionAPI.py`.

- Encryption: AES-GCM with a 256-bit key.
- Key derivation: Scrypt with a random salt per save.
- Nonce: random nonce per save.
- File format: encrypted JSON payload with a small public header.
- Save behavior: atomic file replacement to reduce the risk of corrupting `profile.dat` during updates.

The password protects the local data file. Keep it strong and keep a backup of `profile.dat`; losing the password means the encrypted data cannot be recovered.

## Installation

Use Python 3 and install the dependencies from the `code` directory:

```bash
cd code
python -m pip install -r requirements.txt
```

Prebuilt releases, if available, are published here:

https://github.com/HengyueLi/PersonalButler/releases

## Usage

Start the local server from the `code` directory:

```bash
python main.py
```

Then open:

```text
http://localhost:4999/
```

On first use, the app opens the sign-up page and asks for a password to create a new encrypted profile. After login, use the navbar to switch between `Password`, `Relation`, and `Diary`. Use the shutdown button in the UI when finished.

The encrypted data file is:

```text
code/profile.dat
```

The `Setting` menu includes import/export actions. Export writes decrypted data to disk, so use it only when you understand the risk and delete exported plaintext files when no longer needed.

## Custom Storage Backend

The storage API is intentionally isolated behind one class:

```text
code/DataAPI/encryptionAPI.py
```

To write your own backend, keep the class name `EncryptionAPI` and implement the same public methods. Then either replace `code/DataAPI/encryptionAPI.py`, or import your new class in `code/main.py`.

The app expects the backend to behave like a small table store:

- A backend instance is created with `EncryptionAPI(password)`.
- `connect()` loads or initializes the database.
- `IsConnected()` returns whether the password/data file was accepted.
- `Save()` persists all current data.
- `ResetPassword(password)` changes the password used by later saves.
- `getPassword()` returns the active password for the current import/export workflow.
- `IsUserNew()` returns `True` when no data source exists.

The table API is:

- `CreateTableIfNotExist(tableName, isSorted=False)`
- `DropTableIfExist(tableName)`
- `InsertIntoTable(tableName, data, key1, key2=None)`
- `DeleteOneItemFromTable(tableName, key1, key2=None)`
- `selectItems(tableName, key1, key2=None) -> list`
- `SelectDistinctKey1(tableName) -> list`
- `getAllItems(tableName) -> list`

`data` is always a Python `dict`. When `isSorted=False`, `key1` is the primary key. When `isSorted=True`, the backend should store data by `(key1, key2)`, similar to a partition key and sort key.

Minimal behavior to preserve:

- Return lists from `selectItems()` and `getAllItems()`, even when there is only one result.
- For a missing sorted item, `selectItems()` should return an empty list.
- `InsertIntoTable()` should update an existing item with the same key.
- `Save()` should avoid leaving a partially written data file if possible.
- Do not write decrypted user data to temporary plaintext files.

Optional helper:

- `getDataSource()` is not required by the table API. It may return a human-readable path or description for startup messages. File-based backends can also use it internally from `IsUserNew()`.

An experimental SQLCipher example is available at:

```text
code/DataAPI/encryptionAPI_sqlcipher.py
```

SQLCipher can be harder to install across platforms, so the default backend avoids that dependency.

---

# 个人信息管家

PersonalButler 是一个本地运行的个人信息管理工具，带浏览器界面，主要包含三个模块：

- **Password**：密码管理，以自定义 key-value 形式保存记录。
- **Relation**：联系人管理，可以记录联系人信息和往来笔记。
- **Diary**：私人日记。

程序以本地 Flask 服务运行，所有业务数据保存在当前工作目录下的单个加密文件 `profile.dat` 中。程序运行时会把数据解密到内存里使用，不会主动把明文数据写入临时文件。

## 安全模型

默认存储后端在：

```text
code/DataAPI/encryptionAPI.py
```

当前实现：

- 使用 AES-GCM 加密，密钥长度 256 bit。
- 使用 Scrypt 从用户密码派生密钥。
- 每次保存使用随机 salt 和随机 nonce。
- `profile.dat` 中包含少量公开格式头和加密后的 JSON 数据。
- 保存时使用原子替换，降低更新过程中损坏数据文件的风险。

请使用足够强的密码，并定期备份 `profile.dat`。如果忘记密码，已加密数据无法恢复。

## 安装

进入 `code` 目录并安装依赖：

```bash
cd code
python -m pip install -r requirements.txt
```

如果需要预编译版本，可查看 release 页面：

https://github.com/HengyueLi/PersonalButler/releases

## 使用

在 `code` 目录启动：

```bash
python main.py
```

然后打开浏览器访问：

```text
http://localhost:4999/
```

第一次使用会进入注册页面，输入密码后会创建新的加密 profile。登录后可以通过导航栏切换 `Password`、`Relation`、`Diary`。使用结束后建议通过界面上的关机按钮关闭本地服务。

数据文件位置：

```text
code/profile.dat
```

`Setting` 菜单里有导入和导出功能。导出会把明文数据写到磁盘上，只应在确实需要备份或迁移时使用；导出后的明文文件应妥善保管并及时删除。

## 自定义存储后端

存储接口集中在一个类里：

```text
code/DataAPI/encryptionAPI.py
```

如果你希望替换加密方式、数据库类型或落盘格式，需要保留类名 `EncryptionAPI`，并实现同样的公开方法。之后可以直接替换 `code/DataAPI/encryptionAPI.py`，也可以在 `code/main.py` 中改成导入你自己的类。

程序把后端当作一个简单的表存储使用：

- `EncryptionAPI(password)`：使用密码创建后端对象。
- `connect()`：加载已有数据，或初始化新数据。
- `IsConnected()`：返回当前密码和数据源是否成功连接。
- `Save()`：保存当前全部数据。
- `ResetPassword(password)`：修改后续保存时使用的密码。
- `getPassword()`：返回当前密码，供现有导入/导出流程使用。
- `IsUserNew()`：没有数据源时返回 `True`。

表操作接口如下：

- `CreateTableIfNotExist(tableName, isSorted=False)`
- `DropTableIfExist(tableName)`
- `InsertIntoTable(tableName, data, key1, key2=None)`
- `DeleteOneItemFromTable(tableName, key1, key2=None)`
- `selectItems(tableName, key1, key2=None) -> list`
- `SelectDistinctKey1(tableName) -> list`
- `getAllItems(tableName) -> list`

其中 `data` 始终是 Python `dict`。当 `isSorted=False` 时，`key1` 是主键；当 `isSorted=True` 时，需要按 `(key1, key2)` 存储，类似 partition key + sort key。

实现时建议保持这些行为：

- `selectItems()` 和 `getAllItems()` 必须返回 list，即使只有一条结果。
- sorted 表中找不到指定条目时，`selectItems()` 返回空 list。
- `InsertIntoTable()` 遇到相同 key 时应覆盖旧数据。
- `Save()` 尽量保证原子写入，避免写到一半损坏数据文件。
- 不要把解密后的用户数据写入临时明文文件。

可选辅助接口：

- `getDataSource()` 不是表存储 API 的必要接口。它可以返回一个便于阅读的数据源路径或描述，用于启动日志显示；文件型后端也可以在自己的 `IsUserNew()` 内部复用它。

项目中保留了一个 SQLCipher 示例：

```text
code/DataAPI/encryptionAPI_sqlcipher.py
```

不过 SQLCipher 在不同平台上的安装成本较高，因此默认后端没有依赖它。
