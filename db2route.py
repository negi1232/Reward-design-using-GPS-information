from dis import show_code
from turtle import pos
import numpy as np
import sqlite3
# from gym.envs.toy_text import discrete
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
import folium
import osmnx as ox
from tqdm import tqdm
import os

def import_data(hour):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    #cur.execute('SELECT * FROM expart WHERE "hour" == '+ str(hour))#時間ごとで処理
    #cur.execute('SELECT * FROM expart WHERE "year" == 2021 AND "mon" == 5' )#すべてを一括で処理
    #cur.execute('SELECT * FROM expart WHERE "year" == 2021 AND "mon" == 5 AND "hour" == 12' )#すべてを一括で処理
    
    cur.execute('SELECT * FROM expart WHERE "year" == 2021 AND "hour" == '+ str(hour) )#すべてを一括で処理
    
    data=cur.fetchall()
    con.close()
    return data

class cal_route:
    def __init__(self,z) :
        #z=[35.65, 139.98,35.71, 140.04]#頂点を指定
        self.G = ox.graph_from_bbox(z[2],z[0],z[3] ,z[1], network_type='drive')
        self.fmap = ox.plot_graph_folium(self.G)
        self.last_pos=[0,0]
        self.route_dict={}
        self.point_dict={}

    def calc(self,lat,lon):
        pass
        #print("val")
        if self.last_pos!=[0,0] and self.last_pos!=[lat,lon]:
            
            #もしすでに探索済みの経路であれば
            #最短経路探索用パラメータ設定
            try:
                self.point_dict[(lat, lon)]
                start_node=self.point_dict[(lat, lon)]
            except:
                start_point = (lat, lon)
                start_node = ox.distance.nearest_nodes(self.G, start_point[1], start_point[0])
                self.point_dict[(lat, lon)]=start_node
            
            try:
                self.point_dict[(self.last_pos[0], self.last_pos[1])]
                end_node=self.point_dict[(self.last_pos[0], self.last_pos[1])]
            except:
                end_point = (self.last_pos[0], self.last_pos[1])
                end_node = ox.distance.nearest_nodes(self.G, end_point[1], end_point[0])
                self.point_dict[(self.last_pos[0], self.last_pos[1])]=end_node

            
            #最短経路探索を実施
            

            try:
                #print(self.route_dict[(start_node,end_node)])
                shortest_path=self.route_dict[(start_node,end_node)]
            
            except:
                pass
                shortest_path = ox.shortest_path(self.G, start_node, end_node)
                self.route_dict[(start_node,end_node)]=shortest_path
            pass
            
            if shortest_path !=None:
                for i in shortest_path:

                    yield  self.G._node[i]['y'],self.G._node[i]['x']
            
                self.last_pos=[self.G._node[i]['y'],self.G._node[i]['x']]
            else:
                self.last_pos= [lat,lon]
                #print([lat,lon])
                #yield lat,lon
        else:
            self.last_pos= [lat,lon]
            #print([lat,lon])
            #yield lat,lon

def save_reshape_route(trajectories,hour):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    files = os.listdir("./")
    print(type(files))  # <class 'list'>
    print(files)   
    DB_FILE = "data.db"
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    c = conn.cursor()
    try:
        c.execute('DROP TABLE IF EXISTS reshape_route'+str(hour))
    except:
        pass
    c.execute('create table if not exists  reshape_route'+str(hour)+' (trajectories)')

    bulk_data=list()
    for d in trajectories:
        bulk_data.append([str(d)])
    cur.executemany('INSERT INTO reshape_route'+str(hour)+' (trajectories) values(?)',bulk_data)

    conn.commit()


def import_reshapedata(hour):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    
    cur.execute('SELECT * FROM reshape_route'+str(hour) )#すべてを一括で処理
    data=cur.fetchall()
    st=list()
    for d in data:
        
        st.append(eval(str(d[0])))
    pass
    con.close()
    return st

def db2trajectory(hour,state,calc=True):

    if calc==False:
        trajectory=import_reshapedata(hour)
        return trajectory,state
    
    z=[35.65, 139.98,35.71, 140.04]#頂点を指定
    delta=z[2]-z[0]#パーティション
    #print((z[2]-z[0]),(z[3]-z[1]))
    #z1---------z2
    #|           |
    #|           |
    #|           |
    #|           |
    #z3---------z4
    data=import_data(hour)

    

    apart=int(math.sqrt(state))#分割数

    grid=np.zeros([apart,apart])#訪問回数を保存する
    
    #パーティションを設定
    xapart=[]
    yapart=[]
    for i in range(apart):
        xapart.append(round(z[0]+delta/apart*i, 4))
        yapart.append(round(z[1]+delta/apart*i, 4))
    
    #初期状態の日付を記憶
    now=[data[0][1],data[0][2],data[0][3]]

    trajectory=[]
    trajectory.append([])

    route_cal=cal_route(z)
    for i in tqdm( range(len(data))):
        row=data[i]
        #日にちが変わったら新しい経路とする
        if now[0]!=row[1] or now[1]!=row[2] or now[2]!=row[3]:
            if len(trajectory[-1])!=0:
                trajectory.append([])
            now=[row[1],row[2],row[3]]

        x=y=int()

        lat_lon=list()
        for node in route_cal.calc(row[7],row[8]):
            #print(node)
            lat_lon.append( node )
        pass
        #lat_lon.append( [route_cal.calc(row[7],row[8])] )

        for pos in lat_lon:
            if pos[0]<=z[2] and z[0]<=pos[0] and  pos[1]<=z[3] and z[1]<=pos[1]:
                for x in range(apart-1,-1,-1):
                    if pos[0]>=xapart[x]:
                        break

                for y in range(apart-1,-1,-1):
                    #print(y)
                    if pos[1]>=yapart[y] :
                        break
                

                #if grid[apart-x][y]<=1000:
                grid[apart-1-x][y]+=1
                trajectory[-1].append((x * apart + y)-1)
                
            
            if len(trajectory[-1])==0:
                del trajectory[-1]



    
    save_reshape_route(trajectory,hour)
    return trajectory,apart*apart
    
#db2trajectory()
