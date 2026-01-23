# Algorithm Design: Minimax with Alpha–Beta Pruning

This document explains how the **Minimax algorithm with Alpha–Beta pruning** is implemented in this project and how it has been adapted specifically for **Vanishing Tic-Tac-Toe**.

The goal is not only to describe the algorithm in theory, but to explain **how and why it works in this codebase**.

---

## 1. Why Minimax is Needed

Vanishing Tic-Tac-Toe is a **two-player, turn-based, zero-sum game**:
- One player’s gain is the other player’s loss.
- Both players are assumed to play optimally.

In such games, Minimax is a natural choice. The algorithm allows the AI to:
- Assume the opponent will always make the best possible move.
- Choose moves that maximize its own chances while minimizing the opponent’s.

However, unlike standard Tic-Tac-Toe, this game:
- Does not end when the board is full.
- Has a constantly changing board due to vanishing pieces.
- Can result in repeated states.

Because of this, Minimax must be **depth-limited and heuristic-driven**.

---

## 2. High-Level Idea of Minimax

At a high level, Minimax works as follows:

- The AI (player **O**) tries to **maximize** the evaluation score.
- The opponent (player **X**) tries to **minimize** the evaluation score.
- The algorithm explores future moves by simulating turns alternately.
- When a terminal state or depth limit is reached, a score is returned.
- Scores propagate upward to decide the best move.

Each recursive call represents a possible future board configuration.

---

## 3. Game Tree Representation

In this implementation:
- Each node in the game tree represents:
  - A board configuration
  - Ordered queues of X and O pieces (to track vanishing)
  - The current player to move
- Each edge represents a legal move (placing a piece)

Because piece order matters, two boards that look visually identical may still be **different states**.

---

## 4. Terminal State Evaluation

Before expanding further in Minimax, the algorithm checks whether the game has already ended.

### Terminal conditions:
- AI win (O) → score = **+1000**
- Opponent win (X) → score = **−1000**
- Draw (tie or threefold repetition) → score = **0**

If any of these conditions are met, recursion stops and the score is returned immediately.

This ensures:
- Wins are always preferred over non-terminal states.
- Losses are strongly avoided.

---

## 5. Depth Limiting

Because the game can continue indefinitely, the algorithm uses a **maximum depth limit**.

When the depth limit is reached:
- The algorithm does not expand the game tree further.
- Instead, a **heuristic evaluation function** is applied.
- The heuristic estimates how favorable the position is for the AI.

This allows the AI to make decisions in reasonable time.

---

## 6. Heuristic Evaluation at Leaf Nodes

When a non-terminal state is reached at the depth limit:
- The board is scored using a heuristic function.
- All possible winning lines are evaluated.
- Lines containing only AI pieces increase the score.
- Lines containing only opponent pieces decrease the score.
- Blocked lines contribute nothing.

Exponential weighting (10ⁿ) ensures that:
- Two-in-a-row is far more valuable than one-in-a-row.
- Immediate threats dominate decision-making.

---

## 7. Maximizing vs Minimizing Phases

The Minimax recursion alternates between two phases:

### Maximizing phase (AI turn):
- The algorithm tries all possible moves.
- It selects the move with the **highest score**.
- This represents the AI choosing the most favorable outcome.

### Minimizing phase (Opponent turn):
- The algorithm tries all possible moves.
- It selects the move with the **lowest score**.
- This represents the opponent trying to harm the AI’s position.

This alternating structure models optimal play from both sides.

---

## 8. Alpha–Beta Pruning

Alpha–Beta pruning is an optimization that reduces unnecessary exploration.

### Key variables:
- **Alpha (α)**: the best score the maximizing player can guarantee so far.
- **Beta (β)**: the best score the minimizing player can guarantee so far.

During recursion:
- Alpha is updated during maximizing phases.
- Beta is updated during minimizing phases.

If at any point:
- **β ≤ α**, the current branch is abandoned.

This is because further exploration cannot improve the final decision.

---

## 9. Why Alpha–Beta Works Well Here

Vanishing Tic-Tac-Toe has:
- A high branching factor due to disappearing pieces.
- Many symmetric or unpromising branches.

Alpha–Beta pruning:
- Dramatically reduces the number of nodes explored.
- Allows deeper searches without exponential slowdown.
- Makes real-time gameplay feasible.

The pruning does not affect correctness — only performance.

---

## 10. Handling Vanishing Pieces During Simulation

Each Minimax simulation:
- Works on a **deep copy** of the board.
- Works on **copies of X and O queues**.
- Applies the vanishing rule exactly as in real gameplay.

This ensures:
- Simulations do not affect the real game state.
- Each branch evolves independently.

---

## 11. Repetition Awareness in Minimax

To prevent infinite loops:
- Game states are tracked during simulation.
- If a state repeats three times, it is treated as a draw.
- The algorithm returns a score of **0** for such states.

This ensures correctness even in cyclic game trees.

---

## 12. Move Selection at the Root

At the root level (actual AI turn):
- All legal moves are simulated.
- Each move is scored using Minimax.
- The move with the **highest score** is selected.
- If multiple moves share the same score, the first encountered is chosen.

This final step converts evaluation into action.

---

## 13. Summary

This implementation of Minimax with Alpha–Beta pruning is tailored specifically for Vanishing Tic-Tac-Toe.

Key adaptations include:
- Tracking piece age using queues
- Depth-limited search with heuristics
- Repetition-aware draw handling
- Efficient pruning for real-time play

Together, these allow the AI to play competitively while remaining computationally efficient.

---
