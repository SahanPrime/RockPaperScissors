# RockPaperScissors
# Rock-Paper-Scissors with Adaptive AI (Pygame)

An enhanced Rock-Paper-Scissors game built with Python (Pygame), featuring an AI opponent that learns and adapts to your playstyle.  
Unlike random opponents, this AI analyzes your past moves using multiple strategies and tries to outsmart you.

---

## Features
- Graphical User Interface (Pygame-based)  
- Adaptive AI strategies:
  - Frequency analysis (most common moves)
  - Anti-frequency countering
  - Alternating and repeating pattern detection
  - Cycle detection (e.g., R→P→S loops)
  - Markov Chains (2nd & 3rd order sequence prediction)
  - Randomization for unpredictability  
- Score tracking:
  - Player wins, AI wins, draws
  - AI win rate displayed live  
- Automatic round reset after results  
- Game over summary after max rounds  

---

## Installation & Run

### Prerequisites
- Python 3.8 or higher  
- `pygame`  

### Setup
```bash
# Clone the repository
git clone https://github.com/sahanPrime/RockPaperScissors.git
cd rock-paper-scissors-ai

# Install dependencies
pip install pygame

# Run the game
python main.py

