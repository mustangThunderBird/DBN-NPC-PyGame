import pygame
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("NPC Social Simulation")

# Game variables
npc_states = ["Neutral", "Neutral", "Neutral"]  # Initial states for each of the three NPCs
relationship_scores = [40, 40, 40]  # Initial relationship score for each NPC
interaction_limit = 10   # Maximum number of interactions allowed
interaction_count = 0    # Counter for the number of interactions

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36)

def draw_text(text, x, y):
    text_surface = font.render(text, True, black)
    screen.blit(text_surface, (x, y))

# Interaction logic with risk-reward system
def update_relationship(npc_index, action):
    global relationship_scores, npc_states, interaction_count
    interaction_count += 1  # Increase the interaction count each time an action is taken

    # Action outcomes with risk-reward for each action
    if action == "Greet":
        relationship_scores[npc_index] += random.randint(2, 8)
    elif action == "Insult":
        if random.random() < 0.3:  # 30% chance of positive effect
            relationship_scores[npc_index] += 15
        else:
            relationship_scores[npc_index] -= random.randint(10, 20)
    elif action == "Trade":
        if random.random() < 0.8:  # 80% chance of positive effect
            relationship_scores[npc_index] += random.randint(1, 10)
        else:
            relationship_scores[npc_index] -= 5
    elif action == "Compliment":
        if random.random() < 0.7:  # 70% chance of positive effect
            relationship_scores[npc_index] += random.randint(5, 15)
        else:
            relationship_scores[npc_index] -= 5
    elif action == "Challenge":
        if random.random() < 0.2:  # 20% chance of a big boost
            relationship_scores[npc_index] += 25
        else:
            relationship_scores[npc_index] -= random.randint(5, 15)
    elif action == "Gift":
        if random.random() < 0.3:  # 30% chance of negative effect
            relationship_scores[npc_index] -= 25
        else:
            relationship_scores[npc_index] += 20
    elif action == "Ask for Help":
        # Depends on current state; positive if NPC is Neutral or Friendly, negative if Hostile
        if npc_states[npc_index] == "Hostile":
            relationship_scores[npc_index] -= random.randint(1, 5)
        else:
            relationship_scores[npc_index] += random.randint(1, 5)
    
    # Update npc_state based on the updated relationship score
    score = relationship_scores[npc_index]
    if score >= 75:
        npc_states[npc_index] = "Friendly"
    elif score <= 25:
        npc_states[npc_index] = "Hostile"
    else:
        npc_states[npc_index] = "Neutral"

# Check win/lose/neutral outcome based on final scores
def check_end_conditions():
    if any(score >= 100 for score in relationship_scores):
        draw_text("You Win! You've formed a strong friendship with at least one NPC!", 10, 300)
        return True  # End game
    elif any(score <= 10 for score in relationship_scores):
        draw_text("You Lose! At least one NPC has become extremely hostile.", 10, 300)
        return True  # End game
    elif all(11 <= score <= 99 for score in relationship_scores):
        draw_text("Neutral Outcome. All NPCs are in a neutral range.", 10, 300)
        return True  # End game
    return False  # Continue game

# Game loop
running = True
while running:
    screen.fill(white)
    for i, score in enumerate(relationship_scores):
        draw_text(f"NPC {i+1} State: {npc_states[i]}", 10, 10 + i * 40)
        draw_text(f"NPC {i+1} Relationship Score: {score}", 200, 10 + i * 40)
    draw_text(f"Interactions Left: {interaction_limit - interaction_count}", 10, 150)
    draw_text("Press G to Greet, T to Trade, I to Insult", 10, 190)
    draw_text("Press C to Compliment, L to Gift, E to Challenge, H to Ask for Help", 10, 220)

    # Only check for win/lose conditions after interaction limit is reached
    if interaction_count >= interaction_limit:
        if check_end_conditions():  # Display the end state and end game if conditions met
            running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and interaction_count < interaction_limit:
            # Choose an NPC to interact with (0, 1, or 2)
            npc_index = random.randint(0, 2)
            if event.key == pygame.K_g:  # Greet
                update_relationship(npc_index, "Greet")
            elif event.key == pygame.K_i:  # Insult
                update_relationship(npc_index, "Insult")
            elif event.key == pygame.K_t:  # Trade
                update_relationship(npc_index, "Trade")
            elif event.key == pygame.K_c:  # Compliment
                update_relationship(npc_index, "Compliment")
            elif event.key == pygame.K_l:  # Gift
                update_relationship(npc_index, "Gift")
            elif event.key == pygame.K_e:  # Challenge
                update_relationship(npc_index, "Challenge")
            elif event.key == pygame.K_h:  # Ask for Help
                update_relationship(npc_index, "Ask for Help")

    pygame.display.flip()

pygame.quit()