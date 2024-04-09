import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

// Name: Atharv Adhyapak
// Student Number: 7229479

public class Server {
    public static void main(String[] args){
        int port = 3000; //port number for server

        try{
            ServerSocket socket = new ServerSocket(port);//create a server socket bound to specified port
            while(true){// Loop indefinitley to accept multiple connections
                Socket player1 = socket.accept();//Accept the connections from player 1
                System.out.println("Player 1 connected");//print message indicating player 1 is connected
                Socket player2 = socket.accept();//Accept the connection of player 2
                System.out.println("Player 2 connected");//print message indicating player 2 is connected
                game connect4 = new game(player1, player2);//create a new game instance for two players
                Thread marty = new Thread(connect4);//create a new thread for the game instance
                marty.start();//start the game thread

            }
        }
        catch (IOException e){
            e.printStackTrace();//print the stack trace if an IOException occurs
        }
    }
}
