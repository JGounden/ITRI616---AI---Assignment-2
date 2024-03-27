import pygame
import numpy as np
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class Boid:
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=np.float64)
        self.velocity = np.random.rand(2) * 4 - 2
        self.velocity /= np.linalg.norm(self.velocity)  


    def update(self, boids, obstacles):
        separation = self.computeSeparation(boids)
        alignment = self.computeAlignment(boids)
        cohesion = self.computeCohesion(boids)
        obstacle_avoidance = self.avoidObstacles(obstacles)
          
        new_velocity = separation + alignment + cohesion + obstacle_avoidance
        self.velocity += new_velocity
        self.position += self.velocity
        self.velocity /= np.linalg.norm(self.velocity) 
        
        self.position[0] = np.clip(self.position[0], 0, SCREEN_WIDTH)
        self.position[1] = np.clip(self.position[1], 0, SCREEN_HEIGHT)

    def computeSeparation(self, boids):
        separation_distance = 20
        steer = np.zeros(2)
        for boid in boids:
            if boid != self:
                distance = np.linalg.norm(self.position - boid.position)
                if distance < separation_distance:
                    diff = self.position - boid.position
                    steer += diff / distance
        return steer

    def computeAlignment(self, boids):
        neighbor_distance = 100
        mean_velocity = np.zeros(2)
        count = 0
        for boid in boids:
            if boid != self:
                distance = np.linalg.norm(self.position - boid.position)
                if distance < neighbor_distance:
                    mean_velocity += boid.velocity
                    count += 1
        if count > 0:
            mean_velocity /= count
            return (mean_velocity - self.velocity) / 8  
        return np.zeros(2)

    def computeCohesion(self, boids):
        cohesion_distance = 100
        mean_position = np.zeros(2)
        count = 0
        for boid in boids:
            if boid != self:
                distance = np.linalg.norm(self.position - boid.position)
                if distance < cohesion_distance:
                    mean_position += boid.position
                    count += 1
        if count > 0:
            mean_position /= count
            desired_velocity = (mean_position - self.position) / 100  
            return (desired_velocity - self.velocity) / 8  
        return np.zeros(2)

    def avoidObstacles(self, obstacles):
        avoidance_distance = 50
        steer = np.zeros(2)
        for obstacle in obstacles:
            distance = np.linalg.norm(self.position - obstacle)
            if distance < avoidance_distance:
                diff = self.position - obstacle
                steer += diff / distance
        return steer

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Boids Simulation")
    clock = pygame.time.Clock()

    boids = []
    obstacles = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    boids.append(Boid(event.pos[0], event.pos[1]))
                elif event.button == 3:  
                    obstacles.append(event.pos)

        screen.fill(BLACK)

        
        for obstacle in obstacles:
            pygame.draw.circle(screen, RED, obstacle, 10)

        
        for boid in boids:
            boid.update(boids, obstacles)
            boid_image = pygame.Surface((20, 20))
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.polygon(boid_image, color, [(0, 0), (10, 20), (20, 0)])
            screen.blit(boid_image, boid.position - np.array([10, 10]))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
