if __name__ == "__main__":
    import db2route
    import os
    import sys
    import random
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
    #print (sys.argv[1],sys.argv[2])
    os.makedirs('result/'+str(experiment_name)+'/'+str(hour), exist_ok=True)#実験名/時刻でフォルダを作成
    os.makedirs('result/'+str(experiment_name)+'/result', exist_ok=True)#実験名/時刻でフォルダを作成
    os.chdir('result/'+str(experiment_name)+'/'+str(hour))



    print("start IRL")