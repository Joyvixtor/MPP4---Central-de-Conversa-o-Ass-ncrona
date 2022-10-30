from tkinter import *
import threading
from datetime import datetime
from socket import *
import pickle
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from sys import argv, stdout

class GUI:
    def __init__(self, name, ip_dest, port_dest, sucessFulconnection = False):
        self.root = Tk()
        self.name = str(name)
        self.ip_dest = ip_dest
        self.port_dest= port_dest
        self.successfulConection = sucessFulconnection # booleano para conferir se a conexão já foi feita
        self.EventMsg = threading.Event() # evento para, toda vez que der Enter ou Send, a mensagem enviar
        self.EventFile = threading.Event()
        self.design_root()
        self.creating_sockets()
        self.root.mainloop()
        
    def creating_sockets (self):
        """Criação de sockets e estabelecimento de conexão"""
        self.portInt = int(port_dest) # porta para inteiro, é recebida em string
        self.successfulConection = True # a conexão já vai ser estabelecida de alguma forma pelo try except, então muda para True
        try:
            self.socketMsg = socket(AF_INET, SOCK_STREAM)
            self.socketFile = socket(AF_INET,SOCK_DGRAM)
            self.socketMsg.connect(('localhost',self.portInt))
        except:
            self.socketMsg = socket(AF_INET, SOCK_STREAM)
            self.socketFile = socket(AF_INET,SOCK_DGRAM)
            self.socketMsg.bind(('localhost',self.portInt))
            self.socketMsg.listen(1)
            chat, addr = self.socketMsg.accept()
            self.socketMsg = chat
            self.socketFile.bind(('localhost',self.portInt)) # dois sockets, contanto que sejam de protocolos diferentes, podem escutar numa mesma porta. Por isso, o socket TCP e UDP tão na mesma porta especificada.
        
        '''
            Início das threads de recebimento e envio de mensagens
        '''
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

        self.infos_area = Text(self.root, font='Arial 10', width=60, height=14)
        self.chat = Text(self.root, font='Arial 10', width=60, height=14)

        self.input = Entry(self.root, width=60, font='Arial 10')

        self.btn_clear = Button(self.root, text='Limpar mensagens', padx= 40, command=self.clear)
        self.btn_send = Button(self.root, text='Send', padx = 40, command=self.check_press)
        self.root.bind("<Return>", self.check_press) # configura o enter para enviar mensagem

        self.btn_get_file = Button(self.root, text='Get file', padx = 40, command= self.getFile)
       
        self.msg_area_label.grid(row=0, columnspan=3)
        self.infos_area_label.grid(row=0, columnspan=3, column=3)
        self.infos_area.grid(row=1, column=3, columnspan=3)
        self.chat.grid(row=1, column=0, columnspan=2)
        self.input.grid(row=2, column=0, sticky=W, columnspan=3)
        self.btn_clear.grid(row=2, column=5)
        self.btn_send.grid(row=2, column=3, columnspan=1)
        self.btn_get_file.grid(row=2, column=4)      
    
    def sending(self, event = None):
        """Método para envio de mensagens"""
        if self.successfulConection:
            msg_user_encode = self.name.encode('utf-8') # como a conexão foi bem sucedida, ele vai enviar seu user para o outro lado.
            self.socketMsg.send(msg_user_encode)
            while True:
                self.EventMsg.wait() # se o Evento tiver True -> prossegue para a linha 77 adiante
                self.texto = self.input.get() + '\n'
                sendTime = self.show_date()
                self.input.delete(0,END)
                msg_array = [self.texto,sendTime,self.name]
                msg_data = pickle.dumps(msg_array)
                self.socketMsg.send(msg_data)
                self.EventMsg.clear() # após envio da mensagem, o Evento volta a ser Falso, já que não tem nenhuma mensagem mais para enviar.

    def check_press(self, event = None):
        """Método para setar o Evento para True."""
        self.EventMsg.set()
        # Toda vez que o Enter ou Send for pressionado, o evento vai ser setado para verdadeiro, e aí então a thread do envio passa da linha 77 e envia a mensagem.
                    
    def receiving(self):
        """Método para recebimento de mensagem"""
        if self.successfulConection:
            self.UserOtherSide = self.socketMsg.recv(2048).decode('utf-8') # assim que se conecta, ele vai receber o user do outro lado
            print(self.UserOtherSide)
            while True:
                self.receive_msg = pickle.loads(self.socketMsg.recv(2048))
                self.content = list(self.receive_msg)
                if self.content[0] != '\n':
                    self.chat.insert(END,self.content[0])
                    self.infos_msg = '({}): enviada às {} / recebida às {} \n'.format(self.UserOtherSide,self.content[1],self.show_date())
                    self.infos_area.insert(END,self.infos_msg)
    
    def show_date(self):
        """Função para exibir a hora na área de informações"""
        now = datetime.now()
        date_string = now.strftime("%H:%M:%S")
        return date_string

    def getFile(self):
        path = filedialog.askopenfilename()
        if path == '':
            return
        file_format = path.split('.')[-1]
        if file_format in ['mp3', 'wav', 'ogg']:
            self.chat.insert(END, f"$AUDIO: {path.split('/')[-1]}\n\n")
        elif file_format in ['mp4', 'MOV']:
            self.chat.insert(END, f"$VIDEO: {path.split('/')[-1]}\n\n")
        else:
            try:
                img = Image.open(path)

                miniature_img = img.resize((500,500))
                self.my_img = ImageTk.PhotoImage(miniature_img)  
                self.chat.image_create(END, image=self.my_img)
                self.chat.insert(END, "\n\n")
            except:
                self.chat.insert(END, f"$FILE: {path.split('/')[-1]}\n\n")
        
        self.chat.insert(END,'começando o envio! \n')
        # cenas do proximo capítulo, falta implementar o rdt 

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