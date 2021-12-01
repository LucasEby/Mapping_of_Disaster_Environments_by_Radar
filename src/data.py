# Standard Library Imports
from struct import unpack
from math import sqrt, atan, cos, sin
from binascii import hexlify
from codecs import decode
from enum import Enum
from typing import List, Union, Tuple, Any, Dict

# Package Imports
from serial import Serial
import json
import csv
import math

# Self Imports
from control import Ports

class ParserStatus(Enum):
    """ParserStatus enumeration for parsing status
    """
    TC_PASS = 0
    TC_FAIL = 1

class BytesUtils:
    """BytesUtils are utilities for handling bytes objects
    """

    @classmethod
    def get_uint32(cls, data: bytes) -> int:
        """get_uint32 parse an unsigned 32 bit integer from a bytes object

        Parameters
        ----------
        data : bytes
            the bytes object

        Returns
        -------
        int
            the parsed integer
        """
        try:
            return (data[0] + data[1]*256 + data[2]*65536 + data[3]*16777216)
        except IndexError:
            return None

    @classmethod
    def get_uint16(cls, data: bytes) -> int:
        """get_uint16 parse an unsigned 16 bit integer from a bytes object

        Parameters
        ----------
        data : bytes
            the bytes object

        Returns
        -------
        int
            the parsed integer
        """
        try:
            return (data[0] + data[1]*256)
        except IndexError:
            return None

    @classmethod
    def check_magic_pattern(cls, data: bytes) -> int:
        """check_magic_pattern get the magic pattern (of IWR6843) in a bytes object

        Parameters
        ----------
        data : bytes
            the bytes object

        Returns
        -------
        int
            the 0 or 1 value representing if a magic pattern was found in the IWR6843
        """
        found = 0
        try:
            if (data[0] == 2 and data[1] == 1 and data[2] == 4 and data[3] == 3 and data[4] == 6 and data[5] == 5 and data[6] == 8 and data[7] == 7):
                found = 1
        except IndexError:
            pass
        return found

class MathUtils:
    """MathUtils are utiliites for performing calculations on recieved data
    """
    # One hundred eighty over pi for radian to degrese conversion
    ONEHUNDRENDEIGHTYOVERPI = 57.2957795131

    # Offest for Y-axis rotation
    Y_OFF = 0

    @classmethod
    def radians_to_degrees(cls, angle: float) -> float:
        """radians_to_degrees convert an angle from radians to degrees

        Parameters
        ----------
        angle : float
            an angle in radians

        Returns
        -------
        float
            the angle in degrees
        """
        return cls.ONEHUNDRENDEIGHTYOVERPI*angle

    @classmethod
    def get_range(cls, x: float, y: float, z: float) -> float:
        """get_range calculate the range (norm) from a measured x, y, and z value

        Parameters
        ----------
        x : float
            the measured x value
        y : float
            the measured y value
        z : float
            the measured z value

        Returns
        -------
        float
            the calculated range
        """
        return sqrt((x**2) + (y**2) + (z**2))

    @classmethod
    def get_azimuth(cls, x: float, y: float) -> float:
        """get_azimuth calculate the azimuth angle from a measured x and y value

        Parameters
        ----------
        x : float
            the measured x value
        y : float
            the measured y value

        Returns
        -------
        float
            the meausred azimuth in degrees
        """
        if y != 0.0:
            return cls.radians_to_degrees(atan(x/y))
        else:
            if x < 0.0:
                return -90.0
            else:
                return 90.0

    @classmethod
    def get_elev_angle(cls, x: float, y: float, z: float) -> float:
        """get_elev_angle calculate the elevation angle from a measured x, y, and z value

        Parameters
        ----------
        x : float
            the measured x value
        y : float
            the measured y value
        z : float
            the measured z value

        Returns
        -------
        float
            the measured elevation angle in degrees
        """
        if x == 0.0 and y == 0.0:
            if z < 0.0:
                return -90.0
            else:
                return 90.0
        else:
            return cls.radians_to_degrees(atan(z/sqrt((x**2)+(y**2))))

    @classmethod
    def b_to_d_rotation(cls, x: float, y: float, z: float, h: float, v: float) -> Tuple[float, float, float]:
        """b_to_d_rotation performs rotation of coordinates horizontally and vertically

        Parameters
        ----------
        x : float
            the x-coordinate
        y : float
            the y-coordinate
        z : float
            the z-coordinate
        h : float
            the horizontal angle of rotation
        v : float
            the vertical angle of rotation

        Returns
        -------
        Tuple[float, float, float]
            the rotated x, y, and z coordinates
        """
        rotated_x = x * math.cos(h) - (z * math.sin(h))
        rotated_y = x * math.cos(v) * math.sin(h) + y * math.sin(v) + z * math.cos(h) * math.cos(v)
        rotated_z = x * math.sin(h) * math.sin(v) - y * math.cos(v) + z * math.cos(h) * math.sin(v)
        #pos_array = [rotated_x, rotated_y, rotated_z]

        """
        rotated_x = \
            (x * cos(h)) + \
            (sin(h) * cos(v) * (cls.Y_OFF - y)) + \
            (sin(h) * sin(v) * z)
        rotated_y = \
            ((y - cls.Y_OFF) * sin(v)) + \
            (z * cos(v))
        rotated_z = \
            (-x * sin(h)) + \
            ((cls.Y_OFF - y) * cos(h) * cos(v)) + \
            (z * cos(h) * sin(v))
        """
        return rotated_x, rotated_y, rotated_z

class Utils:
    """Utils are a set of more generic utilities needed for this program and handling data
    """

    @classmethod
    def dump_json_default(cls, obj: Any) -> Union[Dict, str]:
        """dump_json_default default function that dumps an object to a json format

        Parameters
        ----------
        obj : Any
            the object

        Returns
        -------
        Union[Dict, str]
            returns the obj.__dict__ or obj.__repr__
        """
        try:
            return obj.__dict__
        except AttributeError:
            try:
                str(obj)
            except:
                return object.__repr__(obj)

    @classmethod
    def dump_to_json(cls, data: Dict, file: str) -> None:
        """dump_to_json dumps a Dict into a JSON

        Parameters
        ----------
        data : Dict
            the Dict to dump
        file : str
            the JSON filepath
        """
        with open(file, "w") as write_file:
            json.dump(data, write_file, indent=4, default=Utils.dump_json_default)

    @classmethod
    def open_json(cls, file: str) -> Dict:
        """open_json opens a JSON file

        Parameters
        ----------
        file : str
            the JSON filepath

        Returns
        -------
        Dict
            a dict representing the JSON objects in the file
        """
        with open(file, "r") as read_file:
            return json.load(read_file)

    @classmethod
    def create_csv(cls, filepath: str, labels: list) -> None:
        """create_csv creates a CSV file

        Parameters
        ----------
        filepath : str
            the filepath
        labels : list
            the labels (headers) for the csv row
        """
        with open(filepath, 'w+') as file:
            writer = csv.writer(file, lineterminator='\r')
            writer.writerow(labels)

    @classmethod
    def write_row_csv(cls, filepath: str, values: list) -> None:
        """write_row_csv writes a list of values into a row in the CSV file

        Parameters
        ----------
        filepath : str
            the filepath
        values : list
            the values to write into a CSV row
        """
        with open(filepath, 'a+') as file:
            writer = csv.writer(file, lineterminator='\r')
            writer.writerow(values)

class PacketInfo:
    """PacketInfo stores info on a data packet recieved from the IWR6843
    """

    header_start_index: int
    packet_length: int
    number_detected_objects: int
    number_tlv: int
    frame_number: int
    sub_frame_number: int
    time_cpu_cylces: int

    def __init__(self, header_start_index: int = -1, packet_length: int = -1, number_detected_objects: int = -1, number_tlv: int = -1, frame_number: int = -1, sub_frame_number: int = -1, time_cpu_cycles: int = -1):
        """__init__ initialize this object

        Parameters
        ----------
        header_start_index : int, optional
            the index indicating the start of the header, by default -1
        packet_length : int, optional
            the length of the packet in bytes, by default -1
        number_detected_objects : int, optional
            the number of detected objects in the packet, by default -1
        number_tlv : int, optional
            the number of tlv objects in the packet, by default -1
        frame_number : int, optional
            the number of frames, by default -1
        sub_frame_number : int, optional
            the number of sub frames, by default -1
        time_cpu_cycles : int, optional
            the time of cpu cycles in retrieving the objects, by default -1
        """
        self.header_start_index = header_start_index
        self.packet_length = packet_length
        self.number_detected_objects = number_detected_objects
        self.number_tlv = number_tlv
        self.frame_number = frame_number
        self.sub_frame_number = sub_frame_number
        self.time_cpu_cycles = time_cpu_cycles

class DetectedObject:
    """DetectedObject stores info on a detected object parsed from a packet from the IWR6843
    """
    x: float
    y: float
    z: float
    v: float
    computed_range: float
    azimuth: float
    elev_angle: float
    snr: float
    noise: float

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, v: float = 0.0, computed_range: float = 0.0, azimuth: float = 0.0, elev_angle: float = 0.0, snr: float = 0.0, noise: float = 0.0):
        """__init__ initialize this object

        Parameters
        ----------
        x : float, optional
            the measured x coordinate of the object, by default 0.0
        y : float, optional
            the measured y coordinate of the object, by default 0.0
        z : float, optional
            the measured z coordinate of the object, by default 0.0
        v : float, optional
            the measured velocity of the object, by default 0.0
        range : float, optional
            the measured range of the object, by default 0.0
        azimuth : float, optional
            the measured azimuth angle of the object, by default 0.0
        elev_angle : float, optional
            the measured elevation angle of the object, by default 0.0
        snr : float, optional
            the measured signal to noise ratio of the object, by default 0.0
        noise : float, optional
            the measured noise of the object, by default 0.0
        """
        self.x = x
        self.y = y
        self.z = z
        self.v = v
        self.computed_range = computed_range
        self.azimuth = azimuth
        self.elev_angle = elev_angle
        self.snr = snr
        self.noise = noise

    def tlv_type_1(self, x: float, y: float, z: float, v: float, computed_range: float, azimuth: float, elev_angle: float) -> None:
        """tlv_type_1 update this object based on a TLV type 1 sub-packet

        Parameters
        ----------
        x : float
            the measured x coordinate
        y : float
            the measured y coordinate
        z : float
            the measured z coordinate
        v : float
            the measured velocity
        computed_range : float
            the measured range
        azimuth : float
            the measured azimuth angle
        elev_angle : float
            the measured elevation angle

        Returns
        -------
        None
        """
        self.x = x
        self.y = y
        self.z = z
        self.v = v
        self.computed_range = computed_range
        self.azimuth = azimuth
        self.elev_angle = elev_angle
        return

    def tlv_type_7(self, snr: float, noise: float) -> None:
        """tlv_type_7 updates this object based on a TLV type 7 sub-packet

        Parameters
        ----------
        x : float
            the measured x coordinate
        y : float
            the measured y coordinate
        z : float
            the measured z coordinate
        v : float
            the measured velocity
        computed_range : float
            the measured range
        azimuth : float
            the measured azimuth angle
        elev_angle : float
            the measured elevation angle

        Returns
        -------
        None
        """
        self.snr = snr
        self.noise = noise
        return

class DetectedObjectVoxel(DetectedObject):
    """DetectedObjectVoxel DetectedObjectVoxel stores info on a detected object parsed from a packet from the IWR6843 as well as functioning as a voxel
    """
    OBJECT_THRESHOLD = 3

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, v: float = 0.0, computed_range: float = 0.0, azimuth: float = 0.0, elev_angle: float = 0.0, snr: float = 0.0, noise: float = 0.0, resolution: float = 0.04):
        """__init__ initialize this object

        Parameters
        ----------
        x : float, optional
            the measured x coordinate of the object, by default 0.0
        y : float, optional
            the measured y coordinate of the object, by default 0.0
        z : float, optional
            the measured z coordinate of the object, by default 0.0
        v : float, optional
            the measured velocity of the object, by default 0.0
        range : float, optional
            the measured range of the object, by default 0.0
        azimuth : float, optional
            the measured azimuth angle of the object, by default 0.0
        elev_angle : float, optional
            the measured elevation angle of the object, by default 0.0
        snr : float, optional
            the measured signal to noise ratio of the object, by default 0.0
        noise : float, optional
            the measured noise of the object, by default 0.0
        """
        super(DetectedObjectVoxel, self).__init__(x,y,z,v,computed_range,azimuth,elev_angle,snr,noise)
        self.resolution = resolution
        self.x = self._round_pos_to_res(self.x)
        self.y = self._round_pos_to_res(self.y)
        self.z = self._round_pos_to_res(self.z)
        self.hits = 1
        self.is_object = False

    def _round_pos_to_res(self, pos: float) -> float:
        """_round_pos_to_res rounds a passed in position to the nearest interval of resolution used for the voxel

        Parameters
        ----------
        pos : float
            the position that is passed in

        Returns
        -------
        float
            the position rounded to the nearest interval of the resolution
        """
        return round(pos/self.resolution)*self.resolution

    def _round_pos(self, pos: float) -> int:
        """_round_pos rounds a passed in position by dividing the position by the resolution used for
        the voxel so that hashing can occur on the position.

        In order to properly hash this class for using a hash table, the positions need to be represented as
        integers, as hashing does not typically occur on floating numbers.
        Since the program relies upon rounding to the resolution used for the voxels, this function allows
        the integers to be rounded towards an integer by dividing the position by the resolution, which
        always results in a whole number.

        Parameters
        ----------
        pos : float
            the position that is passed in

        Returns
        -------
        int
            the position rounded to an integer by the division of the resolution
        """
        return int(pos/self.resolution)

    def __hash__(self) -> int:
        """__hash__ generates a hash for this voxel for a hash table

        A hash is needed so that a hash table can be used efficiently to compare and iterate through different voxels.
        Only the x, y, and z positions are used for hashing.

        Returns
        -------
        int
            the hash of this voxel
        """
        # Hashing function from here: https://dmauro.com/post/77011214305/a-hashing-function-for-x-y-z-coordinates
        x = self._round_pos(self.x)
        y = self._round_pos(self.y)
        z = self._round_pos(self.z)
        x = 2*x if x >= 0 else -2*x - 1
        y = 2*y if y >= 0 else -2*y - 1
        z = 2*z if z >= 0 else -2*z - 1
        maximum = max([x, y, z])
        hash = pow(maximum, 3) + (2 * maximum * z) + z
        if (maximum == z):
            hash += pow(max([x, y]), 2)
        if (y >= x):
            hash += x + y
        else:
            hash += y
        return hash

    def __eq__(self, other: object) -> bool:
        """__eq__ compare this object to another object

        Parameters
        ----------
        other : object
            the other object

        Returns
        -------
        bool
            False if the other object is not an instance of this object, True if the hashes of the other object and this object are equal
        """
        if isinstance(other, DetectedObjectVoxel):
            return other.__hash__() == self.__hash__()
        else:
            return False

    def visit(self) -> None:
        """visit visit this voxel
        """
        self.hits += 1
        self.is_object = self.hits > self.OBJECT_THRESHOLD
        return

def compare_detected_object_voxels(kv1: Tuple[DetectedObjectVoxel, DetectedObjectVoxel], kv2: Tuple[DetectedObjectVoxel, DetectedObjectVoxel]) -> int:
    """compare_detected_object_voxels key function to compare two detected object voxels

    Parameters
    ----------
    kv1 : Tuple[DetectedObjectVoxel, DetectedObjectVoxel]
        a key, value pair of a detected object
    kv2 : Tuple[DetectedObjectVoxel, DetectedObjectVoxel]
        a key, value pair of a detected object

    Returns
    -------
    int
        the comparision value
    """
    # Get each voxel (key)
    voxel1 = kv1[1]
    voxel2 = kv2[1]
    return (voxel1.x-voxel2.x)+(voxel1.y-voxel2.y)+(voxel1.z-voxel2.z)

class PacketHandler:
    """PacketHandler handles and parses a packet from the IWR6843
    """

    # The byte size of a header
    HEADER_BYTE_SIZE: int = 40
    OBJECT = DetectedObjectVoxel

    def __init__(self):
        pass

    @classmethod
    def _parse_packet_info(cls, data: bytes) -> PacketInfo:
        """_parse_packet_info parses the packet info from a recieved nbuffer

        Parameters
        ----------
        data : bytes
            the recieved buffer

        Returns
        -------
        PacketInfo
            the info on the packet
        """

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
            frame_number = BytesUtils.get_uint32(
                data[header_start_index+20:header_start_index+24:1]
            )
            time_cpu_cycles = BytesUtils.get_uint32(
                data[header_start_index+24:header_start_index+28:1]
            )
            number_detected_objects = BytesUtils.get_uint32(
                data[header_start_index+28:header_start_index+32:1]
            )
            number_tlv = BytesUtils.get_uint32(
                data[header_start_index+32:header_start_index+36:1]
            )
            sub_frame_number = BytesUtils.get_uint32(
                data[header_start_index+36:header_start_index+40:1]
            )
            return PacketInfo(header_start_index, packet_length, number_detected_objects, number_tlv, frame_number, sub_frame_number, time_cpu_cycles)
        return PacketInfo()

    @classmethod
    def _get_status(cls, data: bytes, packet_info: PacketInfo()) -> ParserStatus:
        """get_status get the status of a parsed packet (either fail or success) based on the packet info and read buffer

        Parameters
        ----------
        data : bytes
            the recieved buffer
        packet_info : PacketInfo
            the info on the packet

        Returns
        -------
        ParserStatus
            the status of the parsed packet
        """
        try:
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
                        (BytesUtils.check_magic_pattern(data[next_header_start_index:next_header_start_index+8:1]) == 0):
                    return ParserStatus.TC_FAIL
        except TypeError:
            return ParserStatus.TC_FAIL
        return ParserStatus.TC_PASS

    @classmethod
    def _parse_tlvs(cls, data: bytes, packet_info: PacketInfo) -> List[DetectedObject]:
        """_parse_tlvs parse the sub-packet tlvs from a recieved buffer

        Parameters
        ----------
        data : bytes
            the recieved buffer
        packet_info : PacketInfo
            the packet info

        Returns
        -------
        List[DetectedObject]
            the list of detected objects updated with the sub-packet information
        """

        detected_objects = []
        for _ in range(packet_info.number_detected_objects):
            detected_objects.append(cls.OBJECT())
        tlv_start = packet_info.header_start_index + 40
        tlv_type = BytesUtils.get_uint32(data[(tlv_start+0):(tlv_start+4):1])
        tlv_len = BytesUtils.get_uint32(data[(tlv_start+4):(tlv_start+8):1])
        offset = 8

        if tlv_type == 1 and tlv_len < packet_info.packet_length:
            for obj in range(packet_info.number_detected_objects):
                x = unpack('<f', decode(hexlify(data[tlv_start + offset:tlv_start + offset+4:1]),'hex'))[0]
                y = unpack('<f', decode(hexlify(data[tlv_start + offset+4:tlv_start + offset+8:1]),'hex'))[0]
                z = unpack('<f', decode(hexlify(data[tlv_start + offset+8:tlv_start + offset+12:1]),'hex'))[0]
                v = unpack('<f', decode(hexlify(data[tlv_start + offset+12:tlv_start + offset+16:1]),'hex'))[0]
                computed_range = MathUtils.get_range(x, y, z)
                azimuth = MathUtils.get_azimuth(x, y)
                elev_angle = MathUtils.get_elev_angle(x, y, z)

                detected_objects[obj].tlv_type_1(x, y, z, v, computed_range, azimuth, elev_angle)
                offset = offset + 16

        try:
            tlv_start = tlv_start + 8 + tlv_len
            tlv_type = BytesUtils.get_uint32(data[tlv_start+0:tlv_start+4:1])
            tlv_len = BytesUtils.get_uint32(data[tlv_start+4:tlv_start+8:1])
            offset = 8
        except TypeError:

            tlv_type = None

        if tlv_type == 7:
            for obj in range(packet_info.number_detected_objects):
                snr = BytesUtils.get_uint16(data[tlv_start + offset + 0:tlv_start + offset + 2:1])
                noise = BytesUtils.get_uint16(data[tlv_start + offset + 2:tlv_start + offset + 4:1])
                detected_objects[obj].tlv_type_7(snr, noise)
                offset = offset + 4

        return detected_objects

    @classmethod
    def parser(cls, data: bytes) -> Union[List[DetectedObject], None]:
        """parser the main parser for a recieved buffer

        Parameters
        ----------
        data : bytes
            the recieved buffer

        Returns
        -------
        Union[List[DetectedObject], None]
            the list of detected objects if the parser status is a pass, none if the parser status is a fail
        """
        # TODO: Check for another packet and return that packet as well
        packet_info = cls._parse_packet_info(data)
        status = cls._get_status(data, packet_info)
        if status == ParserStatus.TC_PASS:
            detected_objects = cls._parse_tlvs(data, packet_info)
            if len(detected_objects) > 0:
                return detected_objects
        return None

class Reader:
    """Reader reads from the data port of the IWR6843
    """

    data_port: Serial
    parser: PacketHandler

    def __init__(self, ports: Ports):
        """__init__ initialize the reader

        Parameters
        ----------
        data_port : Serial
            the data port to read from
        """
        self.data_port = ports.data_port
        self.parser = PacketHandler()

    def read(self) -> Union[List[DetectedObject], None]:
        """read read from the data port

        Returns
        -------
        Union[List[DetectedObject], None]
            the list of detected objects if the read buffer contains data, None if the read buffer does not have any data
        """
        read_buffer = self.data_port.read(self.data_port.inWaiting())
        if len(read_buffer) > 0:
            return self.parser.parser(read_buffer)
