import numpy as np

from hamiltonian import HeH_HAMILTONIAN
from check_linear_independence import CHECK_LINEAR_INDEPENDENCE
from qiskit.quantum_info import SparsePauliOp, Operator, Statevector


def BASIS_SET(hamiltonian, starting_state):

    hamiltonian_operator = hamiltonian.to_operator()

    print(hamiltonian_operator)
    psi0 = Statevector.from_label(starting_state)

    basis_states = [psi0]

    while CHECK_LINEAR_INDEPENDENCE(basis_states):
        evolved_state = psi0.evolve(hamiltonian_operator)
        psi_next = evolved_state / np.linalg.norm(evolved_state)
        basis_states.append(psi_next)
        psi0 = psi_next
        print(basis_states)

    # print(CHECK_LINEAR_INDEPENDENCE(basis_states))
    # Recall that rank of a matrix is the number of linearly independant rows or columns
    # So the columns are all linearly indepenadnt if the rank of the matrix equals the number of columns

#     column_matrix = np.column_stack(basis_states + psi0)
#
#     if np.linalg.matrix_rank()
#
#     print(psi_next)
#     print(psi_next.is_valid())



applied_hamiltonian = HeH_HAMILTONIAN()

my_start_state = "0011"

BASIS_SET(applied_hamiltonian, my_start_state)
