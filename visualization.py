import matplotlib.pyplot as plt
import math
def grid_visualization(array,states,filename,title):
    plt.close()
    
    
    plt.figure()
    fig, ax = plt.subplots()
    apart=int(math.sqrt(states))
    array=array.reshape((apart,apart))
    #plt.pcolor(array[::-1, :])
    plt.pcolor(array)
    plt.colorbar()
    
    plt.title(title, fontname="MS Gothic")
    plt.savefig('./'+str(filename)+'.png')
    plt.close()