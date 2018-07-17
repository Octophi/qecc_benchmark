from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError

# Grabs quantum register k from qc
def getQReg(qc,k):   
    desired = list(qc.get_qregs().items())
    return desired[k][1]

def buildCirc(qc, circuitArray, perm):
    qr = getQReg(qc,0)
    n = len(perm)

    firstPerm = {}
    for i in range(n):
            firstPerm[n-i] = i
    for gate in circuitArray:
        addGate(qc, gate, perm)
    qc.barrier()

    registerPerm = {}
    for i in perm.keys():
        registerPerm[firstPerm[i]] = perm[i]

    return registerPerm



def addGate(qc, gate, perm):
    qr = getQReg(qc,0)
    gateSet = {
        "X": addX,
        "Y": addY,
        "Z": addZ,
        "H": addH,
        "P": addS,
        "CNOT": addCX,
        "CX": addCX,
        "CZ": addCZ,
        "Permute": permute
    }
    
    # convert gate string to gate array
    gateSpec = gate.split()
    
    # get appropriate function to add desired generators
    addGens = gateSet.get(gateSpec[0])
    if addGens is None:
        print("Some nonsense was ignored")
    else:
        addGens(qc, gateSpec[1:],perm)
    
    
def addX(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    for num in gateNums:
        qub = perm[int(num)]
        qc.x(qr[qub])

def addY(qc, gateNums,perm):
    qr = getQReg(qc,0)

    for num in gateNums:
        qub = perm[int(num)]
        qc.y(qr[qub])
        
def addZ(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    for num in gateNums:
        qub = perm[int(num)]
        qc.z(qr[qub])

def addH(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    for num in gateNums:
        qub = perm[int(num)]
        qc.h(qr[qub])
        
def addS(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    for num in gateNums:
        qub = perm[int(num)]
        qc.s(qr[qub])
        
def addCX(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    qub1 = perm[int(gateNums[0])]
    qub2 = perm[int(gateNums[1])]
    qc.cx(qr[qub1], qr[qub2])
    
def addCZ(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    qub1 = perm[int(gateNums[0])]
    qub2 = perm[int(gateNums[1])]
    qc.cz(qr[qub1], qr[qub2])

def permute(qc, gateOrder,perm):
    n = len(perm)
    permCopy = perm.copy()
    for i in range(n):
        perm[i+1] = permCopy[int(gateOrder[i])]
    print(perm)

