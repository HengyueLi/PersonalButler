## PersonalButler

It is a complete application contains three major functions: a **password manager**, a **contact manager** and a **diary manager**. All the data is stored in an encrypted file with AES256. The application loads the data from the disk to memory directly (without any other temporary unencrypted file). In this way, all the personal information is protected. The application set-up a local web server to offer a simple GUI.

### Install
This is a 'python3' application. Download the code folder and install the requirement-file: `pip install -r requirments.txt`. Or optionally, one can use an isolated environment.

## Usage

Use command `python main.py` to start the server. After that, one open browser and visit `http://0.0.0.0:4999`. All the personal data will be saved in the file 'profile.dat'. Notice that the position of the file is the CWD (current working directory). When finished using the server, one must remember to shut down the server by simply click the shutdown-button at the up-right side of the page.   
