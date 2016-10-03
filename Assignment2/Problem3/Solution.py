from __future__ import division
def constructHMM(o):
    T=len(o)
    states=2    #Hot-1,Cold-2,Start-0
    a = [[0 for x in range(states+1)] for x in range(states+1)]
    a[0][0] = 0
    a[0][1] = 0.8
    a[0][2] = 0.2
    a[1][1] = 0.7
    a[1][2] = 0.3
    a[2][1] = 0.4
    a[2][2] = 0.6

    #outcome variables are of three type 0,1 and 2
    #b[i][j] is the probability of seeing output j given the state i
    b=[[0 for i in range(T+1)] for j in range(states+1)]
    b[1][1]=0.2
    b[1][2]=0.4
    b[1][3]=0.4
    b[2][1]=0.5
    b[2][2]=0.4
    b[2][3]=0.1

    backtrack=[[0 for i in range(states+1)] for j in range(T+1)]
    v=[[0 for i in range(states+1)] for j in range(T+1)]

    #initialization
    for j in range(1,states+1):
        v[1][j]=a[0][j]*b[j][o[1]]
        backtrack[1][j]=0

    for t in range(2,T+1):
        for j in range(1,states+1):
            for i in range(1,states+1):
                if(v[t-1][i]*a[i][j]*b[j][o[t]]>v[t][j]):
                    backtrack[t][j]=i #argmax
                v[t][j]=max(v[t-1][i]*a[i][j]*b[j][o[t]],v[t][j])








