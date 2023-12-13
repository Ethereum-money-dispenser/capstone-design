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


class MemeTokenProxy(AbstractDetector):
    ARGUMENT = "meme-token-proxy"
    HELP = "meme-token-proxy"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = (
        "meme-token-proxy"
    )

    WIKI_TITLE = "meme-token-proxy"
    WIKI_DESCRIPTION = "meme-token-proxy"

    # region wiki_exploit_scenario
    WIKI_EXPLOIT_SCENARIO = """meme-token-proxy"""
    # endregion wiki_exploit_scenario

    WIKI_RECOMMENDATION = (
        """meme-token-proxy"""
    )



    def detect_etherscan(self, url):
        # url = "https://etherscan.io/address/0xf513b5b70e1f337f54109b02e1dccb530e7cdd8a#readProxyContract"

        headers = {
            'authority': url,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            # 'cookie': 'cf_chl_2=edfd14a2d84d079; ASP.NET_SessionId=kjpq1f4rdhzhai0zhipke0kx; __cflb=0H28vyb6xVveKGjdV3CYUMgiti5JgVrXJ3a3tvdA5gQ; _ga_PQY6J2Q8EP=GS1.1.1698690464.1.0.1698690464.0.0.0; _ga=GA1.1.811380323.1698690464; bscscan_offset_datetime=+9; cf_clearance=kwjpev5x7QLJOOWjzERj6PB9CxyRmYDU_cIBli_7GCs-1698690466-0-1-e7f913a3.5436c44a.2e107480-150.2.1698690466',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }

        # cf_clearance = cf_clearance_set[url]
        # print(cf_clearance)
        cookies = {
            'cf_chl_2': 'edfd14a2d84d079',
            'ASP.NET_SessionId': 'kjpq1f4rdhzhai0zhipke0kx',
            '__cflb': '0H28vyb6xVveKGjdV3CYUMgiti5JgVrXJ3a3tvdA5gQ',
            '_ga_PQY6J2Q8EP': 'GS1.1.1698690464.1.0.1698690464.0.0.0',
            '_ga': 'GA1.1.811380323.1698690464',
            'bscscan_offset_datetime': '+9',
            'cf_clearance': '3WudC1SF47ycVxxnldrwGM1g615v4SvjIkm0fXAge0A-1698724809-0-1-e7f913a3.5436c44a.2e107480-150.2.1698724809',
        }     
        import requests
        response = requests.get(url, headers=headers, cookies=cookies).content

        return b"for the implementation contract" in response

    def _detect(self) -> List[Output]:
        results = []
        flag = False
        filename = self.slither._filename.split(":")

        if len(filename) == 2:
            net = filename[0]
            addr = filename[1]
            NET = {
                "mainet": "etherscan.io",
                "ftm": "ftmscan.com",
                "arbi": "arbiscan.io"
            }
            url = "https://" + NET[net] + "/address/" + addr + "#readProxyContract"
            flag = self.detect_etherscan(url)
            if flag == True:
                results.append(self.generate_result(self.compilation_unit.contracts_derived))
                return results

        return results
