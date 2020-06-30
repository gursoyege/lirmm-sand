from common.imports import *

def clean():
    files = glob.glob(R_PATH + "/beg" + "/*")
    for f in files:
        os.remove(f)
    files = glob.glob(R_PATH + "/end" + "/*")
    for f in files:
        os.remove(f)

def run():
    r = np.zeros(IM_SIZE)
    for x in range(IM_SIZE[0]):
        for y in range(IM_SIZE[1]):
            r[x,y] = math.sqrt(1 + ((x-U0)/FX)**2 + ((y-V0)/FY)**2)
    
    posMeanBeg = findPosMean(XML_PATH + "/beg")
    posMeanEnd = findPosMean(XML_PATH + "/end")
    posMean = ((posMeanBeg + posMeanEnd)/2).astype(int)

    act = 1
    center = [0,0]
    for xml in sorted(glob.glob(XML_PATH + "/beg" + "/*.xml")):
        i = xml.rfind('/')
        if int(xml[i+1]) == act :
            a, name, pos = getXml(xml)

            center[0] = (pos[2] + pos[0])/2
            center[1] = (pos[3] + pos[1])/2

            pos[0] = center[0] - posMean[0]/2
            pos[2] = center[0] + posMean[0]/2

            pos[1] = center[1] - posMean[1]/2
            pos[3] = center[1] + posMean[1]/2

            r_act = r[int(pos[0]):int(pos[2]), int(pos[1]):int(pos[3])]

            np.save(R_PATH + "/beg/" + str(act) + ".npy", r_act)
            act += 1

    act = 1
    center = [0,0]
    for xml in sorted(glob.glob(XML_PATH + "/end" + "/*.xml")):
        i = xml.rfind('/')
        if int(xml[i+1]) == act :
            a, name, pos = getXml(xml)

            center[0] = (pos[2] + pos[0])/2
            center[1] = (pos[3] + pos[1])/2

            pos[0] = center[0] - posMean[0]/2
            pos[2] = center[0] + posMean[0]/2

            pos[1] = center[1] - posMean[1]/2
            pos[3] = center[1] + posMean[1]/2

            r_act = r[int(pos[0]):int(pos[2]), int(pos[1]):int(pos[3])]

            np.save(R_PATH + "/end/" + str(act) + ".npy", r_act)
            act += 1

