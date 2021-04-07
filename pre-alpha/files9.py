import shutil
import os
import os.path
from tkinter import *
from tkinter.messagebox import *
from tkinter.simpledialog import *

main = Tk()
#---
main.rowconfigure(1, weight=1)
main.columnconfigure(1, weight=1)
#---
main.title("MibiFile (cf9) pa")
#===Stringvar===
path_str = StringVar()
path_list_int = IntVar()
path_str_old = StringVar()
copycut_file = StringVar()
copytype = IntVar()
path_str.set("/home")
path_str_old.set("/")
#=============

def refresh():
   path = path_str.get()
   permission = True
   try:
      files = os.listdir(path)
      permission = True
   except PermissionError:
      showerror("Error ...", "Permission denied")
      permission = False
   if permission == True:
      dirs.insert(1, "..")
      item_nb = 2
      for item in files:
         if os.path.isdir(path_str.get() + "/" + item):
            item += " <dir>"
         dirs.insert(item_nb, item)
         item_nb += 1
      path_list_int.set(item_nb)
   return permission
def invertstring(string):
   newstring = ""
   for letter in string:
      newstring = letter + newstring
   return newstring
def opendir(event):
   path = path_str.get()
   dir_sel = dirs.get(ACTIVE)
   if dir_sel == "..":
      # path_str.set(path_str_old.get())
      path = invertstring(path_str.get())
      newpath = ""
      for letter in path:
         if letter == "/":
            newpath += letter
            break
         else:
            newpath += letter
      #newpath_two = invertstring(newpath)
      path = path_str.get()
      newpath_len = len(newpath)
      newpath_len_dub = newpath_len * 2
      newpath_minu = newpath_len - newpath_len_dub
      #path = path - newpath_two
      path = path[:newpath_minu]
      """
      scroll = len(path)
      end = False
      while scroll != 0:
         if end == False:
            letter = path[scroll - 1: scroll]
            if letter == "/":
               print("slash")
               end = True
            else:
               print("Other")
         else:
            newpath = letter + newpath
         scroll = scroll - 1
      path = "/"# + invertstring(newpath)
      """
      path_str.set(path)
      print(path)
      #---
      if path == "":
         path_str.set("/")
      permission = refresh()
      if permission == True:
         dirs.delete(0,END)
         refresh()
   elif not dir_sel == "":
      path_str_old.set(path)
      dir_sel = dir_sel.replace(" <dir>", "")
      newpath = path + "/" + dir_sel
      print("new_dir")
      path_str.set(newpath)
      if not os.path.isfile(path_str.get()):
         permission = refresh()
         if permission == True:
            dirs.delete(0,END)
            refresh()
         else:
            path_str.set(path_str_old.get())
      else:
         path_str.set(path_str_old.get())
         """
         path_items = len(dirs.get('@1,0', END)) + 1
         scroll = 0
         dirs.selection_clear(0, END)
         while scroll != path_items:
            dirs.delete(scroll)
            scroll += 1
         """
#===
path_label = Label(main, textvariable = path_str)
dirs = Listbox(main)
#---
dirs_scrollbar = Scrollbar(main, width = 8, repeatdelay = 50, relief = GROOVE)
# dirs.pack(expand = True, fill = "both")
path_label.grid(row = 0, column = 1, columnspan = 2)
#---
dirs.grid(sticky = "nesw", row = 1, column = 1)
dirs_scrollbar.grid(sticky = "nesw", row = 1, column = 2)
#---
dirs.config(yscrollcommand=dirs_scrollbar.set)
refresh()

dirs.bind("<Return>", opendir)

#===menu===
def copyf(event=None):
   file = dirs.get(ACTIVE)
   copycut_file.set(file)
   copytype.set(1)
def copyf_wm(event=None):
   file = dirs.get(ACTIVE)
   copycut_file.set(file)
   copytype.set(2)
   pass
def pastef(event=None):
   if not copycut_file.get() == "":
      if os.path.exists(copycut_file.get()) and os.path.isfile(copycut_file.get()):
         if copytype.get() == 1:
            shutil.copy(copycut_file.get(), path_str.get())
         elif copytype.get() == 2:
            shutil.copy2(copycut_file.get(), path_str.get())
         dirs.delete(0,END)
         refresh()
      else:
         showerror("Error ...","The same filename as file to copy file was found in this directory.")
   else:
      showerror("Error ...","Nothing to past.")
def mkdir(event=None):
   newdir_name = askstring("Make a new folder ...", "Folder name :", parent=main)
   newdir_path = path_str.get() + "/" + newdir_name
   if not os.path.exists(newdir_path):
      os.mkdir(newdir_path)
   else:
      showerror("Error ...","This folder already exists.")
   dirs.delete(0,END)
   refresh()
def gotop(event=None):
   path = askstring("Go to ...", "Path :", parent=main)
   try:
      path_str_old.set(path_str.get())
      path_str.set(path)
      dirs.delete(0,END)
      refresh()
   except:
      showerror("Error ...","You don't can go to this path.")
      path_str.set(path_str_old.get())
      dirs.delete(0,END)
      refresh()
#===
menu = Menu(main, tearoff = 0)
#=copy submenu=
copymenu = Menu(menu, tearoff = 0)
copymenu.add_command(label="Copy (without metadata : default operation)", command = copyf)
copymenu.add_command(label="Copy (with metadata)", command = copyf_wm)
#==============
menu.add_command(label="Go to a path", command = gotop)
menu.add_command(label="Copy the path to this item")
menu.add_separator()
menu.add_command(label="New directory", command = mkdir)
menu.add_separator()
menu.add_cascade(label = "Copy", menu = copymenu)
menu.add_command(label="Paste", command = pastef)
menu.add_separator()
menu.add_command(label="Cut")
menu.add_separator()
menu.add_command(label="Toggle this menu")
#===
def showmenu(event):
   menu.post(event.x + 84, event.y + 167)
main.bind("<Button-3>", showmenu)
#===========

main.mainloop()
#os.path.isfile('/home/wtlx/rep/file.txt')
#Get items listbox :
#>>> lb.get('@1,0', END)
#>>> ('1', '2', '3', '4')
#===================
