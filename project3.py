import pygame
import time
import os
from npc import NPC

THIS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def draw_text(text, font, screen, x, y, color):    
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Check win/lose conditions and return a result
def check_end_conditions(npc_list):
    for npc in npc_list:
        if npc.relationship_score >= 100:
            return "win"
        elif npc.relationship_score <= 10:
            return "lose"
    return None  # Game continues

def display_end_screen(screen, font, result):
    screen.fill((255, 255, 255))
    if result == "win":
        messages = ["You Win! You've formed a strong friendship", "with at least one NPC!"]
    elif result == "lose":
        messages = ["You Lose! At least one NPC has become", "extremely hostile."]
    else:
        messages = ["You Lose! You have reached the maximum number", "of interactions without forming a strong friendship."]

    #draw_text(message, font, screen, 100, 200, (0, 0, 0))
    y_pos = 200
    for message in messages:
        draw_text(message, font, screen, 100, y_pos, (0, 0, 0))
        y_pos += 25
    draw_text("Press R to Restart or Q to Quit", font, screen, 100, 300, (0, 0, 0))
    pygame.display.flip()

    # Wait for player input to restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def main():
    # Initialize Pygame
    pygame.init()
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
    font = pygame.font.Font(None, 36)

    # Create NPCs
    npc1 = NPC("Sunny", "Neutral", 40, (150, 200), 50, os.path.join(THIS_DIRECTORY, "npc_dialogues", "sunny_dialogue.json"), os.path.join(THIS_DIRECTORY, "npc_images", "sunny.png"))
    npc2 = NPC("Finn", "Neutral", 40, (400, 200), 50, os.path.join(THIS_DIRECTORY, "npc_dialogues", "finn_dialogue.json"), os.path.join(THIS_DIRECTORY, "npc_images", "finn.png"))
    npc3 = NPC("Raven", "Neutral", 40, (650, 200), 50, os.path.join(THIS_DIRECTORY, "npc_dialogues", "raven_dialogue.json"), os.path.join(THIS_DIRECTORY, "npc_images", "raven.png")) 
    npc_list = [npc1, npc2, npc3]

    # Define valid keys and corresponding actions
    valid_keys = {
        pygame.K_g: "Greet",
        pygame.K_t: "Trade",
        pygame.K_i: "Insult",
        pygame.K_c: "Compliment",
        pygame.K_l: "Gift",
        pygame.K_e: "Challenge",
        pygame.K_h: "Ask for Help"
    }

    # Main game loop
    running = True
    error_message = ""
    error_time = 0

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
                draw_text(f"{npc_response}", font, screen, 10, 500, black)
        else:
            # Display selected NPC info and action options
            draw_text(f"{selected_npc.name} State: {selected_npc.state}", font, screen, 10, 10, black)
            draw_text(f"{selected_npc.name}'s Relationship Score: {selected_npc.relationship_score}", font, screen, 10, 50, black)
            draw_text("Press G to Greet, T to Trade, I to Insult", font, screen, 10, 150, black)
            draw_text("Press C to Compliment, L to Gift, E to Challenge, H to Ask for Help", font, screen, 10, 180, black)
            if error_message and current_time - error_time < 2:  # Show error message for 2 seconds
                draw_text(f"{error_message}", font, screen, 10, 550, (255, 0, 0))  # Display error in red
                
        # Check win/lose conditions after each interaction
        game_result = check_end_conditions(npc_list)
        if game_result:
            action = display_end_screen(screen, font, game_result)
            if action == "restart":
                main()  # Restart the game
            return  # End the game if quit

        # Additional check for neutral outcome if interaction limit is reached
        if interaction_count >= interaction_limit and not game_result:
            action = display_end_screen(screen, font, "neutral")
            if action == "restart":
                main()  # Restart the game
            return  # End the game if quit

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
                if event.key in valid_keys:
                    # If key is valid, perform action and increment count
                    action = valid_keys[event.key]
                    npc_response = selected_npc.handle_action(action)
                    interaction_count += 1
                    selected_npc = None  # Reset selected NPC
                    response_time = time.time()  # Set the response timer for 2 seconds
                    error_message = ""  # Clear any previous error message
                else:
                    # Show error message for invalid key
                    error_message = "Invalid key! Please press a valid option."
                    error_time = time.time()  # Start timer for the error message

        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()