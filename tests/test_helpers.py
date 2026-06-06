import pytest

from posnet_connector._helpers import _calculate_crc, _create_frame, _format_value


class TestFormatValue:
    def test_float_formatting(self):
        assert _format_value(1.5) == "1,50"
        assert _format_value(0.99) == "0,99"

    def test_string_conversion(self):
        assert _format_value("test") == "test"


class TestCrcCalculation:
    def test_crc_checksum(self):
        # Test with known values
        result = _calculate_crc(b"rtcset\tda2006-10-20;11:49\t")
        assert isinstance(result, int)


class TestFrameCreation:
    def test_frame_structure(self):
        frame = _create_frame("test", {"param": "value"})
        assert frame.startswith(b"\x02")  # STX
        assert frame.endswith(b"\x03")  # ETX
        assert b"#" in frame  # CRC separator
