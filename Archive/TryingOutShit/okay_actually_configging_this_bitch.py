import serial
import time
import this_is_what_ti_did_and_it_is_shit_code
#import doing_what_ti_did_but_better_because_their_code_is_really_shit
from all_that_parsing_shit_but_for_another_window_cause_vscode_small import PacketHandler
# Change the configuration file name
config_file_name = 'xwr68xx_profile_2021_10_24T03_23_44_468.cfg'

cli_port = None
data_port = None

def config(config_file='xwr68xx_profile_2021_10_24T03_23_44_468.cfg'):
    cli_port = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200)
    data_port = serial.Serial('/dev/tty.SLAB_USBtoUART4', 921600)

    # Read the configuration file and send it to the board
    config = [line.rstrip('\r\n') for line in open(config_file)]
    for i in config:
        cli_port.write((i+'\n').encode('latin-1'))
        print(i)
        time.sleep(0.01)
        
    return cli_port, data_port

cli_port, data_port = config()
parser = PacketHandler()
while True:
    read_buffer = data_port.read(data_port.inWaiting())
    if len(read_buffer) > 0:
        #print("hi bitch")
        #print(doing_what_ti_did_but_better_because_their_code_is_really_shit.parser_one_mmw_demo_output_packet(read_buffer))
        #print(parser.parser(read_buffer))
        this_is_what_ti_did_and_it_is_shit_code.parser_one_mmw_demo_output_packet(read_buffer, len(read_buffer))