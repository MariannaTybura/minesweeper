# 💣  Minesweeper 💣

## Description

This is my first Python project using the Tkinter library. I aimed to create a version of the game that closely resembles the original.
- By default, the board size is set to 8x8 with 10 randomly generated mines.
- The player wins when they uncover all safe fields
- If the player clicks on a button with a mine, they lose the game.
- After losing, all the mines are uncovered.
- The button that led to the loss is highlighted in red.
- It is possible for the player to misplace the bomb sign. In such cases, after losing any misplaced bomb signs are also revealed.

WIN             |  LOSE
:-------------------------:|:-------------------------:
![win](https://github.com/MariannaTybura/minesweeper/assets/97408733/d4a3d86c-eef7-4548-a929-842271d21124)  |  ![game_over](https://github.com/MariannaTybura/minesweeper/assets/97408733/ecf633c5-85df-4917-8af0-84bb453fbfa2)

## Future Plans

I plan to improve the game's initial move, ensuring that the player always reveals a cell with a value of zero. This will eliminate the possibility of hitting a bomb on the first move, providing a more enjoyable gaming experience.
