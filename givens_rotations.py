from qiskit import QuantumCircuit
from qiskit.circuit import Gate

__all__ = ["G1_ROTATION", "G2_ROTATION"]


class GivensRotations:
    """Generate Givens rotation gates for quantum circuits.

    Givens rotations are elementary operations used in quantum algorithms
    to perform rotations in two-dimensional subspaces. These implementations
    use CNOT-based decompositions to create effective single-qubit rotations
    across multi-qubit systems.
    """

    @staticmethod
    def G1_ROTATION(angle: float) -> Gate:
        """Generate a G1 rotation gate for two qubits.

        This rotation acts on the first two qubits (q[0] and q[1]),
        performing a controlled rotation that affects the subspace
        spanned by these qubits.

        Args:
            angle: The rotation angle for the G1 operator.

        Returns:
            A parameterized QuantumCircuit gate representing the G1 rotation.
            The gate can be appended to a larger circuit using to_gate().

        Example:
            >>> from givens_rotations import GivensRotations
            >>> gate = GivensRotations.G1_ROTATION(0.5)
            >>> circuit = QuantumCircuit(2).append(gate)
        """
        circuit = QuantumCircuit(2)

        # Apply CNOT gate with q[0] as control, q[1] as target
        circuit.cx(0, 1)

        # Apply RZ rotation on q[1] with doubled angle
        # The factor of 2 accounts for the division by 2 in the Rz gate
        circuit.rz(2 * angle, 1)

        # Apply inverse CNOT to uncompute previous CNOT
        circuit.cx(0, 1)

        return circuit.to_gate()

    @staticmethod
    def G2_ROTATION(angle: float) -> Gate:
        """Generate a G2 rotation gate for four qubits.

        This rotation acts on the last two qubits of a four-qubit system
        (q[2] and q[3]), using a chain of CNOT gates to extend the
        rotation across the entangled subspace. The CNOT chain creates
        a path from q[0] to q[3] to isolate the rotation target.

        Args:
            angle: The rotation angle for the G2 operator.

        Returns:
            A parameterized QuantumCircuit gate representing the G2 rotation.
            The gate can be appended to a larger circuit using to_gate().

        Example:
            >>> from givens_rotations import GivensRotations
            >>> gate = GivensRotations.G2_ROTATION(0.5)
            >>> circuit = QuantumCircuit(4).append(gate)
        """
        circuit = QuantumCircuit(4)

        # Create CNOT chain: q[0] -> q[1] -> q[2] -> q[3]
        circuit.cx(0, 1)
        circuit.cx(1, 2)
        circuit.cx(2, 3)

        # Apply RZ rotation on q[3] with doubled angle
        # The factor of 2 accounts for the division by 2 in the Rz gate
        circuit.rz(2 * angle, 3)

        # Reverse CNOT chain to uncompute previous CNOT
        circuit.cx(2, 3)
        circuit.cx(1, 2)
        circuit.cx(0, 1)

        return circuit.to_gate()


# Backward compatibility aliases for direct function import
G1_ROTATION = GivensRotations.G1_ROTATION
G2_ROTATION = GivensRotations.G2_ROTATION
