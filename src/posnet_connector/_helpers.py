from typing import Optional

from crc import Calculator, Configuration


# Calculate frame CRC checksum
def _calculate_crc(data: bytes) -> int:
    """
    The CRC used for communication with POSNET devices
    is described as CRC-16/XMODEM (Poly=0x1021, Init=0x0000).
    """
    config = Configuration(
        width=16,
        polynomial=0x1021,
        init_value=0x0000,
        final_xor_value=0x0000,
        reverse_input=False,
        reverse_output=False,
    )
    calculator = Calculator(config)
    return calculator.checksum(data)


def _format_value(value) -> str:
    if isinstance(value, float):
        return f"{value:.2f}".replace(".", ",")
    return str(value)


def _create_frame(
    command: str, parameters: Optional[dict] = None, encoding: str = "cp1250"
) -> bytes:
    STX, ETX = b"\x02", b"\x03"

    payload_parts = [command]
    if parameters:
        for param_id, param_value in parameters.items():
            payload_parts.append(f"{param_id}{_format_value(param_value)}")

    payload_string = "\t".join(payload_parts) + "\t"
    payload_bytes = payload_string.encode(encoding)
    checksum = _calculate_crc(payload_bytes)
    checksum_hex = f"{checksum:04X}"

    return b"".join([STX, payload_bytes, b"#", checksum_hex.encode(encoding), ETX])
