import json
import ipv6
from tkinter import *
from tkinter import filedialog
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import tkinter.messagebox
from matplotlib import pyplot as plt
filename = "10.json"
with open(filename,encoding='utf-8') as f:
    packet = json.load(f)

ss1 = []
for pkt in packet:
    ss1.append(pkt['_source']["layers"]["ipv6"]["ipv6.flow"])

ss2 = set(ss1)
rule_set=[]
for i,j in enumerate(ss2):
    temp=[]
    if i <= 4:
        temp.append(0xfe80)
        temp.append(0xfb)
        temp.append(j)
    else:
        temp.append(0xfe80)
        temp.append(0x0003)
        temp.append(j)
    rule_set.append(temp)

rule_set[0].append(0b001010)
rule_set[1].append(0b001100)
rule_set[2].append(0b001110)
rule_set[3].append(0b010010)
rule_set[4].append(0b010100)
rule_set[5].append(0b010110)
rule_set[6].append(0b011010)
rule_set[7].append(0b011100)
rule_set[8].append(0b011110)#设定规则集

table=ipv6.HashTable()

for x in rule_set:
    table.insert(x[0],x[1],x[2],x[3])#插入规则集

'''
print("rule_set:")
for x in rule_set:
    print(x)



filename = "30.json"
with open(filename,encoding='utf-8') as f:
    packet = json.load(f)

result=[]
#ic={'a':'0b1010','b':'0b1011','c':'0b1100','d':'0b1101','e':'0b1110','f':'0b1111'}
for pkt in packet:#解析文件进行查询
    temp=[]
    src=pkt['_source']["layers"]["ipv6"]["ipv6.src"].split(':')[0]
    src = '0x'+src
    src = int(src,16)
    des=pkt['_source']["layers"]["ipv6"]["ipv6.dst"].split(':')[-1]
    des = '0x'+des
    des = int(des,16)
    flow=pkt['_source']["layers"]["ipv6"]["ipv6.flow"]
    temp.append(src)
    temp.append(des)
    temp.append(flow)
    temp.append(table.search(src,des,flow))
    result.append(temp)

result = np.array(result)
#pd.set_option('display.max_rows', None)
df = pd.DataFrame(result,columns=['源地址','目的地址','流标签','优先级'])
print(df)

print('result:')
for x in result:
    print(x)
'''
start = Tk()
start.title("start menu")
start.geometry('500x500')




def insertrule():
    src = entry1.get().split(':')[0]
    des = entry2.get().split(':')[-1]
    flow = entry3.get()
    priority = entry4.get()
    if len(src) == 0 or len(des) == 0 or len(flow) == 0 or len(priority) == 0:
         tkinter.messagebox.showerror(title='错误',message='请输入完整的规则')
         return
    src = '0x' + src
    src = int(src, 16)
    des = '0x' + des
    des = int(des,16)
    priority = '0b' + priority
    priority = int(priority,2)
    table.insert(src,des,flow,priority)
    entry1.delete(0,END)
    entry2.delete(0,END)
    entry3.delete(0,END)
    entry4.delete(0,END)
    display = Tk()
    display.title('所有规则集')
    display.geometry('500x500')
    sb = Scrollbar(display)
    sb.place(relx=0.9, rely=0.1, relwidth=0.05, relheight=0.8)
    label = Label(display, text='源地址 目的地址 流标签 优先级')
    label.place(relx=0, rely=0, relwidth=0.34, relheight=0.1)
    global lb1
    lb1 = Listbox(display, yscrollcommand=sb.set)
    rule = tranverse(table)
    for x in rule:
        lb1.insert(END, x)
    lb1.place(relx=0, rely=0.1, relwidth=0.95, relheight=0.8)
    cancel = Button(display, text='关闭', command=display.destroy)
    cancel.place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.05)
    display.mainloop()
def btn1add():
    addmenu = Tk()
    addmenu.title("add rule")
    addmenu.geometry('500x500')
    label1 = Label(addmenu,text='源地址')
    label2 = Label(addmenu,text='目的地址')
    label3 = Label(addmenu,text='流标签')
    label4 = Label(addmenu,text='优先级')
    label1.place(relx=0.1, rely=0.1, relwidth=0.1,relheight=0.1)
    label2.place(relx=0.1, rely=0.3, relwidth=0.1, relheight=0.1)
    label3.place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.1)
    label4.place(relx=0.1, rely=0.7, relwidth=0.1, relheight=0.1)
    global entry1
    entry1 = Entry(addmenu)
    global entry2
    entry2 = Entry(addmenu)
    global entry3
    entry3 = Entry(addmenu)
    global entry4
    entry4 = Entry(addmenu)
    entry1.place(relx=0.3,rely=0.12,relwidth=0.6,relheight=0.05)
    entry2.place(relx=0.3,rely=0.32,relwidth=0.6,relheight=0.05)
    entry3.place(relx=0.3,rely=0.52,relwidth=0.6,relheight=0.05)
    entry4.place(relx=0.3,rely=0.72,relwidth=0.6,relheight=0.05)
    insert = Button(addmenu,text='插入',command=insertrule)
    cancel = Button(addmenu,text='关闭',command=addmenu.destroy)
    insert.place(relx=0.3,rely=0.8,relwidth=0.1,relheight=0.05)
    cancel.place(relx=0.6,rely=0.8,relwidth=0.1,relheight=0.05)
    addmenu.mainloop()

def midtranverse(root,store):
    if root == None:
        return
    midtranverse(root.left,store)
    two=[root.flowlabel,root.priority]
    store.append(two)
    midtranverse(root.right,store)
    return

def tranverse(HashTable):
    rule=[]
    for x in HashTable.array:
        if x == None:#该哈希表为空
            continue
        else:#该哈希表不为空
            while True:
              temp = [x.src,x.des]
              store = []
              midtranverse(x.root.root,store)
              for y in store:
                  temp=temp+y
                  rule.append(temp)
                  temp = [x.src, x.des]
              if x.next == None:
                  break
              else:
                  x = x.next
    return rule

def deletetable():
    index= lb.curselection()
    if len(index) == 0:
        return
    content = lb.get(index)
    table.delete(content[0],content[1],content[2],content[3])
    lb.delete(index)


def btn2delete():
    deletemenu = Tk()
    deletemenu.title('删除规则集')
    deletemenu.geometry('500x500')
    sb = Scrollbar(deletemenu)
    sb.place(relx=0.9,rely=0.1,relwidth=0.05,relheight=0.8)
    label = Label(deletemenu,text='源地址 目的地址 流标签 优先级')
    label.place(relx=0,rely=0,relwidth=0.34,relheight=0.1)
    global  lb
    lb= Listbox(deletemenu,yscrollcommand=sb.set)
    rule = tranverse(table)
    for x in rule:
        lb.insert(END,x)
    lb.place(relx=0,rely=0.1,relwidth=0.95,relheight=0.8)
    deletebutton = Button(deletemenu,text='删除',command=deletetable)
    deletebutton.place(relx=0.4,rely=0.9,relwidth=0.1,relheight=0.05)
    cancel = Button(deletemenu,text='关闭',command=deletemenu.destroy)
    cancel.place(relx=0.6,rely=0.9,relwidth=0.1,relheight=0.05)
    deletemenu.mainloop()

def pathselect():
    filepath = filedialog.askopenfilename(filetypes=[('JSON',"*.json")])
    path.insert('insert',filepath)

def fileparse():
    with open(path.get('0.0','end').strip(), encoding='utf-8') as f:
        packet = json.load(f)
        result=[]
        for pkt in packet:  # 解析文件进行查询
            temp = []
            src = pkt['_source']["layers"]["ipv6"]["ipv6.src"].split(':')[0]
            src = '0x' + src
            src = int(src, 16)
            des = pkt['_source']["layers"]["ipv6"]["ipv6.dst"].split(':')[-1]
            des = '0x' + des
            des = int(des, 16)
            flow = pkt['_source']["layers"]["ipv6"]["ipv6.flow"]
            temp.append(src)
            temp.append(des)
            temp.append(flow)
            temp.append(table.search(src, des, flow))
            result.append(temp)

    result = np.array(result)
    col = ["源地址","目的地址","流标签","优先级"]
    df=pd.DataFrame(data=result,columns=col)
    fig = go.Figure(data=[go.Table(header=dict(values=col),cells=dict(values=[df["源地址"],df["目的地址"],df["流标签"],df["优先级"]]))])
    fig.show()
def btn3search():
    searchmenu = Tk()
    searchmenu.title('查询优先级')
    searchmenu.geometry('500x500')
    label1 = Label(searchmenu,text='文件目录')
    global path
    path = Text(searchmenu)
    select = Button(searchmenu,text='选择解析文件',command=pathselect)
    parse = Button(searchmenu,text='解析',command=fileparse)
    cancel = Button(searchmenu,text='关闭',command=searchmenu.destroy)
    select.place(relx=0.1, rely=0.5, relwidth=0.2, relheight=0.1)
    parse.place(relx=0.4,rely=0.5,relwidth=0.2,relheight=0.1)
    cancel.place(relx=0.7,rely=0.5,relwidth=0.2,relheight=0.1)
    label1.place(relx=0.1, rely=0.3, relwidth=0.1, relheight=0.1)
    path.place(relx=0.3, rely=0.32, relwidth=0.6, relheight=0.05)
    searchmenu.mainloop()

btn1 = Button(start,text='插入规则',command=btn1add)
btn2 = Button(start,text='删除规则',command=btn2delete)
btn3 = Button(start,text='匹配数据包',command=btn3search)

btn1.place(relx=0.1,rely=0.4,relwidth=0.2,relheight=0.1)
btn2.place(relx=0.4,rely=0.4,relwidth=0.2,relheight=0.1)
btn3.place(relx=0.7,rely=0.4,relwidth=0.2,relheight=0.1)
start.mainloop()
