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


class MemeTokenBurnable(AbstractDetector):
    ARGUMENT = "meme-token-burnable"
    HELP = "meme-token-burnable"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = (
        "meme-token-burnable"
    )

    WIKI_TITLE = "meme-token-burnable"
    WIKI_DESCRIPTION = "meme-token-burnable"

    # region wiki_exploit_scenario
    WIKI_EXPLOIT_SCENARIO = """meme-token-burnable"""
    # endregion wiki_exploit_scenario

    WIKI_RECOMMENDATION = (
        """meme-token-burnable"""
    )

    def detect_burn(self, contract: Contract) -> List[FunctionContract]:
        result = []
        names = ["burn"]
        for f in contract.functions:
            if any(name in f.canonical_name for name in names):
                if any(name in f.visibility for name in ['external', 'public']):
                    result.append(f)
        return result

    def _detect(self) -> List[Output]:
        results = []

        for c in self.compilation_unit.contracts_derived:
            results.append(self.generate_result(self.detect_burn(c)))

        return results
