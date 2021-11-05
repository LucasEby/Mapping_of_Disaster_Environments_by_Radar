import struct
import math
import binascii
import codecs
from enum import Enum

class ParserStatus(Enum):
    TC_PASS = 0
    TC_FAIL = 1

class ByteUtils:
    @classmethod
    def get_uint32(cls, data: bytes) -> int:
        """!
        This function coverts 4 bytes to a 32-bit unsigned integer.

            @param data : 1-demension byte array  
            @return     : 32-bit unsigned integer
        """ 
        return (data[0] +
                data[1]*256 +
                data[2]*65536 +
                data[3]*16777216)
    
    @classmethod
    def get_uint16(cls, data: bytes) -> int:
        """!
        This function coverts 2 bytes to a 16-bit unsigned integer.

            @param data : 1-demension byte array
            @return     : 16-bit unsigned integer
        """ 
        return (data[0] +
                data[1]*256)

    @classmethod
    def get_hex(cls, data: bytes) -> bytes:
        """! 
        This function coverts 4 bytes to a 32-bit unsigned integer in hex.

            @param data : 1-demension byte array
            @return     : 32-bit unsigned integer in hex
        """ 
        return (binascii.hexlify(data[::-1]))

    @classmethod
    def check_magic_pattern(cls, data: bytes) -> int:
        """!
        This function check if data arrary contains the magic pattern which is the start of one mmw demo output packet.  

            @param data : 1-demension byte array
            @return     : 1 if magic pattern is found
                        0 if magic pattern is not found 
        """ 
        found = 0
        if (data[0] == 2 and data[1] == 1 and data[2] == 4 and data[3] == 3 and data[4] == 6 and data[5] == 5 and data[6] == 8 and data[7] == 7):
            found = 1
        return (found)
            
def initial_process_data(data: bytes):
    """!
       This function is called by parser_one_mmw_demo_output_packet() function or application to read the input buffer, find the magic number, header location, the length of frame, the number of detected object and the number of TLV contained in this mmw demo output packet.

        @param data                   : 1-demension byte array holds the the data read from mmw demo output. It ignorant of the fact that data is coming from UART directly or file read.  
            
        @return header_start_index      : the mmw demo output packet header start location
        @return total_packet_num_bytes   : the mmw demo output packet lenght           
        @return num_det_obj             : the number of detected objects contained in this mmw demo output packet          
        @return num_tlv                : the number of TLV contained in this mmw demo output packet           
        @return sub_frame_number        : the sbuframe index (0,1,2 or 3) of the frame contained in this mmw demo output packet
    """ 

    header_start_index = -1
    read_num_bytes = len(data)

    for index in range (read_num_bytes):
        if ByteUtils.check_magic_pattern(data[index:index+8:1]) == 1:
            header_start_index = index
            break
  
    if header_start_index == -1:
        total_packet_num_bytes = -1
        num_det_obj = -1
        num_tlv = -1
        sub_frame_number = -1
        platform = -1
        frame_number = -1
        time_cpu_cycles = -1
    else:
        total_packet_num_bytes = ByteUtils.get_uint32(data[header_start_index+12:header_start_index+16:1])
        platform = ByteUtils.get_hex(data[header_start_index+16:header_start_index+20:1])
        frame_number = ByteUtils.get_uint32(data[header_start_index+20:header_start_index+24:1])
        time_cpu_cycles = ByteUtils.get_uint32(data[header_start_index+24:header_start_index+28:1])
        num_det_obj = ByteUtils.get_uint32(data[header_start_index+28:header_start_index+32:1])
        num_tlv = ByteUtils.get_uint32(data[header_start_index+32:header_start_index+36:1])
        sub_frame_number = ByteUtils.get_uint32(data[header_start_index+36:header_start_index+40:1])
                              
    return (header_start_index, total_packet_num_bytes, num_det_obj, num_tlv, sub_frame_number)

def parser_one_mmw_demo_output_packet(data: bytes):
    """!
       This function is called by application. Firstly it calls parser_helper() function to find the start location of the mmw demo output packet, then extract the contents from the output packet.
       Each invocation of this function handles only one frame at a time and user needs to manage looping around to parse data for multiple frames.

        @param data                   : 1-demension byte array holds the the data read from mmw demo output. It ignorant of the fact that data is coming from UART directly or file read.  
            
        @return result                : parser result. 0 pass otherwise fail
        @return header_start_index      : the mmw demo output packet header start location
        @return total_packet_num_bytes   : the mmw demo output packet lenght           
        @return num_det_obj             : the number of detected objects contained in this mmw demo output packet          
        @return num_tlv                : the number of TLV contained in this mmw demo output packet           
        @return sub_frame_number        : the sbuframe index (0,1,2 or 3) of the frame contained in this mmw demo output packet
        @return detected_x_array       : 1-demension array holds each detected target's x of the mmw demo output packet
        @return detected_y_array       : 1-demension array holds each detected target's y of the mmw demo output packet
        @return detected_z_array       : 1-demension array holds each detected target's z of the mmw demo output packet
        @return detected_v_array       : 1-demension array holds each detected target's v of the mmw demo output packet
        @return detected_range_array   : 1-demension array holds each detected target's range profile of the mmw demo output packet
        @return detected_azimuth_array : 1-demension array holds each detected target's azimuth of the mmw demo output packet
        @return detected_elev_angle_array : 1-demension array holds each detected target's elevAngle of the mmw demo output packet
        @return detected_snr_array     : 1-demension array holds each detected target's snr of the mmw demo output packet
        @return detected_noise_array   : 1-demension array holds each detected target's noise of the mmw demo output packet
    """

    read_num_bytes = len(data)

    header_number_bytes = 40   

    detected_x_array = []
    detected_y_array = []
    detected_z_array = []
    detected_v_array = []
    detected_range_array = []
    detected_azimuth_array = []
    detected_elev_angle_array = []
    detected_snr_array = []
    detected_noise_array = []

    result = ParserStatus.TC_PASS

    # call parser_helper() function to find the output packet header start location and packet size 
    (header_start_index, total_packet_num_bytes, num_det_obj, num_tlv, sub_frame_number) = initial_process_data(data)
                         
    if header_start_index == -1:
        result = ParserStatus.TC_FAIL
    else:
        next_header_start_index = header_start_index + total_packet_num_bytes 

        if header_start_index + total_packet_num_bytes > read_num_bytes:
            result = ParserStatus.TC_FAIL
        elif next_header_start_index + 8 < read_num_bytes and checkMagicPattern(data[next_header_start_index:next_header_start_index+8:1]) == 0:
            result = ParserStatus.TC_FAIL
        elif num_det_obj <= 0:
            result = ParserStatus.TC_FAIL
        elif sub_frame_number > 3:
            result = ParserStatus.TC_FAIL
        else: 
            # process the 1st TLV
            tlv_start = header_start_index + header_number_bytes
                                                    
            tlv_type    = ByteUtils.get_uint32(data[tlv_start+0:tlv_start+4:1])
            tlv_len     = ByteUtils.get_uint32(data[tlv_start+4:tlv_start+8:1])       
            offset = 8
                    
            print("The 1st TLV") 
            print("    type %d" % (tlv_type))
            print("    len %d bytes" % (tlv_len))
                                                    
            # the 1st TLV must be type 1
            if tlv_type == 1 and tlv_len < total_packet_num_bytes:#MMWDEMO_UART_MSG_DETECTED_POINTS
                         
                # TLV type 1 contains x, y, z, v values of all detect objects. 
                # each x, y, z, v are 32-bit float in IEEE 754 single-precision binary floating-point format, so every 16 bytes represent x, y, z, v values of one detect objects.    
                
                # for each detect objects, extract/convert float x, y, z, v values and calculate range profile and azimuth                           
                for obj in range(num_det_obj):
                    # convert byte0 to byte3 to float x value
                    x = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlv_start + offset:tlv_start + offset+4:1]),'hex'))[0]

                    # convert byte4 to byte7 to float y value
                    y = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlv_start + offset+4:tlv_start + offset+8:1]),'hex'))[0]

                    # convert byte8 to byte11 to float z value
                    z = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlv_start + offset+8:tlv_start + offset+12:1]),'hex'))[0]

                    # convert byte12 to byte15 to float v value
                    v = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlv_start + offset+12:tlv_start + offset+16:1]),'hex'))[0]

                    # calculate range profile from x, y, z
                    comp_detected_range = math.sqrt((x * x)+(y * y)+(z * z))

                    # calculate azimuth from x, y           
                    if y == 0:
                        if x >= 0:
                            detected_azimuth = 90
                        else:
                            detected_azimuth = -90 
                    else:
                        detected_azimuth = math.atan(x/y) * 180 / math.pi

                    # calculate elevation angle from x, y, z
                    if x == 0 and y == 0:
                        if z >= 0:
                            detected_elev_angle = 90
                        else: 
                            detected_elev_angle = -90
                    else:
                        detected_elev_angle = math.atan(z/math.sqrt((x * x)+(y * y))) * 180 / math.pi
                            
                    detected_x_array.append(x)
                    detected_y_array.append(y)
                    detected_z_array.append(z)
                    detected_v_array.append(v)
                    detected_range_array.append(comp_detected_range)
                    detected_azimuth_array.append(detected_azimuth)
                    detected_elev_angle_array.append(detected_elev_angle)
                                                                
                    offset = offset + 16
                # end of for obj in range(num_det_obj) for 1st TLV
                                                            
            # Process the 2nd TLV
            tlv_start = tlv_start + 8 + tlv_len
                                                    
            tlv_type    = ByteUtils.get_uint32(data[tlv_start+0:tlv_start+4:1])
            tlv_len     = ByteUtils.get_uint32(data[tlv_start+4:tlv_start+8:1])      
            offset = 8
                    
            print("The 2nd TLV") 
            print("    type %d" % (tlv_type))
            print("    len %d bytes" % (tlv_len))
                                                            
            if tlv_type == 7: 
                
                # TLV type 7 contains snr and noise of all detect objects.
                # each snr and noise are 16-bit integer represented by 2 bytes, so every 4 bytes represent snr and noise of one detect objects.    
            
                # for each detect objects, extract snr and noise                                            
                for obj in range(num_det_obj):
                    # byte0 and byte1 represent snr. convert 2 bytes to 16-bit integer
                    snr   = ByteUtils.get_uint16(data[tlv_start + offset + 0:tlv_start + offset + 2:1])
                    # byte2 and byte3 represent noise. convert 2 bytes to 16-bit integer 
                    noise = ByteUtils.get_uint16(data[tlv_start + offset + 2:tlv_start + offset + 4:1])

                    detected_snr_array.append(snr)
                    detected_noise_array.append(noise)
                                                                    
                    offset = offset + 4
            else:
                for obj in range(num_det_obj):
                    detected_snr_array.append(0)
                    detected_noise_array.append(0)
            # end of if tlv_type == 7

            print("                  x(m)         y(m)         z(m)        v(m/s)    Com0range(m)  azimuth(deg)  elevAngle(deg)  snr(0.1dB)    noise(0.1dB)")
            for obj in range(num_det_obj):
                print("    obj%3d: %12f %12f %12f %12f %12f %12f %12d %12d %12d" % (obj, detected_x_array[obj], detected_y_array[obj], detected_z_array[obj], detected_v_array[obj], detected_range_array[obj], detected_azimuth_array[obj], detected_elev_angle_array[obj], detected_snr_array[obj], detected_noise_array[obj]))

    return (result, header_start_index, total_packet_num_bytes, num_det_obj, num_tlv, sub_frame_number, detected_x_array, detected_y_array, detected_z_array, detected_v_array, detected_range_array, detected_azimuth_array, detected_elev_angle_array, detected_snr_array, detected_noise_array)




    









