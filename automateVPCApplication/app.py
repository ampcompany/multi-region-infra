import tkinter as tk
import tkinter.ttk as ttk
import socket


class Window:
    def __init__(self, parent):
        parent.geometry('450x300')
        parent.title('AWS Multi Region Strategy VPC Generator')


class App:
    def __init__(self, parent):
        self.access_key_input_val = tk.StringVar()
        self.secret_access_key_input_val = tk.StringVar()
        self.nat_option_input_radiobutton_val = tk.IntVar()
        self.progress_bar_val = tk.DoubleVar()

        self.access_key_label = tk.Label(parent, text='Access Key')
        self.secret_access_key_label = tk.Label(parent, text='Secret Access Key')
        self.nat_option_label = tk.Label(parent, text='Activate NAT Gateway')
        self.alert_label = tk.Label(parent)

        self.access_key_input_box = tk.Entry(parent, width=30, textvariable=self.access_key_input_val)
        self.secret_access_key_input_box = tk.Entry(parent, width=30, textvariable=self.secret_access_key_input_val)
        self.nat_option_input_radiobutton_yes = tk.Radiobutton(parent, text='YES', value=1,
                                                               variable=self.nat_option_input_radiobutton_val)
        self.nat_option_input_radiobutton_no = tk.Radiobutton(parent, text='NO', value=0,
                                                              variable=self.nat_option_input_radiobutton_val)

        self.button = tk.Button(parent, text='Start', height=4, width=7, command=self.start)

        self.progress_bar = ttk.Progressbar(parent, maximum=100, length=400, variable=self.progress_bar_val)

        self.listbox = tk.Listbox(parent, width=60)

        self.grid()
        self.check_internet_connectivity()

    def grid(self):
        self.access_key_label.grid(row=0, column=0, padx=10)
        self.access_key_input_box.grid(row=0, column=1, columnspan=2)
        self.secret_access_key_label.grid(row=1, column=0, padx=10)
        self.secret_access_key_input_box.grid(row=1, column=1, columnspan=2)
        self.nat_option_label.grid(row=2, column=0, padx=10)
        self.nat_option_input_radiobutton_yes.grid(row=2, column=1)
        self.nat_option_input_radiobutton_no.grid(row=2, column=2)
        self.alert_label.grid(row=3, column=0, columnspan=4)
        self.button.grid(row=0, column=3, rowspan=3, padx=10)
        self.progress_bar.grid(row=4, column=0, columnspan=4)
        self.listbox.grid(row=5, column=0, columnspan=4, pady=10)

    def check_internet_connectivity(self):
        ip = socket.gethostbyname(socket.gethostname())

        if ip == '127.0.0.1':
            # Internet Disconnected
            self.alert_label.config(text='Cannot Connect to Internet', fg='#ff0000')
        else:
            # Internet Connected
            self.alert_label.config(text='READY', fg='#0000ff')

    def start(self):
        if len(self.access_key_input_val.get()) <= 0:
            self.alert_label.config(text='Please Enter Your AWS IAM User ACCESS KEY', fg='#ff0000')
            self.access_key_input_box.focus()

        elif len(self.secret_access_key_input_val.get()) <= 0:
            self.alert_label.config(text='Please Enter Your AWS IAM User SECRET ACCESS KEY', fg='#ff0000')
            self.secret_access_key_input_box.focus()

        else:
            self.alert_label.config(text='Processing......', fg='#0000ff')
            self.access_key_input_box.config(state=tk.DISABLED)
            self.secret_access_key_input_box.config(state=tk.DISABLED)
            self.nat_option_input_radiobutton_yes.config(state=tk.DISABLED)
            self.nat_option_input_radiobutton_no.config(state=tk.DISABLED)
            self.button.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    Window(root)
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
