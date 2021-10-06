m = 0 #0 for max, 1 for min
z = [2,-1]
xs = [
    [1,0,100],
    [-1,0,10],
    [0,1,100],
    [0,-1,10],
    [1,1,110]
    ]

##z = [1,3]
##xs = [
##    [1,2,180],
##    [2,1,180],
##    [1,-1,45],
##    [-1,1,45]
##    ]

##z=[1,2,4]
##xs=[
##    [1,1,1,400],
##    [0,1,2,300],
##    [1,1,0,200]
##    ]

z = [7,10,12]
xs = [
    [1,0,0,400],
    [0,1,0,200],
    [0,0,1,100],
    [2,3,7,1000],
    [1,0,1,400],
    [3,5,10,2000],
    [0,-2,1,0],
    [2,4,6,10000]
    ]

def calcValue(o_r,o_c,p_i,o_i):
    return (o_i - (o_r*o_c)/p_i)

def createTableau(xs,z):
    # I need columns to cover the Xs, Ss and RHS
    # I need rows equal to the number of constraints
    tableau = [None for r in range(len(xs)+1)]
    #create identity matrix
    identity = [[1 if c==r else 0 for c in range(len(xs))] for r in range(len(xs))]

    #fill tableau
    for i in range(len(xs)):
        tableau[i] = xs[i][:-1] + identity[i] + [xs[i][-1]]
    tableau[-1] = [-j for j in z] + [0 for i in range(len(xs)+1)]
    bv = [i for i in range(len(z),len(z)+len(xs))]
    return tableau, bv

def isOptimal(t,m):
    if m: #max, count negative values
        return sum(1 for i in t[-1][:-1] if i>0)==0
    else: #min, count positive values
        return sum(1 for i in t[-1][:-1] if i<0)==0

def findPivot(t,m):
    optimal = isOptimal(t,m)
    pc,pr = None,None
    if not optimal:
        val, pc = min((val, idx) for (idx, val) in enumerate(t[-1][:-1]))
        val, pr = min((val, idx) for (idx, val) in enumerate([float('inf') if xx is None or xx<=0 else xx for xx in [None if r[pc]==0 else r[-1]/r[pc] for r in t]]))
    return pc,pr
        
def printTableau(t,bv,xs,z,m=0,pc=None,pr=None):
    heads = ['x_'+str(i+1) for i in range(len(z))] + ['S_'+str(i+1) for i in range(len(xs))]
    
    if not pc is None:
        print(" ", " "*(10 + pc*6) + "↓")
        
        
    header = ' BV    | ' + ' | '.join(heads) + ' | RHS  '
    print(" ", header)
    hr = ''.join(["|" if i=="|" else "-" for i in header])
    print(" ", hr)
    for i in range(len(xs)):
        row = '{0}) {1} |'.format(i+1,heads[bv[i]]) + "|".join([str(x).center(5) for x in t[i]])
        print(" " if (pr is None or pr!=i) else "→" , row)

    print(" ", hr)
    Z_row = "    Z  |" + "|".join([str(x).center(5) for x in t[-1]])
    print(" ", Z_row)
    print(" ", ''.join(["|" if i=="|" else "=" for i in hr]))

def calcValue(o_r,o_c,p_i,o_i):
    return (o_i - (o_r*o_c)/p_i)

def calcItem(t,pc,pr,r,c):
    p_i = t[pr][pc]
    o_i = t[r][c]
    o_c = t[r][pc]
    o_r = t[pr][c]
    return calcValue(o_r,o_c,p_i,o_i)

def iterate(t,bv,pc,pr):
    nt = [[None for c in range(len(xs)+len(z)+1)] for r in range(len(xs)+1)]
    #pivot item
    p_i = t[pr][pc]
    #set pivot column in new tableau
    for r in range(len(t)):
        nt[r][pc] = 0 if r!=pr else 1
    #set pivot row in new tableau
    for c in range(len(t[pr])):
        nt[pr][c] = 1 if c==pc else t[pr][c]/p_i
    #set the rest
    for r in range(len(t)):
        for c in range(len(t[pr])):
            if nt[r][c] is None:
                nt[r][c] = calcItem(t,pc,pr,r,c)
    
    return nt

def printStatus(t,bv,m):
    print("Optimal" if isOptimal(t,m) else "Not optimal")
    heads = ['x_'+str(i+1) for i in range(len(z))] + ['S_'+str(i+1) for i in range(len(xs))] + ['Z']
    vals = [0]*len(heads)
    for i in range(len(bv)):
        vals[bv[i]] = t[i][-1]
    vals[-1] = t[-1][-1]
    print("\t".join([heads[i] + " = " + str(vals[i]) for i in range(len(heads))]))
    
t,bv = createTableau(xs,z)
optimal = False
while not optimal:
    pc,pr = findPivot(t,m)
    optimal = isOptimal(t,m)
    printTableau(t,bv,xs,z,m,pc,pr)
    printStatus(t,bv,m)
    if not optimal:
        bv[pr] = pc
        t = iterate(t,bv,pc,pr)

