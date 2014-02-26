import PyTestObjects
import binascii

if __name__ == "__main__":
    print "Main Program"
    intObj = 4
    pbarr = PyTestObjects.LongAsByteArray(intObj)
    print "ByteArray Length : ", len(pbarr)
    base64String = binascii.b2a_base64(pbarr)
    print "base64String : ", base64String
    print "String Length : ", len(base64String)
    binString = bytearray( binascii.a2b_base64( base64String ) )
    print "ByteArray Length : ", len(binString)
    retIntObj = PyTestObjects.ByteArrayAsLong( binString )
    print "Returned Long : ", retIntObj

    print "Input Var : ", intObj
    pbarr = PyTestObjects.VarAsByteArray(intObj, "l")
    retIntObj = PyTestObjects.ByteArrayAsVar(pbarr, "l")
    print "Var : ", retIntObj

    print "Input Var : ", intObj
    pbarr = PyTestObjects.VarAsByteArray(intObj, "i")
    retIntObj = PyTestObjects.ByteArrayAsVar(pbarr, "i")
    print "Var : ", retIntObj

    print "Input Var : ", intObj
    pbarr = PyTestObjects.VarAsByteArray(intObj, "I")
    retIntObj = PyTestObjects.ByteArrayAsVar(pbarr, "I")
    print "Var : ", retIntObj

    print "Input Var : ", intObj
    pbarr = PyTestObjects.VarAsByteArray(intObj, "k")
    retIntObj = PyTestObjects.ByteArrayAsVar(pbarr, "k")
    print "Var : ", retIntObj

    floatObj = 1.5
    print "Input Var : ", floatObj
    pbarr = PyTestObjects.VarAsByteArray(floatObj, "f")
    retfloatObj = PyTestObjects.ByteArrayAsVar(pbarr, "f")
    print "Var : ", retfloatObj

    print "Input Var : ", floatObj
    pbarr = PyTestObjects.VarAsByteArray(floatObj, "d")
    retfloatObj = PyTestObjects.ByteArrayAsVar(pbarr, "d")
    print "Var : ", retfloatObj


