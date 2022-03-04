from matplotlib.pyplot import stem, step
import numpy as np
import os
import sqlite3
import math

class Environment():

    def __init__(self):

        self.state,self.rr,self.visit_hist,self.expart_features=self.import_data()

        self.apart=int(math.sqrt(self.state))
        self.actions_list=[0,1,2,3,4,5,6,7,8]
        self.actions_label=["滞在","上","下","右","左","右上","右下","左上","左下"]
        self.actions_move=[0,self.apart,-self.apart,+1,-1,self.apart+1,-1*(self.apart-1),self.apart-1,-1*(self.apart+1)]

        #print(self.state)
        pass
        

    def get_states(self):
        return self.state
    
    def get_actions(self):
        return self.actions
    
    
    #整合性を取る
    def step(self,previous_pos,action,time): #--> state = int , action = int
        reward=0
        next_state=action
        id=self.actions[previous_pos][action][0]
        reward=self.actions[previous_pos][action][3]
        step=self.actions[previous_pos][action][4]
        route=self.actions[previous_pos][action][5]
        return id,next_state , step,reward ,route
        
    
    
    def import_data(self):
        
        state=int()
        rr=list()
        visit_hist=list()
        expart_features=list()
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM Rr' )#すべてを一括で処理
        
        data=cur.fetchall()
        con.close()
        for d in data:
            rr.append(d[1])
            visit_hist.append(d[2])
            expart_features.append(d[3])
        
        return len(data),rr,visit_hist,expart_features



if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    env=Environment()
    #pos_list,action_list,action_conv,maxstep,pos_reward=env.importdata()
    # for i in range(0,1):
    #     env.step(i,0)
    pass
    
