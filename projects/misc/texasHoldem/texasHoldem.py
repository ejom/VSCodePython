import random
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Card and Deck Setup ---

# Define standard card ranks and suits
RANKS = '23456789TJQKA'
SUITS = 'shdc' # Spades, Hearts, Diamonds, Clubs

# Map ranks to numerical values for easy comparison. Ace can be high (14) or low (1) for straights.
RANK_MAP = {rank: i for i, rank in enumerate(RANKS, 2)}

# Define hand rankings from best to worst
HAND_NAMES = {
    9: "Royal Flush",
    8: "Straight Flush",
    7: "Four of a Kind",
    6: "Full House",
    5: "Flush",
    4: "Straight",
    3: "Three of a Kind",
    2: "Two Pair",
    1: "One Pair",
    0: "High Card"
}

def create_deck():
    """Creates a standard 52-card deck."""
    return [(r, s) for r in RANKS for s in SUITS]

# --- 2. Hand Evaluation Logic ---

def evaluate_hand(seven_cards):
    """
    Evaluates the best 5-card hand from a given 7 cards.
    Returns a tuple where the first element is the hand rank (0-9)
    and the subsequent elements are tie-breakers.
    """
    ranks_num = sorted([RANK_MAP[r] for r, s in seven_cards], reverse=True)
    suits = [s for r, s in seven_cards]
    
    # Check for Flush and Straight Flush
    suit_counts = Counter(suits)
    flush_suit = None
    for suit, count in suit_counts.items():
        if count >= 5:
            flush_suit = suit
            break
            
    is_flush = flush_suit is not None
    
    # Check for Straight
    # For straights, Ace can be low (A-2-3-4-5). We add a '1' if an Ace (14) is present.
    unique_ranks = sorted(list(set(ranks_num)), reverse=True)
    if 14 in unique_ranks:
        unique_ranks.append(1) # Add Ace as low
        
    straight_high_card = None
    # Find the highest straight possible in the 7 cards
    for i in range(len(unique_ranks) - 4):
        # Check for 5 consecutive ranks
        if unique_ranks[i] - unique_ranks[i+4] == 4:
            straight_high_card = unique_ranks[i]
            # Handle the A-5 straight case (ranks are 5,4,3,2,1)
            if straight_high_card == 5 and unique_ranks[i+4] == 1:
                straight_high_card = 5
            break
            
    is_straight = straight_high_card is not None
    
    # --- Determine hand rank ---
    
    # 1. Straight Flush (and Royal Flush)
    if is_flush and is_straight:
        flush_ranks = sorted([RANK_MAP[r] for r, s in seven_cards if s == flush_suit], reverse=True)
        # Check for a straight within the flush cards
        if 14 in flush_ranks:
            flush_ranks.append(1)
            
        for i in range(len(flush_ranks) - 4):
            if flush_ranks[i] - flush_ranks[i+4] == 4:
                straight_flush_high_card = flush_ranks[i]
                if straight_flush_high_card == 14:
                    return (9, ) # Royal Flush is just an Ace-high Straight Flush
                return (8, straight_flush_high_card)

    # Count rank occurrences for pairs, trips, quads, etc.
    rank_counts = Counter(ranks_num)
    # Creates a sorted list of tuples: [(rank, count), ...], e.g., [(10, 3), (5, 2), ...]
    sorted_counts = sorted(rank_counts.items(), key=lambda item: (item[1], item[0]), reverse=True)

    counts = sorted([c for r, c in sorted_counts])
    ranks = [r for r, c in sorted_counts]

    # 2. Four of a Kind
    if counts in [[1, 1, 1, 4], [1, 2, 4], [3, 4]]:
        # Kicker is the highest single card
        kicker = 0
        return (7, ranks[0], kicker)
    
    # 3. Full House
    if counts in [[1, 1, 2, 3], [1, 3, 3], [2, 2, 3]]: # Handles cases like two sets making a full house
        return (6, ranks[0], ranks[1])

    # 4. Flush
    if is_flush:
        flush_ranks = sorted([RANK_MAP[r] for r, s in seven_cards if s == flush_suit], reverse=True)
        return (5, tuple(flush_ranks[:5]))
    
    # 5. Straight
    if is_straight:
        return (4, straight_high_card)

    # 6. Three of a Kind
    if counts == [1, 1, 1, 1, 3]:
        trips_rank = ranks[0]
        kickers = 0
        return (3, trips_rank, kickers, kickers)
        
    # 7. Two Pair
    if counts in [[1, 1, 1, 2, 2], [1, 2, 2, 2]]:
        high_pair, low_pair = ranks[0], ranks[1]
        kicker_ranks = [r for r, c in sorted_counts if c == 1]
        kicker = max(kicker_ranks)
        return (2, high_pair, low_pair, kicker)

    # 8. One Pair
    if counts == [1, 1, 1, 1, 1, 2]:
        pair_rank = ranks[0]
        kickers = sorted([r for r in ranks_num if r != pair_rank], reverse=True)
        return (1, pair_rank, tuple(kickers[:3]))
        
    # 9. High Card
    return (0, tuple(ranks_num[:5]))

# --- 3. Simulation Core ---

def run_simulation(num_players, num_simulations):
    """Runs the main simulation loop."""
    win_counts = Counter()

    for i in range(num_simulations):
        if (i + 1) % (num_simulations // 10 or 1) == 0:
            print(f"Simulating game {i+1}/{num_simulations}...")
            
        deck = create_deck()
        random.shuffle(deck)

        # Deal cards
        player_hands = [[] for _ in range(num_players)]
        # 2 hole cards for each player
        for _ in range(2):
            for p in range(num_players):
                player_hands[p].append(deck.pop())
        
        # 5 community cards (the board)
        community_cards = [deck.pop() for _ in range(5)]

        player_scores = []
        for p in range(num_players):
            seven_card_hand = player_hands[p] + community_cards
            best_hand_score = evaluate_hand(seven_card_hand)
            player_scores.append(best_hand_score)

        # Determine the winner
        winning_score = max(player_scores)
        winning_hand_rank = winning_score[0]
        win_counts[HAND_NAMES[winning_hand_rank]] += 1
        
    print("\nSimulation complete!")
    return win_counts

# --- 4. Plotting Results ---

def plot_results(win_counts):
    """Plots the frequency distribution of winning hands."""
    # Order hands from weakest to strongest for the plot
    ordered_hand_names = [HAND_NAMES[i] for i in range(10)]
    
    # Get counts for each hand, defaulting to 0 if a hand never won
    counts = [win_counts.get(name, 0) for name in ordered_hand_names]
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    bars = ax.bar(ordered_hand_names, counts, color=sns.color_palette("viridis", len(ordered_hand_names)))
    
    ax.set_title(f'Winning Hand Frequency Distribution ({sum(counts):,} Simulations)', fontsize=16, fontweight='bold')
    ax.set_ylabel('Number of Wins', fontsize=12)
    ax.set_xlabel('Hand Type', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Add labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

# --- 5. Main Execution ---

if __name__ == "__main__":
    # --- Configuration ---
    NUM_PLAYERS = 6
    NUM_SIMULATIONS = 1000
    
    # --- Run Simulation ---
    winning_hand_counts = run_simulation(NUM_PLAYERS, NUM_SIMULATIONS)

    # --- Print Results ---
    print(f"\n--- Results for {NUM_SIMULATIONS:,} simulations with {NUM_PLAYERS} players ---")
    for hand_name, count in winning_hand_counts.most_common():
        print(f"{hand_name:<15}: {count} wins")
        
    # Answer the specific question from the prompt
    two_pair_wins = winning_hand_counts.get("Two Pair", 0)
    print("\n" + "="*40)
    print(f"❓ Specific Answer:")
    print(f"A Two Pair was the winning hand {two_pair_wins} times.")
    print("="*40 + "\n")
    
    # --- Plot the graph ---
    plot_results(winning_hand_counts)