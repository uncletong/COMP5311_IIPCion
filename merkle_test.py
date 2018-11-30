import Merkle2
import json

a = ['1','2','3','4','5','6','7','8']
tree = Merkle2.Merkletree(a)
tree.make_tree()
#json_tree = json.dumps(tree.all_hash)
print(tree.all_hash)
