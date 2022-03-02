Structure of our codes:

projectPython/
├─ game/
│  ├─ AI.py
│  ├─ ActionMenu.py
│  ├─ animation.py
│  ├─ camera.py
│  ├─ game.py
│  ├─ hud.py
│  ├─ map.py
│  ├─ new_AI.py
│  ├─ test.py
│  ├─ utils.py
│  ├─ __init__.py
├─ resources/
│  ├─ common/
│  │  ├─ icon.png
│  ├─ assets/
│  │  ├─models/
│  │  ├─tech_tree/
├─ building.py
├─ main.py
├─ player.py
├─ settings.py
├─ task.txt
├─ tech.py
├─ units.py


Liste des actions possibles (réseau) :
- déplacement d’une unité x d’une tile a vers une tile b
- création d’un batiment x sur une tile y
- attaque d’une unité x sur une unité y
- récolte d’une ressource x par une unité y
- recherche d’une technologie (technologie x, batiment y)
- entrainement d’une unité (batiment x, unité type y).
- changement d’age

Unité 130 (ajouter ID pour chaque entité).

À modifier :
- modifier placements unité de départ (liste de positions disponibles)


Création de la partie :
- bouton créer partie
- bouton rejoindre partie (spécifier IP et port ?)
- pour Jean courageux : mot de passe
- changer couleur/nom (ne doivent pas avoir le meme)
- prendre comme modèle la map créée par le premier joueur ?

Fonction pour sérialiser une donnée (à appeler après chaque action)

Fonction pour désérialiser une donnée reçue

***

mecanique systeme pour attendre plein de trucs en parallele

appel systeme "select", permet d'attendre de tout type de descripteur d'entrée sortie
(l'avantage c'est que "tout ets fichier sous linux")

une boucle unique (unix lol)

basé sur les descripteurs réseau, api socket (couteau suisse systeme donc versatile)

problemes udp spécifiques : taille de message, perte de donnée
probleme plus cachés (config par defaut de taille de buffer kernel pas toujours adaptée)

a retenir : chaque protocole réseau a ses propres problèmes spécifiques

apprendre à utiliser un truc et le maitriser et tout faire avec

simplicité et paresse sont de grandes vertus
