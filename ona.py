#!/usr/bin/python
import csv
import MySQLdb
import getpass
import prettytable

dcmuser = raw_input("What is your dcm.pl username? ")
dcmpasswd = raw_input("What is your dcm.pl password?")

def addDevices():
    csvfile = 'newdev.csv'
    raw_input("Please fill out the file {0} with the appropriate values. (Hint: The type field can be found using option 1 on the main menu.) Press Enter to continue".format(csvfile))
    new_dev = csv.DictReader(open(csvfile, 'rb'), delimiter=',', quotechar='"')
    f = open('newdevices.txt', 'w')
    f.write("alias dcm.pl=\'/opt/ona/bin/dcm.pl -l {0} -p {1}\'\n".format(dcmuser, dcmpasswd))
    for row in new_dev:
        f.write("dcm.pl -r host_add host={0}.spartan-net.local ip={1} location={2} type={3}\n".format(row['hostname'],row['ip'],row['location']),row['type'])
    f.close
    
def addSubnet():
    csvfile = 'newsubnet.csv'
    raw_input("Please fill out the file {0} with the appropriate values. (Hint: The type field using option 3 on the main menu.) Press Enter to continue".format(csvfile))
    new_subnets = csv.DictReader(open(csvfile, 'rb'), delimiter=',', quotechar='"')
    f = open('newsubnets.txt', 'w')
    f.write("alias dcm.pl=\'/opt/ona/bin/dcm.pl -l {0} -p {1}\'\n".format(dcmuser, dcmpasswd))
    for row in new_subnets:
        f.write("dcm.pl -r subnet_add name={0} ip={1} netmask={2} type={3}\n".format(row['name'],row['ip'],row['netmask'],row['type']))
    f.close

def checkDeviceTypeID():
    #Get info to connect to the DB
    dbhost = raw_input("What is the IP of the DB server? ")
    dbuser = raw_input("What user should be used to connect to the DB? ")
    dbpass = getpass.getpass("What is the DB user's password? ")
    vendor = raw_input("What is the name of the device vendor (case sensitive)? ")
    db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass, db="ona_default_11")
    cur = db.cursor()
    cur.execute("SELECT t.id, v.name, m.name, r.name FROM device_types t INNER JOIN models m ON t.model_id = m.id INNER JOIN roles r ON t.role_id = r.id INNER JOIN manufacturers v ON m.manufacturer_id = v.id WHERE v.name = \'{0}\';".format(vendor))
    table = prettytable.PrettyTable(['ID', 'Manufacturer', 'Model', 'Role'])
    for row in cur.fetchall():
        table.add_row([row[0], row[1], row[2], row[3]])
    print table

def checkSubnetTypeID():
    #Get info to connect to the DB
    dbhost = raw_input("What is the IP of the DB server? ")
    dbuser = raw_input("What user should be used to connect to the DB? ")
    dbpass = getpass.getpass("What is the DB user's password? ")
    db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass, db="ona_default_11")
    cur = db.cursor()
    cur.execute("SELECT * FROM subnet_types;")
    table = prettytable.PrettyTable(['ID', 'Type'])
    for row in cur.fetchall():
        table.add_row([row[0], row[2]])
    print table
    
menu = 0
while  menu < 5:
    print("MAIN MENU")
    print("What would you like to do?")
    print("1) Find a device type ID")
    print("2) Add new devices")
    print("3) Find a subnet type ID")
    print("4) Add new subnets")
    print("5) Exit program")
    menu = int(raw_input())
    if menu == 1:
        checkDeviceTypeID()
    elif menu == 2:
        addDevices()
    elif menu == 3:
        checkSubnetTypeID()
    elif menu == 4:
        addSubnet()