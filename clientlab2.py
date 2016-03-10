from socket import socket
import time, random,os,re, sys, thread, linecache


host_image = 'www.planwallpaper.com'
host_music = 'gettune.net'
# using this variable i can control the downloading speed
recv_speed  = 1024
#downloading function
# params: host address,location of file, name for output, type of file
def downloadfile (host,image_adr,name,type):

    request = 'GET ' + image_adr +' HTTP/1.1\r\nUser-Agent: Netscape Navigator 4.2\r\nHost: '+host+'\r\n\r\n'    
   
    s = socket()
    s.connect ((host,80))
    s.send(request)
    s.send('\r\n\r\n')

    while 1:
        response = s.recv(recv_speed)
        #find length of file in header
        b = re.findall('Content-Length: (.+?)\n',response)
        if b:
            size = int(b[0])
            print size
            
            time.sleep(2)
            #check if file is too big or not
            if size > 10000000:
                print 'File is too big\n' + host + image_adr
                return
        
        open(name+'.txt','ab').write(response)
        if len(response)<recv_speed:
            break
    #find file size wihtout header, read this size
    statinfo = os.stat(name+'.txt')
    file = open(name+'.txt','rb+')
    data = file.read(statinfo.st_size)
    part = data.split('\r\n\r\n')
    #split body and header
    if type == 'music':
        open(name+'.mp3','wb').write(part[1])
    else:
        open(name+'.jpg','wb').write(part[1])
    file.close()
    os.remove(name+'.txt')
    print 'Download complete'
    return
#func params: keyword for searching, host address, size(only for picture), type of file
def findfile (keyword,host,size,type):
    if type == 'music':
        request = 'GET /search/?a=music&q=' + keyword +' HTTP/1.1\r\nUser-Agent: Netscape Navigator 4.2\r\nHost: '+host+'\r\n\r\n' 
    else:
        request = 'GET /search/' + keyword +' HTTP/1.1\r\nUser-Agent: Netscape Navigator 4.2\r\nHost: '+host+'\r\n\r\n'
    
    s = socket()
    s.connect ((host,80))
    s.send(request)
    s.send('\r\n\r\n')
    while 1:
        response = s.recv(1024)
        open(keyword+'.txt','a').write(response)
        #last part of file will be less than 1024(or other value) and we stop receiving
        if len(response)<1024:
            break
        
    statinfo = os.stat(keyword+'.txt')
    file = open(keyword+'.txt','r')
    data = file.read(statinfo.st_size)
    file.close()
    #James Bond rule: delete files  after reading
    os.remove(keyword+'.txt')
    if size=='big':
        location = 'images'
    else:
        location = 'cache'
    if type =='music':
        #use regular expression to find location of file
        b = re.findall('/file/(.+?).mp3',data)
        if b:
            element = random.randrange(0,len(b))
            address = '/file/'+b[element]+'.mp3'
            newhost = 'stream.get-tune.net'
        else:
            print '404 NOT FOUND'
            return
    else:
        b = re.findall('/static/'+location+'/(.+?).jpg',data)
        if b: 
            element = random.randrange(0,len(b))
            address = '/static/'+location+'/'+b[element]+'.jpg'
            newhost = host_image
        else:
            print '404 NOT FOUND'
            return
    
    downloadfile(newhost,address,keyword + str(random.randrange(0,1000)),type)

while 1:
    print 'You want to download music or photo? (type: music or photo)?'
    type = sys.stdin.readline()
    type = type.strip('\n')
     
    if type=='music':
        print 'Enter singer and song name (ex: kanye+west+stronger)'
        song_name = sys.stdin.readline()
        song_name = song_name.strip('\n')        
        findfile(song_name,host_music,'big',type)
    elif type =='exit':
        break
    else:
        print 'Enter a keyword or leave it empty if you feel lucky'
        photo_name = sys.stdin.readline()
        photo_name =  photo_name.strip('\n')
        print 'You want a big or small image? (type: big or small)'
        size = sys.stdin.readline()
        size = size.strip('\n')
        findfile(photo_name,host_image,size,type)
        
       
