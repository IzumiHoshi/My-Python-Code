import struct
import numpy as np


class TempInfo:
    id = 1
    name = "Template"
    point_number_of_template = 8100
    point_number_of_waypoints = 422

    points = np.zeros((10, 3))
    waypoints = np.zeros((10, 6))


def PackTempInfo(fobj, info):
    # 转换成struct可用的类型
    utf8_str = info.name.encode('utf-8')
    list_of_points = info.points.flatten().tolist()
    list_of_waypoints = info.waypoints.flatten().tolist()

    # 转换文件头
    format_str = "iiii%dsii" % utf8_str.__len__()
    bytes_data = struct.pack(format_str, info.id, info.point_number_of_template,
                             info.point_number_of_waypoints, info.name.__len__(),
                             utf8_str, list_of_points.__len__(), list_of_waypoints.__len__())
    fobj.write(bytes_data)

    # 转换point
    format_str = "%df" % list_of_points.__len__()
    bytes_data = struct.pack(format_str, *list_of_points)
    fobj.write(bytes_data)

    # 转换waypoint
    format_str = "%df" % list_of_waypoints.__len__()
    bytes_data = struct.pack(format_str, *list_of_waypoints)
    fobj.write(bytes_data)


def UnPackTempInfo(fobj):
    info = TempInfo()

    # 解析文件头
    format_str = "iiii"
    bytes_data = fobj.read(16)
    unpack_data = struct.unpack(format_str, bytes_data)

    info.id = unpack_data[0]
    info.point_number_of_template = unpack_data[1]
    info.point_number_of_waypoints = unpack_data[2]
    name_len = unpack_data[3]

    # 解析name string
    format_str = "%ds" % name_len
    bytes_data = fobj.read(name_len)
    unpack_data = struct.unpack(format_str, bytes_data)
    info.name = unpack_data[0].decode('utf-8')

    # 解析list长度
    format_str = "ii"
    bytes_data = fobj.read(8)
    unpack_data = struct.unpack(format_str, bytes_data)
    len1 = unpack_data[0]
    len2 = unpack_data[1]

    # 解析points
    format_str = "%df" % len1
    bytes_data = fobj.read(len1*4)
    unpack_data = struct.unpack(format_str, bytes_data)
    info.points = list(unpack_data)

    # 解析waypoints
    format_str = "%df" % len2
    bytes_data = fobj.read(len2*4)
    unpack_data = struct.unpack(format_str, bytes_data)
    info.waypoints = list(unpack_data)

    return info


if __name__ == "__main__":
    f = open("output.data", "wb")
    inf = TempInfo()
    PackTempInfo(f, inf)
    f.close()

    f = open("output.data", 'rb')
    new_inf = UnPackTempInfo(f)
    f.close()
