Ryan Park
SID: 54362057
ICS 33 Texas hold 'em GUI project


User Mode or File Mode:

My program when launched will require an arg parse. You must specify which mode you will be using between file mode (-f) which requires the path to the file (-i myPathToTheFile) or user mode (-u) which requires the number of total players you want including yourself (-p NumOfBotPlayers). 

Start of the Game:

Assuming that you will be purely grading the GUI proceeding with the user mode, the GUI will be launched. The window will be titled and it will display that the game is initialized, your hand, and the bot player's actions. Below this will be an Entry box that asks the user to "bet" or "fold" (the first letter can be capitalized). 

[Potential Bug: A potential issue that I've had during my testing was that all entry boxes would be hidden but clicking on the area where it would be or clicking another tab and tabbing back to the GUI would reveal the entry box. I tried different methods of organizing the GUI and the entry box but none of them seemed to affect the end result so I am assumed it was an issue with the import or my iteration of python. (I am unsure if this issue was purely on my end but in case it does appear for you then please try the fixes above that worked for me.)]

The entry box will have a default text inside that says "Type Action Here!". Once you type out Bet or Fold press the "Confirm Action" button to proceed with the program. Once the button is pressed, depending on what the user responds with the GUI will respond differently. Typing "bet" will remove all previous widgets and prompt the user for the amount they want to bet. Once the user confirms how much they want to bet and press 'Submit Value' they will be sent into the next round. Typing "fold" will immediately send the user into the next round.

[Disclaimer: I did not make a sophisticated betting system because the professor never required it. Despite that it works beyond the most simple of purposes so the betting system is functional but not optimal!]


Round 1:

The next round will display the winner of the previous round and the money of each player. Below these statistics the next round will be displayed indicted by the text "~~~~~~~ Round 1 ~~~~~~~~" along with your hand and the community cards. Below that the bot players moves are displayed. The user is then prompted to bet or fold again.


Round 2:

The final round will function similarly to the first with the only difference being the increased amount of community cards (increasing from 3 cards to 5 cards) You will place your final bets or fold during this round.

Final Stats + Aftermath:


After the final round the winner will be displayed and the final stats will also be displayed with the text "The game is now done." With 2 options to either "Restart Game" or "Quit Game". Restart Game will create a new game with the same money pool from the previous game. Quit Game will destroy the GUI.