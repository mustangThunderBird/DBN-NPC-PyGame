import random
import pygame
import json

class NPC:
    def __init__(self, name, state, relationship_score, position, radius, dialogue_file, image_file):
        self.name = name
        self.state = state
        self.relationship_score = relationship_score
        self.position = position
        self.radius = radius
        self.dialogue = self.load_dialogue(dialogue_file)
        self.image = pygame.image.load(image_file)  # Load the image file for the sprite
        self.image = pygame.transform.scale(self.image, (156, 156)) 

    def load_dialogue(self, filename):
        with open(filename, 'r') as file:
            dialogue_data = json.load(file)
        return dialogue_data

    def draw_name(self, screen, font, color):
        name_surface = font.render(self.name, True, color)
        screen.blit(name_surface, (self.position[0] - 30, self.position[1] + 60))

    def draw_score(self, screen, font, color):
        score_surface = font.render(f"Score: {self.relationship_score}", True, color)
        screen.blit(score_surface, (self.position[0] - 30, self.position[1] + 80))

    def draw_face(self, screen):
        screen.blit(self.image, (self.position[0] - 50, self.position[1] - 50))

    def update_state(self):
        if self.relationship_score >= 75:
            self.state = "Friendly"
        elif self.relationship_score <= 25:
            self.state = "Hostile"
        else:
            self.state = "Neutral"

    def update_relationship(self, action):
        previous_score = self.relationship_score
        if action == "Greet":
            self.relationship_score += random.randint(2, 8)
        elif action == "Insult":
            if random.random() < 0.3:
                self.relationship_score += 15
            else:
                self.relationship_score -= random.randint(10, 20)
        elif action == "Trade":
            if random.random() < 0.8:
                self.relationship_score += random.randint(1, 10)
            else:
                self.relationship_score -= 5
        elif action == "Compliment":
            if random.random() < 0.7:
                self.relationship_score += random.randint(5, 15)
            else:
                self.relationship_score -= 5
        elif action == "Challenge":
            if random.random() < 0.2:
                self.relationship_score += 25
            else:
                self.relationship_score -= random.randint(5, 15)
        elif action == "Gift":
            if random.random() < 0.3:
                self.relationship_score -= 25
            else:
                self.relationship_score += random.randint(5, 30)
        elif action == "Ask for Help":
            if self.state == "Hostile":
                self.relationship_score -= random.randint(1, 5)
            else:
                self.relationship_score += random.randint(1, 5)
        
        # Update state after changing the score
        self.update_state()

        # Determine if the outcome is positive, negative, or neutral
        if self.relationship_score > previous_score:
            return "positive"
        elif self.relationship_score < previous_score:
            return "negative"
        else:
            return "neutral"

    def handle_action(self, action):
        outcome = self.update_relationship(action)
        response = self.choose_response(action, outcome)
        return response

    def choose_response(self, action, outcome):
        # Choose response based on action and outcome
        if outcome in self.dialogue[action]:
            return f"{self.name} says: {random.choice(self.dialogue[action][outcome])}"
        return ""
