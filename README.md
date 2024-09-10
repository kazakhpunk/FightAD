# FightAD - An NYU Abu Dhabi Themed Fighting Game

FightAD is a 2D fighting game created using Processing 3, themed around New York University Abu Dhabi (NYUAD). Players can choose from various characters representing different majors and professors at NYUAD, bringing the university's diverse academic environment to life in a fun and competitive way.

## Game Description

In FightAD, players step into the shoes of NYUAD students from different majors or battle as some of the university's notable professors. Each character's fighting style and abilities reflect their academic discipline or teaching style, making for a unique and entertaining experience that showcases the NYUAD community.

Characters include:
- Scientist: Representing the Natural Sciences
- Philosopher: Embodying the spirit of the Humanities
- Artist: Showcasing the Arts and Creative disciplines
- Business: Demonstrating the skills of the Business and Economics programs
- Electrical Engineer: Highlighting the Engineering department
- Thomas Potsch: A tribute to one of NYUAD's esteemed professors
- Faisal Zeeshan: NYUAD Teaching Assistant who brought to digital life in the game.

Battle it out in various NYUAD-inspired locations and prove which discipline (or professor) reigns supreme!

## Prerequisites

To run this game, you need:

1. Processing 3 (Download from: https://processing.org/download/)
2. Minim library for Processing (for sound)

## Installation

1. Clone or download this repository to your local machine.
2. Open Processing 3.
3. Install the Minim library:
   - Go to Sketch > Import Library > Add Library
   - Search for "Minim"
   - Click on Minim and press "Install"

## Running the Game

1. Open Processing 3.
2. File > Open... and navigate to the folder containing `FightAD_Final.pyde`.
3. Select `FightAD_Final.pyde` and click "Open".
4. Click the "Run" button (play icon) in the Processing IDE.

## How to Play

- Player 1 Controls:
  - Move: Left/Right arrow keys
  - Jump: Up arrow key
  - Attack: ','
  - Block: '.'

- Player 2 Controls:
  - Move: 'A' and 'D' keys
  - Jump: 'W' key
  - Attack: '1'
  - Block: '2'

The game ends when one player wins 3 rounds.

## File Structure

Ensure that your project folder contains the following:

- `FightAD_Final.pyde`
- Character image folders (scientist, philosopher, artist, etc.) directly in the project root
- `backimages/` folder for background images
- `sounds/` folder for audio files

## Troubleshooting

If you encounter any issues:
- Make sure all image and sound files are in the correct folders as specified in the code.
- Verify that the Minim library is properly installed.
- Check that your Processing version is up to date.
- Ensure that the `PATH` variable in the code correctly points to the project directory.

Enjoy battling it out with your favorite NYUAD majors and professors!
