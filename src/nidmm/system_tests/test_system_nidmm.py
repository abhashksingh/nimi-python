#!/usr/bin/python

import nidmm

def test_invalid_device_name():
    try:
        nidmm.Session("Foo!")
        assert false
    except nidmm.Error as e:
        assert e.code == -1074118656
        assert e.description.find("Device was not recognized. The device is not supported with this driver or version.") != -1
        assert e.description.find("Foo!") != -1


def test_take_simple_measurement_works():
    with nidmm.Session("PXI1Slot2") as session:
        session.configure_measurement_digits(nidmm.Function.DC_CURRENT, 1, 5.5)
        assert session.read(1000) < 0.01 # Assume nothing is connected to device, reads back around 0.


def test_wrong_parameter_type():
    with nidmm.Session("PXI1Slot2") as session:
        try:
            # We are passing a number where an enum is expected.
            session.configure_measurement_digits(1, 10, 5.5)
            assert False
        except TypeError as e:
            print(e)
            pass


def test_warning():
    with nidmm.Session("PXI1Slot2") as session:
        session.configure_measurement_digits(nidmm.Function.RES_2_WIRE, 1e6, 3.5)
        try:
            print(session.read(1000)) # Assume nothing is connected to device, overrange!
            assert False
        except nidmm.Warning as w:
            print(w)
            pass


def test_ViBoolean_attribute():
    with nidmm.Session("PXI1Slot2") as session:
        assert session.simulate is False
        # TODO(marcoskirsch): set a boolean


def test_ViString_attribute():
    with nidmm.Session("PXI1Slot2") as session:
        assert "1A67CAC" == session.serial_number
        # TODO(marcoskirsch): set a string


def test_ViInt32_attribute():
    with nidmm.Session("PXI1Slot2") as session:
        session.sample_count = 5
        assert 5 == session.sample_count


def test_ViReal64_attribute():
    with nidmm.Session("PXI1Slot2") as session:
        session.range = 50 # Coerces up!
        assert 100 == session.range


def test_Enum_attribute():
    with nidmm.Session("PXI1Slot2") as session:
        session.function = nidmm.Function.AC_CURRENT
        assert session.function == nidmm.Function.AC_CURRENT
        assert type(session.function) is nidmm.Function
        try:
            session.function = nidmm.LCCalculationModel.CALC_MODEL_SERIES
            assert false
        except TypeError as e:
            print(e)
            pass


def test_ViSession_attribute():
    with nidmm.Session("PXI1Slot2") as session:
        try:
            session.io_session = 5
            assert false
        except TypeError as e:
            print(e)
            pass
        try:
            value = session.io_session
            assert false
        except TypeError as e:
            print(e)
            pass


def test_self_test():
    with nidmm.Session("PXI1Slot2") as session:
        result, message = session.self_test()
        assert result == 0
        assert message == 'Self Test passed.'


def test_get_dev_temp():
    with nidmm.Session("PXI1Slot2") as session:
        temperature = session.get_dev_temp('')
        print(temperature)
        assert 20 <= temperature <= 50

