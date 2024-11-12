import random
import pygame

# Possible dialogue responses for each NPC and action
npc_dialogues = {
    "Greet": ["Hello there!", "Nice to see you!", "Hey! How's it going?"],
    "Insult": ["That's not very nice!", "Why would you say that?", "Ouch, that hurts!"],
    "Trade": ["Thank you for the trade!", "I appreciate that!", "This could be useful."],
    "Compliment": ["Aw, thanks!", "You're too kind!", "I appreciate the compliment!"],
    "Challenge": ["Bring it on!", "I'm not afraid!", "Let's see what you got!"],
    "Gift": ["Wow, thanks for the gift!", "This is so nice of you!", "I really appreciate it!"],
    "Ask for Help": ["How can I assist?", "Of course, I'm here to help!", "What do you need?"],
}

class NPC:
    def __init__(self, name, state, relationship_score, color, position, radius):
        self.name = name
        self.state = state
        self.relationship_score = relationship_score
        self.color = color
        self.position = position
        self.radius = radius

    def draw_name(self, screen, font, color):
        # Draw the NPC's name and relationship score
        name_surface = font.render(self.name, True, color)
        screen.blit(name_surface, (self.position[0] - 30, self.position[1] + 60))

    def draw_score(self, screen, font, color):
        # Draw the NPC's name and relationship score
        score_surface = font.render(f"Score: {self.relationship_score}", True, color)
        screen.blit(score_surface, (self.position[0] - 30, self.position[1] + 80))

    def draw_face(self, screen):
        # Draw the NPC's face
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def update_state(self):
        # Update the NPC's state based on the relationship score
        if self.relationship_score >= 75:
            self.state = "Friendly"
        elif self.relationship_score <= 25:
            self.state = "Hostile"
        else:
            self.state = "Neutral"

    def choose_response(self, action):
        # Set the NPC's response dialogue based on the action
        self.response = random.choice(npc_dialogues[action])
        return self.response
    
    def update_relationship(self, action):
        # Update the relationship score based on the action
        if action == "Greet":
            self.relationship_score += random.randint(2, 8)
        elif action == "Insult":
            if random.random() < 0.3:  # 30% chance of positive effect
                self.relationship_score += 15
            else:
                self.relationship_score -= random.randint(10, 20)
        elif action == "Trade":
            if random.random() < 0.8:  # 80% chance of positive effect
                self.relationship_score += random.randint(1, 10)
            else:
                self.relationship_score -= 5
        elif action == "Compliment":
            if random.random() < 0.7:  # 70% chance of positive effect
                self.relationship_score += random.randint(5, 15)
            else:
                self.relationship_score -= 5
        elif action == "Challenge":  # 20% chance of a big boost
            if random.random() < 0.2:
                self.relationship_score += 25
            else:
                self.relationship_score -= random.randint(5, 15)
        elif action == "Gift":  # 30% chance of negative effect
            if random.random() < 0.3:
                self.relationship_score -= 25
            else:
                self.relationship_score += random.randint(5, 30)
        elif action == "Ask for Help":
            if self.state == "Hostile":
                self.relationship_score -= random.randint(1,5)
            else:
                self.relationship_score += random.randint(1,5)
        # Update the NPC's state
        self.update_state()
        # Return the updated relationship score
        self.choose_response(action)