from common.imports import *

def clean():
    files = glob.glob(R_PATH + "/beg" + "/*")
    for f in files:
        os.remove(f)
    files = glob.glob(R_PATH + "/end" + "/*")
    for f in files:
        os.remove(f)

def run():
    r = np.zeros((IM_SIZE[1],IM_SIZE[0], 1))
    for y in range(IM_SIZE[1]):
        for x in range(IM_SIZE[0]):
            r[y,x,0] = math.sqrt(1 + ((x-U0)/FX)**2 + ((y-V0)/FY)**2)

    posMeanBeg = findPosMean(XML_PATH + "/beg")
    posMeanEnd = findPosMean(XML_PATH + "/end")
    posMean = ((posMeanBeg + posMeanEnd)/2).astype(int)

    act_1 = 1
    act_2 = 10
    center = [0,0]
    for xml in sorted(glob.glob(XML_PATH + "/beg" + "/*.xml")):
        i = xml.rfind('/')
        if xml[i+1:i+3].isnumeric() == True:
            if xml[i+1:i+3] == str(act_2):
                a, name, pos = getXml(xml)

                center[0] = (pos[2] + pos[0])/2
                center[1] = (pos[3] + pos[1])/2

                pos[0] = center[0] - posMean[0]/2
                pos[2] = center[0] + posMean[0]/2

                pos[1] = center[1] - posMean[1]/2
                pos[3] = center[1] + posMean[1]/2
            
                while pos[0]<0:
                    pos[0] += 1
                    pos[2] += 1
                while pos[1]<0:
                    pos[1] += 1
                    pos[3] += 1
                while pos[2]>IM_SIZE[0]:
                    pos[0] -= 1
                    pos[2] -= 1
                while pos[3]>IM_SIZE[1]:
                    pos[1] -= 1
                    pos[3] -= 1

                r_act = r[int(pos[1]):int(pos[3]),int(pos[0]):int(pos[2]),:]
                np.save(R_PATH + "/beg/" + str(act_2) + ".npy", r_act)
                act_2 += 1

        elif xml[i+1] == str(act_1):
            a, name, pos = getXml(xml)

            center[0] = (pos[2] + pos[0])/2
            center[1] = (pos[3] + pos[1])/2

            pos[0] = center[0] - posMean[0]/2
            pos[2] = center[0] + posMean[0]/2

            pos[1] = center[1] - posMean[1]/2
            pos[3] = center[1] + posMean[1]/2
        
            while pos[0]<0:
                pos[0] += 1
                pos[2] += 1
            while pos[1]<0:
                pos[1] += 1
                pos[3] += 1
            while pos[2]>IM_SIZE[0]:
                pos[0] -= 1
                pos[2] -= 1
            while pos[3]>IM_SIZE[1]:
                pos[1] -= 1
                pos[3] -= 1

            r_act = r[int(pos[1]):int(pos[3]),int(pos[0]):int(pos[2]),:]
            np.save(R_PATH + "/beg/" + str(act_1) + ".npy", r_act)
            act_1 += 1

    act_1 = 1
    act_2 = 10
    center = [0,0]
    for xml in sorted(glob.glob(XML_PATH + "/end" + "/*.xml")):
        i = xml.rfind('/')
        if xml[i+1:i+3].isnumeric() == True:
            if xml[i+1:i+3] == str(act_2):
                a, name, pos = getXml(xml)

                center[0] = (pos[2] + pos[0])/2
                center[1] = (pos[3] + pos[1])/2

                pos[0] = center[0] - posMean[0]/2
                pos[2] = center[0] + posMean[0]/2

                pos[1] = center[1] - posMean[1]/2
                pos[3] = center[1] + posMean[1]/2
            
                while pos[0]<0:
                    pos[0] += 1
                    pos[2] += 1
                while pos[1]<0:
                    pos[1] += 1
                    pos[3] += 1
                while pos[2]>IM_SIZE[0]:
                    pos[0] -= 1
                    pos[2] -= 1
                while pos[3]>IM_SIZE[1]:
                    pos[1] -= 1
                    pos[3] -= 1

                r_act = r[int(pos[1]):int(pos[3]),int(pos[0]):int(pos[2]),:]
                np.save(R_PATH + "/end/" + str(act_2) + ".npy", r_act)
                act_2 += 1

        elif xml[i+1] == str(act_1):
            a, name, pos = getXml(xml)

            center[0] = (pos[2] + pos[0])/2
            center[1] = (pos[3] + pos[1])/2

            pos[0] = center[0] - posMean[0]/2
            pos[2] = center[0] + posMean[0]/2

            pos[1] = center[1] - posMean[1]/2
            pos[3] = center[1] + posMean[1]/2
        
            while pos[0]<0:
                pos[0] += 1
                pos[2] += 1
            while pos[1]<0:
                pos[1] += 1
                pos[3] += 1
            while pos[2]>IM_SIZE[0]:
                pos[0] -= 1
                pos[2] -= 1
            while pos[3]>IM_SIZE[1]:
                pos[1] -= 1
                pos[3] -= 1

            r_act = r[int(pos[1]):int(pos[3]),int(pos[0]):int(pos[2]),:]
            np.save(R_PATH + "/end/" + str(act_1) + ".npy", r_act)
            act_1 += 1

