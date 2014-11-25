import numpy as np
import scipy

current_page_num = 5
total_page_num = 5

pagerank_matrix = np.zeros((5,5))
pagerank_matrix_original = pagerank_matrix;

page_content = []
deadend_node_reserve = []

# Read content of files
for i in range(1, current_page_num + 1):
    filename = "page" + str(i) + ".txt"
    fd = open(filename)
    page_content.append(fd.read())

# Find out their relationship
for i in range(0, current_page_num):
    for j in range(0, current_page_num):
        hyperlink = "http://page" + str(i + 1) + ".txt"
        if hyperlink in page_content[j]:
            pagerank_matrix[j][i] = 1

# Remove deadend node from pagerank_matrix
while i >= 0 and i < current_page_num:
    if not pagerank_matrix[i].any():
        pagerank_matrix = scipy.delete(pagerank_matrix, i, 0)
        deadend_node_reserve.append(i)
        pagerank_matrix = scipy.delete(pagerank_matrix, i, 1)
        i = 0
        current_page_num -= 1
    i += 1

# Normalize pagerank_matrix
pagerank_matrix_norm = np.zeros((current_page_num, current_page_num))
for i in range(0, current_page_num):
    pagerank_matrix_norm[i] =  (pagerank_matrix[i] / np.sum(pagerank_matrix[i]))

# PageRank
result = np.array([1 / current_page_num for i in range(0, current_page_num)])
for i in range(0, 100):
    result = np.dot(pagerank_matrix_norm.T, result)

# Re-insert deadend nodes
for i in deadend_node_reserve[-1::-1]:
    result = np.insert(result, i, 0)
    for j in range(0, total_page_num):
        if pagerank_matrix_original.T[i][j] == 1:
            tmp = result[j] / np.sum(pagerank_matrix_original[j])
            result[i] += tmp

print("Original PageRank matrix:")
print(pagerank_matrix_original)

print("PageRank result:")
print(result)

# Input and Search
print("Plaese input a keyword to search: ")
search = input()

result = [[result[i], i] for i in range(0, total_page_num)]
result = sorted(result, reverse = True)

print("Search result: ")
rank = 1
for i in range(0, total_page_num):
    if search in page_content[result[i][1]]:
        filename = "page" + str(result[i][1] + 1) + ".txt"
        print("Rank" + str(rank) + ": " + filename)
        rank += 1
