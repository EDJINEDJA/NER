"""
Ce fichier contient le code source utilisé pour construire un graphe
"""

import math

class MyGraph:
  def __init__(self):
    self.adjacency = {} #on représente le graphe avec un dictionnaire dont les clefs sont les noeuds du graphes, et les valeurs des ensembles de noeuds ver lesquels pointe le noeud.
    self.weights = {} #les poids des arcs sont stockés dans un dictionnaire
    
  def __str__(self):
    return "adjacency : " + str(self.adjacency) + ", weights : " + str(self.weights)

  def add_node(self, s):
    if s in self.adjacency:
      return
    self.adjacency[s] = set() #on initialise la liste d'adjacence des avec un ensemble vide

  def add_arc(self, arc, weight = ""):
    s1, s2 = arc
    self.add_node(s1)
    self.add_node(s2)
    self.weights[arc] = weight
    self.adjacency[s1].add(s2)
    
  def remove_arc(self, arc):
    if arc not in set.weights:
      return
    del self.weights[arc]
    s1, s2 = arc
    self.adjacency[s1].remove(s2)
    
  def remove_node(self, node): #il faut d'abord retirer tous les arcs pointant sur le noeud, tous les arc partant du noeuds, puis supprimer le noeud
    if node not in self.adjacency:
      return
    for other in self.adjancency:
      self.remove_arc( (node, other) )
      self.remove_arc( (other, node) )
    del self.adjancency[node]
      
  def nodes(self):
    return set(self.adjacency)#on convertit les clefs du dictionnaire en un ensemble 
    
  def successors(self, node):
    return set(self.adjacency[node])
    
  def predecessors(self, node):
    return set(s for s in self.adjacency if s in self.adjacency[node])
    
  def arc_weight(self, arc):
    return self.weights[arc]




