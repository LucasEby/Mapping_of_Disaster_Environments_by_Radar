import struct
import math
import binascii
import codecs
from enum import Enum
from typing import Tuple, List, Union

class ParserStatus(Enum):
    TC_PASS = 0
    TC_FAIL = 1

class BytesUtils:
    @classmethod
    def get_uint32(cls, data: bytes) -> int:
        return (data[0] +
                data[1]*256 +
                data[2]*65536 +
                data[3]*16777216)
    
    @classmethod
    def get_uint16(cls, data: bytes) -> int:
        return (data[0] +
                data[1]*256)

    @classmethod
    def get_hex(cls, data: bytes) -> bytes:
        return (binascii.hexlify(data[::-1]))

    @classmethod
    def check_magic_pattern(cls, data: bytes) -> int:
        found = 0
        if (data[0] == 2 and data[1] == 1 and data[2] == 4 and data[3] == 3 and data[4] == 6 and data[5] == 5 and data[6] == 8 and data[7] == 7):
            found = 1
        return (found)

class PacketInfo:
    header_start_index: int
    packet_length: int
    number_detected_objects: int
    number_tlv: int
    frame_number: int
    sub_frame_number: int
    time_cpu_cylces: int

    def __init__(self, header_start_index: int = -1, packet_length: int = -1, number_detected_objects: int = -1, number_tlv: int = -1, frame_number: int = -1, sub_frame_number: int = -1, time_cpu_cycles: int = -1):
        self.header_start_index = header_start_index
        self.packet_length = packet_length
        self.number_detected_objects = number_detected_objects
        self.number_tlv = number_tlv
        self.frame_number = frame_number
        self.sub_frame_number = sub_frame_number
        self.time_cpu_cycles = time_cpu_cycles

class DetectedObject:
    x: float
    y: float
    z: float
    v: float
    range: float
    azimuth: float
    elev_angle: float
    snr: float
    noise: float

    def __init__(self, x: float=0.0, y: float=0.0, z: float=0.0, v: float=0.0, range: float=0.0, azimuth: float=0.0, elev_angle: float=0.0, snr: float=0.0, noise: float=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.v = v
        self.range = range
        self.azimuth = azimuth
        self.elev_angle = elev_angle
        self.snr = snr
        self.noise = noise
    
    def tlv_type_1(x: float, y: float, z: float, v: float, range: float, azimuth: float, elev_angle: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.v = v
        self.range = range
        self.azimuth = azimuth
        self.elev_angle = elev_angle
        return self

    def tlv_type_7(snr: float, noise: float) -> None:
        self.snr = snr
        self.noise = noise
        return

    def __repr__(self) -> str:
        return str(self.__dict__)

class PacketHandler:
    HEADER_BYTE_SIZE: int = 40
    status: ParserStatus
    
    def __init__(self):
        self.status = None

    def _parse_packet_info(data: bytes) -> PacketInfo:
        header_start_index = -1
        num_bytes = len(data)

        for index in range(num_bytes):
            if BytesUtils.check_magic_pattern(data[index:index+8:1]) == 1:
                header_start_index = index
                break

        if header_start_index != -1:
            packet_length = BytesUtils.get_uint32(
                data[header_start_index+12:header_start_index+16:1]
            )
            number_detected_objects = BytesUtils.get_uint32(
                data[header_start_index+28:header_start_index+32:1]
            )
            number_tlv = BytesUtils.get_uint32(
                data[header_start_index+32:header_start_index+36:1]
            )
            frame_number = BytesUtils.get_uint32(
                data[header_start_index+20:header_start_index+24:1]
            )
            sub_frame_number = BytesUtils.get_uint32(
                data[header_start_index+36:header_start_index+40:1]
            )
            time_cpu_cycles = BytesUtils.get_uint32(
                data[header_start_index+24:header_start_index+28:1]
            )
            return PacketInfo(packet_length, number_detected_objects, number_tlv, frame_number, sub_frame_number, time_cpu_cycles)
        return PacketInfo()

    @classmethod
    def _get_status(cls, data: bytes, packet_info: PacketInfo()) -> None:
        status = None
        if packet_info.header_start_index == -1:
            return ParserStatus.TC_FAIL
        elif packet_info.number_detected_objects < 0:
            return ParserStatus.TC_FAIL
        elif packet_info.sub_frame_number > 3:
            return ParserStatus.TC_FAIL
        elif (packet_info.header_start_index + packet_info.packet_length) > len(data):
            return ParserStatus.TC_FAIL
        else:
            next_header_start_index = packet_info.header_start_index + packet_info.packet_length
            if (next_header_start_index + 8) < packet_info.packet_length and \
                not(BytesUtils.check_magic_pattern(data[next_header_start_index:next_header_start_index+8:1])):
                return ParserStatus.TC_FAIL
        return ParserStatus.TC_PASS
    
    @classmethod
    def _compute_range(cls, x: float, y: float, z: float) -> float:
        return sqrt((x*x) + (y*y) + (z*z))

    @classmethod
    def _computer_azimuth(cls, x: float, y: float) -> float:
        if y == 0.0:
            if x >= 0.0:
                return 90.0
            else:
                return 90.0
        else:
            return math.atan(x/y)*(180/math.pi)
    
    @classmethod
    def _compute_elev_angle(cls, x: float, y: float, z: float) -> float:
        if x == 0.0 and y == 0.0:
            if z >= 0.0:
                return 90.0
            else:
                return -90.0
        else:
            return math.atan(z/math.sqrt((x*x)+(y*y)))*(180/math.pi)

    @classmethod
    def _parse_tlvs(cls, data: bytes, packet_info: PacketInfo) -> List[DetectedObject]:
        detected_objects = []
        for _ in range(packet_info.number_detected_objects):
            detected_objects.append(DetectedObject())
        tlv_start = packet_info.header_start_index + 40
        tlv_type = BytesUtils.get_uint32(data[(tlv_start+0):(tlv_start+4):1])
        tlv_len = BytesUtils.get_uint32(data[(tlv_start+4):(tlv_start+8):1])
        offset = 8

        if tlv_type == 1 and tlv_len < packet_info.packet_length:
            for obj in range(packet_info.number_detected_objects):
                x = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlv_start + offset:tlv_start + offset+4:1]),'hex'))[0]
                y = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlv_start + offset+4:tlv_start + offset+8:1]),'hex'))[0]
                z = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlv_start + offset+8:tlv_start + offset+12:1]),'hex'))[0]
                v = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlv_start + offset+12:tlv_start + offset+16:1]),'hex'))[0]
                range_ = cls._compute_range(x, y, z)
                azimuth = cls._computer_azimuth(x, y)
                elev_angle = cls._compute_elev_angle(x, y, z)
        
                detected_objects[obj].tlv_type_1(x, z, v, range, azimuth, elev_angle)
                offset = offset + 16

        #tlv_start = tlv_start + 8 + tlv_len
        #tlv_type = BytesUtils.get_uint32(data[tlv_start+0:tlv_start+4:1])
        #tlv_len = BytesUtils.get_uint32(data[tlv_start+4:tlv_start+8:1])
        #offset = 8

        #if tlv_type == 7:
        #    for obj in range(packet_info.number_detected_objects):
        #        snr = BytesUtils.get_uint16(data[tlv_start + offset + 0:tlv_start + offset + 2:1])
        #        noise = BytesUtils().get_hex(data[tlv_start + offest + 2:tlv_start + offset + 4:1])
        #        detected_objects[obj].tlv_type_7(snr, noise)
        #        offset = offest + 4
    
        return detected_objects
          
    @classmethod
    def parser(cls, data: bytes) -> Union[List[DetectedObject], None]:
        packet_info = cls._parse_packet_info(data)
        status = cls._get_status(data, packet_info)
        if status == ParserStatus.TC_PASS:
            #return "got same data to parse bitch but this bitch aint doing shit bitch"
            return cls._parse_tlvs(data, packet_info)
        else:
            return None
