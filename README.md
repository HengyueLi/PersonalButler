## PersonalButler

It is a complete application contains three major functions: a **password manager**, a **contact manager** and a **diary manager**. All the data is stored in an encrypted file with AES256. The application loads the data from the disk to memory directly (without any other temporary unencrypted file). In this way, all the personal information is protected. The application set-up a local web server to offer a simple GUI.

### Install
This is a 'python3' application. Download the code folder and install the requirement-file: `pip install -r requirments.txt`. Or optionally, one can use an isolated environment.

## Usage

### set-up and  shut-down

Use command `python main.py` to start the server. After that, one open browser and visit `http://0.0.0.0:4999`. All the personal data will be saved in the file 'profile.dat'. Notice that the position of the file is the CWD (current working directory). When finished using the server, one must remember to shut down the server by simply click the shutdown-button at the up-right side of the page.

### create a new profile

When fist login the server, one will go to a signup page. A new password is required to create a new profile. When it has done, one goes to the profile page. In the navbar, there are `setting`, `Password`, `Relation` and `Diary` button on the left side and a shutdown-button on the right side.

#### Password manager

All the password are classified. For each item, one can store key-value pairs.

#### Relation manager

One can add records for each relation.

#### Diary

Simple usage.


--------------------

## 个人信息管家  
一个带GUI的个人信息安全管理软件。数据以字符串的形式由AES256加密直接存储在磁盘上，保证硬盘上的内容总是加密啊的，非加密的信息只缓存在内存当中，杜绝中间过程的落盘行为。目前支持三个功能：`密码管理`，`联系人管理`和`日记管理`。因为自己对信息安全比较在意，实在不放心用第三方软件，所以自己花功夫做了这么个玩意，自己也一直在使用。现在加上一个中文说明，喜欢有感冒的同学使用并且一起完善。因为自己也不是专业搞开发的，所以还要多交流学习。


### 安装和使用
这是一个`Python3`程序。下载code之后通过`requirement`文件安装：  
```
pip install -r requirments.txt
```
或者自己使用虚拟环境。
使用方法是直接运行`main.py`,然后从网页中打开`http://localhost:4999/`（可以编辑该文件调调参数）。使用完毕记得点击退出按钮安全的退出。直接杀死程序也没有问题。忘了关就不安全了。  
剩下的过程大约自己摸索就可以了，细节请看英文说明。
