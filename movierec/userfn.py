
###################################################
####              USER-BASED FUNCTIONS        #####
###################################################

def validate(email, password):
  vtar=open('C:/Users/antara_b/Dropbox/project/mysite/movierec/data/u.valid','r')
  for line in vtar:
    if '|' in line:
      (e,pwd,uid)=line.split('|')   
      #print e,pwd,uid
      if( e==email and pwd==password):
        ctar=open('C:/Users/antara_b/Dropbox/project/mysite/movierec/data/u.cur','w')
        ctar.write(str(uid))
        ctar.close()
        return 1
  vtar.close()
  return 0

def getCurrent():
  ctar=open('C:/Users/antara_b/Dropbox/project/mysite/movierec/data/u.cur','r')
  c=ctar.read()
  return c;

def addUser(email,pwd,age,sex,occupation,zipcode,path='C:/Users/antara_b/Dropbox/project/mysite/movierec/data/'):

  usertar = open(path+'movielens/u.user','r+')
  occtar = open(path+'movielens/u.occupation','r+')
  occlist =[]

  #Find end of file and last userID
  for line in usertar:
    (uid,details) = line.split('|',1)[0:5]
  #Add line to user file
  uid=int(uid)+1
  usertar.write('\n'+str(uid)+'|'+str(age)+'|'+sex+'|'+occupation+'|'+zipcode)
  #Close file
  usertar.close()

  validtar = open(path+'/u.valid', 'a')
  validtar.write('\n'+email+'|'+pwd+'|'+str(uid))
  validtar.close()

  #Get occupation
  for line in occtar:
    (name)=line.split('\n')[0:1]
    occlist.append(name)
  #Add occupation to file
  if occupation not in occlist:
    occtar.write('\n'+occupation)
  #Close file
  occtar.close()

  ctar=open('C:/Users/antara_b/Dropbox/project/mysite/movierec/data/u.cur','w')
  ctar.write(str(uid))
  ctar.close()
