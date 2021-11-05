from serial import Serial
from time import sleep
#from pymeasure.instruments import Insturment 
from pymeasure.instruments.validators import truncated_range, strict_discrete_set, joined_validators


class Config:
    cli_port: Serial
    data_port: Serial

    def __init__(self, config_file: str):
        self.cli_port = Serial('/dev/tty.SLAB_USBtoUART', 115200)
        self.data_port = Serial('/dev/tty.SLAB_USBtoUART4', 921600)
        self.cli_port.reset_input_buffer()
        self.cli_port.reset_output_buffer()
        self.data_port.reset_input_buffer()
        self.data_port.reset_output_buffer()
        self._init_config(config_file)
        self.aoa_fov_cfg = self.setting("aoaFovCfg %d %g %g %g %g", validator=[truncated_range, truncated_range, truncated_range, truncated_range], values=[[0,255],[-90.0, 90.0],[-90.0, 90.0],[-90.0, 90.0],[-90.0, 90.0]], stop_start=False)
    
    def _write(self, string: str) -> int:
        self.cli_port.write((string+'\n').encode('latin-1'))

    def _init_config(self, config_file: str) -> None:
        configs = [line.rstrip('\r\n') for line in open(config_file)]
        for config in configs:
            self._write(config)
            sleep(0.01)

    def get_data_port(self) -> Serial:
        return self.data_port

    # from pymeasure.insturment
    def setting(self, set_command: str, docs: str = """""", validator=lambda x, y: x, values=(), map_values=False, set_process=lambda v: v, stop_start: bool = False):
        def fget(self):
            raise LookupError("Properties can not be read.")

        def fset(self, value):
            if stop_start:
                self._write("sensorStop")
                sleep(0.01)
            value = set_process(validator(value, values))
            if not map_values:
                pass
            elif isinstance(values, (list, tuple, range)):
                value = values.index(value)
            elif isinstance(values, dict):
                value = values[value]
            else:
                raise ValueError(
                    'Values of type `{}` are not allowed '
                    'for setting'.format(type(values))
                )
            self._write(set_command % value)
            if stop_start:
                sleep(0.01)
                self._write("sensorStart")
                sleep(0.01)

        # Add the specified document string to the getter
        fset.__doc__ = docs
        return property(fget, fset)

    # Cannot do these
    #dfe_data_output_mode = setting("dfeDataOutputMode %d", validator=strict_discrete_set, values=[1,3])
    #channel_cfg = setting("channelCfg %b %b 0")
    
    # Can do these
    #adc_buf_cfg = setting("adcBufCfg %d 0 1 1 1", validator=truncated_range, values=[-1,255], stop_start=True)
    #profile_cfg = setting("profileCfg 0 %g %g %g %g 0 0 %g %g %d %d %g %g %g", validator=[truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range, truncated_range], values=[[60.0,64.0],[0.0, float("inf")],[0.0, float("inf")],[0.0, float("inf")],[2.220446049250313e-16, float("inf")],[0.0, float("inf")],[0, 256],[0, 65565],[0,3],[0,3],[0.0, float("inf")]], stop_start=True)
    
    


    