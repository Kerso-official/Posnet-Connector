from datetime import datetime
from typing import Optional

from ._communication import PosnetCommunicator


class PosnetPrinter(PosnetCommunicator):
    # List of all Posnet printer commands

    # Custom command support
    def custom(self, command: str, params: Optional[dict] = None) -> Optional[str]:
        """
        Sends custom command to the printer.

        Args:
            command: command that will be sent to the printer
            params: (optional) parameters for the command
        """
        return self.send_command(command, params)

    # Controlling sequences

    def set_datetime(self, timestamp: float) -> Optional[str]:
        """
        Sets date and time on printer.

        Args:
            timestamp: timestamp from datetime module
        """
        datetime_formatted = datetime.fromtimestamp(timestamp).strftime(
            "%Y-%m-%d;%H:%M"
        )
        return self.send_command("rtcset", {"da": datetime_formatted})

    def get_datetime(self) -> Optional[datetime]:
        """
        Gets date and time from printer.
        """
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
        """
        Sets vat rates on printer

        Args:
            timestamp: timestamp from datetime module
            va: Optional A VAT tax rate
            vb: Optional B VAT tax rate
            vc: Optional C VAT tax rate
            vd: Optional D VAT tax rate
            ve: Optional E VAT tax rate
            vf: Optional F VAT tax rate
            vg: Optional G VAT tax rate
        """
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
                params[key] = value

        datetime_formatted = datetime.fromtimestamp(timestamp).strftime(
            "%Y-%m-%d;%H:%M"
        )
        params["da"] = datetime_formatted

        return self.send_command("vatset", params)

    def get_vat(self) -> Optional[dict[str, float]]:
        """
        Gets VAT tax rates
        """
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

    def set_header(self, lines: list[str]) -> Optional[str]:
        """
        Sets the printer header.

        Each line can contain formatting characters:
        &b - bold, &c - center, &h - tall, &u - underline, &w - wide
        Use && to print literal '&'.
        Max 500 characters total, max 40 chars per line (20 for wide).

        Example:
            set_header(["&cSklep spożywczy", "&c&bKONFITURA"])
        """
        tx = "\n".join(lines)
        return self.send_command("hdrset", {"tx": tx})

    def get_header(self) -> Optional[list[str]]:
        response = self.send_command("hdrget")
        if response is None:
            return None
        for part in response.split("\t"):
            if part.startswith("tx"):
                return part[2:].split("\n")
        return None

    def set_footer(self, lines: list[str], all_receipts: bool = False) -> Optional[str]:
        """
        Sets the printer footer (informational lines).

        Args:
            lines: Up to 3 lines. Each line can contain formatting characters:
                   &b - bold, &c - center, &h - tall, &u - underline, &w - wide
                   Use && to print literal '&'. Max 40 chars per line.
            all_receipts: False - only next receipt, True - all receipts.
        """
        params = {
            "tx": "\n".join(lines),
            "lb": "1" if all_receipts else "0",
        }
        return self.send_command("ftrinfoset", params)

    def get_footer(self) -> Optional[list[str]]:
        """
        Gets the footer.
        """
        response = self.send_command("ftrinfoget")
        if response is None:
            return None
        for part in response.split("\t"):
            if part.startswith("tx"):
                return part[2:].split("\n")
        return None

    def fiscalize(self, nip: str) -> Optional[str]:
        """
        Fiscalizes the connected printer.

        Args:
            nip: tax payer id number in this format:
                 xxx-xxx-xx-xx
        """
        return self.send_command("fiscalize", {"ni": nip})

    def authorize(self, auth_code: str) -> Optional[str]:
        """
        Authorizes fiscal printer.

        Args:
            auth_code: authorization code (length: 17)
        """
        return self.send_command("auth", {"co": auth_code})

    def next_maintenance(self, description: str, date: str) -> Optional[str]:
        """
        Sets next maintenance date with description.

        Args:
            description: description of next maintenance (length: 30)
            date: date of the next maintenance, format:
                  yyyy-mm-dd
        """
        return self.send_command("maintenance", {"te": description, "da": date})

    def open_drawer(self) -> Optional[str]:
        """
        Opens drawer that is connected to printer.
        """
        return self.send_command("opendrwr")

    def paper_feed(self, lines: int) -> Optional[str]:
        """
        Feeding paper with the specified number of lines.

        Args:
            lines: number of lines that will be fed (max. number of lines: 20)
        """
        return self.send_command("papfeed", {"ln": lines})

    def print_config(self, state: bool) -> Optional[str]:
        """
        Configures the print.

        Args:
            state: if true - non-fiscal prints on copy and on original,
                   if false - non-fiscal prints only on copy
        """
        return self.send_command("prncfgset", {"nf": state})

    def paper_save_config(self, state: bool) -> Optional[str]:
        """
        Configures paper save state.

        Args:
            state: if true - paper save turned on,
                   if false - paper save turned off
        """
        return self.send_command("papersavecfg", {"ps": state})
