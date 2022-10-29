from tkinter import *
import threading
from datetime import datetime
from socket import *
import pickle

class GUI:
    def __init__(self, name, ip_dest, port_dest, sucessFulconnection = False):
        self.root = Tk()
        self.name = str(name)
        self.ip_dest = ip_dest
        self.port_dest= port_dest
        self.successfulConection = sucessFulconnection
        self.Event = threading.Event()
        self.design_root()
        self.creating_socket()
        self.root.mainloop()
        
    def creating_socket (self):
        self.portInt = int(port_dest)
        self.successfulConection = True
        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect(('localhost',self.portInt))
        except:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.bind(('localhost',self.portInt))
            self.socket.listen(1)
            chat, addr = self.socket.accept()
            self.socket = chat

        self.receber_msg = threading.Thread(target=self.receiving)
        self.receber_msg.start()
        self.enviar_msg = threading.Thread(target=self.sending)
        self.enviar_msg.start() 
            
    def design_root(self):
        """Design da tela"""
        self.root.title('Chat P2P de ' + self.name) 
        
        '''Áreas da tela
            - Área de mensagens: espaço para exibir as mensagens recebidas/enviadas;
            - Área de informações: espaço para exibir horário de envio/recebimento.
        '''
        self.msg_area_label = Label(self.root, text='Area de mensagens') 
        self.infos_area_label = Label(self.root, text='Area de informações')

        self.infos_area = Text(self.root, font='Arial 10', width=40, height=14)
        self.chat = Text(self.root, font='Arial 10', width=60, height=14)

        self.input = Entry(self.root, width=60, font='Arial 10')

        self.btn_clear = Button(self.root, text='Limpar mensagens', padx= 40, command=self.clear)
        self.btn_send = Button(self.root, text='Send', padx = 40, command=self.check_press)
        self.root.bind("<Return>", self.check_press) # configura o enter para enviar mensagem

        self.btn_get_file = Button(self.root, text='Get file', padx = 40)
       
        self.msg_area_label.grid(row=0, columnspan=3)
        self.infos_area_label.grid(row=0, columnspan=3, column=3)
        self.infos_area.grid(row=1, column=3, columnspan=3)
        self.chat.grid(row=1, column=0, columnspan=2)
        self.input.grid(row=2, column=0, sticky=W, columnspan=3)
        self.btn_clear.grid(row=2, column=5)
        self.btn_send.grid(row=2, column=3, columnspan=1)
        self.btn_get_file.grid(row=2, column=4)      
    
    def sending(self, event = None):
        if self.successfulConection:
            while True:
                self.Event.wait()
                self.texto = self.input.get() + '\n'
                sendTime = self.show_date() + '\n'
                self.input.delete(0,END)
                msg_array = [self.texto,sendTime]
                msg_data = pickle.dumps(msg_array)
                self.socket.send(msg_data)
                self.Event.clear()

    def check_press(self, event = None):
        self.Event.set()
          
    def receiving(self):
        if self.successfulConection:
            while True:
                self.receive_msg = pickle.loads(self.socket.recv(2048))
                self.content = list(self.receive_msg)
                if self.content[0] != '\n':
                    self.chat.insert(END,self.content[0])
                    self.infos_area.insert(END,self.content[1])
    
    def show_date(self):
        """Função para exibir a hora na área de informações"""
        now = datetime.now()
        date_string = now.strftime("%H:%M:%S")
        return date_string
 
    def clear(self):
        """Limpa a área de mensagens e de exibição"""
        self.chat.delete("1.0",END)
        self.infos_area.delete("1.0",END)


class connector():
    """Tela inicial pra iniciar a conexão"""
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title('Connect config')

        self.user_name_label = Label(self.root,text="Nome de Usuário")
        self.ip_dest_label = Label(self.root, text="IP de destino")
        self.port_dest_label = Label(self.root, text="Porta de destino")

        self.ip_dest_entry = Entry(self.root)
        self.user_name_entry = Entry(self.root) 
        self.port_dest_entry = Entry(self.root)

        self.btn = Button(self.root, text='connect', command=self.conectar)

        '''Configurações de design'''
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
        fim = Button(self.root, text='Conexão feita. Clique aqui para fechar!', command=self.root.destroy).place(x=25, y=15)
        tela_2 = GUI(user_name,ip_dest,port_dest)
        tela_2()

if __name__ == '__main__':
    tela = connector()
    tela()