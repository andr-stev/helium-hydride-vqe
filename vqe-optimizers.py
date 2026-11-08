import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize

from givens_rotations import GivensRotations
from hamiltonian import HeH_HAMILTONIAN

my_helium_hydride_hamiltonian = HeH_HAMILTONIAN()
number_of_qubits_for_givens_ansatz = my_helium_hydride_hamiltonian.num_qubits


ansatz_circuit = QuantumCircuit(4)

ansatz_circuit.x(0)
ansatz_circuit.x(1)

theta = ParameterVector("theta", length = 3)

# TODO: Replace Givens ansatz with TwoLocal ansatz
givens_gate_1_theta_one = GivensRotations.G1_ROTATION(theta[0])
givens_gate_1_theta_two = GivensRotations.G1_ROTATION(theta[1])
givens_gate_2_theta_three = GivensRotations.G2_ROTATION(theta[2])

ansatz_circuit = ansatz_circuit.compose(givens_gate_1_theta_one, [0, 2])
ansatz_circuit = ansatz_circuit.compose(givens_gate_1_theta_two, [1, 3])
ansatz_circuit = ansatz_circuit.compose(givens_gate_2_theta_three, ansatz_circuit.qubits)

estimator = StatevectorEstimator()

def COST_FUNCTION(angles):
    "Calcualtes energy resulting from chosen angles"

    primitive_unified_block = (ansatz_circuit, my_helium_hydride_hamiltonian, angles)
    job = estimator.run([primitive_unified_block])

    result = job.result()

    energy = result[0].data.evs

    return float(energy)



# print(ansatz_circuit.draw("text"))

initial_angles = np.ones(ansatz_circuit.num_parameters)

print("optimize")

minization_res = minimize(COST_FUNCTION, initial_angles, method="SLSQP")


print("done")
print(f"Energy_0: {minization_res.fun:.6f}")
print(f"Optimal Angles: {minization_res.x}")
