from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError

# This file contains all the encoding schemes we would like to implement.
# If a new scheme is needed, just ensure that the corresponding variables
# and methods are provided. The same prototype should be used for all
# schemes.

class Uncoded:
    # Defines number of qubits for code
    n = 2
    
    # Defines code space
    validOutputs = ["00", "01", "10", "11"]

    # Sets mapping of qubit numbering so that qubits numbered "1 to n" appear
    # in that order left to right
    perm = {}
    for i in range(n):
        perm[n-i] = i
        
    def prepareZeros(self,qc,qr):
        return
        
    def setInput(self,qc,qr,compiler):
        if compiler == 0:
            return
        elif compiler == 1:
            qc.x(qr[1])
        elif compiler == 2:
            qc.x(qr[0])
        elif compiler == 3:
            qc.x(qr)

class FourTwoTwo:
    # Defines number of qubits for code
    n = 4
    
    # Defines code space
    validOutputs = ["0000", "1111", "0101", "1010", "0011", "1100", "0110", "1001"]

    # Sets mapping of qubit numbering so that qubits numbered "1 to n" appear
    # in that order left to right
    perm = {}
    for i in range(n):
        perm[n-i] = i

    # prepare a state of all zeros
    def prepareZeros(self,qc,qr):
        qc.h(qr[1])
        qc.barrier()
        qc.cx(qr[1],qr[0])
        qc.barrier()
        qc.cx(qr[1],qr[2])
        qc.barrier()
        qc.cx(qr[2],qr[3])
        qc.barrier()
        
    def setInput(self, qc, qr, compiler):
        if compiler == 0: 
            return
        elif compiler == 1:
            qc.x(qr[0])
            qc.x(qr[2])
        elif compiler == 2:
            qc.x(qr[0])
            qc.x(qr[1])
        elif compiler == 3:
            qc.x(qr[2])
            qc.x(qr[1])
        qc.barrier()

class SixFourTwo:
    # Defines number of qubits for code
    n = 6
    
    # UNFINISHED
    # If we want to generalize the idea of valid outputs then we
    # eventually need heavier machinery, possibly integrated with matlab
    validOutputs = ["000000", "111111", "0101", "1010", "0011", "1100", "0110", "1001"]

    # Sets mapping of qubit numbering
    perm = {}
    for i in range(n):
        perm[n-i] = i

    # UNFINISHED
    def prepareZeros(self,qc,qr):
        qc.h(qr[1])
        qc.barrier()
        qc.cx(qr[1],qr[0])
        qc.barrier()
        qc.cx(qr[1],qr[2])
        qc.barrier()
        qc.cx(qr[2],qr[3])
        qc.barrier()

    # UNFINISHED
    def setInput(self, qc, qr, compiler):
        if compiler == 0: 
            return
        elif compiler == 1:
            qc.x(qr[0])
            qc.x(qr[2])
        elif compiler == 2:
            qc.x(qr[0])
            qc.x(qr[1])
        elif compiler == 3:
            qc.x(qr[2])
            qc.x(qr[1])
        qc.barrier()
    
