
proposal_id = input("Enter the proposal ID: ")


n_vertices = int(input("Enter the number of vertices: "))

vertices = ["s"]
for i in range(1, n_vertices-1):
    vertices.append(chr(i + 96))
vertices.append("t")


ajdacency_matrix = []

line = [0] * n_vertices


for vertex in vertices[0:len(vertices)-1]:
    print(vertex+">")
    successors = input("Enter the successors of " + vertex + " and their respective weights (e.g.: 'a:10 b:2 c:7'): ").split(" ")

    for successor in successors:
        successor = successor.split(":")
        line[vertices.index(successor[0])] = int(successor[1])

    
    ajdacency_matrix.append(line)

    line = [0] * n_vertices
    
ajdacency_matrix.append([0] * n_vertices)



if int(proposal_id) > 5 :
    bis_ajdacency_matrix = []

line = [0] * n_vertices


for vertex in vertices[0:len(vertices)-1]:
    print(vertex+">")
    successors = input("Enter the successors of " + vertex + " and their respective weights (space separated): ").split(" ")

    for successor in successors:
        successor = successor.split(":")
        line[vertices.index(successor[0])] = int(successor[1])

    
    bis_ajdacency_matrix.append(line)

    line = [0] * n_vertices
    
bis_ajdacency_matrix.append([0] * n_vertices)

with open("proposals/proposal_{}.txt".format(proposal_id), "w") as f:
    

    print(n_vertices, file=f)
    for line in ajdacency_matrix:
        for _ in line:    
            print(_, end=" ", file=f)
        print("", file=f)

    for line in bis_ajdacency_matrix:
        for _ in line:    
            print(_, end=" ", file=f)
        print("", file=f)