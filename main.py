import pygame
import sys
import os

class Utilisateur:
    def __init__(self, nom):
        self.nom = nom
        self.score = 0
        self.historique_scores = []

class Partie:
    def __init__(self, joueur1, joueur2):
        self.joueurs = [joueur1, joueur2]
        self.plateau = [[' ' for _ in range(3)] for _ in range(3)]
        self.tour = 0  # 0 pour joueur1, 1 pour joueur2

    def afficher_plateau(self, screen):
        screen.fill((255, 255, 255))

        for row in range(3):
            for col in range(3):
                pygame.draw.rect(screen, (0, 0, 0), (col * 200, row * 200, 200, 200), 2)  # Dessine les cellules
                font = pygame.font.Font(None, 74)
                text = font.render(str(self.plateau[row][col]), True, (0, 0, 0))
                screen.blit(text, (col * 200 + 70, row * 200 + 70))

        pygame.display.flip()

    def verifier_victoire(self, symbole):
        for i in range(3):
            if all(self.plateau[i][j] == symbole for j in range(3)) or all(self.plateau[j][i] == symbole for j in range(3)):
                return True

        if all(self.plateau[i][i] == symbole for i in range(3)) or all(self.plateau[i][2 - i] == symbole for i in range(3)):
            return True

        return False

    def verifier_match_nul(self):
        return all(all(cellule != ' ' for cellule in ligne) for ligne in self.plateau)

    def jouer(self, screen):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    ligne = mouseY // 200
                    colonne = mouseX // 200

                    joueur = self.joueurs[self.tour]
                    symbole = 'X' if self.tour == 0 else 'O'

                    if self.plateau[ligne][colonne] == ' ':
                        self.plateau[ligne][colonne] = symbole

                        self.afficher_plateau(screen)

                        if self.verifier_victoire(symbole):
                            print(f"{joueur.nom} remporte la partie!")
                            joueur.score += 1
                            joueur.historique_scores.append(joueur.score)
                            self.afficher_scores()
                            return
                        elif self.verifier_match_nul():
                            print("Match nul!")
                            self.afficher_scores()
                            return
                        else:
                            self.tour = (self.tour + 1) % 2  # Changer de joueur pour le tour suivant

            self.afficher_plateau(screen)

    def afficher_scores(self):
        for joueur in self.joueurs:
            print(f"{joueur.nom}: Score - {joueur.score}, Historique des scores - {joueur.historique_scores}")

def jouer_tictactoe():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Tic-Tac-Toe")

    joueur1 = Utilisateur("Joueur X")
    joueur2 = Utilisateur("Joueur O")

    while True:
        partie = Partie(joueur1, joueur2)
        partie.jouer(screen)

if __name__ == "__main__":
    jouer_tictactoe()


