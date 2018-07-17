from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError
from qiskit import available_backends, register, execute, get_backend


# This file contains all the encoding schemes we would like to implement.
# If a new scheme is needed, just ensure that the corresponding variables
# and methods are provided. The same prototype should be used for all
# schemes.


# Grabs quantum register k from qc
def getQReg(qc,k):   
    desired = list(qc.get_qregs().items())
    return desired[k][1]

# Grabs classical register k from qc
def getCReg(qc,k):   
    desired = list(qc.get_cregs().items())
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
        
    
    def prepareZeros(self,qc):
        return
        
    def setInput(self,qc,compiler):
        qr = getQReg(qc,0)
        
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
    def prepareZeros(self,qc):
        qr = getQReg(qc,0)
        
        qc.h(qr[1])
        qc.barrier()
        qc.cx(qr[1],qr[0])
        qc.barrier()
        qc.cx(qr[1],qr[2])
        qc.barrier()
        qc.cx(qr[2],qr[3])
        qc.barrier()
        
    def setInput(self, qc, compiler):
        qr = getQReg(qc,0)
        
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
        qr = getQReg(qc,0)
        
        anc = QuantumRegister(2)
        cr2 = ClassicalRegister(2)
        qc.add(anc)
        qc.add(cr2)
        
    def setInput(self, qc, compiler):
        qr = getQReg(qc,0)
        
        if compiler == 0: 
            return
        elif compiler == 1:
            qc.x(qr)
        else:
            print("Invalid compiler")
        qc.barrier()

    # Measure x from qubit a to target b
    def xMeas(self,qc,a,b):
        qr = getQReg(qc,0)
        anc = getQReg(qc,1)
        
        a = self.perm[a]
        b = self.ind[b]
        qc.h(qr[a])
        qc.cx(qr[a],anc[b])
        qc.h(qr[a])

    def zMeas(self,qc,a,b):
        qr = getQReg(qc,0)
        anc = getQReg(qc,1)
        
        a = self.perm[a]
        b = self.ind[b]
        qc.cx(qr[a],anc[b])

    # stab is stabilizer number, flag is boolean 
    def measure(self, qc, stab, flag):
        qr = getQReg(qc,0)
        anc = getQReg(qc,1)
        reg = getCReg(qc,1)
        
        qc.reset(anc)


        # stabilizer 0 is XZXXI
        if stab ==0:
            if flag:
                qc.h(anc[0])
            self.xMeas(qc,1,6)
            if flag:
                qc.cx(anc[0],anc[1])
            self.zMeas(qc,2,6)
            self.zMeas(qc,3,6)
            if flag:
                qc.cx(anc[0],anc[1])
            self.xMeas(qc,4,6)

            # Check syndrome
            qc.measure(anc[1],reg[0])

            # Check flag
            if flag:
                qc.h(anc[0])
                qc.measure(anc[0],reg[1])

            job = execute(qc,backend)
            result = job.result()
            data = result.get_counts()

            print(data)

            print("Synd: "+str(reg[0]))
            
            if flag:            
                print("Flag: "+str(reg[1]))



        
#    def correct(self, qc):
        

