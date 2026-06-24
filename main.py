import pygame
from settings import *
from entities import AIGuard, Ship, Explosion

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber-Nexus: The Last Node")

font_main = pygame.font.SysFont("Arial", 40, bold=True)
font_sub = pygame.font.SysFont("Arial", 20)

# Load Audio
try:
    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.play(-1)
    shoot_sound = pygame.mixer.Sound("shoot.wav")
    explosion_sound = pygame.mixer.Sound("explosion.wav")
except:
    shoot_sound, explosion_sound = None, None

# Variabel Game
game_state = "MENU"
guards = [AIGuard()]
explosions = []
player = Ship()
health, kill_count, laser_pos = 3, 0, None
clock = pygame.time.Clock()
running = True

while running:
    # 1. INPUT
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state == "MENU":
                game_state = "PLAYING"
                pygame.mixer.music.stop()
            elif game_state == "GAME_OVER":
                game_state, health, kill_count, guards = "PLAYING", 3, 0, [AIGuard()]
                pygame.mixer.music.stop()

        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "PLAYING":
            laser_pos = mouse_pos
            if shoot_sound: shoot_sound.play()
            for guard in guards[:]:
                if guard.rect.collidepoint(mouse_pos):
                    explosions.append(Explosion(guard.rect.centerx, guard.rect.centery))
                    guards.remove(guard)
                    kill_count += 1
                    if explosion_sound: explosion_sound.play()

    # 2. LOGIKA & RENDER
    screen.fill(DARK_BLUE)
    
    if game_state == "MENU":
        title_text = font_main.render("CYBER-NEXUS: THE LAST NODE", True, NEON_CYAN)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 50))
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            start_text = font_sub.render("Tekan [SPACE] untuk memulai game...", True, WHITE)
            screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 50))

    elif game_state == "PLAYING":
        player.update(keys)
        player.draw(screen, mouse_pos)
        
        if len(guards) < 1 + (kill_count // 20): guards.append(AIGuard())
        
        for guard in guards[:]:
            guard.move()
            guard.draw(screen)
            # Deteksi Tabrakan atau Lolos
            if player.rect.colliderect(guard.rect) or guard.x < -20 or guard.x > WIDTH + 20:
                health -= 1
                explosions.append(Explosion(guard.rect.centerx, guard.rect.centery)) # LEDAKAN!
                if explosion_sound: explosion_sound.play() # SUARA!
                guards.remove(guard)
                guards.append(AIGuard())
                if health <= 0: game_state = "GAME_OVER"
        
        for exp in explosions[:]:
            exp.draw(screen)
            if exp.timer <= 0: explosions.remove(exp)
            
        if laser_pos:
            pygame.draw.line(screen, NEON_RED, player.rect.center, laser_pos, 3)
            laser_pos = None
        
        score_text = font_sub.render(f"HEALTH: {health} | KILLS: {kill_count}", True, WHITE)
        screen.blit(score_text, (10, 10))

    elif game_state == "GAME_OVER":
        if not pygame.mixer.music.get_busy(): pygame.mixer.music.play(-1)
        text = font_main.render("GAME OVER - TEKAN [SPACE] RESTART", True, NEON_RED)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()