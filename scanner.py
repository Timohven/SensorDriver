from ctypes import *
import pickle
import numpy as np
import plotly.graph_objects as go

ETHERNETSCANNER_TCPSCANNERDISCONNECTED = 0
ETHERNETSCANNER_TCPSCANNERCONNECTED = 3
ETHERNETSCANNER_PEAKSPERCMOSSCANLINEMAX	= 4
ETHERNETSCANNER_SCANXMAX = 2048
ETHERNETSCANNER_BUFFERSIZEMAX = 2050 * 2050
ETHERNETSCANNER_ERROR = 1
ETHERNETSCANNER_GETINFOSIZEMAX = 128 * 1024
# pointer, status = None, None
# lib = CDLL(r"C:\Users\Admin\PycharmProjects\SensorDriver\EthernetScanner\EthernetScanner.dll")

def connect(lib):
    print('Try to connect ...')
    EthernetScanner_Connect = lib.EthernetScanner_Connect
    EthernetScanner_Connect.restype = c_void_p
    EthernetScanner_Connect.argtypes = [c_char_p, c_char_p, c_int]
    EthernetScanner_GetConnectStatus = lib.EthernetScanner_GetConnectStatus
    EthernetScanner_GetConnectStatus.argtypes = [c_void_p, POINTER(c_int)]
    port = c_char_p(b"32001\0")
    addr = c_char_p(b"192.168.255.8\0")
    t = c_int(0)
    p_scanner = EthernetScanner_Connect(addr, port, t)

    attempt = 0
    ConnectionStatus = c_int()
    ConnectionStatus.value = 0
    p_ConnectionStatus = byref(ConnectionStatus)
    while ConnectionStatus.value != ETHERNETSCANNER_TCPSCANNERCONNECTED:
        EthernetScanner_GetConnectStatus(p_scanner, p_ConnectionStatus)
        # print(f'status of connection: {ConnectionStatus.value}')
        attempt += 1
        if attempt > 999999:
            print('Scanner isn`t connected! Number of attempts is more then 1000000!')
            break

    if p_scanner is None:
        print("Connection Error!")
        print(f"ConnectionStatus: {ConnectionStatus.value}")
    else:
        print(f'Scanner connected! Number of attempts is {attempt}')
        print(f"pointer: {p_scanner}, type: {type(p_scanner)}, ip: {addr.value}, port: {port.value}, time: {t.value}")
        print(f"ConnectionStatus: {ConnectionStatus.value}")

    return p_scanner, ConnectionStatus.value


def disconnect(lib, pointer):
    EthernetScanner_Disconnect = lib.EthernetScanner_Disconnect
    EthernetScanner_Disconnect.restype = c_void_p
    EthernetScanner_Disconnect.argtypes = [c_void_p]
    if EthernetScanner_Disconnect(pointer) == None: print('Connection closed!')
    else:
        print('Closing connection error!')


def getInfo(lib, pointer):
    EthernetScanner_GetInfo = lib.EthernetScanner_GetInfo
    EthernetScanner_GetInfo.argtypes = [c_void_p, c_char_p, c_int, c_char_p]
    str_info = b''.ljust(ETHERNETSCANNER_GETINFOSIZEMAX)
    info = c_char_p(str_info)
    buf = c_int(ETHERNETSCANNER_GETINFOSIZEMAX)
    mode = c_char_p(b'text')
    res = EthernetScanner_GetInfo(pointer, info, buf, mode)
    return info.value, res


def getXZIExtended(lib, pointer):
    EthernetScanner_GetXZIExtended = lib.EthernetScanner_GetXZIExtended
    EthernetScanner_GetXZIExtended.argtypes = [c_void_p,
                                               POINTER(c_double),
                                               POINTER(c_double),
                                               POINTER(c_int),
                                               POINTER(c_int),
                                               c_int,
                                               POINTER(c_uint),
                                               c_char_p,
                                               c_int,
                                               c_char_p,
                                               c_int,
                                               POINTER(c_int)]
    bufX = (c_double * (ETHERNETSCANNER_SCANXMAX * ETHERNETSCANNER_PEAKSPERCMOSSCANLINEMAX))()
    # print(f"cast: {cast(bufX, POINTER(c_double))}")

    bufZ = (c_double * (ETHERNETSCANNER_SCANXMAX * ETHERNETSCANNER_PEAKSPERCMOSSCANLINEMAX))()
    # bufZ = c_double * (ETHERNETSCANNER_SCANXMAX * ETHERNETSCANNER_PEAKSPERCMOSSCANLINEMAX)

    bufIntensity = (c_int * (ETHERNETSCANNER_SCANXMAX * ETHERNETSCANNER_PEAKSPERCMOSSCANLINEMAX))()
    # bufIntensity = c_int * (ETHERNETSCANNER_SCANXMAX * ETHERNETSCANNER_PEAKSPERCMOSSCANLINEMAX)

    bufSignalWidth = (c_int * (ETHERNETSCANNER_SCANXMAX * ETHERNETSCANNER_PEAKSPERCMOSSCANLINEMAX))()
    # bufSignalWidth = c_int * (ETHERNETSCANNER_SCANXMAX * ETHERNETSCANNER_PEAKSPERCMOSSCANLINEMAX)

    buf = c_int(ETHERNETSCANNER_SCANXMAX * ETHERNETSCANNER_PEAKSPERCMOSSCANLINEMAX)
    encoder = c_uint(0)
    uio = c_char(0)
    picCnt = c_int(0)

    dataLength = EthernetScanner_GetXZIExtended(pointer,
                                                bufX,
                                                bufZ,
                                                bufIntensity,
                                                bufSignalWidth,
                                                buf,
                                                byref(encoder),
                                                byref(uio),
                                                c_int(1000),
                                                None,
                                                c_int(0),
                                                byref(picCnt))
    # i = 0
    # for b in bufX:
    #     if b:
    #         print(b)
    #         i += 1
    # print(f"Number of valid points is: {i}")

    return dataLength, bufX, bufZ, bufIntensity


def transformData(bufX, bufZ, bufIntensity):
    X = np.array(bufX)
    Z = np.array(bufZ)
    I = np.array(bufIntensity)

    #arrX = X[np.logical_and(X != 0, Z != 0, I != 0)]
    arrX = X[(X != 0) & (Z != 0) & (I != 0)]
    # print(f'len X: {len(arrX)}, X: {arrX[0:10]}')
    # arrZ = Z[np.logical_and(X != 0, Z != 0, I != 0)]
    arrZ = Z[(X != 0) & (Z != 0) & (I != 0)]
    # print(f'len Z: {len(arrZ)}, Z: {arrZ[0:10]}')
    # arrI = I[np.logical_and(X != 0, Z != 0, I != 0)]
    arrI = I[(X != 0) & (Z != 0) & (I != 0)]
    # print(f'len I: {len(arrI)}, I: {arrI[0:10]}')
    arr = np.array([arrX, arrZ, arrI])
    # print(arr.shape)
    # saveToFile(np.hstack([arrX, arrZ, arrI]).reshape(-1))
    if arrX.size:
        mask = (arrX>=-20).any() and (arrX<=20).any()
        minZ = arrZ[mask].min()
    else:
        minZ = 0
    # print(minZ)
    return arr, minZ


def saveToFile(arr):
    np.save('d', arr)
    # print(f'current len: {len(arr)}')
    # print(f'cur arr: {arr}')
    # np.save('data1', arr)
    # arr0 = np.load('data1.npy')
    # print(f'old len: {len(arr0)}')
    # print(f'arr: {arr0}')

    # arr0 = np.genfromtxt('data.csv')
    # arr1 = np.vstack([arr0, arr])
    # np.savetxt('data.csv', arr1, fmt='%.4f')

    # print(f'old1 len: {len(arr0)}')
    # print(f'arr1: {arr0}')

    # arr0 = np.genfromtxt('data.csv')
    # print(f'old len: {len(arr0[2])}')
    # arr1 = np.vstack([arr0, arr])
    # np.savetxt('data.csv', arr, fmt='%.4f')

    # with open('data.txt', 'a+') as textFile:
    #     textFile.write(";".join(str(el) for el in arr[0,:]))
    #     textFile.write(";".join(str(el) for el in arr[1,:]))
    #     textFile.write(";".join(str(el) for el in arr[2,:]))


def loadFromFile():
    data = np.load('d.npy', allow_pickle=True)
    for el in data:
        print(el)
        print('next')

    # with np.load('d.npy', allow_pickle=True) as data:
    #     for el in data:
    #         print(el)


def makeFig(arr):
    fig = go.Figure(data=go.Scatter(x=arr[0, :],
                                    y=arr[1, :],
                                    mode='markers',
                                    marker=dict(size=2, color=arr[2, :], showscale=True)
                                    )
                    )
    fig.update_xaxes(showgrid=False,
                      zeroline=False,
                      range=[-60, 60],
                      # fixedrange=True,
                     )
    fig.update_yaxes(showgrid=False,
                      zeroline=False,
                      range=[300, 0],
                      # fixedrange=True,
                     )
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black')

    return fig

def makeFigInten(arr, xRange0, xRange1, yRange0, yRange1, minZ):
    fig = go.Figure(data=go.Scatter(x=arr[0, :],
                                    y=arr[1, :],
                                    name='geometry',
                                    mode='markers',
                                    marker=dict(size=2, color='white', showscale=False)
                                    )
                    )
    fig.add_trace(go.Scatter(x=[-20, 20],
                             y=[minZ, minZ],
                             mode='lines',
                             line_dash='dash',
                             name=minZ
                             )
                  )
    # arr[2, :] = arr[2, :]/20
    # fig.add_trace(go.Scatter(x=arr[0, :],
    #                          y=arr[2, :],
    #                          name='intensity',
    #                          mode='markers',
    #                          marker=dict(size=2, color='red', showscale=False)
    #                          )
    #               )

    fig.update_xaxes(showgrid=False,
                     zeroline=False,
                     range=[xRange0, xRange1],
                     fixedrange=True,
                     )
    fig.update_yaxes(showgrid=False,
                     zeroline=False,
                     range=[yRange0, yRange1],
                     fixedrange=True,
                     )
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black')

    return fig

def updateFif3D(fig3D, arr, n_intervals):
    fig3D.add_trace(go.Scatter3d(x=arr[0, :],
                                 y=arr[1, :],
                                 z=np.full(len(arr[0, :]), n_intervals / 1000),
                                 mode='markers',
                                 marker=dict(size=1, color='green')
                                 )
                    )
    return fig3D