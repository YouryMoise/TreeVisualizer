#Import the library
from tkinter import *
import tkinter as tk
import time


exTree = [0,
[5,[1,[8],[90]],[9,[32],[12]]],
[3,[4,[13],[98]],[7,[34],[21]]]
]

exTreeString = '[0,[5,[1,[8.5],[90]],[9,[32],[12]]],[3,[4,[13],[98]],[7,[34],[21]]]]'

def find_close_paren(word, index):
    """
    Find the closing parenthesis of an opening parenthesis in a string
    Word is the string
    Index is the index at which the opening parenthesis occurs 
    """

    count = 1
    #increased = False
    for other_index in range(index+1, len(word)):
        if word[other_index] == '[':
            count+=1
            #increased = True
        if word[other_index] == ']':
            count-=1
        if count == 0:
            return other_index


def intermediate_string_to_string_list(inputString):
    """
    Turn a the string from the user into a list of the characters
    (numbers do not get split by their digits)
    Works for floats and ints
    """
    inputString = inputString[1:len(inputString)-1]
    outputList = []
    index = 0
    while index < len(inputString):
        if inputString[index] == ',':
            index +=1
            continue
        if inputString[index] in '[]':
            outputList.append(inputString[index])
            index +=1
            continue
        else:
            temp = ""
            while index < len(inputString) and inputString[index] not in ('[],'):
                temp += inputString[index]
                index+=1
            outputList.append(temp)
    return outputList



def parse_string_to_list(inputString):
    """
    takes in a string, [node, [child1],[child2]]
    and turns it into an array
    must have the open and closing brackets
    """
    

    inputList = intermediate_string_to_string_list(inputString)
    finalList = []
    index = 0
    while index < len(inputList):
        if inputList[index] not in ('[]'):
            if '.' not in inputList[index]:
                finalList.append(int(inputList[index]))
            else:
                finalList.append(float(inputList[index]))

            index += 1
            continue
        elif inputList[index] == '[':
            last_paren = find_close_paren(inputList,index)
            finalList.append(parse_string_to_list(inputList[index:last_paren+1]))
            index = last_paren+1
    return finalList

#print(parse_string_to_list(exTreeString)) 

def insert_empty_lists(inputTreeList):
    """
    helper for rendering traversal
    Takes the users inputs and adds empty lists
    to represent not having children
    """
    if len(inputTreeList) == 1:
        inputTreeList.extend([[],[]])
    elif len(inputTreeList) == 2:
        insert_empty_lists(inputTreeList[1])
        inputTreeList.append([])
    elif len(inputTreeList) == 3:
        insert_empty_lists(inputTreeList[1])
        insert_empty_lists(inputTreeList[2])

    return inputTreeList


#print(insert_empty_lists([8,[1],[3]]))


def insert_zero(inputTreeList):
    """
    Helper function for rendering traversal
    Takes a list representing a tree and adds a 0 in position 2 of each
    Returns the list
    """
    inputTreeList = insert_empty_lists(inputTreeList)

    #only inserting if there are children
    if inputTreeList[1]:
        insert_zero(inputTreeList[1])
    if inputTreeList[2]:
        insert_zero(inputTreeList[2])
    
    inputTreeList.append(0)
    return inputTreeList

#print(insert_zero([0,[5,[1,[8.5],[90]],[9,[32],[12]]],[3,[4,[13],[98]],[7,[34],[21]]]]))

def draw_node(canvasObject, x, current_lo = (600,80), current_separation = 1280/6):
    #x is a list with [node, [left subtree], [right subtree]]
    #maybe include some other value in this list [node, [ls], [rs], chosen]
    #and render it differently based on value of chosen
    #
    circle_width = 80
    y_separation = 100
    if len(x) < 4:
        x = insert_zero(x)
    if x:
        current_node = canvasObject.create_oval(current_lo[0],current_lo[1],current_lo[0]+circle_width,current_lo[1]+circle_width)
        canvasObject.create_text(current_lo[0]+circle_width/2, current_lo[1]+circle_width/2, text=str(x[0]), fill="black", font=('Helvetica 15 bold'))
        #print(x)
        if x[3] == 1:
            canvasObject.itemconfig(current_node, fill='green')

    if x[1:]:
        if x[1]:
            canvasObject.create_line(current_lo[0]+circle_width/2, current_lo[1]+circle_width,current_lo[0]-current_separation+circle_width/2,current_lo[1]+80+20, fill="green", width=5)
            draw_node(canvasObject, x[1], (current_lo[0]-current_separation, current_lo[1]+y_separation), current_separation/2)
    if x[2:]:
        if x[2]:
            canvasObject.create_line(current_lo[0]+circle_width/2, current_lo[1]+circle_width,current_lo[0]+current_separation+circle_width/2,current_lo[1]+80+20, fill="green", width=5)
            draw_node(canvasObject, x[2], (current_lo[0]+current_separation, current_lo[1]+y_separation), current_separation/2)
        
def placeholder_sleep_function():
    print("waiting")

def traversalWrapper():
    global name_entry
    tree = insert_empty_lists(insert_zero(parse_string_to_list(name_entry.get())))
    in_order_traversal(tree, tree)

#new approach, maybe use generator
#get all the representations of what the tree will look like during traversals
#(elements that become green will stay green)
#will also not show the steps of travelling down the tree, just the results left to right
#when you get to node, if its left child has a 1 in position 3, change yours to 1 and return list
    #then call on right
#otherwise call on left child
#this will require using a for loop in another function and changing the list we call this function 
#on as the loop is running

#[node, recurseResult, [rightChild]]... <- That format

def get_next_step(tree):
    #expecting this to be tree that already has all the 0s and emtpy lists
    #for getting the next node that needs to be colored
    print(tree)

    #check if the left child is colored
    if tree[1]:#mutable lists might make this hard
        if tree[1][3] == 0:#if left child not colored
            new_tree = [tree[0], get_next_step(tree[1]), tree[2],0]
            return new_tree
        if tree[1][3] == 1:
            new_tree = [tree[0], get_next_step(tree[1]), tree[2],tree[3]]
            if new_tree != tree:
                return new_tree
            #otherwise, we have colored left child as much as possible
    if tree[3] == 0:
        return [tree[0], tree[1], tree[2], 1]
    
    if tree[2]:
        if tree[2][3] == 0:
            new_tree = [tree[0], tree[1], get_next_step(tree[2]),1]
            return new_tree
        if tree[2][3] == 1:
            new_tree = [tree[0], tree[1], get_next_step(tree[2]),1]
            if new_tree != tree:
                return new_tree
    return tree

    #if 0, recurse on it
    #if 1, recurse on it, if the result is same as current tree, color yourself and recurse on right

    #if result of recursing on right is same as current tree, return None?
    #otherwise, return the result


    """ if tree[1]:
        if tree[1][3] == 0:
            return [tree[0], get_next_step(tree[1]), tree[2],0]
        else:
            if tree[3] == 0:
                return [tree[0], tree[1], tree[2],1]
    if tree[3] == 0:
        return [tree[0], tree[1], tree[2], 1]

    if tree[2]:
        if tree[2][3] == 0:
            return [tree[0], tree[1], get_next_step(tree[2]),1] """
    


def count_nodes(tree):
    #well formatted tree
    number_left = 0
    number_right = 0
    if tree[1]:
        number_left = count_nodes(tree[1])
    if tree[2]:
        number_right = count_nodes(tree[2])
    return number_left + 1 + number_right

#print(count_nodes(insert_empty_lists(insert_zero(exTree))))

def get_all_steps(tree):
    #also assuming well-formatted tree
    current_tree = tree
    steps = count_nodes(tree)
    #for i in range(steps+1):
    count = 0
    previous_tree = []
    #all_trees.append(current_tree)
    #yield current_tree
    while current_tree != previous_tree:
        previous_tree = current_tree
        if current_tree is not None:
            current_tree = get_next_step(current_tree)
        yield current_tree
        count +=1
    
    #return all_trees
    #maybe a function to count the number of nodes since that is the max number of
    #steps I'll need using this method

def recursive_drawer(list_of_reps):
    """
    For putting in the after
    """
    global c
    c.delete('all')
    if list_of_reps[0] == None:
        return None
    draw_node(c, list_of_reps[0])
    win.after(2000, recursive_drawer, list_of_reps[1:])



def in_order_2(tree):
    #expecting well formatted tree
    queue = [element for element in get_all_steps(tree)]
    recursive_drawer(queue)
    """ global c
    counter = 0
    draw_node(c, queue[0])
    win.after(10000,c.delete, "all")  """
    """ draw_node(c, queue[1])
    win.after(2000,c.delete, "all") 
    draw_node(c, queue[2])
    win.after(2000,c.delete, "all")  """

    """ for element in get_all_steps(tree):
        if element is not None:
            draw_node(c, element)
            win.after(2000,c.delete, "all") """

    """ counter +=1
    if counter == 2:
        break """
            

for element in get_all_steps(insert_empty_lists(insert_zero([8,[1],[2]]))):
    print(element)
            


def in_order_traversal(tree, parentTree):
    """
    should check to see if the current node has left children, if so, recurse on them
    delay 2 seconds, draw this one red and render 
    """
    global win
    global name_entry
    global c
    
    treeToRender = name_entry.get()
    fullTreeToRender = insert_empty_lists(insert_zero(parse_string_to_list(treeToRender)))


    if tree[1]:
        in_order_traversal(tree[1],parentTree)
    #win.after(2000, placeholder_sleep_function)
    time.sleep(1)
    c.delete("all")
    tree[3] = 1
    draw_node(c,parentTree)

    #win.after(2000, placeholder_sleep_function)
    time.sleep(1)
    if tree[2]:
        c.delete("all")
        in_order_traversal(tree[2],parentTree)

    


    #also need to clear the canvas

    #call this on the left child if it exists
    #delay
    #change the 0 for this to a 1 and render
    #delay
    #call this on the right
    #all of these render name_entry.get() so the whole tree gets rendered every time


def in_order_2_wrapper():
    global name_entry
    fixedTree = insert_empty_lists(insert_zero(parse_string_to_list(name_entry.get())))
    in_order_2(fixedTree)

def onClick():
    global c
    global name_entry
    draw_node(c,parse_string_to_list(name_entry.get()))

#Create an instance of tkinter frame
win= Tk()


#Define the geometry of window
win.geometry("900x600")
#win.attributes('-fullscreen', True)

""" myscrollbar=Scrollbar(win,orient="horizontal")
myscrollbar.pack(side="bottom",fill="x")
 """
#Create a canvas object
c= Canvas(win,width=1280, height=720)
name_entry = tk.Entry(win, text = exTreeString,font=('calibre',10,'normal'))

name_entry.place(x=10, y=10)

myButton = Button(win, command = onClick)
myButton.place(x=10,y=20)

traversalButton = Button(win, command = in_order_2_wrapper)
traversalButton.place(x=10,y=30)
#draw_node(c,name_entry.get())
#name_var=tk.StringVar("HELLO")


c.pack()

#name_entry.grid(row=0,column=1)

#draw_node(c, parse_string_to_list('[8,[1],[2,[],[],1]]'), (600,80),1280/6)
#Draw an Oval in the canvas
#c.create_oval(60,60,210,210)

#c.create_text(60, 60, text="HELLO WORLD", fill="black", font=('Helvetica 15 bold'))
#canvas.pack()

win.mainloop()