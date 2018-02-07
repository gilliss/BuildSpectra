"""
A class to facilitate combination of sim results
"""

import numpy as np

class BSCombine():
        """
        A class to facilitate combination of sim results
        """
        def __init__(self, weightFunc, bscv, bscd):
            self.weightFunc = weightFunc
            self.bscv = bscv
            self.bscd = bscd

            self.cut = None
            self.configuration = None
            self.detector = None
            self.decayChain = None
            self.segment = None
            self.branchingRatio = None
            self.hardwareComponent = None
            self.hardwareGroup = None

            self.combinedData = np.zeros(10000)
            return None

        def UpdateSelfCurrentVars(self):
            cvDict = self.bscv.GetCurrentVarsDict()
            self.cut = cvDict['cut']
            self.configuration = cvDict['configuration']
            self.detector = cvDict['detector']
            self.decayChain = cvDict['decayChain']
            self.segment = cvDict['segment']
            self.branchingRatio = cvDict['branchingRatio']
            self.hardwareComponent = cvDict['hardwareComponent']
            self.hardwareGroup = cvDict['hardwareGroup']

        def Add(self, data):
            """
            Add 'obj' to 'into' according to weight expressed in 'comboRule'
            """
            weight = self.GetWeight(self.weightFunc)
            print('  Adding hist with weight ' + self.weightFunc + ' = ' + str(weight))
            self.combinedData = self.combinedData + data*weight
            return None

        def GetCombinedData(self):
            return self.combinedData

        def GetWeight(self, weightFunc):
            self.UpdateSelfCurrentVars()

            if weightFunc == 'One':
                return 1

            if weightFunc == 'BranchingRatio':
                return self.branchingRatio

            if weightFunc == 'TotalMass':
                activeDetectorMassList = []
                for i in range(len(self.bscd.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
                    if self.bscd.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1:
                        activeDetectorMassList.append(self.bscd.GetDetectorMassList()[i])
                return 1/np.sum(activeDetectorMassList)
