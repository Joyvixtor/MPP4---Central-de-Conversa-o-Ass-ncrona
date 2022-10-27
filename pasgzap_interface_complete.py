from tkinter import *

class GUI:
    def __init__(self, name, ip_dest, port_dest):
        self.name = name
        self.ip_dest = ip_dest
        self.port_dest= port_dest
        self.root = Tk()
        self.design_root()
        self.root.mainloop()

    def design_root(self):
        self.root.title('Chat P2P de ' + self.name) 
        

        self.msg_area_label = Label(self.root, text='Area de mensagens') 
        self.infos_area_label = Label(self.root, text='Area de informações') 
        self.infos_area = Text(self.root, font='Arial 10', width=40, height=14)
        self.chat = Text(self.root, font='Arial 10', width=60, height=14)
        self.inpt = Entry(self.root, width=60, font='Arial 10')
        self.btn_clear = Button(self.root, text='Limpar mensagens')
        self.btn_send = Button(self.root, text='send')
        self.btn_get_file = Button(self.root, text='get file')
       
        self.msg_area_label.grid(row=0, columnspan=3)
        self.infos_area_label.grid(row=0, columnspan=3, column=3)
        self.infos_area.grid(row=1, column=3, columnspan=3)
        self.chat.grid(row=1, column=0, columnspan=2)
        self.inpt.grid(row=2, column=0, sticky=W, columnspan=3)
        self.btn_clear.grid(row=2, column=5)
        self.btn_send.grid(row=2, column=3, columnspan=1)
        self.btn_get_file.grid(row=2, column=4)        
        


class connector():
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title('Connect config')

        self.user_name_label = Label(self.root,text="Nome de Usuário")
        self.ip_dest_label = Label(self.root, text='IP de destino')
        self.port_dest_label = Label(self.root, text='Porta de destino')
        self.ip_dest_entry = Entry(self.root)
        self.user_name_entry = Entry(self.root) 
        self.port_dest_entry = Entry(self.root)
        self.btn = Button(self.root, text='connect', command=self.conectar)
        
        self.port_dest_label.grid(row=2, sticky=W)
        self.ip_dest_label.grid(row=1, sticky=W)
        self.user_name_label.grid(row=0, column=0, sticky=W)
        self.user_name_entry.grid(row=0, column=1, sticky=E)
        self.ip_dest_entry.grid(row=1, column=1, sticky=E)
        self.port_dest_entry.grid(row=2, column=1, sticky=E)
        self.btn.grid(row=3, column=1, sticky=E)
        self.root.mainloop()


    def conectar(self):
        global user_name, ip_dest, port_dest
        user_name = self.user_name_entry.get()
        ip_dest = self.ip_dest_entry.get()
        port_dest = self.port_dest_entry.get()
        print(user_name, ip_dest, port_dest)
        fim = Button(self.root, text='A conexão esta sendo feita').place(x=25, y=15)
        tela_2 = GUI(user_name, ip_dest, port_dest)
        tela_2()
   
tela = connector()
tela()