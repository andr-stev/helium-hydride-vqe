import matplotlib.pyplot as plt
import numpy as np
from numpy._core import identity
from qiskit.circuit import Parameter, QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import Pauli, SparsePauliOp
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper


# Build the qubit Hamiltonian for helium hydride (HeH+)
driver = PySCFDriver(
    atom="He 0 0 0; H 0 0 0.772",  # HeH+ molecule
    basis="sto3g",
    charge=1,  # HeH+ has a +1 charge
    spin=0,
)

problem = driver.run()

# Apply Jordan-Wigner mapping with interleaved ordering
# interleaved=True enables Z2 symmetry and uses interleaved Pauli-Z operators
mapper = JordanWignerMapper()

# Convert to qubit operator (qubit Hamiltonian)
heh_electronic_hamiltonian = mapper.map(problem.hamiltonian.second_q_op())
number_of_qubits = heh_electronic_hamiltonian.num_qubits

identity_pauli_string = "I" * number_of_qubits
nuclear_repulsion = 1.370925
nuclear_op = SparsePauliOp([identity_pauli_string], nuclear_repulsion)

helium_hydride_hamiltonian = (heh_electronic_hamiltonian + nuclear_op).simplify()
# helium_hydride_hamiltonian.simplify()

print(helium_hydride_hamiltonian)


#
# number_of_qubits = heh_electronic_hamiltonian.num_qubits
#
#
# collected_dict_2 = dict(heh_electronic_hamiltonian.to_list())
#
#
# identity_pauli_string = "I" * number_of_qubits
# e_nuc = 1.370925
#
# if identity_pauli_string in collected_dict_2:
#     collected_dict_2[identity_pauli_string] += e_nuc
# else:
#     collected_dict_2[identity_pauli_string] = e_nuc
#
# helium_hydride_hamiltionian = SparsePauliOp.from_list(list(collected_dict_2.items()))
#
# print(helium_hydride_hamiltionian)
