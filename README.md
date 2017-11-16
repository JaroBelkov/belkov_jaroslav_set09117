Pythonic Draughts
by Jaroslav Belkov
for Algorithms and Data Structures coursework

Content:
1. Brief description
2. System requirements
3. Installation 
4. pd_config.py explained
5. Graphical User Interface explained and installation
--------------------------------------------------------

1. Brief description

  Pythonic Draughts (PD) is a computer draughts game programmed in accordance with the Coursework Specification of Algorithms & Data Structures module SET09117 for the first trimester of 2017/2018 academic year at Edinburgh Napier University. The game is implemented in Python programming language and runs from the command line and Python shell.  
  
2. System requirements:
 
   - installed Python interpreter version 3.6 or later 
 
 
3. Installation
 
    3.1. Three files are necessary to run the program:
     
           - 1. pythonic_draughts.py or pythonic_draughts.pyc
           
           - 2. pd_functions.py or pd_functions.pyc
           
           - 3. pd_config.py
        
     3.2. All three must be in the same directory with Reading and Writing permissions granted.
   
     3.3. In the first session after the installation, PD checks if it can retrieve the path to its installation directory and if not, it asks the user to enter the path. When it retrieves the correct path, and if pythonic_draughts.py source code file is present, it offers to save the path to the source code overriding the distribution version. If pythonic_draughts.pyc is also present, it automatically compiles the source code overriding the distribution version.
   
 4. pd_config.py explained
 
    4.1.
    - pd_config.py is a tiny bit of source code, which is imported to PD. It contains declaration and initialization of global variables which are configurable via Settings Menu presented in the game and default_main_position variable (explained below). All variables also may be configured "manually" using any text editor.
    - It is crucial that all variables are only assigned allowed values. Also, since it is a part of the code, general syntax rules must be followed when pd_config.py is edited. Otherwise, PD will most likely crash during the execution. The best practice is to take the distributed version as a sample and only modify values of variables on the right side of expressions (right from '=' character).
    
    4.2. Variables also configurable in Settings Menu in the game:
    - auto_move: integer, allowed values 1 and -1. If set to 1, and only one legal move is possible in the game situation, PD automatically executes the move.
    - auto_replay: integer, allowed values 1 and -1. If set to 1, and 'Replay' action is chosen by the user, or previously saved game is loaded from a file, then PD automatically replays the game from the first to the last move. If set to -1, PD waits for the user's input to replay one single move at a time, until the last move or a new move.
    - ar_delay: float, allowed values: non-negative real numbers. The variable represents the number of seconds the PD is paused between single moves on automatic replay. When auto_replay is set to -1, ar_delay must be set to 0! After importing to PD, it is converted to string, and only last three characters of that string are taken into account in PD. Examples: 0, 1.0, 1, 22.1, 999, 0.01 all evaluate to values as they are written. 999.9 evaluates to 99.9, 001 evaluates to 1.0, 1000 evaluates to 0.0.
    - is_gui: integer, allowed values 1 and -1. When set to one, automatically saves a javascript (.js) file after every move in the game. Pythonic_draughts_gui.html then uses the saved file. Pythonic_draughts_gui.html and complementing files are included in distribution version as an add-on to the coursework.
    - diff_level: list (or one-dimensional array). Allowed no less or more than three elements. The first element allowed values: any data type of any value, but best practice: number 0. Second and third elements: non-negative integers. These integers represent the number of legal moves ahead from current position that PD calculates in order to choose the best move. In the game, referred to as "level". The second element is for the red player, third for the white player. When set to 0, PD only makes random moves. The higher numbers, the longer the calculation takes. Playable levels are up to the fifth level. However, the best results are achieved with the level seven and above, when one move takes more than a half an hour on average on Intel i7 3GHZ powered PC. 
    - default_who_am_I: integer, allowed values 1, 0, -1. When set to 1, the red player has the first move. When set to -1: the white player has the first move. When set to zero: at the start of every new game, the first move will be granted randomly.
    
    4.3. Data structure used to record the current position in the game
    
    - default_main_position: list of lists, holds the start position of the game. This variable may be edited in pd_config.py in order to modify the game, for example, to play another game variation or to start from other position than the start position. In distributed version, it is assigned to the start position of English Draughts. default_main_position is imported to the PD at the start-up, and then the variable named main_position is assigned by its values before every new game starts.
    
     - For more information on the main_position variable, its format and construction as a medium to record the current position of the game, and allowed values, please, refer to comments in the source code in GLOBAL VARIABLES DECLARATION part.
     
     - As a part of the distributed version is attached main_position_editor.html. This is a testing tool used during development. Feel free to use it to stage a position and get a string in the format of default_main_position to the clipboard and then paste it to pd_config.py.
     
   5. pythonic_draughts_gui.html explained and installation.
   
   This is also a product of the testing stage of development. The page written in HTML contains a script written in JavaScript, which five times in a second reads the file named position_data.js and if the file is changed, it changes HTML in such a way that actual game position is presented to the user in the browser. PD, if is set to do so, writes a new version of position_data.js after every move in the game. 
   
   5.1.  How to use pythonic_draughts_gui.html:
   
     - The page displayed in the browser contains the playing board with playing figures in the left half of the screen. At the start, it is most likely the last position from a previous game. If it is started for the first time, the board is empty (without figures): that is because the file position_data.js does not exist yet (PD creates it).
     - On the right side of the board are listed possible moves more or less similar to the checker's notation, in contrast to the command line, where possible moves are listed in chess notation. Numbers of moves correspond to those in the command line. 
     - Finally, on the bottom is the button 'Rotate', which when clicked rotates the board.
    
   5.2. How to use main_position_editor.html: 
   
     - Similarly to pythonic_draughts_gui.html, the page presents the playing board.
     - Click to a square with a playing figure removes that figure from the board.
     - Left click to empty square places white figure to that square.
     - Right click does the same for red figures.
     - Figures are switched to man/king clicking the yellow button in the upper left corner.
     - Under the board is the text area which displays a string in the format of main_position. The string can be safely saved to the pd_config.py. When position is set, simply click to the text area and copy the text (Ctrl + a, Ctrl + c).
    
   5.3. Installation guide: 
   
     - within the directory with PD installation create subdirectory named pd_gui.
     - copy files pythonic_draughts_gui.html, main_position_editor.html and pythonic_draughts_gui.css to the subdirectory pd_gui.
     - Internet connection is necessary in most cases to run these html pages from the file because they import bootstrap.min.css and jquery.min.js. Some browsers may have cashed these frameworks - in this case, internet connection is not required.
     - Both pythonic_draughts_gui.html and main_position_editor.html, were tested on Chrome version 62.0.3202.94 (Official Build) (64-bit).
   
   DO NOT set the variable is_gui to 1 in pd_config.py if directory pd_gui is not present. PD will crash on attempt to write position.js to that directory. If pd_gui directory is not present, PD does not offer to change is_gui variable in Settings Menu.
    
   
               
               
               
