from node import Node
from segment import Segment

n1 = Node('Node1', 0, 0)
n2 = Node('Node2', 3, 4)
n3 = Node('Node3', 6, 8)

# Crear 2 segmentos
s1 = Segment('Segment1', n1, n2)
s2 = Segment('Segment2', n2, n3)

print("Segment 1:")
print(f"Name: {s1.name}")
print(f"Origin: {s1.origin.name}")
print(f"Destination: {s1.destination.name}")
print(f"Cost: {s1.cost}")

print("\nSegment 2:")
print(f"Name: {s2.name}")
print(f"Origin: {s2.origin.name}")
print(f"Destination: {s2.destination.name}")
print(f"Cost: {s2.cost}")