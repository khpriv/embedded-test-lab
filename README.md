# Embedded Test Lab

A small embedded-testing playground built around a simulated device and an STM32 NUCLEO-F446RE. Its goal is to run the **same high-level tests against a simulator or real hardware**, while keeping test intent separate from protocol and communication details.

This is a learning/prototyping project, not a production-ready HIL framework. The serial protocol has no transaction identifiers, and the OLED implementation is experimental.

The project uses **Python, pytest, Robot Framework, UART, Docker**, and a sample **GitLab CI** pipeline.

## Architecture

```text
pytest / Robot Framework
         |
   Robot keyword library
         |
       Device API
         |
    Transport interface
       /          \
SimulatorTransport  SerialTransport --> STM32 firmware
```

`Device` implements commands and response validation. Transports handle communication; the simulator implements the same command/response behavior in memory. Robot tests express device behavior through readable keywords, with shared workflows in resource files.

## Run the tests

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"

# Software-only tests (no DUT required)
python -m pytest -m "not hardware" -v
robot -d robot_results robot/smoke.robot robot/negative.robot
```

Alternatively, run the software-only test suites in Docker:

```bash
docker build -t embedded-test-lab .
docker run --rm embedded-test-lab
```

## Physical DUT

The hardware target is an **STM32 NUCLEO-F446RE**, connected over the board's ST-LINK virtual COM port (UART, **115200 8N1**). An SSD1306 OLED is attached over I²C as an additional firmware experiment. Firmware project files belong in `firmware/stm32f446re/`.

With the board connected and compatible test firmware flashed:

```bash
DUT_PORT=/dev/ttyACM0 python -m pytest -m hardware -v
robot -d robot_results robot/hardware.robot
```

Robot hardware suites currently default to `/dev/ttyACM0`; adjust the library argument if your port differs. Hardware tests are excluded from the default software-only pytest run.

## Fault injection and CI

The firmware/test setup includes an experiment with delayed UART responses. It demonstrates a subtle failure mode: **a timed-out request may still execute, and a late response may be mistaken for the response to a later command**. Retrying without response correlation is therefore unsafe for some operations. The retry example is educational, not a production-safe protocol.

`.gitlab-ci.yml` defines separate software, simulator and manually triggered HIL jobs. Hardware jobs require a runner connected to the bench. Test reports can be exported as JUnit/xUnit artifacts.
