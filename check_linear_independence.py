import numpy as np


def CHECK_LINEAR_INDEPENDENCE(basis_array):
    "Return True if linearly indepdndant and false otherwise"

    # Recall that rank of a matrix is the number of linearly independant rows or columns
    # So the columns are all linearly indepenadnt if the rank of the matrix equals the number of columns
    check_matrix = np.column_stack(basis_array)

    return np.linalg.matrix_rank(check_matrix) == len(basis_array)
#
# bool_test = CHECK_LINEAR_INDEPENDENCE([[1,1,0],[1,1,0],[0,0,1]])
# print(bool_test)
