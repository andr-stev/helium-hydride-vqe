# from qiskit.circuit.library.n_local import TwoLocal
#
# from qiskit.circuit.library import TwoLocal

import warnings

from qiskit.circuit.library import n_local
from qiskit.primitives import StatevectorEstimator
from qiskit_algorithms import VQE, AdaptVQE, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA, L_BFGS_B, SPSA
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_nature.second_q.circuit.library import UCCSD, HartreeFock
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import InterleavedQubitMapper, JordanWignerMapper
from qiskit_nature.units import DistanceUnit

warnings.filterwarnings("ignore", message="Unknown solver options: iprint")

driver = PySCFDriver(
    atom="He 0 0 0; H 0 0 0.772",  # HeH+ molecule
    basis="sto3g",
    charge=1,  # HeH+ has a +1 charge
    spin=0,
    unit = DistanceUnit.ANGSTROM,

)

eigenstate_problem = driver.run()

mapper = JordanWignerMapper()
interleaved_mapper = InterleavedQubitMapper(mapper)

qubit_operator = interleaved_mapper.map(eigenstate_problem.hamiltonian.second_q_op())
qubits_needed = qubit_operator.num_qubits

numpy_solver = NumPyMinimumEigensolver()

# ansatz = UCCSD(
#     eigenstate_problem.num_spatial_orbitals,
#     eigenstate_problem.num_particles,
#     interleaved_mapper,
#     initial_state=HartreeFock(
#         eigenstate_problem.num_spatial_orbitals,
#         eigenstate_problem.num_particles,
#         interleaved_mapper,
#
#     )
# )

# two_local_circuit = TwoLocal(
#     rotation_blocks = ["ry"],
#     entanglement_blocks = "cx",
#     entanglement = "full",
#     reps = 1,
#     parameter_prefix = "y",
# )

# COBYLA
print("\nOptimizer: COBYLA")
for r in range(1,4):
    two_local_circuit = n_local(
        num_qubits = qubits_needed,
        rotation_blocks = ["ry"],
        entanglement_blocks = ["cx"],
        entanglement = "full",
        reps = r,
        parameter_prefix = "y",
    )

    another_solver = VQE(StatevectorEstimator(), two_local_circuit, COBYLA())


    calculation = GroundStateEigensolver(interleaved_mapper, another_solver)

    result = calculation.solve(eigenstate_problem)
    ground_state_energy = result.total_energies[0]

    print(f"    Reps: {r}, Ground State Energy: {ground_state_energy:.7}")

print("\nOptimizer: L-BFGS-B")
for r in range(1,4):
    two_local_circuit = n_local(
        num_qubits = qubits_needed,
        rotation_blocks = ["ry"],
        entanglement_blocks = ["cx"],
        entanglement = "full",
        reps = r,
        parameter_prefix = "y",
    )

    another_solver = VQE(StatevectorEstimator(), two_local_circuit, L_BFGS_B())


    calculation = GroundStateEigensolver(interleaved_mapper, another_solver)

    result = calculation.solve(eigenstate_problem)
    ground_state_energy = result.total_energies[0]

    print(f"    Reps: {r}, Ground State Energy: {ground_state_energy:.7}")

print("\nOptimizer: SPSA")
for r in range(1,4):
    two_local_circuit = n_local(
        num_qubits = qubits_needed,
        rotation_blocks = ["ry"],
        entanglement_blocks = ["cx"],
        entanglement = "full",
        reps = r,
        parameter_prefix = "y",
    )

    another_solver = VQE(StatevectorEstimator(), two_local_circuit, SPSA())


    calculation = GroundStateEigensolver(interleaved_mapper, another_solver)

    result = calculation.solve(eigenstate_problem)
    ground_state_energy = result.total_energies[0]

    print(f"    Reps: {r}, Ground State Energy: {ground_state_energy:.7}")

print("\n")
