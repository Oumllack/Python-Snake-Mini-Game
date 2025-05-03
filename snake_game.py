import pygame
import random
import sys
import time

# Initialisation de PyGame
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
TAILLE_BLOC = 20
VITESSE = 10

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)

# Configuration de la fenêtre
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('Jeu de Collecte')
horloge = pygame.time.Clock()

class Joueur:
    def __init__(self):
        self.x = LARGEUR // 2
        self.y = HAUTEUR // 2
        self.vitesse = 30

    def bouger(self, touches):
        if touches[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vitesse
        if touches[pygame.K_RIGHT] and self.x < LARGEUR - TAILLE_BLOC:
            self.x += self.vitesse
        if touches[pygame.K_UP] and self.y > 0:
            self.y -= self.vitesse
        if touches[pygame.K_DOWN] and self.y < HAUTEUR - TAILLE_BLOC:
            self.y += self.vitesse

    def dessiner(self):
        pygame.draw.rect(ecran, VERT, (self.x, self.y, TAILLE_BLOC, TAILLE_BLOC))

    def collision(self, cible):
        return (self.x < cible.x + TAILLE_BLOC and
                self.x + TAILLE_BLOC > cible.x and
                self.y < cible.y + TAILLE_BLOC and
                self.y + TAILLE_BLOC > cible.y)

class Cible:
    def __init__(self):
        self.position_aleatoire()

    def position_aleatoire(self):
        self.x = random.randrange(0, LARGEUR - TAILLE_BLOC)
        self.y = random.randrange(0, HAUTEUR - TAILLE_BLOC)

    def dessiner(self):
        pygame.draw.rect(ecran, ROUGE, (self.x, self.y, TAILLE_BLOC, TAILLE_BLOC))

class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = BLEU
        self.couleur_hover = (0, 100, 255)
        self.police = pygame.font.Font(None, 36)
        
    def dessiner(self, surface):
        pos_souris = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos_souris):
            pygame.draw.rect(surface, self.couleur_hover, self.rect)
        else:
            pygame.draw.rect(surface, self.couleur, self.rect)
            
        texte_surface = self.police.render(self.texte, True, BLANC)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)
        
    def est_clique(self, pos):
        return self.rect.collidepoint(pos)

def afficher_score(score, temps_restant):
    police = pygame.font.Font(None, 36)
    texte_score = police.render(f'Score: {score}', True, BLANC)
    texte_temps = police.render(f'Temps: {temps_restant}s', True, BLANC)
    ecran.blit(texte_score, (10, 10))
    ecran.blit(texte_temps, (LARGEUR - 150, 10))

def afficher_fin_partie(score):
    police = pygame.font.Font(None, 72)
    texte_fin = police.render('Temps écoulé!', True, BLANC)
    texte_score = police.render(f'Score final: {score}', True, BLANC)
    
    ecran.blit(texte_fin, (LARGEUR//2 - 150, HAUTEUR//2 - 100))
    ecran.blit(texte_score, (LARGEUR//2 - 150, HAUTEUR//2 - 20))

def main():
    bouton_restart = Bouton(LARGEUR//2 - 100, HAUTEUR//2 + 50, 200, 50, "Rejouer")
    
    while True:
        joueur = Joueur()
        cible = Cible()
        score = 0
        temps_debut = time.time()
        duree_partie = 60  # 1 minute
        partie_terminee = False
        
        while not partie_terminee:
            temps_actuel = time.time()
            temps_restant = max(0, int(duree_partie - (temps_actuel - temps_debut)))
            
            if temps_restant == 0:
                partie_terminee = True
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Déplacement du joueur
            touches = pygame.key.get_pressed()
            joueur.bouger(touches)

            # Vérification de collision avec la cible
            if joueur.collision(cible):
                score += 1
                cible.position_aleatoire()

            # Dessin
            ecran.fill(NOIR)
            joueur.dessiner()
            cible.dessiner()
            afficher_score(score, temps_restant)
            
            pygame.display.flip()
            horloge.tick(VITESSE)

        # Boucle de fin de partie
        while partie_terminee:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_restart.est_clique(event.pos):
                        partie_terminee = False
                        break

            ecran.fill(NOIR)
            afficher_fin_partie(score)
            bouton_restart.dessiner(ecran)
            pygame.display.flip()
            horloge.tick(30)

if __name__ == "__main__":
    main() 