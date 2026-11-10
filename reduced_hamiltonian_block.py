

import numpy as np
from qiskit.quantum_info import Statevector

from hamiltonian import HeH_HAMILTONIAN


def REDUCED_HAMILTONIAN_BLOCK(hamiltonian, basis_low_to_high):

    matrix_from_hamiltonian = hamiltonian.to_matrix()
    dim_of_block = len(basis_low_to_high)
    # Consrtuct the Hamiltonian block
    hamiltonian_block = np.zeros((dim_of_block, dim_of_block), dtype="complex")
    for i, row in enumerate(basis_low_to_high):
        state_for_bra = Statevector.from_label(row).conjugate()
        bra = np.array(state_for_bra).T

        for j, col in enumerate(basis_low_to_high):
            state_for_ket = Statevector.from_label(col)
            ket = np.array(state_for_ket)
            entry = bra @ matrix_from_hamiltonian @ ket
            hamiltonian_block[i][j] = entry

    eigenvals, eigenvectors = np.linalg.eigh(hamiltonian_block)

    return eigenvals[0], eigenvectors[0]








# Qiskit ordering low to high
basis = ["0011", "1001", "0110", "1100"]
full_basis = [
    "0000",
    "0001",
    "0010",
    "0011",
    "0100",
    "0101",
    "0110",
    "0111",
    "1000",
    "1001",
    "1010",
    "1011",
    "1100",
    "1101",
    "1110",
    "1111"
]
myhamilt = HeH_HAMILTONIAN()
ground_state_energy, eigvec = REDUCED_HAMILTONIAN_BLOCK(myhamilt, basis)

eigenvals, eigenvectors = np.linalg.eigh(myhamilt)
print(eigenvals[0])


# Report amplitudes:
eigvec = np.real(eigvec)
print(f"\nGround State Energy: {ground_state_energy:.7}")
print(f"Eignevector: {eigvec[0]:.6}|0011> +{eigvec[1]:.6}|1001> {eigvec[2]:.5}|0110> +{eigvec[3]:.6}|1100>")


full_ground_state_energy, _ = REDUCED_HAMILTONIAN_BLOCK(myhamilt, full_basis)
print(f"Lowest Energy (Through Invalid States, Unreachable): {full_ground_state_energy:.7}\n")
