import tkinter as tk

root = tk.Tk()
root.geometry("200x200")
# create a scrollbar and listbox
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# set the scrollbar to control the listbox
scrollbar.config(command=listbox.yview)
xx = 0
# define a function to update the listbox
def update_listbox():
    # get the current time and add it to the listbox
    global xx+=1
    current_time = tk.StringVar(value=f"Time: {xx}")
    listbox.insert(tk.END, current_time.get())
    # delete the oldest item from the listbox if there are more than 10 items
    if listbox.size() > 10:
        listbox.delete(0)
    # schedule the function to run again in 2 seconds
    root.after(2000, update_listbox)

# start the update function
update_listbox()

root.mainloop()
