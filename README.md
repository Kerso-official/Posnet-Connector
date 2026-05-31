
# Posnet Connector

A python lib that allows to easily communicate with POSNET printers

> [!NOTE]
> Note that this project is in development, most of the functions aren't implemented yet and because of that the package isn't available on PyPi yet

> [!CAUTION]
> This package don't support online posnet printer actions (e.g. e-paragon).
> If you have access to newer protocol documentation you can use function `PosnetPrinter.custom(command, params)` to communicate with the printer.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)


## Features

- Control sequences (Partially implemented)
- Report printing (Not implemented)
- Non-fiscal prints (Not implemented)
- Database control (Not implemented)
- Transactions (Not implemented)
- Discounts and markups (Not implemented)
- Packaging transactions (Not implemented)
- Device status (Not implemented)
- Fiscal memory and contents read (Not implemented)


## Documentation

Coming soon!


## License

[MIT](LICENSE)


## Note

**This project is not affiliated in any way with Posnet Polska S.A.**

The connection to the POSNET printer is based on posnet protocol documentation that is available [here](https://www.soft-bit.pl/downloads/all/Posnet/pliki/DBC-I-DEV-45-021_specyfikacja_protokolu_Posnet_w_drukarkach.pdf)
