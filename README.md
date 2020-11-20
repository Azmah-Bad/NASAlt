# NASAlt

## Problematique 
Input : descriptif du réseau, matrice de demande (pe1 envoie autant de trafic à tel router)
Graphe : routers et comment ils sont connectés entre eux
Poids IGP
-> on peut calculer les chemins plus courts (en dijkstra). Prendre résultats de Dijkstra + matrice et comptabiliser le trafic sur chaque lien
IA va dire quel poids mettre pour baisser les pressions des liens


## Overview
- CST
    - threshold de saturation
- INPUT 
    - Matrice de demande en input
    - Le graph et les poids (matrices d’adjacence)
- OUTPUT
    - nouveau poids dans le réseau à chaque fois que la matrice de perturbation change (perturbations)

- Étape intermédiaire:
    - convertir la matrice de demande en % de saturation des lien
    - calcul des tables de routages (n*Dijkstra)


