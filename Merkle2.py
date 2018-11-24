import json
import hashlib
import math


def sha256(content):
    content = content.encode('utf-8')
    return hashlib.sha256(content).hexdigest()


# Finding a branch in Merkle tree
class MerkletreeNode:

    def __init__(self, Leftchild,Rightchild, f=sha256):
        self.Leftchild = Leftchild
        self.Rightchild =Rightchild
        self.f = sha256

    def parent(self):
        return self.f(self.Leftchild + self.Rightchild)

    def node(self):
        branch = {
            "parent": self.parent(),
            "left": self.Leftchild,
            "right": self.Rightchild,
        }
        return branch


# Input the transactions and create a tree
class Merkletree:

    def __init__(self, Trans=None):
        self.Trans = Trans
        self.All_hash = {}
        self.level = 1

    def Make_a_tree(self):
        Trans = self.Trans
        All_hash = self.All_hash
        t = []
        level=self.level

        for i in range(0,len(Trans),2):
            Leftchild = Trans[i]
            if i+1!=len(Trans):
                Rightchild = Trans[i+1]
            else:
                Rightchild = ''

            Leftchild_hash=sha256(Leftchild)
            All_hash[Trans[i]] = Leftchild_hash

            if Rightchild != '':
                Rightchild_hash=sha256(Rightchild)
                All_hash[Trans[i+1]] = Rightchild_hash
                t.append(Leftchild_hash+Rightchild_hash)
                level=level+1


            else:
                t.append(Leftchild_hash)
                level=level+1


        if len(Trans)!=1:

            self.Trans = t
            self.All_hash = All_hash
            self.Make_a_tree()
            self.level=level


    def Get_Root(self):
        rootkey = list(self.All_hash.keys())[-1]
        return self.All_hash[rootkey]

    def Get_all_hash(self):
        return self.All_hash

    def Get_level(self):
        return self.level

# Verifying the transaction
class Merkle_verification:

    def __init__(self,data,All_hash,level=0,f=sha256):
        self.data= data
        self.All_hash=All_hash
        self.f=sha256
        self.level=level

    def verification(self,f=sha256):
        hdata = self.data
        temp = ''
        l=list(self.All_hash.keys())
        level=self.level
        k=math.pow(2,level)-1-math.pow(2,level-1)

        while(len(l)!=k):
            hdata = f(self.data)
            for key in self.All_hash:
                if hdata == self.All_hash[key]:
                    left = self.All_hash[key]
                    if ((l.index(key)+1) !=len(l)-1)&((l.index(key)+1) !=len(l)):
                        right = self.All_hash[l[l.index(key)+1]]
                        temp = left+right
                        l.remove(l[l.index(key)+1])
                        l.remove(l[l.index(key)])
                    elif (l.index(key)+1)==len(l)-1:
                        temp = left
                        l.remove(l[l.index(key)])
                    elif (l.index(key)+1)==len(l):
                        temp = left
                    self.data = temp
        print('after calculation, the root is:',f(self.data))
        return f(self.data)
