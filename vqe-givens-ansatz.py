from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np

ansatz_circuit = QuantumCircuit(4)

ansatz_circuit.x(0)
ansatz_circuit.x(1)

print(ansatz_circuit.draw("text"))

angles = Parameter("theta",  length = 3)
parameter_counter = 0
