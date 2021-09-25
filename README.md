## PersonalButler

It is a complete application with UI that contains three major functions: a **password manager (password-keeper)**, a **contact manager** and a **diary manager**. All the data is stored in an encrypted file with AES256 and offline. The application loads the data from the disk to memory directly (without any other temporary unencrypted file). In this way, all personal information is protected. **Security is the first thing to be considered for designing this app**. You can define your own encryption method with a few modifications.

### Install
**method 1: Download source code**  
Download the code folder and install the requirement-file: `pip install -r requirments.txt`.

**method 2: Download exe**  
Just download the bin file and run it.

[download it here](https://github.com/HengyueLi/PersonalButler/releases)

## Usage

### setup and  shutdown

Use command `python main.py` to start the server. After that, open the browser and visit `http://localhost:4999`. All the personal data will be saved in the file `profile.dat` at CWD (current working directory). When finished using the server, one must remember to shut down the server by simply click the shutdown button at the UI.

### create a new profile

When the first login into the server, one will go to a signup page. A new password is required to create a new profile. When it has been done, one goes to the profile page. In the navbar, there are `setting`, `Password`, `Relation` and `Diary` buttons on the left side and a shutdown button on the right side.

#### Password manager (Password-keeper)

All the passwords are classified. Compared with the general password-keeper which can only store a password, here one can store key-value pairs defined by the user.

#### Relation manager

One can add records for each relation.

#### Diary

Simple usage.

### Advanced Usage
You can use another encryption method by modifying the default encryption method `/code/DataAPI/encryptionAPI.py`. An example of using SQL cipher is given by `/code/DataAPI/encryptionAPI_sqlcipher.py`. If you want to try this example, rename it to `encryptionAPI.py` and install the [dependence](https://pypi.org/project/pysqlcipher3/).

--------------------

## 个人信息管家  
一个带UI的个人信息安全管理软件。数据以字符串的形式由AES256加密直接存储在磁盘上，保证硬盘上的内容总是加密啊的，非加密的信息只缓存在内存当中，杜绝中间过程的落盘行为。目前支持三个功能：`密码管理`，`联系人管理`和`日记管理`。因为自己对信息安全比较在意，实在不放心用第三方软件，所以自己花功夫做了这么个玩意，自己也一直在使用。提供自定义的加密接口，不放心的同学可以自己修改成自己的版本（自带一个sqlcipher的例子）。希望有感兴趣的同学一起使用并且完善。因为自己也不是专业搞开发的，所以还要多交流学习。


### 安装
**方案1:下载源码**   
这是一个`Python3`程序。下载code之后通过`requirement`文件安装：  
```
pip install -r requirments.txt
```
或者自己使用虚拟环境。  
**方案2:下载exe文件**   
推荐在终端运行，但是也可鼠标双击。  
[下载](https://github.com/HengyueLi/PersonalButler/releases)

### 使用  
使用方法是直接运行`main.py`,然后从网页中打开`http://localhost:4999/`（可以编辑该文件调调参数）。使用完毕记得点击退出按钮安全的退出。直接杀死程序也没有问题。忘了关就不安全了。  
剩下的过程大约自己摸索就可以了，细节请看英文说明。

### 用户自定义加密方法
如果不放心别人用的加密方式，你可以使用你自己的方法加密。方法是修改`/code/DataAPI/encryptionAPI.py`接口。自带一个使用sqlcipher的例子供参考，`/code/DataAPI/encryptionAPI_sqlcipher.py`,重命名后可以跑（不过要自己安装[依赖](https://pypi.org/project/pysqlcipher3/)）
