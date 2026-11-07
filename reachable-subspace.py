import numpy as np

from hamiltonian import HeH_HAMILTONIAN
from qiskit.quantum_info import SparsePauliOp, Operator, Statevector


def BASIS_SET(hamiltonian, starting_state):

    hamiltonian_operator = hamiltonian.to_operator()
    psi0 = Statevector.from_label(starting_state)

    basis_states = [psi0]


    evolved_state = psi0.evolve(hamiltonian_operator)
    psi_next = evolved_state / np.linalg.norm(evolved_state)


    print(psi_next)
    print(psi_next.is_valid())



applied_hamiltonian = HeH_HAMILTONIAN()

my_start_state = "0011"

BASIS_SET(applied_hamiltonian, my_start_state)
