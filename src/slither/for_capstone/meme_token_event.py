"""
    Module detecting dangerous strict equality
"""
from typing import Any, Dict, List, Union
from slither.analyses.data_dependency.data_dependency import is_dependent_ssa
from slither.core.declarations import Function
from slither.core.declarations.function_top_level import FunctionTopLevel
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import (
    Assignment,
    Binary,
    BinaryType,
    HighLevelCall,
    SolidityCall,
)

from slither.core.solidity_types import MappingType, ElementaryType

from slither.core.variables.state_variable import StateVariable
from slither.core.declarations.solidity_variables import (
    SolidityVariable,
    SolidityVariableComposed,
    SolidityFunction,
)
from slither.core.cfg.node import Node
from slither.core.declarations.contract import Contract
from slither.core.declarations.function_contract import FunctionContract
from slither.slithir.operations.operation import Operation
from slither.slithir.variables.constant import Constant
from slither.slithir.variables.local_variable import LocalIRVariable
from slither.slithir.variables.temporary_ssa import TemporaryVariableSSA
from slither.utils.output import Output
from slither.utils.type import is_underlying_type_address


class MemeTokenEvent(AbstractDetector):
    ARGUMENT = "meme-token-event"
    HELP = "Dangerous strict equalities"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = (
        ""
    )

    WIKI_TITLE = ""
    WIKI_DESCRIPTION = ""

    # region wiki_exploit_scenario
    WIKI_EXPLOIT_SCENARIO = """"""
    # endregion wiki_exploit_scenario

    WIKI_RECOMMENDATION = (
        """Don't use strict equality to determine if an account has enough Ether or tokens."""
    )
    
    def _detect(self) -> List[Output]:
        results = []

        li = ["Approval", "Transfer"]


        for c in self.compilation_unit.contracts_derived:
            chk = {}

            for l in li:
                chk[l] = False

            for f in c.functions:
                for n in f.nodes:
                    for ir in n.irs:
                        from slither.slithir.operations.event_call import EventCall 
                        if isinstance(ir, EventCall):
                            chk[ir.name] = True

            flag = True
            for l in li:
                if chk[l] == False:
                    flag = False
            tokens = ["ERC20", "IERC20"]
            for mk in c._inheritance:
                if mk.name in tokens:
                    if flag == False:
                        results.append(self.generate_result(self.compilation_unit.contracts_derived))
        return results
