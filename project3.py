import pygame
import random
import time
from npc import NPC

def draw_text(text, font, screen, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Check win/lose/neutral outcome based on final scores
def check_end_conditions():    
    relationship_scores = [npc.relationship_score for npc in npc_list]
    if any(score >= 100 for score in relationship_scores):
        draw_text("You Win! You've formed a strong friendship with at least one NPC!", font, screen, 10, 400, (0,0,0))
        return True  # End game
    elif any(score <= 10 for score in relationship_scores):
        draw_text("You Lose! At least one NPC has become extremely hostile.", font, screen, 10, 400, (0,0,0))
        return True  # End game
    elif all(11 <= score <= 99 for score in relationship_scores):
        draw_text("Neutral Outcome. All NPCs are in a neutral range.", font, screen, 10, 400, (0,0,0))
        return True  # End game
    return False  # Continue game

def main():
    # Initialize Pygame
    pygame.init()
    global screen
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("NPC Social Simulation")

    #game variables
    interaction_limit = 10   # Maximum number of interactions allowed
    interaction_count = 0    # Counter for the number of interactions
    selected_npc = None      # Tracks which NPC is selected
    npc_response = ""        # Tracks the NPC's response dialogue
    response_time = 0        # Timer for displaying the response

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    # Font
    global font
    font = pygame.font.Font(None, 36)

    # Create NPCs
    npc1 = NPC("NPC 1", "Neutral", 40, (255, 0, 0), (150, 200), 50)  # Red NPC
    npc2 = NPC("NPC 2", "Neutral", 40, (0, 255, 0), (400, 200), 50)  # Green NPC
    npc3 = NPC("NPC 3", "Neutral", 40, (0, 0, 255), (650, 200), 50)  # Blue NPC
    global npc_list
    npc_list = [npc1, npc2, npc3]

    # Main game loop
    running = True
    while running:
        screen.fill(white)
        current_time = time.time()

        if selected_npc is None:
            for npc in npc_list:
                npc.draw_face(screen)
                npc.draw_name(screen, font, black)
                npc.draw_score(screen, font, black)
            draw_text(f"Interactions Left: {interaction_limit - interaction_count}", font, screen, 10, 50, black)
            if npc_response and current_time - response_time < 2:  # Show response for 2 seconds
                draw_text(f"NPC says: {npc_response}", font, screen, 10, 500, black)
        else:
            # Display selected NPC info and action options
            draw_text(f"{selected_npc.name} State: {selected_npc.state}", font, screen, 10, 10, black)
            draw_text(f"{selected_npc.name}'s Relationship Score: {selected_npc.relationship_score}", font, screen, 10, 50, black)
            draw_text("Press G to Greet, T to Trade, I to Insult", font, screen, 10, 150, black)
            draw_text("Press C to Compliment, L to Gift, E to Challenge, H to Ask for Help", font, screen, 10, 180, black)
        
        # Only check for win/lose conditions after interaction limit is reached
        if interaction_count >= interaction_limit:
            if check_end_conditions():  # Display the end state and end game if conditions met
                running = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and selected_npc is None:
                # Detect if an NPC face was clicked
                mouse_x, mouse_y = event.pos
                npc_positions = [npc.position for npc in npc_list]
                for i, pos in enumerate(npc_positions):
                    distance = ((mouse_x - pos[0]) ** 2 + (mouse_y - pos[1]) ** 2) ** 0.5
                    this_npc = npc_list[i]
                    if distance <= this_npc.radius:
                        selected_npc = this_npc
                        break
            elif event.type == pygame.KEYDOWN and selected_npc is not None and interaction_count < interaction_limit:
                if event.key == pygame.K_g:
                    selected_npc.update_relationship("Greet")
                    npc_response = selected_npc.choose_response("Greet")
                elif event.key == pygame.K_t:
                    selected_npc.update_relationship("Trade")
                    npc_response = selected_npc.choose_response("Trade")
                elif event.key == pygame.K_i:
                    selected_npc.update_relationship("Insult")
                    npc_response = selected_npc.choose_response("Insult")
                elif event.key == pygame.K_c:
                    selected_npc.update_relationship("Compliment")
                    npc_response = selected_npc.choose_response("Compliment")
                elif event.key == pygame.K_l:
                    selected_npc.update_relationship("Gift")
                    npc_response = selected_npc.choose_response("Gift")
                elif event.key == pygame.K_e:
                    selected_npc.update_relationship("Challenge")
                    npc_response = selected_npc.choose_response("Challenge")
                elif event.key == pygame.K_h:
                    selected_npc.update_relationship("Ask for Help")
                    npc_response = selected_npc.choose_response("Ask for Help")
                interaction_count += 1
                selected_npc = None  # Reset selected NPC
                response_time = time.time() + 2  # Set the response timer for 2 seconds

        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()