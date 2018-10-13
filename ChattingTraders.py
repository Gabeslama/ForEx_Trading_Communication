#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:00:41 2017

@author: gabriel slama
"""

import pandas as pd
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

#find all the numbers
users=pd.read_csv("traders/users.tsv",sep= "\t")
discussion_post=pd.read_csv("traders/discussion_posts.tsv",sep= "\t")
discussion=pd.read_csv("traders/discussions.tsv",sep="\t")
messages=pd.read_csv("traders/messages.tsv",sep="\t")

#find the time span of the database
print("There are",len(users),"users in the database")
smallestu = users["memberSince"].head(1)
smallest = smallestu.iloc[0]

largestdp = discussion_post["createDate"].tail(1)
largestd = discussion["createDate"].tail(1)
largestu = users["memberSince"].tail(1)
largestm = messages["sendDate"].tail(1)

large_= []
large_.append(largestdp.iloc[0])
large_.append(largestd.iloc[0])
large_.append(largestu.iloc[0])
large_.append(largestm.iloc[0])
largest = max(large_)
c=smallest

day0 = smallest / 1000/60/60/24
dayn= largest / 1000/60/60/24
lt=dayn-day0

#How many message types have been sent
mholder = messages['type']
cmessage=mholder.value_counts()
slices=cmessage
cols= ['blue','red']
labels=mholder.unique()
plt.axis('equal')
plt.title('Message types sent')
pie = plt.pie(slices, startangle=0)
plt.legend(pie[0],labels, bbox_to_anchor=(1,0.5), loc="lower right", fontsize=8, 
           bbox_transform=plt.gcf().transFigure)
plt.show()

#How many discussions of each type have been started?
dholder=discussion['discussionCategory']
label1 = dholder.unique()
cdiscussion = dholder.value_counts()
slices = cdiscussion
plt.axis('equal')
plt.title('Discussions types')
pie2 = plt.pie(slices,startangle=0)
plt.legend(pie2[0],label1, bbox_to_anchor=(1,0.5), loc="lower right", fontsize=8, 
           bbox_transform=plt.gcf().transFigure)
plt.show()

#How many discussion posts have been posted?
print("There have been", len(discussion_post), "discussion posts")

#part 2
#Activity range is the time between the first and the last message (in ANY category) 
#sent by the same user. What is the distribution of activity ranges?
huser=messages['sender_id']
messages2 = messages[['sendDate','sender_id']]
userid=huser.unique()
useramount=huser.value_counts()
message_sorted=messages2.sort_values('sender_id')

minmessage = messages.groupby('sender_id').min()['sendDate']
maxmessage = messages.groupby('sender_id').max()['sendDate']
time_dif = maxmessage - minmessage
time2days = time_dif /1000/60/60/24 
bins = np.linspace(0,len(userid))
plt.hist(time_dif,bins)
plt.xlabel('Users')
plt.ylabel('Time difference')
plt.title('Activity Range')
plt.show()

#part 3
messages = messages.sort_values('sender_id', ascending=True)
messages.drop('id',1)
messages = messages.drop('id',1)
messages
messages.groupby(['type']).first()

dmessage = messages.loc[messages['type'] == 'DIRECT_MESSAGE'].sort_values('sender_id')
newdmessage = dmessage.groupby( [ "sender_id", "type"] ).first()
fmessage = messages.loc[messages['type'] == 'FRIEND_LINK_REQUEST'].sort_values('sender_id')
newfmessage = fmessage.groupby(["sender_id","type"]).first()

creation_date = users[['id','memberSince']]
mdf = pd.merge(messages, creation_date, left_on = ['sender_id'], right_on = ['id'])
mdf = mdf.loc[mdf['type'] == 'FRIEND_LINK_REQUEST'].sort_values('id')
mdf['timedelay'] = mdf['sendDate'] - mdf['memberSince']
mdf['timedelay']= mdf['timedelay']/1000/60/60/24
mdf = mdf.drop('sender_id',1)
mdf = mdf.groupby(['id']).min()['timedelay']
plt.hist(mdf)
plt.xlabel("Time Delay")
plt.ylabel('Number of friend request')
plt.title('Time delay vs number of request')
plt.show()

ddf = pd.merge(messages, creation_date, left_on = ['sender_id'], right_on = ['id'])
ddf = ddf.loc[ddf['type'] == 'DIRECT_MESSAGE'].sort_values('id')
ddf['timedelay'] = ddf['sendDate'] - ddf['memberSince']
ddf['timedelay']= ddf['timedelay']/1000/60/60/24
ddf = ddf.drop('sender_id',1)
ddf = ddf.groupby(['id']).min()['timedelay']


plt.hist(mdf, alpha=0.5, label='Direct Message')
plt.hist(ddf, alpha=0.5, label='Friend Request')
plt.legend(loc='upper right')
plt.xlabel("Time Delay")
plt.ylabel('Number of messages')
plt.title('Time delay vs number of  messages')
plt.show()



#Part 4
"""
#What is the distribution of discussion categories by the number of posts? 
#What is the most popular category?
"""

explode = (0.2,0,0,0,0,0,0,0,0)
pie3 = plt.pie(slices, shadow=True, explode=explode)
plt.axis('equal')
plt.legend(pie2[0],dholder.unique(), bbox_to_anchor=(1,0.5), loc="lower right", fontsize=8, 
           bbox_transform=plt.gcf().transFigure)
plt.show()

#part 5
"""
Post activity delay is the time between user account creation
and posting the first discussion message.
What is the distribution of post activity delays in the most popular category?
"""
dp = pd.merge(creation_date, discussion, left_on = ['id'], right_on =['creator_id'])
dp = discussion[['creator_id','createDate','discussionCategory']].copy()
newdp = pd.merge(discussion,creation_date,left_on = 'creator_id' , right_on = 'id')
newdp = newdp.drop('id_x',1)
newdp['timedelay'] = newdp['createDate'] - newdp['memberSince']
newdp['timedelay']= newdp['timedelay']/1000/60/60/24
newdp = newdp.loc[newdp['discussionCategory'] == 'QUESTION'].sort_values('id_y')
newdp = newdp.groupby(['creator_id']).min()['timedelay']
plt.hist(newdp)
plt.xlabel("Time Delay")
plt.ylabel('Number of discussion messages')
plt.title('Time delay vs number of messages')
plt.show()

#part 6
#A box plot with whiskers that shows all appropriate statistics for 
#message activity delays in EACH category, post activity delays, and activity ranges.

#plt.boxplot(mdf,ddf)
dfmessagesmin = mdf.min()
dfmessagesmax = mdf.max()
dfmessagesmean = mdf.mean()
totalf = [dfmessagesmin, dfmessagesmax,dfmessagesmean]
ddmessagesmin = ddf.min()
ddmessagesmax = ddf.max()
ddmessagesmean = ddf.mean()
totald = [ddmessagesmin, ddmessagesmax,ddmessagesmean]
plt.boxplot(totalf)
plt.boxplot(totald)
plt.show()







