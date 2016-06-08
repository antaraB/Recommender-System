
#######################################################
####                     DICTIONARY               #####
#######################################################

# A dictionary of movie critics and their ratings of a small
     # set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,  'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,  'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,  'Superman Returns': 3.5, 'The Night Listener': 4.0}, 
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,  'The Night Listener': 4.5, 'Superman Returns': 4.0,  'You, Me and Dupree': 2.5}, 
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,  'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,  'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,  'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5}, 
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


#########################################################
####                SIMILARITY SCORING              #####
#########################################################

from math import sqrt
# Returns distance-based similarity score
def sim_distance(prefs,person1,person2):
  # Get the list of shared_items
  si={}
  for item in prefs[person1]:
    if item in prefs[person2]:
      si[item]=1
  #no ratings in common, score= 0
  if len(si)==0: return 0
  
  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
    for item in prefs[person1] if item in prefs[person2]])

  return 1/(1+sum_of_squares)

# Pearson correlation coefficient
# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]:
    if item in prefs[p2]: si[item]=1
  # Find the number of elements
  n=len(si)
  # if they are no ratings in common, return 0
  if n==0: return 0

  # Add up all the preferences
  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])
  
  # Sum up the squares
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
  # Sum up the products
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  # Calculate Pearson score
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0
  r=num/den
  return r


###########################################################
####           USER BASED COLLABORATIVE FILTERING     #####
###########################################################

# Returns the best matches for person from prefs dictionary
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other)
                for other in prefs if other!=person]
  # Sort the list in desc. order
  scores.reverse( )
  return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)
  
    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:
    # only score movies I haven't seen yet 
      if item not in prefs[person] or prefs[person][item]==0:
        # Similarity * Score
        totals.setdefault(item,0) 
        totals[item]+=prefs[other][item]*sim 
        # Sum of similarities
        simSums.setdefault(item,0) 
        simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]
  # Return the sorted list
  rankings.sort( ) 
  rankings.reverse( ) 
  return rankings

def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      # Flip item and person
      result[item][person]=prefs[person][item]
  return result

###########################################################
####           ITEM BASED COLLABORATIVE FILTERING     #####
###########################################################
def calculateSimilarItems(prefs,n=10):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}
  
  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # Status updates for large datasets
    c+=1
    #if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # Find the most similar items to this one
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result

def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # Loop over items rated by this user
  for (item,rating) in userRatings.items():
  
    # Loop over items similar to this one
    for (similarity,item2) in itemMatch[item]:
      # Ignore if this user has already rated this item
      if item2 in userRatings: continue
      
      # Weighted sum of rating times similarity
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      
      # Sum of all the similarities
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity
  # Divide each total score by total weighting to get an average 
  rankings=[(score/totalSim[item],item) for item,score in scores.items()]
  
  # Return the rankings from highest to lowest 
  rankings.sort( )
  rankings.reverse( )
  return rankings


###########################################################
####           ITEM BASED COLLABORATIVE FILTERING     #####
###########################################################
import os
defaultpath=os.path.abspath(os.curdir)+'\\movierec\\data\\movielens\\'
defaultpathview=os.path.abspath(os.curdir)+'\\data\\movielens\\'

def loadMovies(path=defaultpath):
    movies=[]
    for line in open(path+'u.item','r'):
      (id,title)=line.split('|')[0:2]
      movies.append(title)

    return movies

def loadMovieLens(path=defaultpath):
  #Get movie movies
  #titles={}
  #movies=loadMovies()
  movies={}
  with open(path+'u.item', 'r') as f:
    for line in f:
      (id,title)=line.split('|')[0:2]
      movies[id]=title
  f.close()
  # Load data
  
  prefs={}
  with open(path+'u.data','r') as f2:
    for line in f2:
      if line and (not line.isspace()):
        (user,movieid,rating,ts)=line.split('\t')[0:4]
        ts=ts.rstrip()
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)
  f2.close()
  return prefs

###################################################
####              ADDITIONAL FUNCTIONS        #####
###################################################

def displayGenre(movieid,path=defaultpath):
  
  movies={}
  gref=[]
  gfinal=[]
  genre=range(19)
  #Get genre names
  for line in open(path+'u.genre2'):
    name=line.split('|')[0:1]
    name=''.join(name)
    gref.append(name)
    #
  #Match movie title
  for line in open(path+'u.item'):
    (id,title,releasedate,vrd,url)=line.split('|')[0:5]
    movies[id]=title
    if(id==movieid):
      #print (movies[id])
      #Get genre of movie
      for i in range(0,19):
        genre[i]=line.split('|')[i+5:i+6]
        if genre[i]==['1']:
          gfinal.append(gref[i])
          #print (gref[i])
  return gfinal


def addRating(uid, movieid, rating, path=defaultpath):
  #Open file in append mode
  if(int(rating)>0):
    datatar = open(path+'u.data','a')
  #Add data to file
    datatar.write('\n'+str(uid)+'\t'+str(movieid)+'\t'+str(rating)+'\t'+'time')
    datatar.close()

def getRecsUserBased(uid,n=10):
  prefs=loadMovieLens()
  rank=getRecommendations(prefs,uid)[0:n]
  final=[None]*n
  movies=[]
  movies=loadMovies()
  counter=0
  for counter,(rating,item) in enumerate(rank):
    i=movies.index(item)
    g=displayGenre(str(i))
    genre=', '.join(g)
    final[counter]=(item,genre)
  return final

def ratedMovie(uid):
  prefs=loadMovieLens()
  #movies=[]
  movies=loadMovies()
  final={}
  g=[]
  for id,values in prefs.items():
    if id==uid:
      for movie,rating in values.items():
        i=movies.index(movie)+1
        g=displayGenre(str(i))
        genre=', '.join(g)
        final[movie]=(rating,genre)
  return final
    
#prefs=loadMovieLens()
#itemsim=calculateSimilarItems(prefs);  

#def getRecsItemBased(uid,n=10):
 # prefs=loadMovieLens()
  #rank=getRecommendedItems(prefs,itemsim,uid)[0:n]
  #return rank;



  

  
