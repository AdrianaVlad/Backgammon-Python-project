# Backgammon-Python-project

features:
- local coop (2 players) or vs AI (1 player)
- display whose turn it is
- display dice rolls
- dice roll button
- can only roll if previous turn finnished (all dice used)
- can only make valid moves (only your pieces, only on top of yours or on free spaces, only as much as the value of 1 dice)
- show selected 'column' (meaning: piece at the top of the 'triangle'/space* will move on next valid click)
- deselect piece button (so you don't get stuck)
- stack pieces on space if > 5 (so they don't overlap with the space below/above)
TODO:
- double dice: ex: if player rolls '3 3' they can move 3 spaces 4 times
- taking pieces functionality
	- place your piece if only one opponent piece on space
	- place taken piece in the middle of the board
	- can only move other pieces if no pieces in the middle, otherwise can only move taken pieces
	- taken pieces can only be placed in opponent's house
- bearing off functionality:
	- if no pieces outside of your house, can take pieces out of the board
	- update 'borne off' label for respective color
- win functionality:
	- if all pieces borne off, display winner
	- back to main menu button on win screen
- AI opponent:
	- on player 2 turn
	- automatically roll dice 
	- make (any) valid moves until all moves are used


*note: top right is indexed 0, top left 11, bottom left 12, bottom right 23 (so move order from white POV)