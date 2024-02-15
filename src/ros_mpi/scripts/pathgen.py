import math
from unittest import result
num_slides=30
radius=40
angle = 360/num_slides
x=[]
y=[]
points={}
for i in range(num_slides):
    x.append(round(radius*math.cos(math.radians(angle*i)),2))
    # y.append(math.ceil(radius*math.sin(math.radians(angle*i))))
    y.append(round(radius*math.sin(math.radians(angle*i)),2))
print(x)
print(len(x))
print('\n')
print(y)


num_uav = 3
result='{"uav1": {"x": [0,0,0,0,0,0,0,0,0,0,0], "y": [0,0,0,0,0,0,0,0,0,0,0], "z": [10, 10, 10,10,10, 10, 10,10,10, 10, 10]},'
list=[0,10,20]
idx=2
for i in list:
    if(list[-1] == i):
        result += '"uav%d": {"x": [%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d], "y": [%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d], "z": [10, 10, 10,10,10, 10, 10,10,10, 10, 10]}'%(idx,x[i],x[i+1],x[i+2],x[i+3],x[i+4],x[i+5],x[i+6],x[i+7],x[i+8],x[i+9],x[0],
                                                                                           y[i],y[i+1],y[i+2],y[i+3],y[i+4],y[i+5],y[i+6],y[i+7],y[i+8],y[i+9],y[0])
    else:
        result += '"uav%d": {"x": [%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d], "y": [%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d], "z": [10, 10, 10,10,10, 10, 10,10,10, 10, 10]}'%(idx,x[i],x[i+1],x[i+2],x[i+3],x[i+4],x[i+5],x[i+6],x[i+7],x[i+8],x[i+9],x[i+10],
                                                                                           y[i],y[i+1],y[i+2],y[i+3],y[i+4],y[i+5],y[i+6],y[i+7],y[i+8],y[i+9],y[i+10])
    idx+=1
    if(idx <=num_uav):
        result +=','
result +='}'
print(result)
with open('path.txt','w') as f:
    f.write(result)
    f.close