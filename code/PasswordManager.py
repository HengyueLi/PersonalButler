#!/usr/bin/env python3

#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# Class:   PasswordManager
#──────────────────────────
# Author:  Hengyue Li
#──────────────────────────
# Version: 2018/10/23
#──────────────────────────
# discription:
#
#
#──────────────────────────
# Used :
import EncryDB,os
#──────────────────────────
# Interface:
#
#        [ini]
#
#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════



class PasswordManager(EncryDB):

    def __init__(self,key = ''):
        PWD = self.GetFolderPath()
        PasswordFile = os.path.join( PWD , 'Data' , 'Password.mimi'  )
        super().__init__(PasswordFile,key = key)
        self.CreateTableIfNotExist('table_password')
        
