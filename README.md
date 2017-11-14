Pythonic Draughts
by Jaroslav Belkov
for Algorithms and Data Structures coursework

Content:
1. Brief description
2. System requirements
3. Installation 
4. pd_config.py explained
--------------------------------------------------------

1. Brief description
  Pythonic Draughts (PD) is a computer draughts game programmed in accordance with the Coursework Specification of Algorithms & Data Structures module SET09117 for the first trimester of 2017/2018 academic year at Edinburgh Napier University. The game is implemented in Python programming language. It represents all necessary features to allow two players to play English Draughts game by the rules described on  https://en.wikipedia.org/wiki/English_draughts). Both players may be people, or one person may choose the side (White or Red) and let the program to imitate an opponent.
  
 2. System requirements:
   - installed Python interpreter version 3.4 or later 
 
 3. Installation
 
     3.1. Three files are necessary to run the program:
     
           - 1. pythonic_draughts.py or pythonic_draughts.pyc
           
           - 2. pd_functions.py or pd_functions.pyc
           
           - 3. pd_config.py
        
     3.2. All three must be in the same directory with Read and Write permissions.
   
     3.3. In the first session after installation PD will check if it can retrieve the path to its installation and if not, it will ask the user to enter the path manually. When it retrieves the correct path, and if pythonic_draughts.py source code file is present, it will offer to save the path to the source code overriding the distribution version. If pythonic_draughts.pyc is also present, it will automatically compile the source code overriding the distribution version.
   
 4. pd_config.py explained
 
    4.1.
    - pd_config.py is a tiny bit of the source code, which is imported to PD during variables declaration and initialization start up. It contains declaration and initialisation of global variables which are configurable via Settings Menu presented in the game and default_main_position variable (explained below). All variables also may be configured "manually" using any text editor.
    - It is crucial that all variables are only assigned allowed values. Also, since it is a part of the code, general syntax rules must be followed when pd_config.py is edited. Otherwise, PD will most likely crash during the execution. The best practice is to take the distributed version as a sample and only modify values of variables on the right side of expressions (right from '=' character).
    
    4.2. Variables configurable in Settings Menu in the game:
    - auto_move: integer, allowed values 1 and -1. If set to 1, and only one legal move is possible in the game situation, it will automatically execute the move.
    - auto_replay: integer, allowed values 1 and -1. If set to 1, and 'Replay' action is chosen by the user, or previously saved game is loaded from a file, will automatically replay the game until the last move. Otherwise, will wait for users input to replay one single move until the last move or a new move.
    - ar_delay: float, allowed values: non-negative real numbers consist of three characters (only last three are taken into account in PD). Examples: 0, 1.0, 22.1, 999, 0.01 all will evaluate to values as they are written. 999.9 will evaluate to 99.9, 001 will evaluate to 1.0, 1000 will evaluate to 0.
The variable represents the number of seconds the PD is paused between single moves on automatic replay. When auto_replay is set to -1, ar_delay must be set to 0! 
    - is_gui: integer, allowed values 1 and -1. When set to one, automatically saves a javascript (.js) file after every move in the game. Pythonic_draughts_gui.html then uses the saved file. Pythonic_draughts_gui.html and complementing files are included in distribution version, but they are not a part of the coursework: they only are the product of the testing phase of development. More information in readme.txt within the 'pd_gui' folder.
    - diff_level: list (or one-dimensional array). Allowed no less or more than three elements. The first element allowed values: any data type of any value, but best practice: number 0. Second and third elements: non-negative integers. These integers represent the number of legal moves ahead from current position will PD calculate in order to choose the best move. In the game referred to as "level". The second element is for the red player, third for the white player. When set to 0, PD will only make random moves. The higher numbers, the longer calculation takes. Playable levels are up to four. However, the best results are achieved with the level seven and above, when one move takes more than ten minutes on average on Intel i7 3GHZ powered PC. 
    - default_who_am_I: integer, allowed values 1, 0, -1. When set to 1, the red player has the first move. When set to -1: the white player has the first move. When set to zero: at the start of every new game, the first move will be granted randomly.
    
    4.3. Data structure used to record the current position in the game
    
    - default_main_position: list of lists, holds the start position of the game. This variable may be edited in pd_config.py in order to modify the game, for example, to play another game variation or to start from other position than the start position. In distributed version, it is assigned to the start position of English Draughts. default_main_position is imported to the PD at the start-up, and then the variable named main_position is assigned by its values before every new game starts.
    
     - For more information on main_position variable, its construction as a medium to record the current position of the game, and allowed values, please, refer to notation in source code in GLOBAL VARIABLES DECLARATION part. 
    
   
               
               
               
