
import visualization
import numpy as np
import db2route
import os
import sys
import random
import math
np.set_printoptions(precision=3)
class reward_estimation:
    def __init__(self,trajectories,states):
        self.states=states
        self.apart=int(math.sqrt(states))
        self.trajectories=trajectories
        self.actions_list=[0,1,2,3,4,5,6,7,8]
        self.actions_prop=[.2,.1,.1,.1,.1,.1,.1,.1,.1]
        self.actions_label=["滞在","上","下","右","左","右上","右下","左上","左下"]
        self.actions_move=[0,self.apart,-self.apart,+1,-1,self.apart+1,-1*(self.apart-1),self.apart-1,-1*(self.apart+1)]
        #print(self.actions_move)
        self.probs=np.zeros((states, len(self.actions_list)))
        pass
        if True:
            print("パラメータ")
            for i in range(len(self.actions_list)):
                print('{0}, {1}, {2}, {3}'.format(self.actions_list[i], self.actions_label[i],self.actions_prop[i],self.actions_move[i]))
        


    def Rr(self):
        pass    
        features = np.zeros(states)

        for t in self.trajectories:
            #print(t)
            pos=t[0]#先頭のアドレスを取得
            for p in t[1:]:#[n-1]と[n]を要素としているため
                #action_listのどの行動をしているかを推定
                for a in range(len(self.actions_move)):
                    pass
                    if p==pos+self.actions_move[a]:
                        #print("{0}:{1}".format(pos,p))
                        self.probs[pos][a]+=1
                pos=p
        
        if True:
            for i in range(len(self.probs)):
                if sum(self.probs[i])!=0:
                    print(i,self.probs[i]/sum(self.probs[i]),sum(self.probs[i]/sum(self.probs[i])))
        
        for s in range(len(self.probs)):
            pass
            for a in range(len(self.actions_list)):
                if 0<=s+self.actions_move[a]<1600 and self.probs[s][a]!=0:
                    features[s+self.actions_move[a]]+=self.probs[s][a]/sum(self.probs[s])
                
                else:
                    print("out of range {0}".format(s+self.actions_move[a]))
                #print(a)
        visualization.grid_visualization(features ,states,"Rr","Rr")
        pass
        


    
def onehot_feature(trajectories,states):
        features = np.zeros(states)#特徴量ベクトルを宣言(use env)
        for i in trajectories:#各軌道データごとで回す
            for s in i:#各軌道から1stepごと
                features[s] += 1#0~nまでの訪問回数をカウント

        features /= len(trajectories)#平均訪問回数を計算(特殊な計算式だが、リスト内の各要素に対して割り算を行っているだけ)1/M*Σfs
        return features#平均訪問回数を返えす

def visit_history_features(trajectories,states):
    features = np.zeros(states)#特徴量ベクトルを宣言(use env)
    for i in trajectories:#各軌道データごとで回す
        for s in i:#各軌道から1stepごと
            features[s] = 1#0~nまでの訪問回数をカウント

    return features#平均訪問回数を返えす

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    #実験名とIRLに入力する時刻を決定
    try:
        sys.argv[1]
        experiment_name=sys.argv[1]
    except:
        experiment_name=random.randrange(10000)
    try:
        hour=sys.argv[2]
    except:
        hour=12
    
    trajectories,states=db2route.db2trajectory(hour,1600)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs('result/'+str(experiment_name)+'/'+str(hour), exist_ok=True)#実験名/時刻でフォルダを作成
    os.makedirs('result/'+str(experiment_name)+'/result', exist_ok=True)#実験名/時刻でフォルダを作成
    os.chdir('result/'+str(experiment_name)+'/'+str(hour))

    
    expart_features = onehot_feature(trajectories,states)#平均訪問回数を計算
    visualization.grid_visualization(expart_features,states,"平均訪問回数","平均訪問回数")

    visit_history = visit_history_features(trajectories,states)#訪問履歴を計算
    visualization.grid_visualization(visit_history ,states,"訪問履歴","訪問履歴")

    Rr=reward_estimation(trajectories,states)
    print("start Rr")
    Rr.Rr()

