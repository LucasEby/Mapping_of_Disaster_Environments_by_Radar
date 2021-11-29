# Standard Library Imports
from typing import Union, List, Any
from time import sleep
from itertools import compress

# Package Imports
from serial import Serial, SerialException
from serial.tools import list_ports
from pymeasure.instruments.validators import truncated_range, strict_discrete_set

# Self Imports
from timer import Timer, TimeOutException

class Utils:
    """Utils are utilities for this file
    """

    @classmethod
    def len_safe(cls, object: Any) -> int:
        """len_safe checks the length of an object without any error
        If the object is not iterable then the length is negative 1

        Parameters
        ----------
        object : Any
            the object

        Returns
        -------
        int
            the length of the object if iterable, if not -1
        """
        try:
            return len(object)
        except TypeError:
            return -1

class Ports:
    """Ports stores the serial ports used to communicate with the IWR6843 chip
    """

    SERIAL_CODE = "SER=00CF6"
    cli_port: Union[str, Serial]
    data_port: Union[str, Serial]
    arduino_port: Union[str, Serial]

    def __init__(self, attach_time: float = None, attach_to_ports: bool = True, find_arduino: bool = False):
        """__init__ looks for the serial ports of the arduino if specified and the IWR6843 and attaches to the ports if specified

        Parameters
        ----------
        attach_time : float, optional
            the time to wait to discover and attach to ports if specified, by default None
        attach_to_ports : bool, optional
            if True the class will attach to the found ports, if False the class will return the filepaths of the ports, by default True
        find_arduino : bool, optional
            if True the class will find the arduino, if False it will not find the arduino

        Raises
        ------
        TimeOutException
            if the class times out when searching for ports
        """
        # Set objects meant to be global
        timer = None
        cli_path = None
        data_path = None
        arduino_path = None
        # Create timer if a timeout is set
        if attach_time:
            timer = Timer(attach_time)
        while True:
            try:
                # List the serial/comports
                ports = list_ports.comports()
                if ports:
                    # Loop through each port
                    for port in ports:
                        name = port.name
                        hwid = port.hwid
                        # Attach CLI port
                        if ("cu.SLAB_USBtoUART" in name) and (self.SERIAL_CODE in hwid) and (cli_path is None):
                            cli_path = "/dev/" + name
                        # Attach Data port
                        elif ("cu.SLAB_USBtoUART" in name) and (self.SERIAL_CODE in hwid) and (data_path is None):
                            data_path = "/dev/" + name
                        # Attach Arduino/ESP32 port
                        elif (("PID=1A86:7523" in hwid) or (("cu.SLAB_USBtoUART" in name) and ("SER=0001" in hwid))) and (arduino_path is None):
                            arduino_path = "/dev/" + name
                # Run the timer
                if timer:
                    timer.run()
                # Set class data
                if not(cli_path is None) and not(data_path is None) and (not(arduino_path is None) or not(find_arduino)):
                    # Attach to ports
                    if attach_to_ports:
                        self.cli_port = Serial(cli_path, 115200, timeout=0.1)
                        self.data_port = Serial(data_path, 921600, timeout=0.1)
                        if find_arduino:
                            self.arduino_port = Serial(arduino_path, 9600, timeout=0.1)
                    # Leave data as the paths
                    else:
                        self.cli_port = cli_path
                        self.data_port = data_path
                        if find_arduino:
                            self.arduino_port = arduino_path
                    break
                # Keep on searching
                else:
                    continue
            # Handle serial exception or index error and keep searching
            except (SerialException, IndexError, OSError):
                sleep(0.05)
                continue
            # Raise exception when a timeout occurs
            except TimeOutException:
                raise TimeOutException(message="Searching for serial ports timed out after " + str(attach_time) + " seconds")

        # Setup the CLI port and data port if attaching to ports and ports succesfully found
        if attach_to_ports and not(cli_path is None) and not(data_path is None) and not(arduino_path is None):
            self.cli_port.reset_input_buffer()
            self.cli_port.reset_output_buffer()
            self.cli_port.flushInput()
            self.cli_port.flushOutput()
            self.data_port.reset_input_buffer()
            self.data_port.reset_output_buffer()
            self.data_port.flushInput()
            self.data_port.flushOutput()

class Control:
    """Control provides an interface to controlling the IWR6843
    """

    def __init__(self, init_config_file: str, ports: Ports):
        """__init__ initialize the IWR6843 as well as setting up the CLI options

        Parameters
        ----------
        init_config_file : str
            the initial configuration file
        ports : Ports
            the ports object storing the ports of the IWR6843
        """
        if isinstance(ports.cli_port, str):
            self.cli_port = Serial(ports.cli_port, 115200, timeout=0.1)
            self.cli_port.reset_input_buffer()
            self.cli_port.reset_output_buffer()
            self.cli_port.flushInput()
            self.cli_port.flushOutput()
        else:
            self.cli_port = ports.cli_port
        self.init_config_file = init_config_file
        self._setup_configs()
        self._init_configuration(self.init_config_file)

    def _setup_configs(self) -> None:
        """_setup_configs sets up all the configuration options
        """
        # The dictionary of configurations
        self.configs = {}

        # TODO: Fix this configuration section and add ways to sort the dictinoary

        # All the configurations
        self.sensor_stop = Config("sensorStop", "", no_value=True)
        self.flush_cfg = Config("flushCfg", "", no_value=True)
        self.dfe_data_output_mode = Config("dfeDataOutputMode", "%d", validator=strict_discrete_set, values=[1,3], need_reboot=True)
        self.channel_cfg = Config("channelCfg", "%d %d 0", need_reboot=True, validator=[truncated_range, truncated_range], values=[[1,15],[1,7]])
        self.adc_cfg = Config("adcCfg", "2 %d", need_reboot=True, validator=strict_discrete_set, values=[1,2])
        self.adc_buf_cfg = Config("adcbufCfg", "%d 0 1 1 1", validator=truncated_range, values=[-1,255], stop_start=True)
        self.profile_cfg = Config("profileCfg", "0 %g %g %g %g 0 0 %g %g %d %d %g %g %g", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[60.0,64.0],[0.0, float("inf")],[0.0, float("inf")],[0.0, float("inf")],[2.220446049250313e-16, float("inf")],[0.0, float("inf")],[0, 256],[0, 65565],[0,3],[0,3],[0.0, float("inf")]], stop_start=True)
        self.chirp_cfg = Config("chirpCfg", "%d %d 0 0 0 0 0 %d", stop_start=True, n_inputs=3, validator=[truncated_range,truncated_range,truncated_range], values=[[0,2],[0,2],[0,4]])
        self.low_power = Config("lowPower", "0 0", need_reboot=True)
        self.frame_cfg = Config("frameCfg", "%d %d %d %d %g 1 %g", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[0, 511], [0, 511], [0, 65535], [0, float("inf")], [0, float("inf")], [0, float("inf")]], stop_start=True)
        self.adv_frame_cfg = Config("advFrameCfg", "%d 0 %d 1 %g", validator=[truncated_range, truncated_range, truncated_range], values=[[0, 65535], [0, 65535], [0, float("inf")]], stop_start=True)
        self.sub_frame_cfg = Config("subFrameCfg", "%d %d %d %d %d %g 0 1 1 %g", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[0, 65535], [0, 65535], [0, 65535], [4, 65535], [0, float("inf")], [0, float("inf")]], stop_start=True)
        self.gui_monitor = Config("guiMonitor", "%d %d %d %d %d %d %d", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[-1,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]], stop_start=True)
        self.cfar_cfg = Config("cfarCfg", "%d %d %d %d %d %d %d %g %d", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[-1, 65535], [0,1], [0,2], [0, 65535], [0, 65535], [0, 65535], [0,1], [0.0, 100.0], [0,1]], n_inputs=2)
        self.multi_obj_beam_forming = Config("multiObjBeamForming", "%d %d %g", validator=[truncated_range, truncated_range, truncated_range], values=[[-1, 65535], [0,1], [0,1]])
        self.calib_dc_range_sig = Config("calibDcRangeSig", "%d %d %d %d %d", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[-1, 65535], [0,1], [-65535, 65535], [0, 65535], [0, 65535]])
        self.clutter_removal = Config("clutterRemoval", "%d %d", validator=[truncated_range, truncated_range], values=[[-1, 65535], [0,1]])
        self.aoa_fov_cfg = Config("aoaFovCfg", "%d %g %g %g %g", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[-1,255],[-90.0, 90.0],[-90.0, 90.0],[-90.0, 90.0],[-90.0, 90.0]], stop_start=True)
        self.cfar_fov_cfg = Config("cfarFovCfg", "%d %d %g %g", validator=[truncated_range, truncated_range, truncated_range, truncated_range], values=[[-1, 65535], [-1,1], [-float("inf"), float("inf")], [-float("inf"), float("inf")]], n_inputs=2)
        self.comp_range_bias_and_rx_chan_phase = Config("compRangeBiasAndRxChanPhase", "%g 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0", validator=truncated_range, values=[0.0, float("inf")])
        self.measure_range_bias_and_rx_chan_phase = Config("measureRangeBiasAndRxChanPhase", "%d %g %g", validator=[truncated_range, truncated_range, truncated_range], values=[[0,1], [0.0, float("inf")], [0.0, float("inf")]])
        self.extended_max_velocity = Config("extendedMaxVelocity", "%d %d", validator=[truncated_range, truncated_range], values=[[-1, 65535], [0,1]])
        self.cq_rx_sat_monitor = Config("CQRxSatMonitor","0 %d %d %d %d", validator=[truncated_range,truncated_range,truncated_range,truncated_range],values=[[0, 65535], [4, 65535], [1, 127], [0,1]], stop_start=True)
        self.cq_sig_img_monitor = Config("CQSigImgMonitor", "0 %d %d", validator=[truncated_range,truncated_range], values=[[0, 127], [4, 65535]], stop_start=True)
        self.analog_monitor = Config("analogMonitor", "%d %d", validator=[truncated_range,truncated_range], values=[[0, 1], [0, 1]], stop_start=True)
        self.lvds_stream_cfg = Config("lvdsStreamCfg", "%d %d %d %d", validator=[truncated_range,truncated_range,strict_discrete_set,truncated_range], values=[[-1, 65535], [0,1], [0,1,4], [0,1]], stop_start=True)
        self.bpm_cfg = Config("bpmCfg", "%d %d %d %d", validator=[truncated_range,truncated_range,truncated_range,truncated_range], values=[[-1, 65535],[0,1],[0, 65535],[0, 65535]], stop_start=True)
        self.calib_data = Config("calibData", "%d %d %d",validator=[truncated_range,truncated_range,truncated_range], values=[[0,1],[0,1],[0, 65535]], need_reboot=True)
        self.config_data_port = Config("configDataPort", "%d %d", validator=[truncated_range,truncated_range], values=[[0, 3125000], [0,1]], stop_start=True)
        self.query_demo_status = Config("queryDemoStatus", "",no_value=True)
        self.sensor_start = Config("sensorStart", "", no_value=True)

        # Setup the dictionary
        self.configs[self.sensor_stop] = self.sensor_stop
        self.configs[self.flush_cfg] = self.flush_cfg
        self.configs[self.dfe_data_output_mode] = self.dfe_data_output_mode
        self.configs[self.channel_cfg] = self.channel_cfg
        self.configs[self.adc_cfg] = self.adc_cfg
        self.configs[self.adc_buf_cfg] = self.adc_buf_cfg
        self.configs[self.profile_cfg] = self.profile_cfg
        self.configs[self.chirp_cfg] = self.chirp_cfg
        self.configs[self.frame_cfg] = self.frame_cfg
        self.configs[self.low_power] = self.low_power
        # self.configs[self.adv_frame_cfg] = self.adv_frame_cfg
        # self.configs[self.sub_frame_cfg] = self.sub_frame_cfg
        self.configs[self.gui_monitor] = self.gui_monitor
        self.configs[self.cfar_cfg] = self.cfar_cfg
        self.configs[self.multi_obj_beam_forming] = self.multi_obj_beam_forming
        self.configs[self.clutter_removal] = self.clutter_removal
        self.configs[self.calib_dc_range_sig] = self.calib_dc_range_sig
        self.configs[self.extended_max_velocity] = self.extended_max_velocity
        self.configs[self.bpm_cfg] = self.bpm_cfg
        self.configs[self.lvds_stream_cfg] = self.lvds_stream_cfg
        self.configs[self.comp_range_bias_and_rx_chan_phase] = self.comp_range_bias_and_rx_chan_phase
        self.configs[self.measure_range_bias_and_rx_chan_phase] = self.measure_range_bias_and_rx_chan_phase
        self.configs[self.cq_rx_sat_monitor] = self.cq_rx_sat_monitor
        self.configs[self.cq_sig_img_monitor] = self.cq_sig_img_monitor
        self.configs[self.analog_monitor] = self.analog_monitor
        self.configs[self.aoa_fov_cfg] = self.aoa_fov_cfg
        self.configs[self.cfar_fov_cfg] = self.cfar_fov_cfg
        self.configs[self.calib_data] = self.calib_data
        # self.configs[self.config_data_port] = self.config_data_port
        # self.configs[self.query_demo_status] = self.query_demo_status
        self.configs[self.sensor_start] = self.sensor_start

    def _init_configuration(self, init_config_file: str) -> None:
        """_init_configuration initially configures the IWR6843 with an initial configuration file

        Parameters
        ----------
        init_config_file : str
            the initial configuration file
        """
        init_configs = [line.rstrip('\r\n') for line in open(self.init_config_file)]

        for init_config in init_configs:
            if init_config[0] != "%":
                config_and_vals = init_config.split(" ")
                config = config_and_vals.pop(0)
                values = []
                for value in config_and_vals:
                    converted = value
                    if value.lstrip("-").replace(".","").isdigit():
                        try:
                            converted = int(value)
                        except ValueError:
                            converted = float(value)
                    values.append(converted)
                if values and len(values) < 2:
                    values = values[0]
                self.configs[config].set_value(values)
        self.config()

    def config(self) -> None:
        """config configures the IWR6843
        """
        # Sets up loop that continously configures if there is an error in configuration and if there is no error in configuration then the loop terminates
        result = "error"
        while "error" in result.lower():
            # Write the configurations
            for value in self.configs.values():
                value.write(self)
                sleep(0.01)
            # Check the result of the configuration
            result = self.read()
            result = ''.join(result)

    def write(self, string: str) -> int:
        """_write write to the CLI port in the IWR6843

        Parameters
        ----------
        string : str
            the string to write

        Returns
        -------
        int
            the number of bytes written to the CLI port
        """
        print(string)
        return self.cli_port.write((string+"\n").encode('latin-1'))

    def read(self) -> List[str]:
        """read reads from the IWR6843 CLI port, supposed to be called post configuration

        Returns
        -------
        List[str]
            the lines read from the CLI port
        """
        lines = self.cli_port.readlines(10000)
        for i, line in enumerate(lines):
            line = line.decode().strip('\r\n')
            line = line.split("mmwDemo:/>")
            line = line[-1]
            lines[i] = line
        return lines

class Config:
    """Config is a configuration in the IWR6843
    """

    def __init__(self, command: str, input: str, validator=lambda x, y: x, values=(), stop_start: bool = False, need_reboot: bool = False, no_value: bool = False, n_inputs: int = 1):
        """__init__ sets up the configuration

        Parameters
        ----------
        command : str
            the command to send to the IWR6843
        input : str
            the input format specifier string
        validator : [type], optional
            the validator functions to validate passed in inputs, by default lambdax
        values : tuple, optional
            the values to input into the validator, by default ()
        stop_start : bool, optional
            if True then the chip will be stopped and re-started and re-configured to update the configuration, by default False
        need_reboot : bool, optional
            if True then this configuration will not be written and an exception will be raised informing that a reboot of the chip needs to occur, by default False
        no_value : bool, optional
            if True then this configuration has no value attached to it, by default False
        n_inputs : int, optional
            the number of times (number of values) this config is inputted into the IWR6843, by default 1
        """
        self.validator = validator
        self.values = values
        self.value = None
        self.stop_start = stop_start
        self.need_reboot = need_reboot
        self.no_value = no_value
        self.command = command
        self.input = input
        self.mask = []
        self.enabled = self.no_value
        self.n_inputs = n_inputs
        if self.n_inputs > 1:
            self.prev_values = []
            for i in range(self.n_inputs):
                self.prev_values.append(None)
            self.prev_index = 0

        if self.input:
            inputs = self.input.split(" ")
            for spec in inputs:
                self.mask.append(spec[0] == "%")

    def get_value(self) -> Any:
        """get_value get the value set in the configuration

        Returns
        -------
        Any
            the value
        """
        if self.n_inputs > 1:
            return self.prev_values[self.prev_index]
        return self.value

    def set_value(self, value: Any = None) -> None:
        """set_value set the value of this configuration

        Parameters
        ----------
        value : Any, optional
            the value to set of the configuration, by default None

        Raises
        ------
        ValueError
            If no value is passed in or if the validators raise an exception
        """
        # Check that value is there and that this configuration has a value
        if value and not(self.no_value):
            # Try to compress the value with the mask (mask shows which values are not non-static in the configuration)
            try:
                value = list(compress(value, self.mask))
                if value and len(value) < 2:
                    value = value[0]
            except TypeError:
                pass
            # Do multiple validation if the length of the value and validator are a list of size greater than 1
            if Utils.len_safe(value) > 1 and Utils.len_safe(self.validator) > 1:
                for i, v in enumerate(self.validator):
                    value[i] = v(value[i], self.values[i])
            # Otherwise do a single validation
            else:
                value = self.validator(value, self.values)
            # Check if multiple inputs are being set in this configuration
            if self.n_inputs > 1:
                # Loop through the values
                for i, val in enumerate(self.prev_values):
                    # If the value is not set then set the value now
                    if not(val):
                        self.prev_values[i] = value
                        self.value = value
                        self.prev_index = i
                        break
                    # If the value has been set then check which value needs to be set next
                    elif val and self.prev_values[self.prev_index]:
                        # Try to set the next prev value
                        try:
                            self.prev_values[self.prev_index+1] = value
                            self.value = value
                            self.prev_index = self.prev_index + 1
                        # Otherwise set the first prev value
                        except IndexError:
                            self.prev_values[0] = value
                            self.value = value
                            self.prev_index = 0
                        break
            # Just need to set one value
            else:
                self.value = value
            # Enable the configuration if it is not enabled
            if not(self.enabled):
                self.enabled = True
        # No value is passed in
        else:
            # Do nothing if the configuration does not have a vlue
            if self.no_value:
                pass
            # Raise exception that no value is passed in
            else:
                raise ValueError("Did not pass in any value")

    def get_cmd(self) -> Union[str, None]:
        """get_cmd get the string representing the command to send to the IWR6843

        Returns
        -------
        Union[str, None]
            if the configuration is not enabled then None will be returned, else the string representing the command is returned
        """
        if self.enabled:
            # Return the command w/ value
            if not(self.input is None) and not(self.value is None):
                try:
                    return self.command + " " + (self.input % tuple(self.value))
                except TypeError:
                    return self.command + " " + (self.input % self.value)
            # Return the command w/ input format
            elif not(self.input is None) and not(self.input == ""):
                return self.command + " " + self.input
            # Just return the command
            else:
                return self.command
        else:
            return None

    def __eq__(self, other: Any) -> bool:
        """__eq__ compare this object to another object

        Parameters
        ----------
        other : Any
            the other object

        Returns
        -------
        bool
            True if the objects are equal, false if not
        """
        if isinstance(other, Config):
            return self.__hash__() == other.__hash__()
        elif isinstance(other, str):
            return self.__hash__() == other.__hash__()
        return False

    def __hash__(self) -> int:
        """__hash__ produce the hash of htis object

        Returns
        -------
        int
            the has of this object
        """
        return self.command.__hash__()

    def __repr__(self) -> str:
        """__repr__ provides the string representation of this object

        Returns
        -------
        str
            the string representation of this object
        """
        return self.get_cmd()

    def write(self, control: Control) -> None:
        """write write this configuration to the IWR6843

        Parameters
        ----------
        control : Control
            the control object that enables writing to the IWR6843

        Raises
        ------
        AssertionError
            If the configuration needs to be set after rebooting the IWR6843
        """
        # if self.need_reboot:
        #    raise AssertionError("Must restart the board to setup this configuration")
        cmd = self.get_cmd()
        if cmd:
            # Writing multiple values
            if self.n_inputs > 1:
                # Write the multiple values
                for val in self.prev_values:
                    self.value = val
                    cmd = self.get_cmd()
                    control.write(cmd)
                    sleep(0.01)
                # Reset self.value to the starting self.value
                self.value = self.prev_values[self.prev_index]
            # Writing a single value
            else:
                control.write(cmd)

    def set_and_write(self, control: Control, value: Any = None) -> None:
        """set_and_write set the value of the configuration and then write it to the IWR6843

        Parameters
        ----------
        control : Control
            the control object that enables writing to the IWR6843
        value : Any, optional
            the value to set of the configuration, by default None

        Raises
        ------
        AssertionError
            If the configuration needs to be set after rebooting the IWR6843
        """
        self.set_value(value)
        if self.need_reboot:
            raise AssertionError("Must restart the board to setup this configuration")
        elif self.stop_start:
            control.config()
        else:
            self.write(control)
