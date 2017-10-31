nProc = 13
        
        cantProcP1 = 6
        pcpP1 = 0
        mP1 = 4
        eP1 = 2
        q1 = (((pcpP1 * tPCP)/cantProcP1) + ((mP1 * tM)/cantProcP1) + ((eP1 * tE)/cantProcP1))/3
        
        cantProcP2 = 4
        pcpP2 = 1
        mP2 = 1
        eP2 = 2
        q2 = (((pcpP2 * tPCP)/cantProcP2) + ((mP2 * tM)/cantProcP2) + ((eP2 * tE)/cantProcP2))/3
        
        cantProcP3 = 3
        pcpP3 = 3
        mP3 = 0
        eP3 = 0
        q3 = (((pcpP3 * tPCP)/cantProcP3) + ((mP3 * tM)/cantProcP3) + ((eP3 * tE)/cantProcP3))/3

        tPCP = 25
        tM = 5
        tE = 12
        
        return (q1 + q2 + q3)/3
