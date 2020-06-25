"""

Title = 'CR2 Deleter'
Description = 'Manually selecting and moving only .CR2 images (Canon's RAW images) to another folder can be tedious.
               This code provides a simple window to move and delete the RAW images within few clicks'
Author = 'Mukil Saravanan'
Version = 'v1'
Email = 'senjerimalaimukil@gmail.com'


"""


#Importing the neccessary libraries 

import tkinter as tk                 #Tkinter for GUI
from tkinter import filedialog,ttk   #filedialog package to get path to the directory ; ttk to use scrollbar method
import os,shutil                     #os,shutil is used for various operations related to the operating system (Here : move and delete operations)


##############################################   FUNCTION DEFINITIONS  ###########################################################################


def dropdown():
    
    """ To get the path to the directory containing .CR2 images """
    
    source_path = tk.filedialog.askdirectory()   #selecting the directory
    entry.delete(0,tk.END)                       #deleting the text from zeroth index to the end,in case any text is present before
    entry.insert(0,source_path)                  #inserting the path to the directory selected
    
def move():
    
    """ To move the .CR2 images to another directory """
    
    source_path=entry.get()
    
    #if the entered path does not exist
    if not os.path.exists(source_path):
        text.insert(tk.INSERT,'No such directory exists.\nEnter a valid path or use the dropdown button.\n')
    else:
        #if the path exists,do the following
        os.chdir(source_path)
        items=os.listdir()
        #shows the total number of files
        total_files='Total files: {}\n'.format(len(items))
        global destination_path
        destination_path=os.path.join(source_path,'Only Raw Images')
        #if the directory ( to move .CR2 images ) does not exist, it creates a new directory 
        if not os.path.exists(destination_path):
            os.mkdir('Only Raw Images')
        #moves the .CR2 images to the destination directory
        i=0
        for item in items:
            if '.CR2' in item:
                filepath=os.path.join(os.getcwd(),item)
                shutil.move(filepath,destination_path)
                i+=1
        #shows the number of .CR2 images and destination path in which the images are moved          
        total_raw_files='{} raw files are moved to {}\n'.format(i,destination_path)
        text.insert(tk.INSERT,total_files+total_raw_files)

def delete():
    
    """To delete the .CR2 images"""
    
    os.chdir(destination_path)
    #checks the directory before deleting
    if 'Only Raw Images' in os.getcwd():
        text.insert(tk.INSERT,'The following images will be deleted\n')
        #prints the name of the items in the directory
        for item in os.listdir():
            text.insert(tk.INSERT,(item+'\n'))
        delete_confirmation()
    else:
        text.insert(tk.INSERT,'Something went wrong.\nTry reopening the application')
        
def delete_confirmation():
    
    "Adding an extra level of confirmation.Since deletion can't be undone"
    
    #initaliasing a message window
    global prompt
    prompt=tk.Tk()                      
    prompt.geometry('450x200')         #setting the dimensions of the window
    prompt.title('Confirmation')       #Adding a title to the window
    
    #Creating a canvas
    prompt_canvas=tk.Canvas(prompt,bg='#191919')
    prompt_canvas.pack(expand=True,fill='both')

    #Creating a frame at the top
    prompt_upper_frame=tk.Frame(prompt,bg='#595959',bd=5)
    prompt_upper_frame.place(relx=0.5,rely=0.1,relheight=0.2,relwidth=0.75,anchor='n')
    
    #Creating a label that shows the message to the user
    prompt_label=tk.Label(prompt_upper_frame,font=40,text="The files will be deleted and it can't be undone.")
    prompt_label.place(relheight=1,relwidth=1)
    
    #Creating a delete confirmation button
    prompt_delete_button=tk.Button(prompt_canvas,font=40,text='DELETE',command=deletion_confirmed)
    prompt_delete_button.place(relx=0.20,rely=0.50,relwidth=0.25,relheight=0.15)
    
    #Crearing a cancel button
    prompt_cancel_button=tk.Button(prompt_canvas,font=40,text='CANCEL',command=cancel)
    prompt_cancel_button.place(relx=0.55,rely=0.50,relwidth=0.25,relheight=0.15)

    prompt.mainloop()

def  deletion_confirmed():
    
    """Deletes the .CR2 images ,only if it is confirmed by the user"""
    
    for item in os.listdir():
        #Deletes the files in the directory
        os.remove(item)
        print(item,os.getcwd())
    text.insert(tk.INSERT,'Deleted successfully\n')
    #Finally closes the message window
    prompt.destroy() 

def cancel():
    
    """Cancels the operation"""
    
    text.insert(tk.INSERT,'Cancelled\n')
    #Finally closes the message window
    prompt.destroy()

    
##############################################   MAIN BLOCK  ###########################################################################    
    
        
#Initialising a window     
root=tk.Tk()                                   
root.geometry('800x600')                       #setting the dimensions of the window
root.title('CR2 Deleter')                      #Adding a title to the window
root.iconbitmap('cr2.ico')                     #Adding a icon to the window

#Creating a canvas 
canvas=tk.Canvas(root,bg='#191919')            
canvas.pack(expand=True,fill='both')

#Creating a frame at the top
upper_frame=tk.Frame(root,bg='#595959',bd=5)
upper_frame.place(relx=0.5,rely=0.1,relheight=0.2,relwidth=0.75,anchor='n')

#Creating a label to show information
info_label=tk.Label(upper_frame,text='Enter the source path or use the dropdown button',font=50)
info_label.place(relwidth=1)

#Creating a entry box to type text into it.
entry=tk.Entry(upper_frame,font=40)
entry.place(relwidth=0.65,rely=0.25,relheight=0.5)

#Creating a button to select the directory and calls the function dropdown, when it is pressed
drop_button=tk.Button(upper_frame,font=40,text='v',command=dropdown)
drop_button.place(relx=0.65,rely=0.25,relwidth=0.05,relheight=0.5)

#Creating another button for move command and calls the function move, when it is pressed
move_button=tk.Button(upper_frame,font=40,text='MOVE',command=move)
move_button.place(relx=0.7,rely=0.25,relwidth=0.15,relheight=0.5)

#Creating another button for delete command and calls the function delete, when it is pressed
delete_button=tk.Button(upper_frame,font=40,text='DELETE',command=delete)
delete_button.place(relx=0.85,rely=0.25,relwidth=0.15,relheight=0.5)

#Crearting a frame that sits below the elements above
lower_frame=tk.Frame(root,bg='#595959',bd=10)
lower_frame.place(relwidth=0.75,relheight=0.6,relx=0.5,rely=0.25,anchor='n')

#Creating a vertical scrollbar to avoid overflow
vertical_scroller=tk.Scrollbar(lower_frame,orient=tk.VERTICAL,wrap=None)
vertical_scroller.pack(side=tk.RIGHT,fill=tk.Y)

#This shows the status and information for the end user
text=tk.Text(lower_frame,font=40,cnf='',yscrollcommand=vertical_scroller.set)
text.pack(expand=True,fill='both')

vertical_scroller.config(command=text.yview)

root.mainloop()    
    