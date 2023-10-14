#Import the library
from tkinter import *
import tkinter as tk
import time
from tkinter.ttk import *
from functools import partial



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
    Turn the string from the user into a list of the characters
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
    """
    Draw a node and its left and right subtrees
    """
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
    """
    To determine the next node that needs to be colored in an in_order traversal
    """
    #expecting this to be tree that already has all the 0s and emtpy lists
    #for getting the next node that needs to be colored
    
    #if 0, recurse on it
    #if 1, recurse on it, if the result is same as current tree, color yourself and recurse on right

    #if result of recursing on right is same as current tree, return None?
    #otherwise, return the result



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

def get_next_step_preorder(tree):
    #expecting properly formatted tree

    #pre order is node, node.left, node.right
    #if current node is not colored, color it
    if tree[3] == 0:
        return [tree[0], tree[1], tree[2], 1]
    
    #if current is colored, check left node
    if tree[1] and tree[1][3] == 0:
        subTree = get_next_step_preorder(tree[1])
        return [tree[0], subTree, tree[2], tree[3]]
    #if left node colored, still need to make sure left node kids are good
    if tree[1] and tree[1][3] == 1:
        subTree = get_next_step_preorder(tree[1])
        #return if it made a difference
        if subTree != tree[1]:
            print('h')
            return [tree[0], subTree, tree[2], tree[3]]
    
    #same logic for right child
    if tree[2] and tree[2][3] == 0:
        subTree = get_next_step_preorder(tree[2])
        return [tree[0], tree[1], subTree, tree[3]]
    #if left node colored, still need to make sure left node kids are good
    if tree[2] and tree[2][3] == 1:
        subTree = get_next_step_preorder(tree[2])
        #return if it made a difference
        if subTree != tree[2]:
            return [tree[0], tree[1], subTree, tree[3]]

    return tree

def get_next_step_postorder(tree):
    #expecting properly formatted tree

    #pre order is node.left, node.right, node
    #if current node is not colored, color it
    
    
    if tree[1] and tree[1][3] == 0:
        subTree = get_next_step_postorder(tree[1])
        return [tree[0], subTree, tree[2], tree[3]]
    #if left node colored, still need to make sure left node kids are good
    if tree[1] and tree[1][3] == 1:
        subTree = get_next_step_postorder(tree[1])
        #return if it made a difference
        if subTree != tree[1]:
            return [tree[0], subTree, tree[2], tree[3]]
    
    #same logic for right child
    if tree[2] and tree[2][3] == 0:
        subTree = get_next_step_postorder(tree[2])
        return [tree[0], tree[1], subTree, tree[3]]
    #if left node colored, still need to make sure left node kids are good
    if tree[2] and tree[2][3] == 1:
        subTree = get_next_step_postorder(tree[2])
        #return if it made a difference
        if subTree != tree[2]:
            return [tree[0], tree[1], subTree, tree[3]]
    
    #if current is colored, check left node
    if tree[3] == 0:
        return [tree[0], tree[1], tree[2], 1]

    return tree

smallTree = [8,[2],[9]]
fullSmallTree = [8, [2, [], [], 0], [9, [], [], 0], 0]
t = get_next_step_preorder(fullSmallTree)

for i in range(3):
    print(t)
    t = get_next_step_preorder(t)




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

def get_all_steps(tree, traversalType):
    """
    A generator that yields a list representation for what the tree
    should look like at every step of the in_order traversal
    """
    if traversalType == 'inorder':
        func = get_next_step
    elif traversalType == 'preorder':
        func = get_next_step_preorder
    elif traversalType == 'postorder':
        func = get_next_step_postorder
    #also assuming well-formatted tree
    current_tree = tree
    #for i in range(steps+1):
    previous_tree = []
    #all_trees.append(current_tree)
    #yield current_tree
    yield current_tree
    while current_tree != previous_tree:
        previous_tree = current_tree
        if current_tree is not None:
            current_tree = func(current_tree)
        yield current_tree
    
    #return all_trees
    #maybe a function to count the number of nodes since that is the max number of
    #steps I'll need using this method

def recursive_drawer(list_of_reps):
    """
    For coloring the tree
    """
    global c
    c.delete('all')
    if not list_of_reps:
        return None
    draw_node(c, list_of_reps[0])
    win.after(500, recursive_drawer, list_of_reps[1:])
    

def traversal_wrapper(traversalType):
    global name_entry
    fixedTree = insert_empty_lists(insert_zero(parse_string_to_list(name_entry.get())))
    queue = [element for element in get_all_steps(fixedTree,traversalType)]
    recursive_drawer(queue)

def onClick():
    global c
    global name_entry
    draw_node(c,parse_string_to_list(name_entry.get()))

#Create an instance of tkinter frame
win= Tk()


#Define the geometry of window
win.geometry("900x600")
#win.attributes('-fullscreen', True)


#Create a canvas object
c= Canvas(win,width=1280, height=720)
name_entry = tk.Entry(win, text = exTreeString,font=('calibre',10,'normal'))

name_entry.place(x=10, y=10)

myButton = Button(win, command = onClick, text = "Visualize")
myButton.place(x=200,y=10)

style = Style()
 
# This will be adding style, and 
# naming that style variable as 
# W.Tbutton (TButton is used for ttk.Button).
style.configure('W.TButton', font =
               ('calibri', 10, 'bold', 'underline'),
                foreground = 'red')
 

traversalButton = Button(win, style = 'W.TButton',text = "Inorder traversal",command = partial(traversal_wrapper,'inorder'))
traversalButton.place(x=200,y=60)

preTraversalButton = Button(win, style = 'W.TButton',text = "Preorder traversal",command = partial(traversal_wrapper,'preorder'))
preTraversalButton.place(x=200,y=110)

preTraversalButton = Button(win, style = 'W.TButton',text = "Postorder traversal",command = partial(traversal_wrapper,'postorder'))
preTraversalButton.place(x=200,y=160)
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