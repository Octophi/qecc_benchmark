from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError


# This file contains all the encoding schemes we would like to implement.
# If a new scheme is needed, just ensure that the corresponding variables
# and methods are provided. The same prototype should be used for all
# schemes.


# Grabs quantum register k from qc
def getReg(qc,k):   
    desired = list(qc.get_qregs().items())
    return desired[k][1]    

class Uncoded:
    # Defines number of qubits for code
    n = 2
    
    # Defines code space
    validOutputs = ["00", "01", "10", "11"]

    # Sets mapping of qubit numbering so that qubits numbered "1 to n" appear
    # in that order left to right
    perm = {}

    def setPerm(self):
        n = self.n
        for i in range(n):
            self.perm[n-i] = i
        
    
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

    def setPerm(self):
        n = self.n
        for i in range(n):
            self.perm[n-i] = i

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

class FiveOneThree:
    # Number of qubits
    n = 5
    
    # Defines code space
    validOutputs = ["00000", "10010", "01001", "10100", "01010", "11011", "00110",
                    "11000", "11101", "00011", "11110", "01111", "10001", "01100",
                    "10111", "00101", "11111", "01101", "10110", "01011", "10101",
                    "00100", "11001", "00111", "00010", "11100", "00001", "10000",
                    "01110", "10011", "01000", "11010"]

    # Read things left to right
    ind = {6:1, 7:0}
    
    # Sets mapping of qubit numbering so that qubits numbered "1 to n" appear
    # in that order left to right
    perm = {}
    
    def setPerm(self):
        n = self.n
        for i in range(n):
            self.perm[n-i] = i

    
    # prepare a state of all zeros
    def prepareZeros(self,qc):
        #FILL ME IN
        # First time we add error correction
        # 2 ancilla qubits used to check
        qr = getReg(qc,0)
        
        anc = QuantumRegister(2)
        cr2 = ClassicalRegister(2)
        qc.add(anc)
        qc.add(cr2)
        qc.reset(anc)
        
    def setInput(self, qc, qr, compiler):
        if compiler == 0: 
            return
        elif compiler == 1:
            qc.x(qr)
        else:
            print("Invalid compiler")
        qc.barrier()

    # Measure x from qubit a to target b
    def xMeas(self,qc,qr,anc,a,b):
        a = perm[a]
        b = ind[b]
        qc.h(qr[a])
        qc.cx(qr[a],anc[b])
        qc.h(qr[a])

    def zMeas(self,qc,qr,anc,a,b):
        a = perm[a]
        b = ind[b]
        qc.cx(qr[a],anc[b])

    # stab is stabilizer number, flag is boolean 
    def measure(self, qc, stab, flag):
        qr = getReg(qc,0)
        anc = getReg(qc,1)
        qc.reset(anc)

        # stabilizer 0 is XZXXI
        if stab ==0:
            if flag:
                qc.h(anc[0])
            self.xMeas(self,qc,qr,1,6)
            if flag:
                qc.cx(anc[0],anc[1])
            self.zMeas(self,qc,qr,2,6)
            self.zMeas(self,qc,qr,3,6)
            if flag:
                qc.cx(anc[0],anc[1])
            self.xMeas(self,qc,qr,4,6)
            # Check syndrome
            qc.measure(anc[1],cr[0])

            # Check flag
            qc.h(anc[0])
            qc.measure(anc[0],cr[1])

            print("Synd: "+cr[0])
            print("Flag: "+cr[1])

        # stabilizer 1 is IXZZX
        if stab ==1:
            if flag:
                qc.h(anc[0])
            self.xMeas(self,qc,qr,1,6)
            if flag:
                qc.cx(anc[0],anc[1])
            self.zMeas(self,qc,qr,2,6)
            self.zMeas(self,qc,qr,3,6)
            if flag:
                qc.cx(anc[0],anc[1])
            self.xMeas(self,qc,qr,4,6)
            # Check if it's a zero or a one
            qc.measure(anc[1],cr[0])
            qc.measure(anc[0],cr[1])

        # stabilizer 2 is XIXZZ
        if stab ==0:
            if flag:
                qc.h(anc[0])
            self.xMeas(self,qc,qr,1,6)
            if flag:
                qc.cx(anc[0],anc[1])
            self.zMeas(self,qc,qr,2,6)
            self.zMeas(self,qc,qr,3,6)
            if flag:
                qc.cx(anc[0],anc[1])
            self.xMeas(self,qc,qr,4,6)
            # Check if it's a zero or a one
            qc.measure(anc[1],cr[0])
            qc.measure(anc[0],cr[1])

        # stabilizer 3 is ZXIXZ
        if stab ==0:
            if flag:
                qc.h(anc[0])
            self.xMeas(self,qc,qr,1,6)
            if flag:
                qc.cx(anc[0],anc[1])
            self.zMeas(self,qc,qr,2,6)
            self.zMeas(self,qc,qr,3,6)
            if flag:
                qc.cx(anc[0],anc[1])
            self.xMeas(self,qc,qr,4,6)
            # Check if it's a zero or a one
            qc.measure(anc[1],cr[0])
            qc.measure(anc[0],cr[1])

        
#    def correct(self, qc, qr):
        

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
    
