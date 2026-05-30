from datetime import datetime
from typing import Optional

from ._communication import PosnetCommunicator


class PosnetPrinter(PosnetCommunicator):
    # List of all Posnet printer commands

    """Controlling sequences"""

    def set_datetime(self, timestamp: float) -> Optional[str]:
        datetime_formatted = datetime.fromtimestamp(timestamp).strftime(
            "%Y-%m-%d;%H:%M"
        )
        return self.send_command("rtcset", {"da": datetime_formatted})

    def get_datetime(self) -> Optional[datetime]:
        response = self.send_command("rtcget")
        if response is None:
            return None
        # e.g response: "rtcget\tda2006-10-20;11:49\t#CRC16"
        for part in response.split("\t"):
            if part.startswith("da"):
                return datetime.strptime(part[2:], "%Y-%m-%d;%H:%M")
        return None

    def set_vat(
        self,
        timestamp: float,
        va: Optional[float] = None,
        vb: Optional[float] = None,
        vc: Optional[float] = None,
        vd: Optional[float] = None,
        ve: Optional[float] = None,
        vf: Optional[float] = None,
        vg: Optional[float] = None,
    ) -> Optional[str]:
        params = {}

        for key, value in [
            ("va", va),
            ("vb", vb),
            ("vc", vc),
            ("vd", vd),
            ("ve", ve),
            ("vf", vf),
            ("vg", vg),
        ]:
            if value is not None:
                params[key] = f"{value:.2f}"

        datetime_formatted = datetime.fromtimestamp(timestamp).strftime(
            "%Y-%m-%d;%H:%M"
        )
        params["da"] = datetime_formatted

        return self.send_command("vatset", params)

    def get_vat(self) -> Optional[dict[str, float]]:
        response = self.send_command("vatget")
        if response is None:
            return None

        result = {}
        for part in response.split("\t"):
            for key in ("va", "vb", "vc", "vd", "ve", "vf", "vg"):
                if part.startswith(key):
                    value_str = part[2:].replace(",", ".")
                    result[key] = float(value_str)

        return result
