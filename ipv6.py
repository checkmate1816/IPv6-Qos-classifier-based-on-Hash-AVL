'''
import json
filename = "ipv6json.json"
with open(filename,encoding='utf-8') as f:
    packet = json.load(f)

for pkt in packet:
    print(pkt['_source']["layers"]["ipv6"]["ipv6.flow"])
'''
import matplotlib.pyplot as plt
import networkx as nx
class TreeNode:
    #height = 1
    flowlabel = 0
    priority = 0
    left = None
    right = None
    def __init__(self,flowlabel,priority):
        self.flowlabel = flowlabel
        self.priority = priority


class Tree:
    def __init__(self,flowlabel,prority):
        self.root = TreeNode(flowlabel,prority)
    def getheight(self,node):
        if node==None:
            return 0
        if node.left!=None and node.right!=None:
            return max(self.getheight(node.left),self.getheight(node.right))+1
        elif node.left!=None and node.right==None:
            return self.getheight(node.left)+1
        elif node.left==None and node.right!=None:
            return self.getheight(node.right)+1
        else:
            return 1
    def balance(self,node):
        if node == None:
            return 0
        else:
            return self.getheight(node.left)-self.getheight(node.right)

    def rightrotate(self,node):
        x=node.left
        t3=node.right
        x.right=node
        node.left=t3
        return x

    def leftrotate(self,node):
        x=node.right
        t2=x.left
        x.left=node
        node.right=t2
        return x
    def add(self,root,leaf):
        if root==None:
            root=leaf
            return root

        if leaf.flowlabel<root.flowlabel:
            root.left=self.add(root.left,leaf)
        elif leaf.flowlabel>root.flowlabel:
            root.right=self.add(root.right,leaf)

        factor=self.balance(root)
        if factor>1 and self.balance(root.left)>0:
            return self.rightrotate(root)
        if factor<-1 and self.balance(root.right)<0:
            return self.leftrotate(root)
        if factor>1 and self.balance(root.left)<0:
            root.left=self.leftrotate(root.left)
            return self.rightrotate(root)
        if  factor<-1 and self.balance(root.right)>0:
            root.right=self.rightrotate(root.right)
            return self.leftrotate(root)

        return root
    def search(self,root,flowlabel):
        if root == None:
            return -1;

        valueleft = -1;
        valueright = -1;
        if root.flowlabel == flowlabel:
            return root.priority
        elif (root.flowlabel > flowlabel):
          valueleft = self.search(root.left, flowlabel)
        else:
          valueright = self.search(root.right, flowlabel)

        if valueleft > valueright:
           return valueleft
        else:
            return valueright

    def tranverse(self,node):
        if node == None:
            return None
        right = self.tranverse(node.right)
        if right == None:
            return node
        else:
            return right


    def delete(self,root,leaf):
      if root == None:
          return None
      if root.flowlabel < leaf.flowlabel:
          root.right = self.delete(root.right,leaf)
      elif root.flowlabel > leaf.flowlabel:
          root.left =  self.delete(root.left,leaf)
      else:  #找到待删除节点
          if root.left == None and root.right == None:#待删除节点为叶子节点
              return None
          elif root.left != None and root.right == None:#只有左节点
              return root.left
          elif root.left == None and root.right != None:
             return root.right
          else:
              root.flowlabel = self.tranverse(root.left).flowlabel#找出左子树最大节点
              root.priority  = self.tranverse(root.left).flowlabel
              root.left = self.delete(root.left,root)#从左子树中删除该节点
              factor = self.balance(root)
              if factor > 1 and self.balance(root.left) > 0:
                  return self.rightrotate(root)
              if factor < -1 and self.balance(root.right) < 0:
                  return self.leftrotate(root)
              if factor > 1 and self.balance(root.left) < 0:
                  root.left = self.leftrotate(root.left)
                  return self.rightrotate(root)
              if factor < -1 and self.balance(root.right) > 0:
                  root.right = self.rightrotate(root.right)
                  return self.leftrotate(root)
              if factor <-1  and self.balance(root.right) == 0:
                  return self.leftrotate(root)
              if factor>1 and self.balance(root.right) == 0:
                  return self.rightrotate(root)
              return root
      factor = self.balance(root)
      if factor > 1 and self.balance(root.left) > 0:
          return self.rightrotate(root)
      if factor < -1 and self.balance(root.right) < 0:
          return self.leftrotate(root)
      if factor > 1 and self.balance(root.left) < 0:
          root.left = self.leftrotate(root.left)
          return self.rightrotate(root)
      if factor < -1 and self.balance(root.right) > 0:
          root.right = self.rightrotate(root.right)
          return self.leftrotate(root)

      return root





def create_graph(G, node, pos={}, x=0, y=0, layer=1):
        pos[node.flowlabel] = (x, y)
        if node.left:
            G.add_edge(node.flowlabel, node.left.flowlabel)
            l_x, l_y = x - 1 / 2 ** layer, y - 1
            l_layer = layer + 1
            create_graph(G, node.left, x=l_x, y=l_y, pos=pos, layer=l_layer)
        if node.right:
            G.add_edge(node.flowlabel, node.right.flowlabel)
            r_x, r_y = x + 1 / 2 ** layer, y - 1
            r_layer = layer + 1
            create_graph(G, node.right, x=r_x, y=r_y, pos=pos, layer=r_layer)


        return (G, pos)

def draw(node):  # 以某个节点为根画图
      graph = nx.DiGraph()
      graph, pos = create_graph(graph, node)
      fig, ax = plt.subplots(figsize=(8, 10))  # 比例可以根据树的深度适当调节
      nx.draw_networkx(graph, pos, ax=ax, node_size=300)
      plt.show()

'''
tree=Tree(1,1)
node0=TreeNode(2,2)
node1=TreeNode(3,3)
node2=TreeNode(4,4)
node3=TreeNode(5,5)
node4=TreeNode(6,6)
node5=TreeNode(7,7)
node6=TreeNode(8,8)
node7=TreeNode(9,9)
tree.root=tree.add(tree.root,node0)
tree.root=tree.add(tree.root,node1)
tree.root=tree.add(tree.root,node2)
tree.root=tree.add(tree.root,node3)
tree.root=tree.add(tree.root,node4)
tree.root=tree.add(tree.root,node5)
tree.root=tree.add(tree.root,node6)
tree.root=tree.add(tree.root,node7)
tree.root = tree.delete(tree.root,node4)
#print(tree.search(tree.root,3))
draw(tree.root)
'''
class LinkNode:
    def __init__(self,src,des,flowlabel,priority):
        self.src = src
        self.des = des
        self.next = None
        self.root = Tree(flowlabel,priority)
    def insert(self, node):
        self.root.root=  self.root.add(self.root.root,node)
    def search(self,flowlabel):
        return self.root.search(self.root.root,flowlabel)
    def delete(self,node):
        self.root.root = self.root.delete(self.root.root,node)


class HashTable:
    def __init__(self):
        self.array= [None]*10


    def Hash1(self,src,des):
        value=((src%10)+(des%10))%10
        return value

    def Hash2(self,oldvalue):
        value= (oldvalue+1)%10
        return value

    def insert(self,src,des,flowlabel,priority):#向哈希表中插入节点
        value = self.Hash1(src,des)#计算第一个哈希值
        if self.array[value] == None:#若哈希表为空，直接插入
            self.array[value] = LinkNode(src,des,flowlabel,priority)
        else:#不为空
            value = self.Hash2(value)
            if self.array[value] == None:
                self.array[value] = LinkNode(src, des, flowlabel, priority)
            else:
               pointer = self.array[value]
               while True:
                   if pointer.src == src and pointer.des ==des:#两个地址相同
                       node = TreeNode(flowlabel,priority)
                       self.array[value].insert(node)
                       break
                   else:
                       if pointer.next != None:
                           pointer = pointer.next
                       else:
                           pointer.next = LinkNode(src,des,flowlabel,priority)
                           break


    def search(self,src,des,flowlabel):
        value = self.Hash1(src,des)
        priority = -1
        if self.array[value] != None:#第一次哈希查找不为空
            pointer = self.array[value]
            while True:
                if pointer.src == src and pointer.des == des:
                    priority = pointer.search(flowlabel)
                    if priority != -1:
                        return priority
                    else:
                        break
                else:
                    if pointer.next != None:
                        pointer = pointer.next
                    else:
                        break
        else:#第一次查找为空，说明没有插入到哈希表内，直接退出
            return 0
        value = self.Hash2(value) #再哈希
        if self.array[value] == None:#在哈希表中无地址时
            return 0
        else:
            pointer = self.array[value]
            while True:
                if pointer.src == src and pointer.des == des:
                    priority = pointer.search(flowlabel)
                    if priority != -1:
                        return priority
                    else:
                        break
                else:
                    if pointer.next != None:
                        pointer = pointer.next
                    else:
                        break

        return 0

    def delete(self,src,des,flowlabel,priority):
        value = self.Hash1(src,des)
        node = TreeNode(flowlabel, priority)
        if self.array[value] != None:
           pointer = self.array[value]
           slow = self.array[value]
           while True:
               if pointer.src == src and pointer.des == des:
                   pointer.delete(node)
                   if pointer.root.root == None:#树上无节点的情况
                       if slow == pointer:
                           self.array[value] = pointer.next#删除的节点为头节点
                           break
                       else:
                           slow.next = pointer.next
                           break
                   else:
                       break
               else:
                   if pointer.next != None:
                       slow = pointer
                       pointer = pointer.next
                   else:
                       break
        else:#为空直接退出
            return
        value = self.Hash2(value)
        if self.array[value] == None:#第二次查找不存在，则无法删除
            return
        else:
            pointer = self.array[value]
            slow = self.array[value]
            while True:
                if pointer.src == src and pointer.des == des:
                    pointer.delete(node)
                    if pointer.root.root == None:  # 树上无节点的情况
                        if slow == pointer:
                            self.array[value] = pointer.next  # 删除的节点为头节点
                            break
                        else:
                            slow.next = pointer.next
                            break
                    else:
                        break
                else:
                    if pointer.next != None:
                        slow = pointer
                        pointer = pointer.next
                    else:
                        break
        return



table = HashTable()
table.insert(20,19,1,1)
table.insert(20,19,2,2)
table.insert(20,19,3,3)
table.insert(10,19,4,4)
table.insert(20,19,5,5)
#draw(table.array[9].root)
'''
print(table.search(20,19,5))
print(table.search(20,19,1))
print(table.search(20,19,2))
print(table.search(20,19,3))
print(table.search(10,19,4))
'''