#!/usr/bin/python3
import hashlib
import base58

def rehash(hash_bytes: bytes, bet: int, balance: int) -> list:
    # Combine the hash bytes, bet, and balance into a seed
    seed = hash_bytes + bet.to_bytes(8, 'little') + balance.to_bytes(8, 'little')
    # Hash the seed using SHA256
    result_hash = hashlib.sha256(seed).digest()  # 32 bytes
    # Split the hash into four 8-byte chunks and convert to integers
    
    result = []
    for i in range(4):
        start = i * 8
        cur_bytes = result_hash[start:start+8]
        v = int.from_bytes(cur_bytes, 'little')
        result.append(v)
    return result

SOL_TO_LAMPORTS_COEF = 1000000000

def lamports_to_str(n):
    first_part = n // SOL_TO_LAMPORTS_COEF
    second_part = n % SOL_TO_LAMPORTS_COEF
    return str(first_part)+"."+str(second_part)

def str_to_lamports(s):
    parts = s.split(".")
    if len(parts) > 2:
        print("invalid number:", s)
        exit()
    elif len(parts) == 2:
        first_part = int(parts[0])*SOL_TO_LAMPORTS_COEF
        second_part_first = int(parts[1])*SOL_TO_LAMPORTS_COEF
        deg = 10**len(parts[1])
        if second_part_first % deg != 0:
            print("Invalid amount:", s)
            exit()
        return first_part + (second_part_first // deg)
    else:
        first_part = int(parts[0])*SOL_TO_LAMPORTS_COEF
        return first_part

def play(recent_block_hash: str, bet_lam: int, balance_lam: int, max_loss_promil: int, mean_delta_promil: int) -> dict:
    # Constants
    MIN_BET_LAM = 1000000
    MAX_BET_PROMIL = 100

    bet_sol = bet_lam / SOL_TO_LAMPORTS_COEF

    # Check for minimum bet amount
    if bet_lam < MIN_BET_LAM:
        bet_sol = lamports_to_str(bet_lam)
        min_bet_sol = lamports_to_str(MIN_BET_LAM)
        return {
            'error': f"Bet amount {bet_sol} SOL is below the minimum allowed of {MIN_BET_SOL} SOL."
        }
    # Check for maximum bet amount
    max_bet_lam = MAX_BET_PROMIL*balance_lam//1000
    if bet_lam > max_bet_lam:
        # Refund the bet amount
        bet_sol = lamports_to_str(bet_lam)
        return {
            'error': "Bet amount exceeds 10% of the lottery balance. Refunding your bet of " + bet_sol + " SOL."
        }
    hash_bytes = base58.b58decode(recent_block_hash)

    # Rehash to generate random values
    cur_hash = rehash(hash_bytes, bet_lam, balance_lam)
    rand_val_for_amount = cur_hash[1] ^ cur_hash[2] ^ cur_hash[3]
    rand_val_promille = abs(rand_val_for_amount) % 1000

    rand_val_win = cur_hash[0] % 1000
    player_wins = abs(rand_val_win) < 500 - mean_delta_promil

    if player_wins:
        max_loss_abs = (max_loss_promil*balance_lam) // 1000
        max_win_abs = min(max_loss_abs, bet_lam)
        win = (max_win_abs * rand_val_promille) // 1000
        payout_lamports = bet_lam + win
    else:
        loss = (bet_lam*rand_val_promille) // 1000
        payout_lamports = bet_lam - loss

    return {
        'outcome': 'win' if player_wins else 'loss',
        'initial_bet_prom': bet_lam,
        'payout_prom': payout_lamports,
        'promil_change': rand_val_promille
    }

def main():
    print("Welcome to the Game Result Verifier!")

    # Provide guidance on where to find the required information
    print("\nTo find the Recent Block Hash, transaction amount, and lottery balance, please visit:")
    print("https://solscan.io/tx/{transaction_id}")
    print("You can find the Recent Block Hash in the transaction details, and the amounts in the 'Change Balance' tab.")
    
    # Get user inputs
    recent_block_hash = input("Enter Recent Block Hash: ").strip()
    bet_sol = input("Enter bet amount (in SOL): ").strip()
    balance_sol = input("Enter lottery preBalance (in SOL): ").strip()

    # Game parameters (fixed values)
    max_loss_promil = 100
    mean_delta_promil = 300
    
    result = play(recent_block_hash, str_to_lamports(bet_sol), str_to_lamports(balance_sol), max_loss_promil, mean_delta_promil)

    # Display results
    print("\n--- Game Result ---")
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        outcome_text = "You **won**!" if result['outcome'] == 'win' else "You **lost**."
        bet_sol = lamports_to_str(result['initial_bet_prom'])
        payout_sol = lamports_to_str(result['payout_prom'])
        percent_change_int = result['promil_change']//10
        percent_change_frac = result['promil_change']%10
        percent_change = str(percent_change_int) + "." + str(percent_change_frac)
        print(f"Outcome: {outcome_text}")
        print(f"Initial Bet: {bet_sol} SOL")
        print(f"Payout: {payout_sol} SOL")
        print(f"Percentage Change: {percent_change}%")
    print("--------------------")

    print("\nPlease note that we use only one address for this service: soLV8oMjQtwihUmYEJsbgpdFya7CrmC1JYujSoLmV47")

if __name__ == "__main__":
    main()
