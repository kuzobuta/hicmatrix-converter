'''
Convert the cooler sparse format data to dense matrix
Contact : hisabou-m@cdb.riken.jp
'''

import numpy as np
from scipy.sparse import coo_matrix
import sys


argvs = sys.argv
argc = len(argvs)

if (argc != 4):
    print "Usage: python %s [bin file] [sparse matrix file] [out dense file name] " % argvs[0]
    quit()


def main():
    pos_file=argvs[1]
    sparse_file=argvs[2]
    out_dense_file=argvs[3]
    
    #load the pos file
    pos=np.loadtxt(pos_file,delimiter='\t',skiprows=0,dtype='string')
    min=np.min(np.array(pos[:,3],dtype=int))
    max=np.max(np.array(pos[:,3],dtype=int))
    size=max - min + 1
    
    #load the sparse format
    data=np.loadtxt(sparse_file,delimiter='\t',skiprows=0,dtype='string')
    bin1=np.array(data[:,0],dtype="float")-min
    bin2=np.array(data[:,1],dtype="float")-min
    counts=np.array(data[:,2],dtype="float")
    coo_tri=coo_matrix((counts,(bin1,bin2)), shape=(size,size))
    
    #remove the diagonal of the sparse matrix and transpose
    diag= bin1 != bin2
    bin1_diag=np.array(bin1[diag],dtype="float")
    bin2_diag=np.array(bin2[diag],dtype="float")
    counts_diag=np.array(counts[diag],dtype="float")
    coo_tri_T_wo_diag=coo_matrix((counts_diag,(bin1_diag,bin2_diag)), shape=(size,size)).transpose()
    
    #Combined the two sparse matrix to symmetric
    coo_complete = coo_tri+coo_tri_T_wo_diag
    out=coo_complete.todense()
    np.savetxt(out_dense_file,out,fmt='%s',delimiter='\t',header='', comments='')


if __name__=="__main__":
    main()

