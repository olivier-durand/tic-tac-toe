import pygame
import sys
import random
import os

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
GRID_SIZE = 3
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Fonction pour dessiner la grille
def draw_grid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT), 2)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), 2)

# Fonction pour dessiner le X ou O dans une cellule
def draw_symbol(row, col, symbol):
    font = pygame.font.Font(None, 100)
    text = font.render(symbol, True, RED)
    text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
    screen.blit(text, text_rect)

# Fonction pour vérifier l'état du jeu
def check_game_state(board):
    # Vérifier les lignes et les colonnes
    for i in range(GRID_SIZE):
        if all(board[i][j] == 1 for j in range(GRID_SIZE)) or all(board[j][i] == 1 for j in range(GRID_SIZE)):
            return "Victoire joueur"

        if all(board[i][j] == 2 for j in range(GRID_SIZE)) or all(board[j][i] == 2 for j in range(GRID_SIZE)):
            return "Victoire IA"

    # Vérifier les diagonales
    if all(board[i][i] == 1 for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - i - 1] == 1 for i in range(GRID_SIZE)):
        return "Victoire joueur"

    if all(board[i][i] == 2 for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - i - 1] == 2 for i in range(GRID_SIZE)):
        return "Victoire IA"

    # Vérifier s'il y a un match nul
    if all(all(cell != 0 for cell in row) for row in board):
        return "Match nul"

    # Le jeu continue
    return "En cours"

# Fonction pour l'IA de niveau facile (aléatoire)
def facile_ai(board):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    return random.choice(empty_cells) if empty_cells else None

# Fonction pour l'IA de niveau moyen
def moyen_ai(board):
    # Priorité : gagner, bloquer le joueur, jouer au hasard
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                # Test de la victoire
                board[i][j] = 2
                if check_game_state(board) == "Victoire IA":
                    board[i][j] = 0
                    return i, j
                board[i][j] = 0

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                # Test du blocage du joueur
                board[i][j] = 1
                if check_game_state(board) == "Victoire joueur":
                    board[i][j] = 0
                    return i, j
                board[i][j] = 0

    return facile_ai(board)

# Fonction pour l'IA de niveau difficile (minimax)
def minimax(board, depth, maximizing_player):
    scores = {"Victoire IA": 1, "Match nul": 0, "Victoire joueur": -1}

    game_state = check_game_state(board)
    if game_state in scores:
        return scores[game_state]

    if maximizing_player:
        max_eval = float("-inf")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i][j] == 0:
                    board[i][j] = 2
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = 0
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i][j] == 0:
                    board[i][j] = 1
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = 0
                    min_eval = min(min_eval, eval)
        return min_eval

def difficile_ai(board):
    best_move = None
    best_eval = float("-inf")
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                board[i][j] = 2
                eval = minimax(board, 0, False)
                board[i][j] = 0
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move if best_move else facile_ai(board)

# Fonction principale du jeu
def main(difficulty):
    board = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]

    current_player = 1  # 1 pour le joueur, 2 pour l'IA
    game_state = "En cours"

    while game_state == "En cours":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_player == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                col = mouseX // CELL_SIZE
                row = mouseY // CELL_SIZE
                if board[row][col] == 0:
                    board[row][col] = 1  # Le joueur joue
                    current_player = 2

        # Logique de l'IA
        if current_player == 2:
            if difficulty == "facile":
                move = facile_ai(board)
            elif difficulty == "moyen":
                move = moyen_ai(board)
            elif difficulty == "difficile":
                move = difficile_ai(board)

            if move:
                row, col = move
                board[row][col] = 2  # L'IA joue
                current_player = 1

        # Affichage
        screen.fill(WHITE)
        draw_grid()

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == 1:
                    draw_symbol(row, col, 'X')
                elif board[row][col] == 2:
                    draw_symbol(row, col, 'O')

        pygame.display.flip()

        # Vérification de l'état du jeu après chaque coup
        game_state = check_game_state(board)
        if game_state != "En cours":
            print("État du jeu:", game_state)

# Exécution du jeu
if __name__ == "__main__":
    difficulty = input("Choisissez la difficulté (facile, moyen, difficile): ").lower()
    if difficulty not in ["facile", "moyen", "difficile"]:
        print("Difficulté non valide. Utilisation de la difficulté par défaut (moyen).")
        difficulty = "moyen"

    main(difficulty)
