# solanalottery.org-verify
```markdown
# Game Result Verifier

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Verification Process](#verification-process)
  - [Step 1: User Input](#step-1-user-input)
  - [Step 2: Obtaining the Bet Amount and Lottery Balance](#step-2-obtaining-the-bet-amount-and-lottery-balance)
  - [Step 3: Entering Retrieved Values](#step-3-entering-retrieved-values)
  - [Step 4: Game Parameters](#step-4-game-parameters)
  - [Step 5: Hashing and Randomness](#step-5-hashing-and-randomness)
  - [Step 6: Determining the Outcome](#step-6-determining-the-outcome)
  - [Step 7: Calculating Payout](#step-7-calculating-payout)
  - [Step 8: Displaying Results](#step-8-displaying-results)
  - [Step 9: Verification](#step-9-verification)
- [Notes](#notes)
- [Example Output](#example-output)
- [License](#license)

## Description

**Game Result Verifier** is a program that allows any user to verify the results of a given game. It ensures transparency by enabling users to independently reproduce and confirm game outcomes.

## Installation

### Dependencies

Install the required dependencies with `pip`:

```bash
pip install base58
```

## Usage

To run the program, use the following command:

```bash
python3 proof-transaction.py
```

## Verification Process

The verification process involves the following steps:

### Step 1: User Input

You will be prompted to enter the Recent Block Hash.

### Step 2: Obtaining the Bet Amount and Lottery Balance

After entering the Recent Block Hash, follow these steps:

1. Visit [Solscan](https://solscan.io) for your transaction by replacing `{transaction_id}` with your actual transaction ID:

    ```
    https://solscan.io/tx/{transaction_id}
    ```

2. On the transaction page, find:
    - **Recent Block Hash**: Listed in the transaction details.
    - **Bet Amount (`bet_sol`)**: The amount of SOL wagered in the game.
    - **Lottery Pre Balance (`balance_sol`)**: The total SOL balance of the lottery at the time of the transaction (found under the "Change Balance" tab).

### Step 3: Entering Retrieved Values

Enter the bet amount and lottery balance into the program when prompted.

### Step 4: Game Parameters

The program uses fixed game parameters:

- **Maximum Loss Percent (`max_loss_percent`)**: 10%
- **Mean Delta Percent (`mean_delta_percent`)**: 3% (which implies a 47% win chance, since 50% - 3% = 47%)

### Step 5: Hashing and Randomness

- **Hashing**: The Recent Block Hash is hashed using SHA256 to produce a 32-byte hash.
- **Combining Values**: The hash, bet amount, and lottery balance are combined and rehashed to generate random values. These values are used to determine the game outcome.

### Step 6: Determining the Outcome

The program calculates the win or loss outcome based on:
- The generated random values
- The predefined probabilities

If the player wins, the potential win amount is calculated. If the player loses, the loss amount is determined.

### Step 7: Calculating Payout

The payout is calculated based on the bet amount and the win/loss outcome.

- **No Fees**: No fees are deducted from the payout.

### Step 8: Displaying Results

The outcome (win or loss) is displayed along with detailed financial information:

- Initial Bet
- Payout
- Percentage Change

### Step 9: Verification

By replicating these steps, users can independently verify game results using their own Recent Block Hash and the game parameters.

## Notes

**Single Address**: We use only one address for this service:

```
soLV8oMjQtwihUmYEJsbgpdFya7CrmC1JYujSoLmV47
```

**Assumptions**: The script assumes that you can access and interpret the Solscan page to find the required values.

## Example Output

```plaintext
Welcome to the Game Result Verifier!

To find the Recent Block Hash, transaction amount, and lottery PreBalance, please visit:

https://solscan.io/tx/{transaction_id}

You can find the Recent Block Hash in the transaction details, and the amounts in the 'Change Balance' tab.

Enter Recent Block Hash: GHf5...

Enter bet amount (in SOL): 0.05

Enter lottery balance (in SOL): 10

Game Result

Outcome: You won!

Initial Bet: 0.05 SOL
Payout: 0.090000 SOL
Percentage Change: 80.00%

Please note that we use only one address for this service: soLV8oMjQtwihUmYEJsbgpdFya7CrmC1JYujSoLmV47
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
