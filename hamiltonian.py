from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper

driver = PySCFDriver(
    atom = "H 0 0 0; H 0 0 0.735",
    basis = "sto-3g",
    charge = 0,
    spin = 0,
)

problem = driver.run()

print("Number of molecular orbitals: ", problem.num_spatial_orbitals)
print("Number of particles:", problem.num_particles)
