# -*- coding: utf-8 -*-
"""RockPaperScissorGame.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fxXCxw27Sqag7NyaLnQkPAb9AckKZCDr
"""

import random
user_input=input(print("Choose the option 1 for Paper 2 for Rock 3 for Scissor"))

possibleactions=["1","2","3"]
computeraction=random.choice(possibleactions)
if computeraction=="1":
  if user_input=="2":
    print("user input is = ",user_input)
    print("computer response",computeraction)
    print("You Lost")
  if user_input=="3":
    print("user input is = ",user_input)
    print("computer response",computeraction)
    print("You Won")

if computeraction=="2":
  if user_input=="3":
    print("user input is = ",user_input)
    print("computer response",computeraction)
    print("You Lost")
  if user_input=="1":
    print("user input is = ",user_input)
    print("computer response",computeraction)
    print("You Won")

if computeraction=="3":
  if user_input=="1":
    print("user input is = ",user_input)
    print("computer response",computeraction)
    print("You Lost")
  if user_input=="2":
    print("user input is = ",user_input)
    print("computer response",computeraction)
    print("You Won")
if user_input==computeraction:
  print("tie")

print("1-Paper 2-Rock 3-Scissor")