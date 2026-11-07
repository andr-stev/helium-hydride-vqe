import numpy as np
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
qubit_op = mapper.map(problem.hamiltonian.second_q_op())

print(qubit_op)

pauli_strings = qubit_op.paulis # type: ignore
coeffs = qubit_op.coeffs # type: ignore

print(pauli_strings, coeffs)

# Collect terms with the same coefficient
collected_dict = {}
for i in range(len(coeffs)):
    collected_dict.setdefault(np.round(np.real(coeffs[i]), 6), []).append(str(pauli_strings[i]))

for key, values in collected_dict.items():
    print(key, values)
