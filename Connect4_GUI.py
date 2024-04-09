#Name: Atharv Adhyapak
#Student Number: 7229479


import tkinter as tk  #Import the tkinter module for GUI
from tkinter import messagebox  # Import the messagebox submodule for displaying messages
import socket
import threading


class MYGUI:
   


    def __init__(self):

        self.player = 1 #Initalize player variable to keep track of player turn

        self.turn = False #Intialize turn variable to keep track of players turn

        

        num_rows = 6  #Number of rows
        num_cols = 7  #Number of columns 

        # Create an empty grid to represent the game board
        self.grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]



        self.root = tk.Tk()  #Create a tkinter window
        self.root.geometry("700x700")  #Set the size of the window
        self.root.title("Assignment 2: Connect 4")  #Set the title of the window

       #Connect to server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(('localhost', 3000))
     
      
        #Create and pack a label widget into window
        self.label = tk.Label(self.root, text="Welcome to Connect 4!", font=('Arial', 18))
        self.label.pack()  

        #Create and pack a canvas widget into the window for drawing the game board
        self.canvas = tk.Canvas(self.root, width=560, height=480, bg='blue')
        self.canvas.pack()  

        #Draw the empty game board on the canvas
        for i in range(num_rows):  #Iterate over rows
            for j in range(num_cols):  #Iterate over columns
                # Draw a rectangle for each cell in the game board
                self.canvas.create_rectangle(j * 80, i * 80, (j + 1) * 80, (i + 1) * 80, width=1)
        response = b''  #Initialize an empty byte string for the response
        while True:
            try:
                #Receive data from the server
                chunk = self.server_socket.recv(1024)
                #Set a timeout after the first chunk is received
                self.server_socket.settimeout(0.5)
                if not chunk: #If no more data is received, break the loop
                    break
                response += chunk  #Append the received data to the response variable
            except socket.timeout:  #Timeout occurred
                break  #Break out of the loop if timeout occurs
        
        response = response.decode()  #Convert the response from bytes to string
        response = response.split("\n")
       

        if(response[7] == "You are player 2"):#Check if the player is player 2
            self.player = 2
            #Start a new thread to handle receving message from the server
            thread = threading.Thread(target = self.threadFunction)
            thread.start()
            #Bind the canvas click event to the canvasClick 2 method
            self.canvas.bind("<Button-1>", self.canvasClick2)
            self.root.mainloop()

        else:
            #Bind the canvas click event to the canvasClick 2 method
            self.canvas.bind("<Button-1>", self.canvasClick)
            self.root.mainloop()

    #Method to haandle recieving messaages from the server in a seperate thread
    def threadFunction(self):
        response = b''  #Initialize an empty byte string for the response
        chunk = None #Initalize variable to store chuncks of data recieved from the server
        first_chunk_received = False#Flag to indicate wether the first chunk of data has been recevied

        self.server_socket.settimeout(None)#Disable the timeout for receving data from the server
        while True: #Infinite loop to continously recieve data from the server
            try:
                # Receive data from the server
                chunk = self.server_socket.recv(1024)
                    
                if not first_chunk_received: #Check if its the first chunk of data
                    first_chunk_received = True #Set flag to indicate the first chunk is recieved 
                    
                    self.server_socket.settimeout(0.5)#Set a timeout for subsequent recv calls
                    
                if chunk == b'':  #Check if empty chunk is recieved
                    print("Received an empty chunk. Exiting the loop.")
                    break  # Break out of the loop if an empty chunk is received
                    
                response += chunk  #Append the received data to the response variable

            except socket.timeout: #Handle timeout exception
                break  #Break out of the loop if no more data is received within the timeout
                    
            except Exception as e: #Handle other exceptions
                print("Exception occurred:", e)
                break  # Break out of the loop if any exception occurs



        response = response.decode()  #Convert the response from bytes to string
        response = response.split("\n") #Split the response into lines
        for i in range(6): #Iterate over each row in the grid
            columns =  response[i].split("]") #Split each row into columns
            for j in range(7):#iterate over each column in the row
                self.grid[i][j] = columns[j][1]#Update the grid with the recieved data
        #Update GUI
        self.update_GUI()

    
      
        self.turn = True #Set the turn flag to indicate if its players turn
     
    #Method to handle canvas click event for player 1
    def canvasClick(self, event):

        column = event.x // 80 #Calculate the column index based on the x-cord of the click event
        #Check if the top row of the clicked column is already occupied
        if self.grid[0][column] == "O" or self.grid[0][column] =='X':
            #Display the message box indicating that the column is full
            messagebox.showinfo("Full", "column is full")
            return
        self.send_move(column) #Send the players movd to the server

    #Method to handle canvas click event for player 2
    def canvasClick2(self, event):

        column = event.x // 80##Calculate the column index based on the x-cord of the click event
         #Check if it's player 2s top row of the clicked column is not occupied
        if self.grid[0][column] == "O" or self.grid[0][column] =='X':
            #Display the message box indicating that the column is full
            messagebox.showinfo("Full", "column is full")
            return
        if(self.turn):
            self.send_move(column)#Send player 2s move to the server
        

    #Method to send the player's move to the server
    def send_move(self, column):
        #Send the column index of the move to the server, adding 1 to match the servers indexing
        self.server_socket.send((str(column + 1) + "\n").encode())
        response = b''  #Initialize an empty byte string for the response
        chunk = None #Initalize a variable to sotre chunks of data recevied from the server
        first_chunk_received = False #Flag to indicate whether the first chunk of data has been recieved

        self.server_socket.settimeout(None) #Disable the timeout for receving data from the server
        while True: #Infinte loop to continously recevie data from the server
            try:
                #Receive data from the server
                chunk = self.server_socket.recv(1024)
                    
                if not first_chunk_received: #Check if its the first chunk of the data
                    first_chunk_received = True #Set the flag to indicate the first chunk is received
                    #Set a timeout for subsequent recv calls
                    self.server_socket.settimeout(1)
                    
                if chunk == b'':  #If an empty chunk is received, handle it differently
                    print("Received an empty chunk. Exiting the loop.")
                    break  #Break out of the loop if an empty chunk is received
                    
                response += chunk  #Append the received data to the response variable

            except socket.timeout: #Handle timeout exception
                break  #Break out of the loop if no more data is received within the timeout
                    
            except Exception as e: #Handle other exceptions
                print("Exception occurred:", e)
                break  #Break out of the loop if any exception occurs



        response = response.decode()  #Convert the response from bytes to string
        response = response.split("\n") #Split the response into lines
        for i in range(6): #Iterate over each row in the grid
            columns =  response[i].split("]") #Split each row into columns
            for j in range(7): #Iterate over each column in the row
                self.grid[i][j] = columns[j][1] #Update the grid with the recevied data
        
      #Update GUI 
        self.update_GUI()


       
        if len(response) > 8: 
            if(response[8] == "Player 1 wins!"):
                #Display a message box indicating that PLayer 1 wins
                messagebox.showinfo("Winner", "Player 1 wins!")
                #Reset the grid
                self.grid = [[0 for _ in range(7)] for _ in range(6)]
                self.turn = False
                #Update the GUI
                self.update_GUI()
                #If the current player is player 2, start a new thread to handle receiving messages from the server
                if self.player == 2:
                    thread = threading.Thread(target=self.threadFunction)
                    thread.start()
                return
            elif (response[8] == "Player 2 wins!"):
                #Display a message box indicating that PLayer 2 wins
                messagebox.showinfo("Winner", "Player 2 wins!")
                #Rest the grid
                self.grid = [[0 for _ in range(7)] for _ in range(6)]
                self.turn = False
                #UpdateG GUI
                self.update_GUI()
                #If the current player is player 2, start a new thread to handle receiving messages from the server
                if self.player == 2:
                    thread = threading.Thread(target=self.threadFunction)
                    thread.start()
                return
            elif response[8] == "It's a tie!":
                #Display a message box indicating that it's a tie
                messagebox.showinfo("No Winner", "its A TIE!")
                #Reset the grid
                self.grid = [[0 for _ in range(7)] for _ in range(6)]
                self.turn = False
                #Update GUI
                self.update_GUI()
                # If the current player is player 2, start a new thread to handle receiving messages from the server
                if self.player == 2:
                    thread = threading.Thread(target=self.threadFunction)
                    thread.start()
                return

        response = b''  #Initialize an empty byte string for the response
        chunk = None #Reset the chunk variable to None
        first_chunk_received = False #Reset the first_chunk_recived flag to False

        self.server_socket.settimeout(None) #Disable the timeout for receving data from the server
        while True: #Infinite loop to continuously receive data from the server
            try:
                # Receive data from the server
                chunk = self.server_socket.recv(1024)
                    
                if not first_chunk_received:  #Check if it's the first chunk of data
                    first_chunk_received = True  #Set the flag to indicate the first chunk is received
                    #Set a timeout for subsequent recv calls
                    self.server_socket.settimeout(0.5)
                    
                if chunk == b'':  #If an empty chunk is received, handle it differently
                    print("Received an empty chunk. Exiting the loop.")
                    break  #Break out of the loop if an empty chunk is received
                    
                response += chunk  #Append the received data to the response variable

            except socket.timeout: #Handle timeout exception
                break  #Break out of the loop if no more data is received within the timeout
                    
            except Exception as e: #Handle other exception
                print("Exception occurred:", e)
                break  #Break out of the loop if any exception occurs



        response = response.decode()  #Convert the response from bytes to string
        response = response.split("\n") #Split the response into lines
        for i in range(6):  #Iterate over each row in the grid
            columns =  response[i].split("]")#Split each row into columns
            for j in range(7): #Iterate over each column in the row
                self.grid[i][j] = columns[j][1] #Update the grid with the received data
       

        #update GUI
        self.update_GUI()
        if len(response) > 8:
            if(response[8] == "Player 1 wins!"):
                 #Display a message box indicating that PLayer 1 wins
                messagebox.showinfo("Winner", "Player 1 wins!")
                #Reset the grid
                self.grid = [[0 for _ in range(7)] for _ in range(6)]
                self.turn = False
                #Update the GUI
                self.update_GUI()
                #If the current player is player 2, start a new thread to handle receiving messages from the server
                if self.player == 2:
                    thread = threading.Thread(target=self.threadFunction)
                    thread.start()
            elif (response[8] == "Player 2 wins!"):
                 #Display a message box indicating that PLayer 2 wins
                messagebox.showinfo("Winner", "Player 2 wins!")
                #Reset the grid
                self.grid = [[0 for _ in range(7)] for _ in range(6)]
                self.turn = False
                #Update GUI
                self.update_GUI()
                #If the current player is player 2, start a new thread to handle receiving messages from the server
                if self.player == 2:
                    thread = threading.Thread(target=self.threadFunction)
                    thread.start()
            elif response[8] == "It's a tie!":
                #Display a message box indicating that it's a tie
                messagebox.showinfo("No Winner", "its A TIE!")
                #Reset grid
                self.grid = [[0 for _ in range(7)] for _ in range(6)]
                self.turn = False
                #Update GUI
                self.update_GUI()
                #If the current player is player 2, start a new thread to handle receiving messages from the server
                if self.player == 2:
                    thread = threading.Thread(target=self.threadFunction)
                    thread.start()
            


        
    #Method to update the GUI based on the current state of the game grid
    def update_GUI(self):
        ovals = self.canvas.find_withtag("chips")# Find all chips on the canvas
        for oval in ovals: #Iterate over each oval found
            self.canvas.delete(oval) #Delete the oval from the canvas
        
        for i in range(len(self.grid)): #Iterate over each row in the grid
            for j in range(len(self.grid[i])):#Iterate over each column in the row
                 #Check the value in the grid cell
                if self.grid[i][j] == 'X': #If it's 'X' (player 1)
                     #Create a red chip on the canvas at the appropriate position
                    self.canvas.create_oval(j * 80 + 10, i * 80 + 10, (j + 1) * 80 - 10, 
                                            (i + 1) * 80 - 10, fill="red", tags="chips")
                    
                    
                elif self.grid[i][j] == 'O':  #If it's 'O' (player 2)
                     # Create a yellow chip on the canvas at the appropriate position
                    self.canvas.create_oval(j * 80 + 10, i * 80 + 10, (j + 1) * 80 - 10, 
                                            (i + 1) * 80 - 10, fill="yellow", tags="chips")
        self.root.update()  #Update the root window to reflect the changes in the canvas
                    
    


    

    
        
# Create an instance of MYGUI to start the GUI
my_gui = MYGUI()
