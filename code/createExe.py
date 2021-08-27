#!/usr/bin/env python3

import sys,shutil,os,datetime





def getplatformOS():
    return sys.platform


def getexeName(prefix):
    OSname = getplatformOS()
    if OSname =='win32':
        return prefix + '_win32.exe'
    elif OSname =='darwin':
        return prefix + '_darwin.app'
    else:
        print('exeName not defined for OS ='+str(OSname))



PREFIX = 'butler_' + datetime.datetime.now().strftime("%Y%m%d")
DIR = os.path.dirname(os.path.abspath(__file__))
pyMAIN = os.path.join(DIR,'main.py')
exeName = getexeName(PREFIX)

staticPath = os.path.join(DIR,'static')
templatesPath = os.path.join(DIR,'templates')

if getplatformOS() == 'win32':
    compileCMD = '''pyinstaller --add-data "static;static" --add-data "templates;templates" -F -n {} main.py'''.format(exeName)
elif getplatformOS() == 'darwin':
    compileCMD = '''pyinstaller --add-data "static:static" --add-data "templates:templates"  -F -n {}  main.py'''.format(exeName)




print('CMD='+str(compileCMD))
os.system(compileCMD)

#----
try:
    os.makedirs(DIR,'bin')
except:
    pass
try:
    os.remove( os.path.join(DIR,'bin',exeName)  )
except:
    pass
os.rename( os.path.join(DIR,'dist',exeName)   ,   os.path.join(DIR,'bin',exeName)   )
shutil.rmtree(os.path.join(DIR,'dist'))
shutil.rmtree(os.path.join(DIR,'build'))
os.remove(os.path.join(DIR,exeName+".spec"))
