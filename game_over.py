import pygame

def game_over_screen(screen, score, top4):
    font = pygame.font.SysFont("Arial", 32)
    screen.fill((0, 0, 0))

    text = font.render(f"GAME OVER - Score : {score}", True, (255, 0, 0))
    screen.blit(text, (50, 50))

    y = 120
    for rank, (username, data) in enumerate(top4, start=1):
        line = font.render(f"{rank}. {username} : {data['best_score']}", True, (255, 255, 255))
        screen.blit(line, (50, y))
        y += 40

    restart = font.render("ESPACE pour rejouer — ESC pour quitter", True, (0, 255, 0))
    screen.blit(restart, (50, y + 40))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    return
