Random Password Generator
Python Programming Internship — Project 3
📋 Project Overview
A command-line + GUI Random Password Generator built with Python and Tkinter. Users can define password criteria such as length, character types, and excluded characters.

🚀 Features
Feature	Details
Randomization	Cryptographically-seeded random module for unpredictable passwords
User Input Validation	Validates length range (4–128) and requires at least one character type
Character Set Handling	Uppercase, Lowercase, Digits, Symbols — toggle any combination
Exclude Characters	Type characters you never want in your password
Strength Meter	Live animated strength bar with score (Weak / Fair / Strong / Very Strong)
Clipboard Integration	One-click COPY button copies the password to your clipboard
Show/Hide Password	Eye toggle button to reveal or mask the generated password
Quick Length Presets	One-click buttons for lengths 8, 12, 16, 24, 32
Beautiful Dark UI	Gold-on-black cyberpunk theme built with Tkinter
🛠️ Setup Instructions
Prerequisites
Python 3.8 or newer installed on your machine
1. Install dependencies
pip install -r requirements.txt
2. Run the application
python password_generator.py
🎮 How to Use
Set Length — Drag the slider or click a preset button (8, 12, 16, 24, 32)
Choose Character Types — Check/uncheck: Uppercase, Lowercase, Digits, Symbols
Exclude Characters — Type any characters you want to avoid (e.g. 0O1l)
Click ⚡ GENERATE — A new password appears instantly
Click 📋 COPY — Password is copied to your clipboard
Click 👁 — Toggle show/hide the password
📁 File Structure
RandomPasswordGenerator/
│
├── password_generator.py   # Main application (GUI + logic)
├── requirements.txt        # Python dependencies
└── README.md               # This file
🔑 Key Concepts Covered
Randomization — random.choice() and random.shuffle() for unpredictable output
User Input Validation — Validates length, character set selection, exclusions
Character Set Handling — string.ascii_uppercase, string.digits, string.punctuation
GUI Design — Tkinter with custom styling, frames, sliders, checkboxes, canvases
Clipboard Integration — pyperclip library with Tkinter fallback
Password Strength Rules — Scoring based on length, variety, uniqueness ratio
📸 UI Preview
┌─────────────────────────────────────────┐
│ 🔐 PASSWORD GENERATOR                   │
│ Secure · Customisable · Instant         │
├─────────────────────────────────────────┤
│ GENERATED PASSWORD                      │
│ K#9mL@pQv2Xn!rTs              👁        │
│ ████████████░░░░  Strong  78/100        │
├─────────────────────────────────────────┤
│ PASSWORD LENGTH              [ 16 ]     │
│ ─────────────●──────────────────        │
│  [8]  [12]  [16]  [24]  [32]           │
│                                         │
│ CHARACTER TYPES                         │
│ ☑ ABC Uppercase   ☑ abc Lowercase       │
│ ☑ 123 Digits      ☐ #@! Symbols        │
│                                         │
│ EXCLUDE CHARACTERS                      │
│ [0O1l                               ]   │
├─────────────────────────────────────────┤
│  [⚡ GENERATE]  [📋 COPY]  [🗑 CLEAR]   │
└─────────────────────────────────────────┘
Built for Python Programming Internship — Project 3 Proposal
