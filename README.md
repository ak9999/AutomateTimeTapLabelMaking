# Automatic Appointment Label Printer

## Dependencies
* [DYMO Label v8](https://www.dymo.com/en-AU/dymo-label-software-v8-windows)
* Python 3.9
    * PyInstaller 4.0
    * PySimpleGUI 4.29.0
    * pywin32 228
    * PyYAML 5.3.1
    * requests
    * timetappy 0.0.2a0
* Address Label (supplied in resources folder)
* clock.ico (supplied in resources folder)
    * See ATTRIBUTION.md for attribution.

## Configuration
* config.yaml
    Needs to be in the following format:
    ```yaml
    --- # API configuration for TimeTap
    key: <TIMETAP KEY GOES HERE>
    secret: <TIME TAP API PRIVATE KEY GOES HERE>
    ```
    Needs to be saved in the same directory as `AutoTimeTapLabelMaker` executable.

## Building
1. Create your Python 3.9 virtual environment with the above listed dependencies
    * `python3 -m venv env`
2. Activate your virtual environment depending on Python distribution and operating system.
3. Install required packages with `pip install -r requirements.txt`
4. Run `make` to build the executable and check the `dist/` directory for `AutoTimeTapLabelMaker`.