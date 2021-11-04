class RegManager:
    """
    Contains information about
    - What registers are available for use
    - What registers a variable maps to
    - What variable a register maps to
    """
    def __init__(self) -> None:
        self.scratchRegs = ["v1", "v2", "v3", "v4", "v5"]
        self.regToVar = {}
        self.varToReg = {}
        
    def getReg(self, var):
        if var in self.varToReg:
            return self.varToReg[var]
        
        reg = self.allocateReg()
        self.varToReg[var] = reg
        return reg

    def allocateReg(self):
        """
        Get next available scratch register. If none available, spill existing
        """
        if self.scratchRegs:
            reg = self.scratchRegs.pop(0)
            return reg

        #TODO spilling heuristic

