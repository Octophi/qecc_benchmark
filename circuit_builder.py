from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError

def buildCirc(qc, qr, cr, circuitArray, perm):
    for gate in circuitArray:
        lastGate = addGate(qc, qr, gate, perm)
    qc.measure(qr,cr)

def addGate(qc, qr, gate, perm):
    gateSet = {
        "X": addX,
        "Z": addZ,
        "H": addH,
        "P": addS,
        "CNOT": addCX,
        "CZ": addCZ,
        "Permute": permute
    }
    
    # convert gate string to gate array
    gateSpec = gate.split()
    
    # get appropriate function to add desired generators
    addGens = gateSet.get(gateSpec[0])
    if addGens == None:
        print("Some nonsense was ignored")
    else:
        addGens(qc, qr, gateSpec[1:],perm)
    if gateSpec[0] == "Permute":
        return 1
    else:
        return 0
    
def addX(qc, qr, gateNums,perm):
    for num in gateNums:
        qub = perm[int(num)]
        qc.x(qr[qub])
        
def addZ(qc, qr, gateNums,perm):
    for num in gateNums:
        qub = perm[int(num)]
        qc.z(qr[qub])

def addH(qc, qr, gateNums,perm):
    for num in gateNums:
        qub = perm[int(num)]
        qc.h(qr[qub])
        
def addS(qc, qr, gateNums,perm):
    for num in gateNums:
        qub = perm[int(num)]
        qc.s(qr[qub])
        
def addCX(qc, qr, gateNums,perm):
    qub1 = perm[int(gateNums[0])]
    qub2 = perm[int(gateNums[1])]
    qc.cx(qr[qub1], qr[qub2])
    
def addCZ(qc, qr, gateNums,perm):
    qub1 = perm[int(gateNums[0])]
    qub2 = perm[int(gateNums[1])]
    qc.cz(qr[qub1], qr[qub2])

def permute(qc, qr, gateOrder,perm):
    permCopy = perm.copy()
    for i in range(len(perm)):
        perm[i+1] = permCopy[int(gateOrder[i])]
