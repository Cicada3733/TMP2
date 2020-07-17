#!/usr/bin/env python3.7
import math
from random import randrange
import pandas as pd
from copy import copy

#no. of inbound trains = 3
#each train has railcar = 5
#time starts at 0
#humping time = 5 minutes
#pullout time = 10 minutes
#no. of tracks = 2
#track length = 100

def Block_to_track(Out_dest,railcars,bowl,time,Cl_track,M,Outbound_train_dest,Departure_time,Available_trains,Railcars_per_train,L,days,obj,Lag):
    total = 0
    bowl[0].append(railcars[0])
    railcars[0][4] = 0
    track_dest = [-1 for m in  range(Cl_track)]
    track_dest[0]= 0
    time += 0.5
    for car in range(1,M):
        time = time%1440

        '''
        if (car%int(M/10)) == 0 :
            Out,time,bowl,coupling = Pullout(Out_dest,Outbound_train_dest,Available_trains,Departure_time,bowl,time,Cl_track,Lag)
            total+=  Out
            obj +=coupling
        '''
        flag = 0
        while flag==0:
            if time <= 1439:
                for track in range(Cl_track):
                    if railcars[car][3] == track_dest[track] :
                        s= 0
                        for x in (bowl[track]):
                            s+= x[2]
                        if s+railcars[car][2]<= L:
                            bowl[track].append(railcars[car])
                            railcars[car][4] = track
                            time += 0.5
                            print("railcar "+str(car)+" goes to track no "+str(track)+" at "+str(time)+" minutes")
                            flag = 1
                            break
                    elif bowl[track] == []:
                        bowl[track].append(railcars[car])
                        railcars[car][4] = track
                        track_dest[track] = railcars[car][3]
                        flag = 1
                        time += 0.5
                        print("railcar "+str(car)+" goes to track no "+str(track)+" at "+str(time)+" minutes")
                        break
            else:
                time = -0.5
            if flag == 1:
                continue
            for x in Departure_time:
                if x>time:
                    break
            if x-Lag>time:
                time = x- Lag
            if flag != 1:
                start = time
                Out,time,bowl,coupling = Pullout(Out_dest,Outbound_train_dest,Available_trains,Departure_time,bowl,time,Cl_track,Lag)
                total+=  Out
                stop = time
                obj +=coupling
                if start > stop:
                    days+=1
                while Out==0:
                    if time == 1439.5:
                        time = 0
                    else:
                        time+=0.5
                    start = time
                    Out,time,bowl,coupling = Pullout(Out_dest,Outbound_train_dest,Available_trains,Departure_time,bowl,time,Cl_track,Lag)
                    #print(Out)
                    stop = time
                    total+=  Out
                    obj += coupling
                    if start > stop:
                        days+=1

                #Departure.remove(Departure[-1])


    return bowl,time,total,days,obj

def LongestTrack(bowl,b,Cl_track):
    arr = []
    poscount  = 0
    for i in range(Cl_track):
        flag = 0
        for j in range(len(bowl[i])):
            if bowl[i][j][3] == b:
                flag+=1
            else:
                break
        if flag!=0:
            poscount+=1
        arr.append(flag)
    m = max(arr)
    track = arr.index(m)
    return track,m,poscount

def pop(a):
    a.remove(a[0])
    '''
    if len(a)>1:
        for i in range(len(a)-1):
            a[i]=a[i+1]
            a.remove(a[-1])
    else:
        a = []
    '''
    return a

def longest_n_tracks(bowl,p,b,Cl_track):
    yard = bowl.copy()
    best_tracks = []
    for i in range(p):
        track, l, pos = LongestTrack(yard,b,Cl_track)
        best_tracks.append([track,l])
        yard[track] = []
    return best_tracks


def Pullout(Out_dest,Outbound_train_dest,Available_trains,Departure_time, bowl, time,Cl_track,Lag):
    Out = 0
    coupling = 0
    #print(Departure)
    if time == int(time):
        time = int(time)
    else:
        time = int(time)+1
        time = time%1440
    array = Available_trains[time]

    while array==[]:
        time+=1
        array = Available_trains[time]
    index=0
    #array = list(set(array))
    #print(array)\
    '''
    for time_pt in range(len(Departure_time)):
        if Departure_time[time_pt] < time:
            Out_dest[time_pt] = Outbound_train_dest[time_pt]
    '''
    f = 0
    while Out == 0 and index<len(array):
        for i in range(len(Out_dest[array[index]])) :
            rem = []
            track, l,poscount = LongestTrack(bowl,Out_dest[array[index]][i],Cl_track)
            p = 0
            if Departure_time[array[index]] - time >= 0:
                a = Departure_time[array[index]] - time
            else:
                a = Departure_time[array[index]] + 1440 - time

            while a >= p*10:
                p+=1
            if p>0:
                p = p-1
            else:
                p = 0
            if p >poscount:
                p = poscount
            coupling += p
            best_tracks = longest_n_tracks(bowl,p,Out_dest[array[index]][i],Cl_track)
            for j in best_tracks:
                print("Railcars : ")
                a =[]
                for x in bowl[j[0]]:
                    a.append(x[0])
                print(a)
                print("from track "+str(j[0])+" are added to train "+str(array[index]))
                bowl[j[0]] = []
                Out+=j[1]
            if i>0:
                rem.append(i-1)
            if p>=f:
                p = p-f
                f = (3 - (p%3))%3
            else:
                f = f - p
                p = 0


            if p>0:
                p = int(((p-1)/3)+1)

            time+= p*10
            time = time%1440


        for x in rem:
            Out_dest[array[index]].remove(Out_dest[array[index]][x])

            '''
            while l>0:
                Out.append(bowl[track][0][0])
                pop(bowl[track])
                track, l, poscount= LongestTrack(bowl,b,Cl_track)
            '''
        if time> Departure_time[0]:
            Out_dest[0]=[1, 2, 3]
        if time> Departure_time[1]:
            Out_dest[1]=[4]
        if time> Departure_time[2]:
            Out_dest[2]= [5, 6, 7]
        if time> Departure_time[3]:
            Out_dest[3]= [8, 9, 10]
        if time> Departure_time[4]:
            Out_dest[4]= [11, 12]
        if time> Departure_time[5]:
            Out_dest[5]= [13, 14, 15]
        if time> Departure_time[6]:
            Out_dest[6]= [16, 17, 18, 19, 20, 21, 22, 23]
        if time> Departure_time[7]:
            Out_dest[7]=  [24, 25, 26, 27]
        if time> Departure_time[8]:
            Out_dest[8]= [28, 29, 30, 31, 32, 33]
        if time> Departure_time[9]:
            Out_dest[9]= [34]
        if time> Departure_time[10]:
            Out_dest[10]= [35, 36, 37]
        if time> Departure_time[11]:
            Out_dest[11]= [38, 39, 40, 41, 42]
        if time> Departure_time[12]:
            Out_dest[12]= [43, 44]
        if time> Departure_time[13]:
            Out_dest[13]= [45]
        if time> Departure_time[14]:
            Out_dest[14]= [46, 47, 48]
        if time> Departure_time[15]:
            Out_dest[15]= [49, 50]

        index+=1
    return Out, time,bowl,coupling

def main():
    cars  = pd.read_csv("data/Cars Data.csv")
    Outbound_train = pd.read_csv("data/Outbound Train Schedule.csv")
    Out_tr_config = pd.read_csv("data/Outbound Train Configuration.csv")


    time = 0
    print("Enter no. of inbound trains:")
    No_of_inbound_trains = int(input())
    print("Enter no. of outbound trains:")
    No_of_outbound_trains = int(input())
    #print("Enter no. of destinations:")
    #d = int(input())
    print("Enter no. of railcars in each train:")
    Railcars_per_train = int(input())
    print("Enter no. of tracks in  bowl:")
    Cl_track = int(input())
    print("Enter track length:")
    L = int(input())
    print("Enter Lag:")
    Lag = int(input())
    M = Railcars_per_train*No_of_inbound_trains
    # length = the array of lengths of railcars

    Out_train_name = Outbound_train['Train Name'].to_list()
    Out_train_time = Outbound_train['Departure Time'].to_list()
    Out_train_cap = Outbound_train['Length Capacity Feet'].to_list()

    sched = []
    Departure_time = []
    l = len(Out_train_time)
    #print(Out_train_time)
    while len(Departure_time)<l :
        minimum  = min(Out_train_time)
        #print(minimum)
        ind = Out_train_time.index(minimum)
        sched.append(ind)
        Departure_time.append(minimum)
        Out_train_time[ind] = 2000

    temp_name = []
    temp_cap = []
    for i in range (l):
        temp_name.append(Out_train_name[sched[i]])
        temp_cap.append(Out_train_cap[sched[i]])
    Out_train_name = temp_name[2:]
    Out_train_cap = temp_cap[2:]
    Departure_time= Departure_time[2:]
    Departure_time[4] = 511
    #print(Out_train_name)

    Out_name_config = Out_tr_config['Train Name'].to_list()
    Out_block_config = Out_tr_config['Block Name'].to_list()
    station = 1
    Outbound_train_dest = []
    for tr_name in Out_train_name:
        temp_dest = []
        while tr_name in Out_name_config:
            a = Out_name_config.index(tr_name)
            Out_name_config[a] = station
            temp_dest.append(station)
            station += 1
        Outbound_train_dest.append(temp_dest)
    #print(Outbound_train_dest)
    Out_dest = [[1, 2, 3], [4], [5, 6, 7], [8, 9, 10], [11, 12], [13, 14, 15], [16, 17, 18, 19, 20, 21, 22, 23], [24, 25, 26, 27], [28, 29, 30, 31, 32, 33], [34], [35, 36, 37], [38, 39, 40, 41, 42], [43, 44], [45], [46, 47, 48], [49, 50]]
    Destination = cars['Outbound Block'].to_list()
    Destination = Destination[: M]
    '''
    Dest_list = list(set(Destination))
    Dest_len = len(Dest_list)

    for station in Destination:
        for index in range(1,Dest_len+1):
            if station == Dest_list[index]:
                station = index
    '''

    for dest in range(len(Destination)):
        for st in range(len(Out_block_config)) :
            if Destination[dest] == Out_block_config[st]:
                Destination[dest] = Out_name_config[st]


    #Destination = [1,3,4,3,4,5,3,6,1,2,7,5,1,1,2,4,2,3,4,5,6,4,7,3,5,4,3,5,6,1,2,7,3,5,7,4,3,7,2,7,5,2,7,1,2,4,3,6,4,5,3,4,1,6,2,5,1,3,6,7]#[randrange(1,d+1) for x in  range(M)]

    Length = cars['Car Length Feet'].to_list()
    Length = Length[: M]                      #[10*randrange(1,5) for i in range(M)]

    #Arrival_time = [30*i for i in range (M)]

    #Outbound_train_dest= [[3,4],[1,2],[1,2],[3,4],[5,6],[1,2],[3,4],[7],[2],[4],[1],[5,6],[3],[4],[5],[6],[7]]

    #Departure_time = [120,200,240,330,460,510,600,630,750,780,840,960,1080,1120,1200,1290,1410]

    Time_array = [i for i in range (1440)]

    Available_trains = []
    for time_pt in Time_array:
        temp = []
        for y in Departure_time:
            if (time_pt >= y-Lag and time_pt <= y) :
                temp.append(Departure_time.index(y))
            if  (time_pt-1440 >= y-Lag) :
                temp.append(Departure_time.index(y))
        Available_trains.append(temp)
    #print(len(Available_trains))
    #print(Available_trains)
    #print(len(Departure))
    #Destinations= Departure[::-1]


    #### railcar consistis of 6 parts
    #### ID
    #### Inboundtrain no.
    #### Outbound train no.
    #### Length
    #### Destination
    #### Classification track no. on which it is assigned
    #### Outbound train no.

    railcars = [[i,int(i/Railcars_per_train)+1,Length[i],Destination[i],0,0] for i in range (M)]

    bowl = [[] for j in range(Cl_track)]
    days = 0
    obj = 0
    bowl,time,total,days,obj = Block_to_track(Out_dest,railcars,bowl,time,Cl_track,M,Outbound_train_dest,Departure_time,Available_trains,Railcars_per_train,L,days,obj,Lag)
    #print(Departure)
    #print(total)
    '''
    while time<= 1439.5:
        start = time
        Out,time,bowl,coupling = Pullout(Out_dest,Outbound_train_dest,Available_trains,Departure_time,bowl,time,Cl_track,Lag)
        #print(Out)
        stop = time
        if start > stop :
            days +=1
        obj+= coupling
        if Out==0:
            time+=0.5
        else:
            print(Out)
            #print(time)
            total += Out
        #Departure.remove(Departure[-1])
        #print(Departure)
    '''
    #print(total)
    #print(Departure_time[-1])
    #print(Outbound_train_dest)
    while total < M-1:
        start = time
        Out,time,bowl,coupling = Pullout(Out_dest,Outbound_train_dest,Available_trains,Departure_time,bowl,time,Cl_track,Lag)
        #print(Out)
            #print(Outbound_train_dest)
            #print(Out_dest)
        stop = time
        if start > stop :
            days += 1
        obj+= coupling
        if Out==0:
            time+=0.5
        else:
            print(Out)
            #print(time)
            total += Out
            print(total)
        '''
            Out,time,bowl,coupling = Pullout(Out_dest,Outbound_train_dest,Available_trains,Departure_time,bowl,time,Cl_track,Lag)
        #print(Out)

            obj+= coupling
            if Out==0:
                time+=0.5
            else:
                print(Out)
            #print(time)
                total += Out


        '''

    print("Total "+str(total)+" railcars got dispatched.")
    print("It took total "+str(days) +" day(s) to finish the work.")
    print("Total "+str(obj)+" couplings are done.")

if __name__ == '__main__':
    main()
