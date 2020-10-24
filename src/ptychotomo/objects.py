import numpy as np

# Probe as a gaussian
def probe(size,maxint=1,rin=0.8, rout=1):
    r, c = np.mgrid[:size, :size] + 0.5
    rs = np.sqrt((r - size/2)**2 + (c - size/2)**2)
    rmax = np.sqrt(2) * 0.5 * rout * rs.max() + 1.0
    rmin = np.sqrt(2) * 0.5 * rin * rs.max()
    img = np.zeros((size, size), dtype='float32')
    img[rs < rmin] = 1.0
    img[rs > rmax] = 0.0
    zone = np.logical_and(rs > rmin, rs < rmax)
    img[zone] = np.divide(rmax - rs[zone], rmax - rmin)    
    prb = np.sqrt(maxint)*img*np.exp(1j*0.2*img)
    return prb

def probesquare(size,maxint=1,rin=0.8, rout=1):
    prb = np.zeros([size,size],dtype='float32')
    rinp = int(rin/2*size)
    routp = int(rout/2*size)
    print(rinp)
    print(routp)
    t = np.zeros(size//2-rinp,dtype='float32')
    t0 = np.sin((np.arange(rinp,routp)-rinp)/(routp-rinp)*np.pi/2)
    print(t0)
    t[size//2-routp:size//2-rinp]=t0 
    print(t)
    prb1d = np.zeros(size,dtype='float32')
    prb1d[:len(t)] = t
    prb1d[len(t):-len(t)] = 1
    prb1d[-len(t):] = t[::-1]
    prb = np.transpose(prb1d[np.newaxis,...])*prb1d[np.newaxis,...]     
    #prb = np.sqrt(maxint)*prb*np.exp(1j*prb)
    
    return prb    

# 3d scanner positions
def scanner3(theta, shape, sx, sy, psize, spiral=0, randscan=False, save=False):
    scx, scy = np.meshgrid(
        np.arange(0, shape[1]-psize+1, sx), np.arange(0, shape[0]-psize+1, sy))
    shapescan = np.size(scx)
    scanax = -1+np.zeros([len(theta), shapescan], dtype='float32')
    scanay = -1+np.zeros([len(theta), shapescan], dtype='float32')
    a = spiral
    for m in range(len(theta)):
        scanax[m] = np.ndarray.flatten(scx)+np.mod(a, sx)
        scanay[m] = np.ndarray.flatten(scy)
        a += spiral
        if randscan:
            scanax[m] += sx*(np.random.random(1)-0.5)*1
            scanay[m] += sy*(np.random.random(1)-0.5)*1
            scanax[m] += sx*(np.random.random(shapescan)-0.5)*0.1
            scanay[m] += sy*(np.random.random(shapescan)-0.5)*0.1
            # print(scanax[m])        
    scanax[np.where(np.round(scanax) < 0)] = 0
    scanay[np.where(np.round(scanay) < 0)] = 0
    scanax[np.where(np.round(scanax) > shape[1]-psize)] = shape[1]-psize-1
    scanay[np.where(np.round(scanay) > shape[0]-psize)] = shape[0]-psize-1
    # plot probes
    if save:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        def random_color():
            rgbl=[0.75,0.75,0]
            #np.random.shuffle(rgbl)
            return tuple(rgbl)
        for j in range(0,1):
            fig, ax = plt.subplots(1)
            plt.xlim(-1, shape[1]+2)
            plt.ylim(-1, shape[0]+2)
            plt.gca().set_aspect('equal', adjustable='box')
            plt.axis('off')
            for k in range(0, len(scanax[j])):
                if(scanax[j, k] < 0 or scanay[j, k] < 0):
                    continue
                c = patches.Circle(
                    (scanax[j, k]+psize//2, scanay[j, k]+psize//2), psize//2, fill=False, edgecolor=[*random_color(),1], linewidth=8)
                ax.add_patch(c)
            
            plt.savefig('scan'+str(j)+'.png')
            
    scan = np.zeros([2,len(theta), shapescan], dtype='float32',order='C')             
    scan[0]=scanax
    scan[1]=scanay
    return scan
