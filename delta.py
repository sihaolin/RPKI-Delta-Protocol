# Import package
# system package
import sys
import os
import time

# function package
import xml.etree.ElementTree as ET  # this package be used to parse .xml file
import urllib  # this package be used to download files
import hashlib  # this pachage be used to get hash of the control file
from lxml import etree  # this package to create another node tree
import subprocess

# user package

# obtain and parse the DeltaConf.xml file
def delta_Read_Conf():
    try:
        tree = ET.parse('DeltaConf.xml')  # create structure tree of the .xml file
        root = tree.getroot()  # obtain root node
    except Exception, e:
        print "Error: cannot parse file!"  # warning user
        print e  # print error information
        sys.exit(1)
        
    notification_File_URL = []  # a list to record all URL of tal
    
    for child in root:
        # if found valid configuraion data 
        if child.find('notification').text != None and child.find('notify').text != None:
            url_Group = [child.tag]
            # record data by a tuple
            url_Pair = [(child.find('notification').tag, child.find('notification').text),
                        (child.find('notify').tag, child.find('notify').text)]
            
            url_Group.append(url_Pair)
            # record the list by a list
            notification_File_URL.append(url_Group)
            
    return notification_File_URL  # return the list value

def obtain_File(current_Node):
    # create folder to stor control file
    path = os.getcwd() + '/ControlFile'
    # if the path is exist
    if not os.path.exists(path):
        os.mkdir(path)  # create the path
    
    file_Name = current_Node[0] + '.xml'
    # structure file's location
    location = os.path.join(path, file_Name)
    
    try:
        urllib.urlretrieve(current_Node[1], location)
    except Exception, e:
        print "Error: cannot download file!"  # warning user
        print e  # print error information

def obtain_Hash_Sha256(file_Name):
    file_Path = os.getcwd() + '/ControlFile/'+file_Name
    with open(file_Path, 'rb') as f:  # open the binary file
        sha256_Object = hashlib.sha256()
        sha256_Object.update(f.read())  # submit the file
        HASH = sha256_Object.hexdigest()  # calculate the hash Value
        HASH = HASH.upper()
        
        return HASH
    
def validate_Notification_File_Format():
    path = os.getcwd() + '/ControlFile/notification.xml'
    
    if not os.path.exists(path):
        print 'Error: no notification file!'
        sys.exit(1)
    else: 
        try:
            tree = ET.parse(path)  # create structure tree of the .xml file
            root = tree.getroot()  # obtain root node
        except Exception, e:
            print "Error: cannot parse file!"  # warning user
            print e  # print error information
            sys.exit(1)
    
    try:       
        xml = etree.parse(path)
        xmlroot = xml.getroot()
        xmlns = xmlroot.nsmap
    except Exception, e:
        print "Error: cannot obtain the namespace of notification file!"  # warning user
        print e  # print error information
        sys.exit(1)
    
    xmlnsstring = '{' + xmlns[None] + '}'
    
    if xmlnsstring != '{http://www.ripe.net/rpki/rrdp}':
        print "Error: the namespace atribute of notification file is incorrect!"
        return False
    
    if root.get('version') == None:
        print 'Error: the version attribute of notification file is inexistence!'
        return False
    elif root.get('session_id') == None:
        print 'Error: the session_id attribute of notification file is inexistence!'
        return False
    elif root.get('serial') == None:
        print 'Error: the serial attribute of notification file is inexistence!'
        return False
    
    snapshot = root.findall(xmlnsstring + 'snapshot')
    for element in snapshot:
        if element.get('uri') == None:
            print 'Error: the uri attribute of snapshot file is inexistence!'
            return False
        elif element.get('hash') == None:
            print 'Error: the hash attribute of snapshot file is inexistence!'
            return False
        
    delta = root.findall(xmlnsstring + 'delta')
    for element in delta:
        if element.get('serial') == None:
            print 'Error: the serial attribute of delta file is inexistence!'
            return False
        elif element.get('uri') == None:
            print 'Error: the uri attribute of delta file is inexistence!'
            return False
        elif element.get('hash') == None:
            print 'Error: the hash attribute of delta file is inexistence!'
            return False
        
    return True

def validate_Notify_File_Format():
    path = os.getcwd() + '/ControlFile/notify.xml'
    
    if not os.path.exists(path):
        print 'Error: no notify file!'
        sys.exit(1)
    else: 
        try:
            tree = ET.parse(path)  # create structure tree of the .xml file
            root = tree.getroot()  # obtain root node
        except Exception, e:
            print "Error: cannot parse file!"  # warning user
            print e  # print error information
            sys.exit(1)
    
    try:       
        xml = etree.parse(path)
        xmlroot = xml.getroot()
        xmlns = xmlroot.nsmap
    except Exception, e:
        print "Error: cannot obtain the namespace of notify file!"  # warning user
        print e  # print error information
        sys.exit(1)
    
    xmlnsstring = '{' + xmlns[None] + '}'
    
    if xmlnsstring != '{http://www.ripe.net/rpki/rrdp}':
        print "Error: the namespace atribute of notify file is incorrect!"
        return False
    
    if root.get('version') == None:
        print 'Error: the version attribute of notify file is inexistence!'
        return False
    elif root.get('session_id') == None:
        print 'Error: the session_id attribute of notify file is inexistence!'
        return False
    elif root.get('serial') == None:
        print 'Error: the serial attribute of notify file is inexistence!'
        return False
    
    snapshot = root.findall(xmlnsstring + 'snapshot')
    for element in snapshot:
        if element.get('uri') == None:
            print 'Error: the uri attribute of snapshot file is inexistence!'
            return False
        elif element.get('hash') == None:
            print 'Error: the hash attribute of snapshot file is inexistence!'
            return False
        
    delta = root.findall(xmlnsstring + 'delta')
    for element in delta:
        if element.get('serial') == None:
            print 'Error: the serial attribute of delta file is inexistence!'
            return False
        elif element.get('uri') == None:
            print 'Error: the uri attribute of delta file is inexistence!'
            return False
        elif element.get('hash') == None:
            print 'Error: the hash attribute of delta file is inexistence!'
            return False
        
    return True

def validate_Snapshot_File_Format():
    path = os.getcwd() + '/ControlFile/snapshot.xml'
    
    if not os.path.exists(path):
        print 'Error: no snapshot file!'
        sys.exit(1)
    else: 
        try:
            tree = ET.parse(path)  # create structure tree of the .xml file
            root = tree.getroot()  # obtain root node
        except Exception, e:
            print "Error: cannot parse file!"  # warning user
            print e  # print error information
            sys.exit(1)
    
    try:       
        xml = etree.parse(path)
        xmlroot = xml.getroot()
        xmlns = xmlroot.nsmap
    except Exception, e:
        print "Error: cannot obtain the namespace of snapshot file!"  # warning user
        print e  # print error information
        sys.exit(1)
    
    xmlnsstring = '{' + xmlns[None] + '}'
    
    if xmlnsstring != '{http://www.ripe.net/rpki/rrdp}':
        print "Error: the namespace atribute of snapshot file is incorrect!"
        return False
    
    if root.get('version') == None:
        print 'Error: the version attribute of notify file is inexistence!'
        return False
    elif root.get('session_id') == None:
        print 'Error: the session_id attribute of notify file is inexistence!'
        return False
    elif root.get('serial') == None:
        print 'Error: the serial attribute of notify file is inexistence!'
        return False
    
    publish = root.findall(xmlnsstring + 'publish')
    for element in publish:
        if element.get('uri') == None:
            print 'Error: the uri attribute of publish file is inexistence!'
            return False
        
    return True

def validate_Delta_File_Format():
    path = os.getcwd() + '/ControlFile/delta.xml'
    
    if not os.path.exists(path):
        print 'Error: no delta file!'
        sys.exit(1)
    else: 
        try:
            tree = ET.parse(path)  # create structure tree of the .xml file
            root = tree.getroot()  # obtain root node
        except Exception, e:
            print "Error: cannot parse file!"  # warning user
            print e  # print error information
            sys.exit(1)
    
    try:       
        xml = etree.parse(path)
        xmlroot = xml.getroot()
        xmlns = xmlroot.nsmap
    except Exception, e:
        print "Error: cannot obtain the namespace of delta file!"  # warning user
        print e  # print error information
        sys.exit(1)
    
    xmlnsstring = '{' + xmlns[None] + '}'
    
    if xmlnsstring != '{http://www.ripe.net/rpki/rrdp}':
        print "Error: the namespace atribute of delta file is incorrect!"
        return False
    
    if root.get('version') == None:
        print 'Error: the version attribute of delta file is inexistence!'
        return False
    elif root.get('session_id') == None:
        print 'Error: the session_id attribute of delta file is inexistence!'
        return False
    elif root.get('serial') == None:
        print 'Error: the serial attribute of delta file is inexistence!'
        return False
    
    publish = root.findall(xmlnsstring + 'publish')
    for element in publish:
        if element.get('uri') == None:
            print 'Error: the uri attribute of publish file is inexistence!'
            return False
        elif element.get('hash') == None:
            print 'Error: the hash attribute of publish file is inexistence!'
            return False
            
    withdraw = root.findall(xmlnsstring + 'withdraw')
    if withdraw != []:
        for element in withdraw:
            if element.get('uri') == None:
                print 'Error: the uri attribute of withdraw file is inexistence!'
                return False
            elif element.get('hash') == None:
                print 'Error: the hash attribute of withdraw file is inexistence!'
                return False
  
    return True

def parse_Notification_File():
    path = os.getcwd() + '/ControlFile/notification.xml'
    
    if not os.path.exists(path):
        print 'Error: no notification file!'
        sys.exit(1)
    else: 
        try:
            tree = ET.parse(path)  # create structure tree of the .xml file
            root = tree.getroot()  # obtain root node
        except Exception, e:
            print "Error: cannot parse file!"  # warning user
            print e  # print error information
            sys.exit(1)
    
    try:       
        xml = etree.parse(path)
        xmlroot = xml.getroot()
        xmlns = xmlroot.nsmap
    except Exception, e:
        print "Error: cannot obtain the namespace of notification file!"  # warning user
        print e  # print error information
        sys.exit(1)
    
    xmlnsstring = '{' + xmlns[None] + '}'
    
    notification_Element = [];  # this list to record value of notification file
    
    # obtain attribute value of the notification file 
    notification_Attri = [root.get('version'),
                          root.get('session_id'),
                          root.get('serial')]
    
    # adding notificaiotn_Attri to notification_Element
    notification_Element.append(notification_Attri)
    
    # obtain atribute value of snapshot file
    snapshot = root.findall(xmlnsstring + 'snapshot')
    for element in snapshot:
        snapshot_Attri = [element.get('uri'),
                          element.get('hash')]
    
    # adding snapshot_Attri to notification_Element
    notification_Element.append(snapshot_Attri)
    
    # obtain atribute value of delta file   
    delta = root.findall(xmlnsstring + 'delta')
    for element in delta:
        delta_Attri = [element.get('serial'),
                       element.get('uri'),
                       element.get('hash')]
        
        # adding snapshot_Attri to notification_Element
        notification_Element.append(delta_Attri)
        
    return notification_Element
    
def parse_Notify_File():
    path = os.getcwd() + '/ControlFile/notify.xml'
    
    if not os.path.exists(path):
        print 'Error: no notify file!'
        sys.exit(1)
    else: 
        try:
            tree = ET.parse(path)  # create structure tree of the .xml file
            root = tree.getroot()  # obtain root node
        except Exception, e:
            print "Error: cannot parse file!"  # warning user
            print e  # print error information
            sys.exit(1)
    
    try:       
        xml = etree.parse(path)
        xmlroot = xml.getroot()
        xmlns = xmlroot.nsmap
    except Exception, e:
        print "Error: cannot obtain the namespace of notify file!"  # warning user
        print e  # print error information
        sys.exit(1)
    
    xmlnsstring = '{' + xmlns[None] + '}'
    
    notify_Element = [];  # this list to record value of notify file
    
    # obtain attribute value of the notify file 
    notify_Attri = [root.get('version'),
                    root.get('session_id'),
                    root.get('serial')]
    
    # adding notify_Attri to notify_Element
    notify_Element.append(notify_Attri)
    
    # obtain atribute value of snapshot file
    snapshot = root.findall(xmlnsstring + 'snapshot')
    for element in snapshot:
        snapshot_Attri = [element.get('uri'),
                          element.get('hash')]
    
    # adding snapshot_Attri to notify_Element
    notify_Element.append(snapshot_Attri)
    
    # obtain atribute value of delta file   
    delta = root.findall(xmlnsstring + 'delta')
    for element in delta:
        delta_Attri = [element.get('serial'),
                       element.get('uri'),
                       element.get('hash')]
        
        # adding snapshot_Attri to notify_Element
        notify_Element.append(delta_Attri)
        
    return notify_Element

def parse_Snapshot_File():
    path = os.getcwd() + '/ControlFile/snapshot.xml'
    
    if not os.path.exists(path):
        print 'Error: no snapshot file!'
        sys.exit(1)
    else: 
        try:
            tree = ET.parse(path)  # create structure tree of the .xml file
            root = tree.getroot()  # obtain root node
        except Exception, e:
            print "Error: cannot parse file!"  # warning user
            print e  # print error information
            sys.exit(1)
    
    try:       
        xml = etree.parse(path)
        xmlroot = xml.getroot()
        xmlns = xmlroot.nsmap
    except Exception, e:
        print "Error: cannot obtain the namespace of snapshot file!"  # warning user
        print e  # print error information
        sys.exit(1)
    
    xmlnsstring = '{' + xmlns[None] + '}'
    
    snapshot_Element = [];  # this list to record value of snapshot file
    
    # obtain attribute value of the snapshot file 
    snapshot_Attri = [root.get('version'),
                      root.get('session_id'),
                      root.get('serial')]
    
    # adding snapshot_Attri to snapshot_Element
    snapshot_Element.append(snapshot_Attri)
    
    # obtain atribute value of publish file   
    publish = root.findall(xmlnsstring + 'publish')
    for element in publish:
        publish_Attri = [element.get('uri')]
        
        # adding publish_Attri to snapshot_Element
        snapshot_Element.append(publish_Attri)
        
    return snapshot_Element

def parse_Delta_File():
    path = os.getcwd() + '/ControlFile/delta.xml'
    
    if not os.path.exists(path):
        print 'Error: no delta file!'
        sys.exit(1)
    else: 
        try:
            tree = ET.parse(path)  # create structure tree of the .xml file
            root = tree.getroot()  # obtain root node
        except Exception, e:
            print "Error: cannot parse file!"  # warning user
            print e  # print error information
            sys.exit(1)
    
    try:       
        xml = etree.parse(path)
        xmlroot = xml.getroot()
        xmlns = xmlroot.nsmap
    except Exception, e:
        print "Error: cannot obtain the namespace of delta file!"  # warning user
        print e  # print error information
        sys.exit(1)
    
    xmlnsstring = '{' + xmlns[None] + '}'
    
    delta_Element = [];  # this list to record value of delta file
    
    # obtain attribute value of the delta file 
    delta_Attri = [root.get('version'),
                   root.get('session_id'),
                   root.get('serial')]
    
    # adding delta_Attri to delta_Element
    delta_Element.append(delta_Attri)
    
    # obtain atribute value of withdraw file
    withdraw = root.findall(xmlnsstring + 'withdraw')
    if withdraw != []:
        for element in withdraw:
            withdraw_Attri = ['withdraw',
                              element.get('uri'),
                              element.get('hash')]
            # adding withdraw_Attri to delta_Element
            delta_Element.append(withdraw_Attri)
            
    # obtain atribute value of publish file   
    publish = root.findall(xmlnsstring + 'publish')
    for element in publish:
        publish_Attri = [element.get('uri'),
                         element.get('hash')]
        
        # adding publish_Attri to delta_Element
        delta_Element.append(publish_Attri)
        
    return delta_Element

def rsync_File(URI):
    path = os.getcwd() + '/Certificate'
    
    # create date folder 
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except Exception, e:
            print e
            sys.exit(1)           
    
    cmd = 'rsync ' + URI + ' ' + path
    
    try:
        subprocess.call(cmd, shell=True)  # use the rsync command
    except Exception, e:
        print 'Error: file synchronize failed!'
        print e

def processing_Snapshot_File(snapshot_Element):
    for element in snapshot_Element:
        rsync_File(element[0])
        
def processing_Delta_File(delta_Element):
    for element in delta_Element:
        if element[0]=='withdraw':
            rsync_File(element[1])
            print 'Warning: obtain a withdraw object!'
        else:
            rsync_File(element[0])
        
def main():
    # init local serial of notification
    local_Notification_Serial = {}
    local_Notification_Serial['afrinic'] = None
    local_Notification_Serial['apnic-afrinic'] = None
    local_Notification_Serial['apnic-arin'] = None
    local_Notification_Serial['apnic-iana'] = None
    local_Notification_Serial['apnic-lacnic'] = None
    local_Notification_Serial['apnic-ripe'] = None
    local_Notification_Serial['lacnic'] = None
    local_Notification_Serial['ripe-ncc'] = None
    
    # init local serical of notify
    local_Notify_Serial = {}
    local_Notify_Serial['afrinic'] = None
    local_Notify_Serial['apnic-afrinic'] = None
    local_Notify_Serial['apnic-arin'] = None
    local_Notify_Serial['apnic-iana'] = None
    local_Notify_Serial['apnic-lacnic'] = None
    local_Notify_Serial['apnic-ripe'] = None
    local_Notify_Serial['lacnic'] = None
    local_Notify_Serial['ripe-ncc'] = None
    
    # init local serical of snapshot
    local_Snapshot_Serial = {}
    local_Snapshot_Serial['afrinic'] = None
    local_Snapshot_Serial['apnic-afrinic'] = None
    local_Snapshot_Serial['apnic-arin'] = None
    local_Snapshot_Serial['apnic-iana'] = None
    local_Snapshot_Serial['apnic-lacnic'] = None
    local_Snapshot_Serial['apnic-ripe'] = None
    local_Snapshot_Serial['lacnic'] = None
    local_Snapshot_Serial['ripe-ncc'] = None
    
    # init local serical of delta
    local_Delta_Serial = {}
    local_Delta_Serial['afrinic'] = None
    local_Delta_Serial['apnic-afrinic'] = None
    local_Delta_Serial['apnic-arin'] = None
    local_Delta_Serial['apnic-iana'] = None
    local_Delta_Serial['apnic-lacnic'] = None
    local_Delta_Serial['apnic-ripe'] = None
    local_Delta_Serial['lacnic'] = None
    local_Delta_Serial['ripe-ncc'] = None
    
    # main loop
    while(True):
        # obtain URL of tal
        notification_File_URL = delta_Read_Conf()
        # loop to processing all tal
        for CA in notification_File_URL:
            
            #one source notification
            obtain_File(CA[1][0])  # obtain notification file
            if validate_Notification_File_Format():  # validate the file format
                notification_Element = parse_Notification_File()
                if notification_Element[0][0] == '1':
                    if local_Notification_Serial[CA[0]] == None:
                        snapshot_URL=['snapshot']
                        snapshot_URL.append(notification_Element[1][0])
                        obtain_File(snapshot_URL)# obtain snapshot file
                        # validate the file format
                        if validate_Snapshot_File_Format():
                            # validate the hash of snapshot file
                            if obtain_Hash_Sha256('snapshot.xml') == notification_Element[1][1]:
                                snapshot_Element = parse_Snapshot_File()
                                if snapshot_Element[0][0] == '1':
                                    if snapshot_Element[0][1] == notification_Element[0][1]:
                                        if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                            snapshot_Info = snapshot_Element[0]
                                            del snapshot_Element[0]
                                            processing_Snapshot_File(snapshot_Element)
                                            local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                        else:
                                            print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                    else:
                                        print 'Error: session_i of snapshot file does not match session_id of notification file, refused to implement snapshot file!'
                                else:
                                    print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                            else:
                                print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                        else:
                            print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                    elif notification_Element[0][2] > local_Notification_Serial[CA[0]]:
                        # obtain delta informations
                        delta_List = notification_Element[2:]
                        # transform string to int
                        for index, content in enumerate(delta_List):
                            delta_List[index][0] = int(content[0])
                        # sort
                        delta_List = sorted(delta_List, key=lambda student: student[0])
                        for delta_List_Element in delta_List:
                            delta_URL = ['delta']
                            delta_URL.append(delta_List_Element[1])
                            obtain_File(delta_URL)
                            # validate the format of delta file
                            if validate_Delta_File_Format:
                                # validate the hash value of delta file
                                if obtain_Hash_Sha256('delta.xml') == delta_List_Element[2]:
                                    delta_Element = parse_Delta_File()
                                    if delta_Element[0][0] == '1':
                                        if delta_Element[0][1] == notification_Element[0][1]:
                                            if local_Delta_Serial[CA[0]] == None or (local_Delta_Serial[CA[0]] + 1) == delta_Element[0][2]:
                                                delta_Info = delta_Element[0]
                                                del delta_Element[0]
                                                processing_Delta_File(delta_Element)
                                                local_Delta_Serial[CA[0]] = int(delta_Info[2])
                                            else:
                                                print 'Error: the serial of delta is error, refused to implement delta file!'
                                                print 'Warning: will try to implement snapshot file!'
                                                if validate_Snapshot_File_Format():
                                                    # validate the hash of snapshot file
                                                    if obtain_Hash_Sha256('snapshot.xml') == notification_Element[1][1]:
                                                        snapshot_Element = parse_Snapshot_File()
                                                        if snapshot_Element[0][0] == '1':
                                                            if snapshot_Element[0][1] == notification_Element[0][1]:
                                                                if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                                                    snapshot_Info = snapshot_Element[0]
                                                                    del snapshot_Element[0]
                                                                    processing_Snapshot_File(snapshot_Element)
                                                                    local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                                                else:
                                                                    print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                                            else:
                                                                print 'Error: session_i of snapshot file does not match session_id of notification file, refused to implement snapshot file!'
                                                        else:
                                                            print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                                                    else:
                                                        print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                                                else:
                                                    print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                                        else:
                                            print 'Error: session_i of delta file does not match session_id of notification file, refused to implement delta file!'
                                            print 'Warning: will try to implement snapshot file!'
                                            if validate_Snapshot_File_Format():
                                                # validate the hash of snapshot file
                                                if obtain_Hash_Sha256('snapshot.xml') == notification_Element[1][1]:
                                                    snapshot_Element = parse_Snapshot_File()
                                                    if snapshot_Element[0][0] == '1':
                                                        if snapshot_Element[0][1] == notification_Element[0][1]:
                                                            if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                                                snapshot_Info = snapshot_Element[0]
                                                                del snapshot_Element[0]
                                                                processing_Snapshot_File(snapshot_Element)
                                                                local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                                            else:
                                                                print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                                        else:
                                                            print 'Error: session_i of snapshot file does not match session_id of notification file, refused to implement snapshot file!'
                                                    else:
                                                        print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                                                else:
                                                    print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                                            else:
                                                print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                                    else:
                                        print 'Error: the version of delta file is not 1, refused to implement delta file!'
                                        print 'Warning: will try to implement snapshot file!'
                                        if validate_Snapshot_File_Format():
                                            # validate the hash of snapshot file
                                            if obtain_Hash_Sha256('snapshot.xml') == notification_Element[1][1]:
                                                snapshot_Element = parse_Snapshot_File()
                                                if snapshot_Element[0][0] == '1':
                                                    if snapshot_Element[0][1] == notification_Element[0][1]:
                                                        if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                                            snapshot_Info = snapshot_Element[0]
                                                            del snapshot_Element[0]
                                                            processing_Snapshot_File(snapshot_Element)
                                                            local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                                        else:
                                                            print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                                    else:
                                                        print 'Error: session_i of snapshot file does not match session_id of notification file, refused to implement snapshot file!'
                                                else:
                                                    print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                                            else:
                                                print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                                        else:
                                            print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                                else:
                                    print 'Error: the hash value of delta file is incorrect, refused to implement delta file!'
                                    print 'Warning: will try to implement snapshot file!'
                                    if validate_Snapshot_File_Format():
                                        # validate the hash of snapshot file
                                        if obtain_Hash_Sha256('snapshot.xml') == notification_Element[1][1]:
                                            snapshot_Element = parse_Snapshot_File()
                                            if snapshot_Element[0][0] == '1':
                                                if snapshot_Element[0][1] == notification_Element[0][1]:
                                                    if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                                        snapshot_Info = snapshot_Element[0]
                                                        del snapshot_Element[0]
                                                        processing_Snapshot_File(snapshot_Element)
                                                        local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                                    else:
                                                        print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                                else:
                                                    print 'Error: session_i of snapshot file does not match session_id of notification file, refused to implement snapshot file!'
                                            else:
                                                print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                                        else:
                                            print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                                    else:
                                        print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                            else:
                                print 'Error: the format of delta file is incorrect, refused to implement delta file!'
                                print 'Warning: will try to implement snapshot file!'
                                if validate_Snapshot_File_Format():
                                    # validate the hash of snapshot file
                                    if obtain_Hash_Sha256('snapshot.xml') == notification_Element[1][1]:
                                        snapshot_Element = parse_Snapshot_File()
                                        if snapshot_Element[0][0] == '1':
                                            if snapshot_Element[0][1] == notification_Element[0][1]:
                                                if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                                    snapshot_Info = snapshot_Element[0]
                                                    del snapshot_Element[0]
                                                    processing_Snapshot_File(snapshot_Element)
                                                    local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                                else:
                                                    print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                            else:
                                                print 'Error: session_i of snapshot file does not match session_id of notification file, refused to implement snapshot file!'
                                        else:
                                            print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                                    else:
                                        print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                                else:
                                    print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                    else:
                        print 'Error: the serial of notification file is error, refused to implement notification file!'
                else:
                    print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
            else:
                print 'Error: the format of notification file is incorrect, refused to implement notification file!'          
            local_Notification_Serial[CA[0]] = int(notification_Element[0][2])
            
            #another source notify
            obtain_File(CA[1][1])  # obtain notify file
            if validate_Notify_File_Format():  # validate the file format
                notify_Element = parse_Notify_File()
                if notify_Element[0][0] == '1':
                    if local_Notify_Serial[CA[0]] == None:
                        snapshot_URL = ['snapshot']
                        snapshot_URL.append(notify_Element[1][0])
                        obtain_File(snapshot_URL)  # obtain snapshot file 
                        # validate the file format
                        if validate_Snapshot_File_Format():
                            # validate the hash of snapshot file
                            if obtain_Hash_Sha256('snapshot.xml') == notify_Element[1][1]:
                                snapshot_Element = parse_Snapshot_File()
                                if snapshot_Element[0][0] == '1':
                                    if snapshot_Element[0][1] == notify_Element[0][1]:
                                        if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                            snapshot_Info = snapshot_Element[0]
                                            del snapshot_Element[0]
                                            processing_Snapshot_File(snapshot_Element)
                                            local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                        else:
                                            print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                    else:
                                        print 'Error: session_i of snapshot file does not match session_id of notify file, refused to implement snapshot file!'
                                else:
                                    print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                            else:
                                print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                        else:
                            print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                    elif notify_Element[0][2] > local_Notify_Serial[CA[0]]:
                        # obtain delta informations
                        delta_List = notify_Element[2:]
                        # transform string to int
                        for index, content in enumerate(delta_List):
                            delta_List[index][0] = int(content[0])
                        # sort
                        delta_List = sorted(delta_List, key=lambda student: student[0])
                        for delta_List_Element in delta_List:
                            delta_URL = ['delta']
                            delta_URL.append(delta_List_Element[1])
                            obtain_File(delta_URL)
                            # validate the format of delta file
                            if validate_Delta_File_Format:
                                # validate the hash value of delta file
                                if obtain_Hash_Sha256('delta.xml') == delta_List_Element[2]:
                                    delta_Element = parse_Delta_File()
                                    if delta_Element[0][0] == '1':
                                        if delta_Element[0][1] == notify_Element[0][1]:
                                            if local_Delta_Serial[CA[0]] == None or (local_Delta_Serial[CA[0]] + 1) == delta_Element[0][2]:
                                                delta_Info = delta_Element[0]
                                                del delta_Element[0]
                                                processing_Delta_File(delta_Element)
                                                local_Delta_Serial[CA[0]] = int(delta_Info[2])
                                            else:
                                                print 'Error: the serial of delta is error, refused to implement delta file!'
                                                print 'Warning: will try to implement snapshot file!'
                                                if validate_Snapshot_File_Format():
                                                    # validate the hash of snapshot file
                                                    if obtain_Hash_Sha256('snapshot.xml') == notify_Element[1][1]:
                                                        snapshot_Element = parse_Snapshot_File()
                                                        if snapshot_Element[0][0] == '1':
                                                            if snapshot_Element[0][1] == notify_Element[0][1]:
                                                                if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                                                    snapshot_Info = snapshot_Element[0]
                                                                    del snapshot_Element[0]
                                                                    processing_Snapshot_File(snapshot_Element)
                                                                    local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                                                else:
                                                                    print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                                            else:
                                                                print 'Error: session_i of snapshot file does not match session_id of notify file, refused to implement snapshot file!'
                                                        else:
                                                            print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                                                    else:
                                                        print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                                                else:
                                                    print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                                        else:
                                            print 'Error: session_i of delta file does not match session_id of notify file, refused to implement delta file!'
                                            print 'Warning: will try to implement snapshot file!'
                                            if validate_Snapshot_File_Format():
                                                # validate the hash of snapshot file
                                                if obtain_Hash_Sha256('snapshot.xml') == notify_Element[1][1]:
                                                    snapshot_Element = parse_Snapshot_File()
                                                    if snapshot_Element[0][0] == '1':
                                                        if snapshot_Element[0][1] == notify_Element[0][1]:
                                                            if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                                                snapshot_Info = snapshot_Element[0]
                                                                del snapshot_Element[0]
                                                                processing_Snapshot_File(snapshot_Element)
                                                                local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                                            else:
                                                                print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                                        else:
                                                            print 'Error: session_i of snapshot file does not match session_id of notify file, refused to implement snapshot file!'
                                                    else:
                                                        print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                                                else:
                                                    print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                                            else:
                                                print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                                    else:
                                        print 'Error: the version of delta file is not 1, refused to implement delta file!'
                                        print 'Warning: will try to implement snapshot file!'
                                        if validate_Snapshot_File_Format():
                                            # validate the hash of snapshot file
                                            if obtain_Hash_Sha256('snapshot.xml') == notify_Element[1][1]:
                                                snapshot_Element = parse_Snapshot_File()
                                                if snapshot_Element[0][0] == '1':
                                                    if snapshot_Element[0][1] == notify_Element[0][1]:
                                                        if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                                            snapshot_Info = snapshot_Element[0]
                                                            del snapshot_Element[0]
                                                            processing_Snapshot_File(snapshot_Element)
                                                            local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                                        else:
                                                            print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                                    else:
                                                        print 'Error: session_i of snapshot file does not match session_id of notify file, refused to implement snapshot file!'
                                                else:
                                                    print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                                            else:
                                                print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                                        else:
                                            print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                                else:
                                    print 'Error: the hash value of delta file is incorrect, refused to implement delta file!'
                                    print 'Warning: will try to implement snapshot file!'
                                    if validate_Snapshot_File_Format():
                                        # validate the hash of snapshot file
                                        if obtain_Hash_Sha256('snapshot.xml') == notify_Element[1][1]:
                                            snapshot_Element = parse_Snapshot_File()
                                            if snapshot_Element[0][0] == '1':
                                                if snapshot_Element[0][1] == notify_Element[0][1]:
                                                    if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                                        snapshot_Info = snapshot_Element[0]
                                                        del snapshot_Element[0]
                                                        processing_Snapshot_File(snapshot_Element)
                                                        local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                                    else:
                                                        print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                                else:
                                                    print 'Error: session_i of snapshot file does not match session_id of notify file, refused to implement snapshot file!'
                                            else:
                                                print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                                        else:
                                            print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                                    else:
                                        print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                            else:
                                print 'Error: the format of delta file is incorrect, refused to implement delta file!'
                                print 'Warning: will try to implement snapshot file!'
                                if validate_Snapshot_File_Format():
                                    # validate the hash of snapshot file
                                    if obtain_Hash_Sha256('snapshot.xml') == notify_Element[1][1]:
                                        snapshot_Element = parse_Snapshot_File()
                                        if snapshot_Element[0][0] == '1':
                                            if snapshot_Element[0][1] == notify_Element[0][1]:
                                                if local_Snapshot_Serial[CA[0]] == None or int(local_Snapshot_Serial[CA[0]]) < int(snapshot_Element[0][2]):
                                                    snapshot_Info = snapshot_Element[0]
                                                    del snapshot_Element[0]
                                                    processing_Snapshot_File(snapshot_Element)
                                                    local_Snapshot_Serial[CA[0]] = int(snapshot_Info[2])
                                                else:
                                                    print 'Error: the serial of snapshot file is error, refused to implement snapshot file!'
                                            else:
                                                print 'Error: session_i of snapshot file does not match session_id of notify file, refused to implement snapshot file!'
                                        else:
                                            print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
                                    else:
                                        print 'Error: the hash value of snapshot file is incorrect, refused to implement snapshot file!'
                                else:
                                    print 'Error: the format of snapshot file is incorrect, refused to implement snapshot file!'
                    else:
                        print 'Error: the serial of notify file is error, refused to implement notify file!'
                else:
                    print 'Error: the version of snapshot file is not 1, refused to implement snapshot file!'
            else:
                print 'Error: the format of notify file is incorrect, refused to implement notify file!'          
            local_Notify_Serial[CA[0]] = int(notify_Element[0][2])
    
    time.sleep(300) #synchronization interval is 5 minutes
    
if __name__ == '__main__':
    main()
