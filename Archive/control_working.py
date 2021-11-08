# Standard Library Imports
from time import sleep
from typing import List, Any, Tuple, Union

# External Imports
from serial import Serial
from pymeasure.instruments.validators import truncated_range, strict_discrete_set, joined_validators, strict_range

# Self Imports
None

class Utils:
    """Utils are utilities for this file
    """    

    @classmethod
    def is_instances_list_or_tuple(cls, objects: List[Any]) -> List[bool]:
        """is_instances_list_or_tuple checks if each object in a list of objects is a list or tuple

        Parameters
        ----------
        objects : List[Any]
            the list of objects

        Returns
        -------
        List[bool]
            The result of each check on each object
        """        
        return list(map(lambda x: isinstance(x, (list, tuple)), objects))

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

    @classmethod
    def len_is_same_lists(cls, objects: List[Any]) -> bool:
        """len_is_same_lists checks if the length of all objects in a list is the smae

        Parameters
        ----------
        objects : List[Any]
            the list of objects

        Returns
        -------
        bool
            True if the length of all objects is the same, False if not
        """        
        return len(set(list(map(lambda x: cls.len_safe(x), objects))))==1

    @classmethod
    def instance_and_len_test(cls, objects: Union[Any, List[Any]]) -> Tuple[List[bool], bool]:
        """instance_and_len_test calls both is_instances_list_or_tuple and len_is_same_lists at the same time

        Parameters
        ----------
        objects : Union[Any, List[Any]]
            an object or a list of objects

        Returns
        -------
        Tuple[List[bool], bool]
            A list of booleans and a boolean, see is_instances_list_or_tuple and len_is_same_lists
        """        
        return Utils.is_instances_list_or_tuple(objects), Utils.len_is_same_lists(objects)

class Ports:
    """Ports stores the serial ports used to communicate with the IWR6843 chip
    """    

    cli_port: Serial
    data_port: Serial

    def __init__(self):
        """__init__ sets up the ports to communicate with the IWR6843
        """        
        self.cli_port = Serial('/dev/tty.SLAB_USBtoUART', 115200)
        self.data_port = Serial('/dev/tty.SLAB_USBtoUART4', 921600)
        self.cli_port.reset_input_buffer()
        self.cli_port.reset_output_buffer()
        self.data_port.reset_input_buffer()
        self.data_port.reset_output_buffer()

class Config:
    def __init__(self, command: str = None, input: str = None, validator=lambda x, y: x, values=(), stop_start: bool = False, need_reboot: bool = False, full_command: str = None):
        tests, len_test = Utils.instance_and_len_test([validator, values])
        if any(tests):
            if not all(tests):
                raise ValueError("both validator and values are not lists or tuples")
            if not len_test:
                raise ValueError("validator and values do not have the same length")
        self.validator = validator
        self.values = values
        self.value = None
        self.stop_start = stop_start
        self.need_reboot = need_reboot
        if full_command:
            full_command = full_command.strip("\r\n")
            cmd_and_inputs = full_command.split(" ")
            self.command = cmd_and_inputs.pop(0)
            self.value = []
            self.input = ""
            for an_input in cmd_and_inputs:
                decarator = ""
                an_input_ = an_input.strip(".")
                is_number = (an_input.replace('.','',1).isdigit())
                if an_input == an_input_ and is_number:
                    decarator = "%d"
                    self.value.append(int(an_input))
                elif is_number:
                    decarator = "%g"
                    self.value.append(float(an_input))
                else:
                    decarator = "%s"
                    self.value.append(an_input)
                self.input = self.input + decarator + " "
            self.input = self.input[:-2]
            if len(self.value) < 2:
                self.value = self.value[0]
        else:
            self.command = command
            self.input = input
            
    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, value: Any) -> None:
        tests, len_test = Utils.instance_and_len_test([validator, value])
        if any(tests):
            if not all(tests):
                raise ValueError("Value is not a list while the validator or values are a list")
            if not len_test:
                raise ValueError("Value does not have the same length as the validator or values")
            for i, v in enumerate(self.validator):
                value[i] = v(value[i], self.values[i])
        else:
            value = self.validator(value, self.values)
        self.value = value

    def return_cmd(self) -> str:
        if self.input:
            return self.command + " " + (self.input % tuple(self.value))
        else:
            return self.command

class ControlBase:
    """ControlBase provides a base class that aids in controlling the IWR6843
    """    

    cli_port: Serial

    def __init__(self, init_config_file: str, ports: Ports):
        """__init__ initialize the IWR6843 as well as setting up the CLI options

        Parameters
        ----------
        init_config_file : str
            the initial configuration file
        ports : Ports
            the ports object storing the ports of the IWR6843
        """
        self.cli_port = ports.cli_port
        self.init_config_file = config_file
        self.configs = None
        self._config(config_file=init_config_file)

    def _write(self, string: str) -> int:
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
        return self.cli_port.write((string+"\n").encode('latin-1'))

    def _init_config(self, config_file: str = None) -> None:
        """_init_config initially configures the IWR6843 with the configuration file

        Parameters
        ----------
        config_file : str
            the path to the configuration file
        """        
        if config_file:
            self.configs = [line.rstrip('\r\n') for line in open(config_file)]
        for config in self.configs:
            self._write(config)
            sleep(0.01)

    def _sensor_start(self) -> None:
        """_sensor_start starts the IWR6843 sensor
        """        
        self._write("sensorStart 0")
        sleep(0.01)

    def _sensor_stop(self, flush_cfg: bool = False) -> None:
        """_sensor_stop stops the IWR6843 sensor

        Parameters
        ----------
        flush_cfg : bool, optional
            if True it flushes the configuration existing in the IWR6843, if False nothing happens, by default False
        """        
        self._write("sensorStop")
        if flush_cfg:
            sleep(0.01)
            self._write("flushCfg")
        sleep(0.01)

    @staticmethod
    def setting(set_command: str, docs: str = """""", validator=lambda x, y: x, values=(), stop_start: bool = False, need_reboot: bool = False) -> property:
        """_setting sets up a setting for the sensor

        Parameters
        ----------
        set_command : str
            the command to set a value
        docs : str, optional
            the doc string of the setting, by default """"""
        validator : Any, optional
            the validator, by default lambdax,y:x
        values : tuple, optional
            the values to set for the validator, by default ()
        stop_start : bool, optional
            specifies wheter or not to stop and start the sensor to set up the setting, by default False
        need_reboot : bool, optional
            specifies if the sensor needs to be rebooted for the settings to change, by default False

        Returns
        -------
        property
            the property object for the setting
        """        
        tests, len_test = Utils.instance_and_len_test([validator, values])
        if any(tests):
            if not all(tests):
                raise ValueError("both validator and values are not lists or tuples")
            if not len_test:
                raise ValueError("validator and values do not have the same length")

        def fget(self):
            try:
                return self.value
            except AttributeError:
                return None

        def fset(self, value):
            if need_reboot:
                print("Property cannot be written in real time, reboot the board and reconfigure settings")
            if stop_start:
                self._sensor_stop()
            tests, len_test = Utils.instance_and_len_test([validator, value])

            if any(tests):
                if not all(tests):
                    raise ValueError("value is not a list while the validator or values are a list")
                if not len_test:
                    raise ValueError("value does not have the same length as the validator or values")
                for i, v in enumerate(validator):
                    value[i] = v(value[i], values[i])
            else:
                value = validator(value, values)
            self._write(set_command % tuple(value))
            if stop_start:
                sleep(0.01)
                self._sensor_start()
                self.cli_port.reset_output_buffer()
                sleep(0.01)
                self._sensor_start() 
            self.value = value

        # Add the specified document string to the getter
        fget.__doc__ = docs
        fset.__doc__ = docs
        return property(fget, fset)
    
class Control(ControlBase):
    
    def __init__(self, config_file: str, ports: Ports):
        """__init__ initialize the controller for the IWR6843

        Parameters
        ----------
        config_file : str
            the initial configuration file for the sensor
        ports : Ports
            the ports object storing the ports of the IWR6843
        """        
        super(Control, self).__init__(config_file, ports)

    #self.dfe_data_output_mode = self._setting("dfeDataOutputMode %d", validator=strict_discrete_set, values=[1,3], need_reboot=True)
    #self.channel_cfg = self._setting("channelCfg %b %b 0", need_reboot=True)
    #self.adc_cfg =  self._setting("adcCfg 2 %d", need_reboot=True, validator=truncated_range, values=[])
    #self.adc_buf_cfg = self._setting("adcBufCfg %d 0 1 1 1", validator=truncated_range, values=[-1,255], stop_start=True)
    #self.profile_cfg = self._setting("profileCfg 0 %g %g %g %g 0 0 %g %g %d %d %g %g %g", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[60.0,64.0],[0.0, float("inf")],[0.0, float("inf")],[0.0, float("inf")],[2.220446049250313e-16, float("inf")],[0.0, float("inf")],[0, 256],[0, 65565],[0,3],[0,3],[0.0, float("inf")]], stop_start=True)
    #self.chirp_cfg = self._setting("chirpCfg %d %d 0 0 0 0 0 %b", stop_start=True)
    #self.low_power = self._setting("lowPower 0 %b", need_reboot=True)
    #self.frame_cfg = self._setting("frameCfg %d %d %d %d %g 1 %g", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[0, 511], [0, 511], [0, 65535], [0, float("inf")], [0, float("inf")]], stop_start=True)
    #self.adv_frame_cfg = self._setting("advFrameCfg %d 0 %d 1 %g", validator=[truncated_range, truncated_range, truncated_range], values=[[0, 65535], [0, 65535], [0, float("inf")]], stop_start=True)
    #self.sub_frame_cfg = self._setting("subFrameCfg %d %d %d %d %d %g 0 1 1 %g", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[0, 65535], [0, 65535], [0, 65535], [4, 65535], [0, float("inf")], [0, float("inf")]], stop_start=True)
    #self.gui_monitor = self._setting("guiMonitor %d %d %d %d %d %d %d", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]], stop_start=True)
    #self.cfar_cfg = self._setting("cfarCfg %d %d %d %d %d %d %d %g %d", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[-1, 65535], [0,1], [0,2], [0, 65535], [0, 65535], [0, 65535], [0,1], [0.0, 100.0], [0,1]])
    #self.multi_obj_beam_forming = self._setting("multiObjBeamForming %d %d %d", validator=[truncated_range, truncated_range, truncated_range], values=[[-1, 65535], [0,1], [0,1]])
    #self.calib_dc_range_sig = self._setting("calibDcRangeSig %d %d %d %d %d", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[0, 65535], [0,1], [-65535, 65535], [0, 65535], [0, 65535]])
    #self.clutter_removal = self._setting("clutterRemoval %d %d", validator=[truncated_range, truncated_range], values=[[0, 65535], [0,1]])
    aoa_fov_cfg = ControlBase.setting("aoaFovCfg %d %g %g %g %g", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[-1,255],[-90.0, 90.0],[-90.0, 90.0],[-90.0, 90.0],[-90.0, 90.0]], stop_start=True)
    #self.cfar_fov_cfg = self._setting("cfarFovCfg %d %d %g %g",  validator=[truncated_range, truncated_range, truncated_range, truncated_range], values=[[0, 65535], [0,1], [0, float("inf")], [0, float("inf")]])
    #self.comp_range_bias_and_rx_chan_phase = self._setting("compRangeBiasAndRxChanPhase %g 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0", validator=truncated_range, values=[0.0, float("inf")])
    #self.measure_range_bias_and_rx_chan_phase = self._setting("measureRangeBiasAndRxChanPhase %d %g %g", validator=[truncated_range, truncated_range, truncated_range], values=[[0,1], [0.0, float("inf")], [0.0, float("inf")]])
    #self.extended_max_velocity = self._setting("extendedMaxVelocity %d %d", validator=[truncated_range, truncated_range], values=[[0, 65535], [0,1]])
    #self.cq_rx_sat_monitor = self._setting("0 %d %d %d %d", validator=[truncated_range,truncated_range,truncated_range,truncated_range],values=[[0, 65535], [4, 65535], [1, 127], [0,1]], stop_start=True)
    #self.cq_sig_img_monitor = self._setting("CQSigImgMonitor 0 %d %d", validator=[truncated_range,truncated_range], values=[[0, 127], [4, 65535]], stop_start=True)
    #self.analog_monitor = self._setting("analogMonitor %d %d", validator=[truncated_range,truncated_range], values=[[0, 1], [0, 1]], stop_start=True)
    #self.lvds_stream_cfg = self._setting("lvdsStreamCfg %d %d %d %d", validator=[truncated_range,truncated_range,strict_discrete_set,truncated_range], values=[[0, 65535], [0,1], [0,1,4], [0,1]], stop_start=True)
    #self.bpm_cfg = self._setting("bpmCfg %d %d %d %d", validator=[truncated_range,truncated_range,truncated_range,truncated_range], values=[[0, 65535],[0,1],[0, 65535],[0, 65535]], stop_start=True)
    #self.calib_data = self._setting("calibData %d %d %d",validator=[truncated_range,truncated_range,truncated_range], values=[[0,1],[0,1],[0, 65535]], need_reboot=True)
    #self.config_data_port = self._setting("configDataPort %d %d", validator=[truncated_range,truncated_range], values=[[0, 3125000], [0,1]], stop_start=True)
    #self.query_demo_status = self._setting("queryDemoStatus")
