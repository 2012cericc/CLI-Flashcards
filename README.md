# CLI-Flashcards

This is a basic flashcard program that runs in the terminal. 

## How to use the program
flashcards.py takes a text file(s) as an argument.
In the text file, cards are separated by a newline.
Question and answers within a card are separated by " ; ".
Cards can be hidden from subsequent rounds if the answer is already known.
A timer is provided to help gamify the learning process.

## Features
- shuffled cards between rounds
- ability to hide cards if the user already knows it
- reset hidden status of all cards
- ability to use multiple flashcard files
- detect and indicate formatting errors in flashcard files
- print fastest time taken to complete a round
- print time it took to complete the round
- print previous time to complete a round
- print number of non hidden cards at start of round

## Features to add
- undo hide of the previous card if applicable
- flag cards in text file to never show again unless desired
- GUI version, maybe Tkinker?
- save non-hidden cards in a new file for later use
- guard against multiple question/answer separators in a line

## Improvements to make
- find a more human readable way to format flashcard text file

## General design goals/justifications
- Create a reasonably robust flashcard program
- Leave card creation to a text editor, no need to reinvent the wheel
  - Its simpler to type/edit cards in a text editor
  - Text editors all have a search function, easy to find/edit cards

## Purpose
I had a neuromechanics class in school taught by a graduate student. Although they tried to make the class fun and interesting, the exam format was a bit of a mess. Many of the questions forced students to rote memorize facts that were somewhat unimportant, such as who discovered a disease rather than testing deeper understanding of the subject. As a result, I made a primitive flashcard program in python to help get through the class. 

Constantly being quizzed really helped in quickly remembering terminology and concepts as opposed to just staring at notes. I find it a way for me to be able to steamroll through material and still retain it.

This is a much improved version of that original program. This is also for me to practice programming and get used to using Github.
