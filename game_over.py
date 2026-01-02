import pygame
import os
from snake_game import screen_height, screen_width

podium_positions = {
    1: {"x": screen_width // 2 - 65   , "y_name": 145, "y_score": 145 + 80},
    2: {"x": screen_width // 2 - 215  , "y_name": 190, "y_score": 190 + 80},
    3: {"x": screen_width // 2 + 75   , "y_name": 228, "y_score": 230 + 80},
    4: {"x": screen_width // 2 + 220  , "y_name": 270, "y_score": 270 + 80},
}


def game_over_screen(screen, score, top4):
    pygame.font.init()
    clock = pygame.time.Clock()

    big_font = pygame.font.SysFont("Comic Sans MS", 100, bold=True)
    font = pygame.font.SysFont("Comic Sans MS", 20)
    font_score = pygame.font.SysFont("Comic Sans MS", 30)

    start_time = pygame.time.get_ticks()  # temps de départ
    show_score = False

    waiting = True
    while waiting:
        elapsed = pygame.time.get_ticks() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Les touches ne fonctionnent qu'après les 10 secondes
            if show_score and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        # -------- PHASE 1 : YOU LOSE (10 secondes) --------
        if elapsed < 2000:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            background = pygame.image.load(os.path.join(base_dir, "snake_game_over.png")).convert()
            background = pygame.transform.scale(background, (screen_width, screen_height))
            screen.blit(background, (0, 0))

            lose_text = big_font.render("GAME OVER", True, (170, 0, 0))
            rect = lose_text.get_rect(center = (screen_width // 2, screen_height // 3))
            screen.blit(lose_text, rect)

        # -------- PHASE 2 : SCORE + TOP 4 --------
        else:
            show_score = True
            # screen.fill((0, 0, 0))
            background = pygame.image.load(os.path.join(base_dir, "podium.png")).convert()
            background = pygame.transform.scale(background, (screen_width, screen_height))
            screen.blit(background, (0, 0))

            title = font_score.render(f"Your score : {score}", True, (255, 255 , 255))
            screen.blit(title, (screen_width // 2 - 100, 10))

            y = 120
            # for rank, (username, data) in enumerate(top4, start=1):
            #     line = font.render(f"{rank}. {username} : {data['best_score']}",True,(255, 255, 255))
            #     screen.blit(line, (50, y))
            #     y += 40

            for rank, (username, data) in enumerate(top4, start=1):
                if rank > 4:
                    break

                pos = podium_positions[rank]

                # Prénom
                name_text = font.render(username, True, (255, 255, 255))
                name_rect = name_text.get_rect(center=(pos["x"], pos["y_name"]))
                screen.blit(name_text, name_rect)

                # Score sous la médaille
                score_text = font.render(str(data["best_score"]), True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(pos["x"], pos["y_score"]))
                screen.blit(score_text, score_rect)

            restart = font.render("SPACE to play again - ESC to quit", True, (255, 255, 255))
            screen.blit(restart, (screen_width // 2 - 175, screen_height - 30))

        pygame.display.flip()
        clock.tick(30)
