###############################
## optimised Latin hypercube ##
###############################
# 'config' file should specify:
# Number of input dimensions p 
# Number of inputs points desired n 
# Number of LHCs to be generated N 
# min and max of each dimension

import numpy as _np

def optLatinHyperCube(dim, n, N, minmax, filename):

#    minmax = []
#    for i in range(1,dim+1):
#        templist = ( float(config['min'+str(i)]) , float(config['max'+str(i)]) )
#        minmax.append(templist)
    #print(minmax)
    inputs = _np.array(minmax)
    print("Sim-input ranges:\n" , inputs)

    #inputs_map = inputs ## this line will break later stuff because pass by ref
    #for i in range(0,dim):
    #    #inputs_map[:,i] = (inputs[:,i] -  inputs[0,i])/(inputs[1,i]-inputs[0,i])
    #    inputs_map[i,:] = (inputs[i,:] -  inputs[i,0])/(inputs[i,1]-inputs[i,0])
    #print(inputs)

    print("Generating oLHC samples...")
    # for each dimension i, generate n (no. of inputs) random numbers u_i1, u_i2
    # as well as random purturbation of the integers b_i1 -> b_in : 0, 1, ... n-1
    u=_np.zeros((dim,n))
    b=_np.zeros((dim,n), dtype=_np.int)
    x=_np.zeros((dim,n,N))
    # produce the numbers x
    for k in range(0,N):
        for i in range(0,dim):
            u[i,:] = _np.random.uniform(0.0, 1.0, n)
            b[i,:] = _np.arange(0,n,1)
            _np.random.shuffle(b[i,:])
            x[i,:,k] = ( b[i,:] + u[i,:] ) / float(n)

    print("Applying criterion...")
    # do criterion test to find maximum of minimum distance
    C=_np.zeros(N)
    C[:] = 10 # set high impossible original max distance
    for k in range(0,N):
        for j1 in range(0,n):
            for j2 in range(0,n):
                val = _np.linalg.norm( x[:, j1 , k] - x[: , j2, k] )
                if val < C[k] and j1 != j2:
                    C[k] = val

    K = _np.argmax(C)
    D = x[: , : , K]
    #print("Optimal LHC is " , K, " with D:\n" , D)

    print("Saving inputs to file...")
    #_np.savetxt('emu-input.txt', D, delimiter=" ", fmt='%1.4f')
    # unscale the simulator input
    for i in range(0,dim):
        D.T[:,i] = D.T[:,i]*(inputs[i,1]-inputs[i,0]) + inputs[i,0]
    _np.savetxt(filename, D.T, delimiter=" ", fmt='%1.4f')

    print("DONE!")
