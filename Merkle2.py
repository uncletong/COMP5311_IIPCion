import hashlib


class Merkletree:

    def __init__(self, Trans = None, all_hash = None):
        self.Trans = Trans
        self.root = None
        if not all_hash:
            self.all_hash = dict()
        else:
            self.all_hash = all_hash

    def get_root(self):
        for key in self.all_hash:
            if len(self.all_hash[key]) == 1:
                self.root = self.all_hash[key][0]

    def make_tree(self):
        Trans = self.Trans
        all_hash = self.all_hash
        #t = []
        leaf = list()
        #level = self.level
        for temp_transaction in Trans:
            leaf.append(hashlib.sha256(temp_transaction.encode()).hexdigest())
        temp_parents = leaf
        all_hash['leaf'] = leaf
        i = 1
        while len(temp_parents) != 1:
            str_parent = 'level' + str(i)
            parents = list()
            for j in range(0, len(temp_parents), 2):
                lf_child = temp_parents[j]
                if j == len(temp_parents):
                    rt_child = temp_parents[j]
                else:
                    rt_child = temp_parents[j+1]
                node = hashlib.sha256((lf_child + rt_child).encode()).hexdigest()
                parents.append(node)
            all_hash[str_parent] = parents
            temp_parents = parents
            i = i + 1
        self.root = temp_parents

    def verify_tree(self, data):
        key = None
        for key in self.all_hash:
            if len(self.all_hash[key]) == 1:
                break
            else:
                try:
                    num = self.all_hash[key].index(data)
                    print(num)
                    if num % 2 == 0:
                        temp_data = self.all_hash[key][num + 1]
                        data = hashlib.sha256((data + temp_data).encode()).hexdigest()
                    else:
                        temp_data = self.all_hash[key][num - 1]
                        data = hashlib.sha256((temp_data + data).encode()).hexdigest()
                except:
                    return False
        if data == self.all_hash[key][0]:
            print(data)
            return True
        else:
            print(data)
            return False





        # for i in range(0,len(Trans),2):
        #     Leftchild = Trans[i]
        #     if i+1!=len(Trans):
        #         Rightchild = Trans[i+1]
        #     else:
        #         Rightchild = Trans[i]
        #
        #     Leftchild_hash=sha256(Leftchild)
        #     All_hash[Trans[i]] = Leftchild_hash
        #
        #     if Rightchild != '':
        #         Rightchild_hash=sha256(Rightchild)
        #         All_hash[Trans[i+1]] = Rightchild_hash
        #         t.append(Leftchild_hash+Rightchild_hash)
        #         level=level+1
        #
        #
        #     else:
        #         t.append(Leftchild_hash)
        #         level=level+1
        #
        #
        # if len(Trans)!=1:
        #
        #     self.Trans = t
        #     self.All_hash = All_hash
        #     self.Make_a_tree()
        #     self.level=level


    # def Get_Root(self):
    #     rootkey = list(self.All_hash.keys())[-1]
    #     return self.All_hash[rootkey]
    #
    # def Get_all_hash(self):
    #     return self.All_hash
    #
    # def Get_level(self):
    #     return self.level

# Verifying the transaction
# class Merkle_verification:
#
#     def __init__(self,data,All_hash,level=0,f=sha256):
#         self.data= data
#         self.All_hash=All_hash
#         self.f=sha256
#         self.level=level
#
#     def verification(self,f=sha256):
#         hdata = self.data
#         temp = ''
#         l=list(self.All_hash.keys())
#         level=self.level
#         k=math.pow(2,level)-1-math.pow(2,level-1)
#
#         while(len(l)!=k):
#             hdata = f(self.data)
#             for key in self.All_hash:
#                 if hdata == self.All_hash[key]:
#                     left = self.All_hash[key]
#                     if ((l.index(key)+1) !=len(l)-1)&((l.index(key)+1) !=len(l)):
#                         right = self.All_hash[l[l.index(key)+1]]
#                         temp = left+right
#                         l.remove(l[l.index(key)+1])
#                         l.remove(l[l.index(key)])
#                     elif (l.index(key)+1)==len(l)-1:
#                         temp = left
#                         l.remove(l[l.index(key)])
#                     elif (l.index(key)+1)==len(l):
#                         temp = left
#                     self.data = temp
#         print('after calculation, the root is:',f(self.data))
#         return f(self.data)
