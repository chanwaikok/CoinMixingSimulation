import math
import random
import numpy
from numpy import *
from random import shuffle
# max userNo = 20, Max coin per user = 20

arr1 = arange(1, 15, 1)

#create a list of 1 dimensional array
arr2 = zeros(500000, int)

#reshape the 1 dimensional array into 2 dimensional
# each arr
# arr[CoinJoinID, CoinID, Denomination, OwnFrm, OwnTo, RealFrm, RealTo, PrevCoinJoinID, spare, spare]

Db1 = arr2.reshape(50000,10)

#Specify the pegging package, denomination.
#deno[0,1,2,3,4,..,11] = $0.25,$0.5, $1, $2, $1024] 
#deno[3] represent number of $1 coin in a package
deno = array([0,0,10,4,3,3,0,0,0,0,0,0,0], dtype=int)
#actual value = stored value/4, so that we can use integer datatype instead.
deno1 = array([1,2,4,8,16,32,64,128,256,512,1024,2048,4096])
# integer value is used to save space!
print(deno1)
denoID = zeros(100, int);

#specify the number of users; Min should be 4
NoUser = 4

#specify no of transaction to generate
NoTx = 2

#determine the no of round per user for pegging


NoOfCoin = 0
for i in range(0,13):
  if (deno[i] != 0):
    for j in range(0, deno[i]):
       #print("$ ", deno1[i])  
       denoID[NoOfCoin] = deno[i]
       NoOfCoin = NoOfCoin + 1
       
#    NoOfCoin = deno[i] + NoOfCoin

RoundPerUser = math.ceil(NoOfCoin/20)

print("NoOfCoin = ", NoOfCoin, "No of Round", RoundPerUser)

#################################
# Pegging for each user
#got some bug if > 20 coins per users.

CoinJoinID = 0
CoinID = 0

for i in range (0, NoUser):
     p = 1
     for k in range(0,13):
        if (deno[k] != 0):
          #print("deno[k] value ", deno[k], deno1[k])
          for l in range(0, deno[k]):
               Db1[CoinID]=([CoinJoinID+1, CoinID+1,deno1[k],-1,i+1,-1,i+1,-1,0,0])
               CoinID = CoinID + 1
               p = p + 1
               if (p >= 20):
                 #CoinJoinID = CoinJoinID + 1
                 #print("Max Coin is 20 per users for this code")
                 p = 1
     CoinJoinID = CoinJoinID + 1
     
## Pegging done. Tested correct with > 60coins 


#Build a coinID database array with the latest users, denomination
#
# Mixing ???
# all numbers can be obtained from the pegging database.
# CoinID = COin# + ((User# -1)X NoOfCoin)
#.e.g 20th coin = user1 coinID = 20, user2 coinID =(user#-1)*62) + NthCoin = 82
# coinJoinID; user1 : ceil(coinID/20)
# coinJoinID; user2 : (User#-1 x NoOfROund)NoOfCoin + ceil(Nth Coin


#Mix coin by coin.All users mix 1st coin. All users mix 2nd coin. etc
#Waste CoinJoinID
# Mix 1st coin for all users
# use list1 = [1,2,3,4,5]
# shuffle(list1)
#U R unclear with the array list! what it should do?
#list1 is the original version
#list2 is the mixed version

RawCoin = zeros(NoUser*NoOfCoin, int)
RawCoin1 = zeros(NoUser*NoOfCoin, int)
Coins = RawCoin.reshape(NoOfCoin,NoUser)
CoinsMix=RawCoin1.reshape(NoOfCoin,NoUser)


x = 0

for j in range(0,NoOfCoin):
  for i in range(0,NoUser):
     x = (i * NoOfCoin)+j  
     Coins[j][i] = Db1[x][1]   # CoinID
     CoinsMix[j][i] = Db1[x][1]
     
print("No of Users :", NoUser, "CoinID per user: ", NoOfCoin)
print("CoinIDs Before Mixing. One user per column.")
print(Coins)
for i in range (0, NoOfCoin):
    shuffle(CoinsMix[i])
print("CoinIDs After Mixing. One user per column.")
print(CoinsMix)


# must get a translation table for this
# for Coin1: User1 -> UserN.


## From here Coins[CoinPosition][UserNo] = original CoinID
## From here CoinsMix[CoinPosition][UserNo] = Mixed positionCoinID
## user1 to userN coinID is shuffled
# Now put into CoinJoin

## Pending 19th June 2021: How to find the RealTo?

PeggingID = CoinID

CoinJoinID = CoinJoinID + 1
for j in range (0, NoUser):
 for i in range(0, NoOfCoin):
      for k in range (0, NoOfCoin):
        if Coins[i,j] == CoinsMix[i,k]:
          break
      Db1[CoinID] = ([CoinJoinID, Coins[i,j],Db1[(Coins[i,j]-1),2],j+1,CoinID+1,j+1,k+1,Db1[(Coins[i,j]-1),0],0,0])
      Db1[(Coins[i,j]-1),8] = -1   # Mark the information as prunable.
      CoinID = CoinID + 1
 CoinJoinID = CoinJoinID + 1

   
#Db1[JoinID, CoinID, Deno, OwnFrm, OwnTo, RealFrm, RealTo, PrevCoinJoinID, spare, spare]

#for i in range (0, 90):
#    print("i:: ", i, Db1[i])

## 19th June 2021: Mixing done! Print trace and see the output correct or not!
## 19th JUne 2021: 11 am , trace done verify correct.
    
###_________________________________    
# Coin transaction generation
# Specify the number of Tx


# generate the latest coinID database, CoinID, RealTo, JoinID, OwnTo??
#coinID 1 to (NoOfCoin x NoUser)


# randomly select N coins from the coinID database with userID = U1_ID or U2_ID
# how do u deal with previous CoinJoinID

TotalCoin = NoOfCoin * NoUser
CoinDB1 = zeros(TotalCoin*5, int)
CoinDB2 = CoinDB1.reshape(TotalCoin,5)


# Database of latest coinID ownership!
# coinID , OwnTo, RealTo, JoinID.
# This database will be updated from time to time
               
for i in range (TotalCoin, 2*TotalCoin):
  CoinDB2[i-TotalCoin][0] = Db1[i][1];  #coinID
  CoinDB2[i-TotalCoin][1] = Db1[i][2]   #Deno
  CoinDB2[i-TotalCoin][2] = Db1[i][4]   # OwnTo
  CoinDB2[i-TotalCoin][3] = Db1[i][6]   #RealTo
  CoinDB2[i-TotalCoin][4] = Db1[i][0]   #CoinJoinID

print(CoinDB2)

print("Mixing done")
### WHILE LOOP here for each tx ####

# 19th JUne. 11:25 pm.
# specify no of TX, no of coins, No of users= default =2.
# search the coin for the users => get the list of coinID
# Create the coinJoin, add entry to the Db1 database
# update the latest coinID ownership database
# Go for the next TX. 

#Run through the CoinDatabase to get the NoOfCoin for Each User
# array userlist, NoOfCoin

NoTx = 1
z1 = 0
print("No of transaction", NoTx+1)

############# Begin Transaction Looping ################
while (z1 <= NoTx): 
  CoinPerUser = zeros(NoUser, int)
  for i in range (0, NoOfCoin*NoUser):
     CoinPerUser[(CoinDB2[i][3])-1] = CoinPerUser[(CoinDB2[i][3])-1] + 1

  print("COinPeruser", CoinPerUser)
  
###
# We believe most tx are 2 parties but sometimes there is 1 party tx
# for each tx between which users

#Generate the user pair. who is talking to who?
#for i in range (0, NoTx*5):
  User1_2Coin = 0
  GetAnotherUser = 0
  SingleTransfer = 0
  while (GetAnotherUser ==0):
   Habis = 0
   while (Habis == 0):
    User1 = random.randint(0,NoUser)
    User2 = random.randint(0,NoUser)
        
    while ( User1 == User2):
      print("same user. repeat")
      User2 = random.randint(0,NoUser)
    # the simulation may ended with a single user owning all the coin
    # once detected a user with zero coins. find another users with coins and transfer to them.
    while ((CoinPerUser[User1] + CoinPerUser[User2]) == 0):
        User2 = random.randint(0,NoUser)
        while ( User1 == User2):
          User2 = random.randint(0,NoUser)
    # end while same user.

    print("TxNo", z1+1, "User1:", User1,"NoOfUser1Coin:", CoinPerUser[User1], "User2:", User2, "NoOfUser2Coin:", CoinPerUser[User2])
    if (CoinPerUser[User1]== 0):
       Habis = 1
       SingleTransfer = 1
       print("User1 zero coin")
       
    elif (CoinPerUser[User2]== 0):
       Habis = 1
       SingleTransfer = 2
       print("User2 zero coin")
    else:
      if (User1 != User2):
        Habis = 1
      #print("Both Users enough coin") #loop again! 
  #end while Habis == 0 get another user
      
   User1_2Coin = CoinPerUser[User1] + CoinPerUser[User2] 
   #print("rand ", User1, User2, "User1+2 coin", User1_2Coin)

# From no of coins, we need to decide
#a1 :No of User1 -> User2 coin 
#a2 :No of User2 -> User1 coin 
#a3 :No of User1 -> User1 coin 
#a4 :No of User2 -> User2 coin 
# what happen if a1 = 20, but a1 (user1) coins only got 10.
# if random.randint(1,1) is called, this function may hang
# must check the generated no of coins! is sufficient! otherwise regenerate
   Habis = 0
   Looping = 0
   mini = 0

  # if (SingleTransfer == 0):
   while (Habis ==0 | Looping < 20):
     NoOfCoinSel = random.randint(1, 21)
     while (NoOfCoinSel > User1_2Coin):
         NoOfCoinSel = random.randint(1, User1_2Coin) #Possible bug
     if NoOfCoinSel == 1:
        a1 = 1
        a2 = 0
        a3 = 0
        a4 = 0
     elif NoOfCoinSel == 2:
        a1 = random.randint(1,3)  # No 3 will never come up.
        if a1 == 2:
              a1 = 2
              a2 = 0
              a3 = 0
              a4 = 0
        else:
              a1 = 1
              a2 = 1
              a3 = 0
              a4 = 0
     else:  
        a1 = random.randint(1,NoOfCoinSel)
        if a1 == NoOfCoinSel:
           a2=0
           a3=0
           a4 = 0
        else:
           b1 = NoOfCoinSel - a1
           if b1 == 1:
               a2 = 1
               a3 = 0
               a4 = 0
           elif b1 == 2:
              b2 = random.randint(1,3)
              if b2 == 1:
                a2 = 1
                a3 = 1
                a4 = 0
              else:
                a2 = 2
                a3 = 0
                a4 = 0
           else:
             a2 = random.randint(1,b1)
             if a2 == b1:
                a3=0
                a4=0
             else:
               c1 = b1 - a2
               if c1 == 1:
                 a3 = 1
                 a4 = 0
               elif c1 == 2:
                 c2 = random.randint(1,3)
                 if c2 == 1:
                   a3 = 1
                   a4 = 1
                 else:
                   a3 = 2
                   a4 = 0
               else:
                 a3 = random.randint(1,c1)
                 if a3 == c1:
                    a4 = 0
                 else:
                    a4 = c1 - a3

     if ((a1+a3) <= CoinPerUser[User1]):
       if ((a2+a4) <= CoinPerUser[User2]):
          Habis = 1
          GetAnotherUser = 1
     else:   
          print("Looping", Looping,"Habis", Habis)
          Looping = Looping + 1
          
  #endwhile habis
          
 #endwhile GetAnotherUser
  if (SingleTransfer == 1):  #User1 coin = 0
     if (CoinPerUser[User2] > 1):
        a2 = int(CoinPerUser[User2]/2)
        a1 = 0
        a3 = 0
        a4 = 0
        SingleTransfer = 0

  elif (SingleTransfer == 2): #User2 coin = 0
      if (CoinPerUser[User1] > 1):
          a2 = 0
          a1 = int(CoinPerUser[User1]/2)
          a3 = 0
          a4 = 0
          SingleTransfer = 0
  else:
      print("ST")
  print("NoOfCoinSelected", NoOfCoinSel, "Buyer2Seller Seller2Buyer Buyer2Buyer Seller2Seller Total", a1,a2,a3,a4,a1+a2+a3+a4, "BuyerCoin", CoinPerUser[User1], "SellerCoin", CoinPerUser[User2])


### Grab all coins for user1 and user2 and form the coinjoin
###


# Create TX for a1, user1 to user2
# need to random shuffle the list b4 selecting it
# call phython rand shuffle function

#print("CoinID", CoinID, "JoinID", CoinJoinID) : output is correct!
  #print("User1", User1, "User2", User2) #output is correct



# need to sort all user1 and user2 coin
# then shuffle them
# then assign to a1, a2, a3, a4



#sort coins to user1 coinID, user2 coinID 

  User1Coin = zeros(CoinPerUser[User1],int)
  User2Coin = zeros(CoinPerUser[User2],int)

  c1 =0
  c2 = 0
  for i in range (0, TotalCoin):
    if (CoinDB2[i][3] == User1+1):
      User1Coin[c1] = CoinDB2[i][0]
      c1 = c1 + 1
    if (CoinDB2[i][3] == User2+1):
      User2Coin[c2] = CoinDB2[i][0]
      c2 = c2 + 1

  #print(User1Coin)
  #print(User2Coin)
  #Random shuffle the User CoinID position before generating a transaction
  random.shuffle(User1Coin)
  random.shuffle(User2Coin)
  #print(User1Coin)
  #print(User2Coin)

# Now we can assign the a1 a2 a3 a4 into this code.
# create the database entry for CoinID tx
# Update the latest coin database
# loop again for next tx.

#for i in range (TotalCoin, 2*TotalCoin):
#  CoinDB2[i-TotalCoin][0] = Db1[i][1];  #coinID
#  CoinDB2[i-TotalCoin][1] = Db1[i][2]   #Deno
#  CoinDB2[i-TotalCoin][2] = Db1[i][4]   # OwnTo
#  CoinDB2[i-TotalCoin][3] = Db1[i][6]   #RealTo
#  CoinDB2[i-TotalCoin][4] = Db1[i][0]   #CoinJoinID


  
  Count=0
  User1S = 0
  #print("CoinJoinID  CoinID Denomination Sender Receiver RealSender RealReceiver PrevCoinID")
  
  while (a1 !=0):
#Db1[CoinID] = ([CoinJoinID, User1Coin[Count],[(Coins[i,j]-1),2],j+1,CoinID+1,j+1,k+1,Db1[(Coins[i,j]-1),0],0,0])
#CoinJoiNID, CoinID, Deno,OwnFrm, OwnTo, RealFrm, RealTo, PrevCoinJoin,0,0)
    t1 = User1Coin[Count]  # CoinID
    t2 = t1 - 1 #t2 is the CoinID Index in CoinDB2
    CoinID = CoinID + 1
    #print("Db", CoinJoinID, t1, CoinDB2[t2][1], CoinDB2[t2][2],"-->", CoinID, CoinDB2[t2][3],"-->", User2+1, CoinDB2[t2][4])
    print("CoinJoinID", CoinJoinID, "CoinID", t1, "$",CoinDB2[t2][1]/4, CoinDB2[t2][2],"-->", CoinID, CoinDB2[t2][3],"Real-->", User2+1,"PrevCoinJoinID", CoinDB2[t2][4])

    Db1[CoinID-1] = ([CoinJoinID, t1, CoinDB2[t2][1], CoinDB2[t2][2],CoinID, CoinDB2[t2][3], User2+1, CoinDB2[t2][4], 0,0])
    CoinDB2[t2][0] = t1
    CoinDB2[t2][2] = CoinID
    CoinDB2[t2][3] = User2+1
    CoinDB2[t2][4] = CoinJoinID
    Count = Count + 1
    a1  = a1 - 1
    User1S = User1S + CoinDB2[t2][1]
 # end while a1 != 0
  
  Count1 = 0
  User2S = 0
  while (a2 !=0):
    u1 = User2Coin[Count1] #CoinID
    u2 = u1 - 1 #u2 is the CoinID index in CoinDB2
    CoinID = CoinID + 1
    #print("Db", CoinJoinID, u1, CoinDB2[u2][1], CoinDB2[u2][2],"-->", CoinID, CoinDB2[u2][3],"-->", User1+1, CoinDB2[u2][4])
    print("CoinJoinID", CoinJoinID, "CoinID", u1, "$",CoinDB2[u2][1]/4, CoinDB2[u2][2],"-->", CoinID, CoinDB2[u2][3],"Real-->", User1+1,"PrevCoinJoinID", CoinDB2[u2][4])

    Db1[CoinID-1] = ([CoinJoinID, u1, CoinDB2[u2][1], CoinDB2[u2][2],CoinID, CoinDB2[u2][3], User1+1, CoinDB2[u2][4], 0,0])
    CoinDB2[u2][0] = u1
    CoinDB2[u2][2] = CoinID
    CoinDB2[u2][3] = User1+1
    CoinDB2[u2][4] = CoinJoinID
    Count1 = Count1 + 1
    User2S = User2S + CoinDB2[u2][1]
    a2  = a2 - 1
    # end while a2 != 0
  

  User1SelfS = 0
  while (a3 !=0):
   t1 = User1Coin[Count]  # CoinID
   t2 = t1 - 1 #t2 is the CoinID Index in CoinDB2
   CoinID = CoinID + 1
   #print("Db", CoinJoinID, t1, CoinDB2[t2][1], CoinDB2[t2][2],"-->", CoinID, CoinDB2[t2][3],"-->", User1+1, CoinDB2[t2][4])
   print("CoinJoinID", CoinJoinID, "CoinID", t1, "$",CoinDB2[t2][1]/4, CoinDB2[t2][2],"-->", CoinID, CoinDB2[t2][3],"Real-->", User1+1,"PrevCoinJoinID", CoinDB2[t2][4])
   Db1[CoinID-1] = ([CoinJoinID, t1, CoinDB2[t2][1], CoinDB2[t2][2],CoinID, CoinDB2[t2][3], User1+1, CoinDB2[t2][4], 0,0])
   CoinDB2[t2][0] = t1
   CoinDB2[t2][2] = CoinID
   CoinDB2[t2][3] = User1+1
   CoinDB2[t2][4] = CoinJoinID
   Count = Count + 1
   User1SelfS = User1SelfS + CoinDB2[t2][1]
   a3  = a3 - 1
   # end while a3 != 0
  
  User2SelfS = 0 
  while (a4 !=0):
    u1 = User2Coin[Count1] #CoinID
    u2 = u1 - 1 #u2 is the CoinID index in CoinDB2
    CoinID = CoinID + 1
    print("CoinJoinID", CoinJoinID,"CoinID", u1, "$",CoinDB2[u2][1]/4, CoinDB2[u2][2],"-->", CoinID, CoinDB2[u2][3],"Real-->", User2+1,"PrevCoinJoinID", CoinDB2[u2][4])
    Db1[CoinID-1] = ([CoinJoinID, u1, CoinDB2[u2][1], CoinDB2[u2][2],CoinID, CoinDB2[u2][3], User2+1, CoinDB2[u2][4], 0,0])
    CoinDB2[u2][0] = u1
    CoinDB2[u2][2] = CoinID
    CoinDB2[u2][3] = User2+1
    CoinDB2[u2][4] = CoinJoinID
    Count1 = Count1 + 1
    User2SelfS = User2SelfS + CoinDB2[u2][1]
    a4  = a4 - 1
  # end while a4 != 0
  
# print out the tx details.
#
  print("TxNo", z1+1,"User1->User2", User1S-User2S, "User1Self", User1SelfS, "User2Self", User2SelfS)
# update the latest coin database

  #for i in range (80, 100):
   # print(Db1[i])
#single tx finished. 23rd June. Do multiple Tx.
  #print(CoinDB2)
  CoinJoinID = CoinJoinID + 1
  z1 = z1 + 1
  print("**************************************************************************************")

    
#end while z1 <= TxNo
# when increase the number of coin problems
# Print out latest Coin Database
# Print out the database
# remove the real ID
# print out the simulated blockchain

print("Complete database Information")
print("CoinJoinID CoinID $ Sender Receiver RealSender RealReceiver PreviousJoinID")
for i in range (0, 200):
  print(Db1[i][0],"CoinID",Db1[i][1],"$", Db1[i][2]/4,Db1[i][3],"-->", Db1[i][4],Db1[i][5],"Real-->", Db1[i][6],Db1[i][7])
  


print("Simulated BlockChain with Real Sender and Real Receiver Removed")
print("CoinJoinID CoinID $ Sender Receiver PreviousJoinID")
for i in range (0, 200):
  print(Db1[i][0],"CoinID", Db1[i][1],"$", Db1[i][2]/4,Db1[i][3],"-->",Db1[i][4],Db1[i][7])
