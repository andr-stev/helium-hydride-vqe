from qiskit.primitives import StatevectorEstimator
from qiskit_algorithms import VQE, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import SLSQP
from qiskit_nature.second_q.circuit.library import UCCSD, HartreeFock
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import InterleavedQubitMapper, JordanWignerMapper
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.algorithms import GroundStateEigensolver

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

numpy_solver = NumPyMinimumEigensolver()

ansatz = UCCSD(
    eigenstate_problem.num_spatial_orbitals,
    eigenstate_problem.num_particles,
    interleaved_mapper,
    initial_state=HartreeFock(
        eigenstate_problem.num_spatial_orbitals,
        eigenstate_problem.num_particles,
        interleaved_mapper,

    )
)

vqe_solver = VQE(StatevectorEstimator(), ansatz, SLSQP())
vqe_solver.initial_point = [0.0] * ansatz.num_parameters


calculation = GroundStateEigensolver(interleaved_mapper, vqe_solver)

result = calculation.solve(eigenstate_problem)
# print(result)
gnd_state_energy = result.total_energies[0]
corres_eigenvec = result.groundstate

# tester_thing = result.eigenvalues
# print(tester_thing)

print(result, "\n")
print(gnd_state_energy, "\n")

# print(corres_eigenvec)
