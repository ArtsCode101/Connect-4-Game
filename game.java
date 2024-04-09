import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.net.SocketException;

// Name: Atharv Adhyapak
// Student Number: 7229479
public class game implements Runnable {
    int playerTurn =  1;//Initializing player turn
    Socket player1; //Declaring socket variable for player 1
    Socket player2; //Declaring socket variable for player 1
    private int[][] connectBoard; //Declaring a 2D array to represent game board
    boolean over = false;
    public game(Socket player1, Socket player2){
        this.player1 = player1; // Assigning player 1 socket
        this.player2 = player2; // Assigning player 2 socket

    }

    @Override
    public void run() {
        initializeBoard(); //initalizing game board

        try(InputStream inputplayer1 = player1.getInputStream(); //creating input stream for player 1
            InputStream inputplayer2 = player2.getInputStream(); //creating input stream for player 2
            OutputStream outputplayer1 = player1.getOutputStream(); //creating output stream for player 1
            OutputStream outputplayer2 = player2.getOutputStream()){ //creating output stream for player 2
            displayBoard(outputplayer1, outputplayer2);// Displaying the inital game board

            try{
                outputplayer1.write("You are player 1\n".getBytes());//Notifying whose player 1

            }
            catch (IOException e){
                e.printStackTrace();
            }

            try{
                outputplayer2.write("You are player 2\n".getBytes()); //Notifying whose player 2
            }
            catch (IOException e){
                e.printStackTrace();
            }
            while(true) {
                if(playerTurn == 1) {
                try {
                    byte[] buffer = new byte[1024];//Creating a byte array for input
                    int bytes;
                    while ((bytes = inputplayer1.read(buffer)) != -1) {//Reading input from player 1
                        String input = new String(buffer, 0, bytes);//Converting input to string
                        getInputs(input, 1, outputplayer1, outputplayer2);//Processing player 1s input
                        break;
                    }
                    if (over) {
                        over = false;
                        continue;
                    }

                } catch(SocketException ignored){} catch (IOException e) {
                    e.printStackTrace();

                }
                }
            else{
                    try {
                        byte[] buffer = new byte[1024];//Creating a byte array for input
                        int bytes;
                        while ((bytes = inputplayer2.read(buffer)) != -1) {//Reading input from player 2
                            String input = new String(buffer, 0, bytes); //Converting input to string
                            getInputs(input, 2, outputplayer2, outputplayer1);//Processing players 2s input
                            break;
                        }
                        if (over) {
                            over = false;

                        }
                    } catch (IOException e) {
                        e.printStackTrace();

                    }
                }

            }
        }
        catch(SocketException ignored){}
        catch (IOException e){
            e.printStackTrace();
        }
    }

    //Method the process players inputs
    public void getInputs(String input, int player, OutputStream result, OutputStream result2){
        input = input.replaceAll("\n", "");//Removing new line characters from input
        int secondInput = Integer.parseInt(input)-1;//Converting input to integer
            if(secondInput < 0 || secondInput >= 7){ //Validating players input
                try{
                    result.write("Invalid input\n".getBytes());//sending error message for valid input
                    return;
                }
                catch (IOException e){
                    e.printStackTrace();
                }}else{
                //Game Logic
                if(!MakeMove(secondInput ,player)){//checking if move is valid
                    try{
                        result.write("Column is already full\n".getBytes());// sending error message if column is full
                        return;
                    }
                    catch (IOException e){
                        e.printStackTrace();
                    }
                }
                displayBoard(result, result2); //Displaying updated game board

                if (checkForWinner(result, result2)) { //checking for winner
                    try{
                        over = true;
                        String output = "Player " + playerTurn + " wins!\n"; //Generating winning message
                        result.write(output.getBytes());//sends win message to player 1
                        result2.write(output.getBytes());//sends win message to player 2
                    }
                    catch (IOException e){
                        e.printStackTrace();
                    }
                    initializeBoard();// Reinitalizing the game board
                    playerTurn = 2; //Switiching player turn
                    displayBoard(result, result2);//Displaying the updated board
                }
                else if (isBoardFull()) {//checking for tie
                    try{
                        over = true;
                        String output = "It's a tie!\n";//generates tie message
                        result.write(output.getBytes());//Sending message to player 1
                        result2.write(output.getBytes());//Sending message to player 2
                    }
                    catch (IOException e){
                        e.printStackTrace();
                    }
                    initializeBoard();//Reinitalizing the game board
                    playerTurn = 2;//switching player turn
                    displayBoard(result, result2);//Displaying updated board
                }
                playerTurn = ((playerTurn) % 2) + 1; // Switching player turn
            }

    }
    public void initializeBoard(){ // Creating connect 4 board

        connectBoard = new int[6][7];//creating a 6x7 array for the game board
        for(int row = 0; row < 6; row++){//looping through rows
            for(int col = 0; col < 7; col++){//looping thorugh columns
                connectBoard[row][col] = 0 ;//setting each cell to empty

            }//inner loop
        }//outer loop
    }
    public void displayBoard(OutputStream connect1, OutputStream connect2){ //Method to display the game board
        for(int row = 0; row < connectBoard.length; row++ ){//looping through rows
            for(int col = 0; col < connectBoard[row].length; col++){//looping through columns
                switch (connectBoard[row][col]) {//Switching based on cell value
                    case 0:
                        try{
                            connect1.write("[ ]".getBytes()); //writing empty cell to player 1
                            connect2.write("[ ]".getBytes());//writing empty cell to player 2
                        }
                        catch (IOException e){
                            e.printStackTrace();
                        }
                        break;
                    case 1:
                        try{
                            connect1.write("[X]".getBytes());//writing X to player 1
                            connect2.write("[X]".getBytes());// Writing 0 to player 2
                        }
                        catch (IOException e){
                            e.printStackTrace();
                        }
                        break;
                    case 2:
                        try{
                            connect1.write("[O]".getBytes());//writing 0 to player 1
                            connect2.write("[O]".getBytes());//writing 0 to player 2
                        }
                        catch (IOException e){
                            e.printStackTrace();
                        }
                        break;
                    default:
                        break;
                }
            }//outer loop
            try{
                connect1.write("\n".getBytes());//writing new line to player 1
                connect2.write("\n".getBytes());//writing new line to player 2
            }
            catch (IOException e){
                e.printStackTrace();
            }
        }//inner loop
        try{
            connect1.write("\n".getBytes()); //writing new line to player 1
            connect2.write("\n".getBytes()); //writing new line to player 2
        }
        catch (IOException e){
            e.printStackTrace();
        }
    }
    public boolean MakeMove(int column, int player){ //method to make move
        int row = connectBoard.length - 1; // Start from bottom of the row
        while(row >= 0 && connectBoard[row][column] !=0 ){
            row--;
        }
        if(row >= 0){
            connectBoard[row][column] = player;//set players chip in the cell
            return true;//
        }
        else{
            return false;// coulumn  is full, move failed
        }
    }
    public boolean checkForWinner(OutputStream connect1, OutputStream connect2){
        //Horizontal Check
        for(int row = 0; row < connectBoard.length; row++){
            for(int col= 0; col < connectBoard[row].length - 4 ; col++){
                //check is there is a seqeunce of a four equal non-zero values horizontally
                if(connectBoard[row][col] != 0 &&
                        connectBoard[row][col] == connectBoard[row][col + 1] &&
                        connectBoard[row][col] == connectBoard[row][col + 2] &&
                        connectBoard[row][col] == connectBoard[row][col + 3]){
                    try{
                        //generate winning message
                        String output = "Player " + connectBoard[row][col] + " Wins Horizontally\n";
                        connect1.write(output.getBytes()); //sending winning message to player 1
                        connect2.write(output.getBytes()); // sending winning message to player 2
                    }
                    catch (IOException e){
                        e.printStackTrace();
                    }
                    return true;
                }

            }//inner
        }//outer

        //Vertical Check
        for(int col = 0; col < connectBoard[0].length; col++){
            for(int row= 0; row <= connectBoard.length - 4; row++){
                //check is there is a seqeunce of a four equal non-zero values vertically
                if(connectBoard[row][col] != 0 &&
                        connectBoard[row][col] == connectBoard[row + 1][col] &&
                        connectBoard[row][col] == connectBoard[row + 2][col] &&
                        connectBoard[row][col] == connectBoard[row + 3][col]){
                    try{
                        String output = "Player " + connectBoard[row][col] + " Verically\n";
                        connect1.write(output.getBytes());//sending winning message to player 1
                        connect2.write(output.getBytes());// sending winning message to player 2
                    }
                    catch (IOException e){
                        e.printStackTrace();
                    }
                    return true ;
                }

            }//inner
        }//outer

        //Diagonal from top right to bottom left
        for(int row = 0; row <= connectBoard.length -  4; row++){
            for(int col = connectBoard[row].length - 1;  col >= 3; col--){
                //check if there is a sequence of four equal non-zero values diagonally from top right to bottom left
                if(connectBoard[row][col] != 0 &&
                        connectBoard[row][col] == connectBoard[row + 1][col - 1] &&
                        connectBoard[row][col] == connectBoard[row + 2][col - 2] &&
                        connectBoard[row][col] == connectBoard[row + 3][col - 3]){
                    try{
                        String output = "Player " + connectBoard[row][col] + " Diagonally\n";
                        connect1.write(output.getBytes());//sending winning message to player 1
                        connect2.write(output.getBytes());//sending winning message to player 2
                    }
                    catch (IOException e){
                        e.printStackTrace();
                    }
                    return true;
                }

            }//inner
        }//outer

        //Diagonal from top left to bottom right
        for(int row = 0; row <= connectBoard.length - 4; row++){
            for(int col= 0; col <= connectBoard[row].length - 4 ; col++){
                // Check if there is a sequence of four equal non-zero values diagonally from top left to bottom right
                if(connectBoard[row][col] != 0 &&
                        connectBoard[row][col] == connectBoard[row + 1][col + 1] &&
                        connectBoard[row][col] == connectBoard[row + 2][col + 2] &&
                        connectBoard[row][col] == connectBoard[row + 3][col + 3]){
                    try{
                        String output = "Player " + connectBoard[row][col] + " Diagonally\n";
                        connect1.write(output.getBytes());//sending winning message to player 1
                        connect2.write(output.getBytes());//sending winning message to player 2
                    }
                    catch (IOException e){
                        e.printStackTrace();
                    }
                    return true;
                }

            }//inner
        }//outer
        return false;
    }
    public boolean isBoardFull(){//Method to check if the board is full
        for(int row = 0; row < connectBoard.length; row++){
            for(int col = 0; col < connectBoard[row].length; col++){
                if(connectBoard[row][col] == 0){

                    return false;//if any empty cell, board is not full
                }
            }
        }
        return true;// is no empty cell board is full
    }
}
