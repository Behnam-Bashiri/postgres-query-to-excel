from fetch import *


if __name__ == "__main__":
    key_fetch ={
        "host":"",
        "db":"",
        "user":"",
        "password":"",
        "execute":"",
        "excelName":""
    }
    for inputUser in key_fetch.keys():
       i = str(input("{}-> ".format(inputUser))) 
       key_fetch[inputUser] = i
    
    fetch(key_fetch)