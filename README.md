<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>

<h1>🌀 Vanishing Tic-Tac-Toe AI</h1>
<p><em>Chakravyuh of Shunya</em></p>

<blockquote>
    A strategic AI for a game where pieces don’t last forever.
</blockquote>

<hr>

<h2>🧠 What is this project?</h2>

<p>
This project implements an AI agent for <strong>Vanishing Tic-Tac-Toe</strong>, a modified version of classic Tic-Tac-Toe where
<strong>each player can have only three pieces on the board at any time</strong>. When a player places their fourth piece,
their <strong>oldest piece immediately disappears</strong>.
</p>

<p>
Unlike standard Tic-Tac-Toe, the game does not end when the board fills up. Because pieces vanish over time, the game becomes
more dynamic and rewards <strong>timing, short-term planning, and tactical awareness</strong> rather than slow long-term strategies.
</p>

<p>
This project was developed as part of a competitive problem-solving challenge, with a focus on correctness, clean design,
and strategic reasoning.
</p>

<hr>

<h2>🎯 Game Rules (Quick Summary)</h2>

<ul>
    <li>Board size: <strong>3 × 3</strong></li>
    <li>Players: <strong>X (human)</strong> and <strong>O (AI)</strong></li>
    <li>Maximum pieces per player: <strong>3</strong></li>
    <li>On placing the 4th piece → <strong>oldest piece vanishes</strong></li>
    <li>Win condition: <strong>3 in a row</strong> (horizontal, vertical, diagonal)</li>
    <li>
        <strong>Threefold Repetition Rule:</strong>
        If the exact same game state (same positions, same piece ages, same player to move)
        occurs three times, the game is declared a draw.
    </li>
</ul>

<hr>

<h2>🧩 Project Structure</h2>

<pre>
vanishing_ttt/
├── main.py        # Entry point, wires all components together
├── gui.py         # Tkinter-based graphical user interface
├── game_state.py  # Core game rules and state management
├── ai.py          # Minimax AI with alpha–beta pruning
├── README.md
└── Algorithm.md   # Algorithm logic explaination

</pre>

<hr>

<h2>⚙️ Core Components</h2>

<h3>1️⃣ Game State Management (<code>game_state.py</code>)</h3>

<ul>
    <li>Board representation</li>
    <li>Tracking the order of X and O pieces using queues</li>
    <li>Enforcing the 3-piece limit and vanishing rule</li>
    <li>Detecting win conditions</li>
    <li>Handling draw conditions, including threefold repetition</li>
    <li>Creating immutable snapshots of game states for simulation</li>
</ul>

<p>This module is completely independent of both the GUI and the AI.</p>

<h3>2️⃣ AI Engine (<code>ai.py</code>)</h3>

<ul>
    <li>Minimax search with Alpha–Beta pruning</li>
    <li>Depth-limited search for performance</li>
    <li>Heuristic evaluation of non-terminal states</li>
    <li>Neutral handling of repetition-based draws</li>
</ul>

<h3>3️⃣ Graphical User Interface (<code>gui.py</code>)</h3>

<ul>
    <li>Rendering the board</li>
    <li>Handling user interactions</li>
    <li>Displaying game results</li>
    <li>Updating visuals after each move</li>
</ul>

<hr>

<h2>🧠 Heuristic Evaluation Logic (Detailed)</h2>

<p>
Since Vanishing Tic-Tac-Toe can continue for many turns and pieces may disappear,
the AI cannot always search until a final win or loss. In such cases, the board
is evaluated using a heuristic scoring function that estimates how favorable the
current position is for the AI (<strong>O</strong>) versus the opponent (<strong>X</strong>).
</p>

<p>
The heuristic is designed to prioritize <strong>immediate threats</strong>,
<strong>short-term advantages</strong>, and <strong>stable piece configurations</strong>,
as long-term plans may collapse due to the vanishing rule.
</p>

<h3>🔢 Terminal State Scores</h3>

<p>
If a terminal game state is reached during Minimax search, fixed scores are assigned:
</p>

<table>
    <tr>
        <th>Game State</th>
        <th>Score</th>
        <th>Reasoning</th>
    </tr>
    <tr>
        <td>AI win (O)</td>
        <td><strong>+1000</strong></td>
        <td>Strongly preferred outcome</td>
    </tr>
    <tr>
        <td>Opponent win (X)</td>
        <td><strong>-1000</strong></td>
        <td>Strongly avoided outcome</td>
    </tr>
    <tr>
        <td>Draw / Tie</td>
        <td><strong>0</strong></td>
        <td>Neutral outcome</td>
    </tr>
</table>

<h3>📈 Scoring Non-Terminal Board States</h3>

<p>
When the depth limit is reached and no terminal state is found, the heuristic
evaluates the board by examining all possible winning lines
(rows, columns, and diagonals).
</p>

<p>
For each line:
</p>

<ul>
    <li>The number of AI pieces (<strong>O</strong>) in the line is counted</li>
    <li>The number of opponent pieces (<strong>X</strong>) in the line is counted</li>
</ul>

<p>
The contribution of a line to the total score follows these rules:
</p>

<ul>
    <li>
        If a line contains only AI pieces and empty cells:
        <br>
        <strong>Score += 10<sup>n</sup></strong>,
        where <em>n</em> is the number of AI pieces in that line
    </li>
    <li>
        If a line contains only opponent pieces and empty cells:
        <br>
        <strong>Score -= 10<sup>n</sup></strong>,
        where <em>n</em> is the number of opponent pieces in that line
    </li>
    <li>
        If a line contains both X and O:
        <br>
        <strong>No score contribution</strong> (the line is blocked)
    </li>
</ul>

<p>
This exponential scoring ensures that:
</p>

<ul>
    <li>Two-in-a-row is valued far more than one-in-a-row</li>
    <li>Immediate threats dominate evaluation</li>
    <li>Defensive blocking is strongly encouraged</li>
</ul>

<h3>🎯 Center Control Bonus</h3>

<p>
The center cell is part of four possible winning lines and is therefore
strategically important.
</p>

<ul>
    <li>If the AI occupies the center, a small positive bonus of 5 points is added</li>
    <li>If the opponent occupies the center, a small penalty of 5 points is applied</li>
</ul>

<p>
This bonus helps guide early-game decisions when no immediate threats exist.
</p>

<h3>⏳ Vanishing-Aware Design</h3>

<p>
Because pieces disappear after three moves, the heuristic intentionally avoids
rewarding slow or long-term plans. Lines that appear strong but rely on pieces
about to vanish do not accumulate excessive score unless they pose an
immediate threat.
</p>

<p>
As a result, the AI prefers:
</p>

<ul>
    <li>Short-term tactical pressure</li>
    <li>Blocking opponent threats early</li>
    <li>Board positions that remain strong even after vanishing occurs</li>
</ul>

<p>
This heuristic design aligns closely with the dynamic nature of
Vanishing Tic-Tac-Toe and allows the AI to remain competitive without exhaustive
search.
</p>


<hr>

<h2>⚠️ Limitations</h2>

<ul>
    <li>Optimized specifically for a 3×3 board</li>
    <li>Heuristic weights are manually tuned</li>
    <li>GUI focuses on functionality rather than aesthetics</li>
</ul>

<hr>

<h2>🏁 Conclusion</h2>

<p>
This project demonstrates how classical game-solving techniques such as Minimax can be adapted to a dynamic rule set
involving piece disappearance and repetition constraints. The emphasis is on clean design, correct rule enforcement,
and strategic reasoning rather than brute-force computation.
</p>

</body>
</html>
