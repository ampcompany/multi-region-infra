import tkinter as tk

root = tk.Tk()

root.geometry('400x240')
root.title('AWS Multi Region Strategy VPC Generator')

access_key_label = tk.Label(root, text='Access Key')
secret_access_key_label = tk.Label(root, text='Secret Access Key')

access_key_input_box = tk.Entry(root, width=30)
secret_access_key_input_box = tk.Entry(root, width=30)

button = tk.Button(root, text='Start', height=2)

access_key_label.grid(row=0, column=0)
access_key_input_box.grid(row=0, column=1)
secret_access_key_label.grid(row=1, column=0)
secret_access_key_input_box.grid(row=1, column=1)
button.grid(row=0, column=2, rowspan=2)

root.mainloop()
