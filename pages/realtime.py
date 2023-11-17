import dash
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from scanner import connect, getInfo, getXZIExtended, makeFig, makeFigInten, updateFif3D, saveToFile, loadFromFile
from ctypes import *
import numpy as np
import plotly.graph_objects as go

arr0 = [0]  # !!! only with this two rows
arr1 = np.zeros(1280 * 3)  # !!! only with this two rows
arr = [arr0, arr1]
arr = np.array(arr, dtype=np.object_)
fig3D = go.Figure(data=[go.Scatter3d(x=[0],
                                     y=[0],
                                     z=[0],
                                     mode='markers',
                                     marker=dict(size=1, color='green'))
                        ])
pointer, status = None, None
lib = CDLL(r"C:\Users\Admin\PycharmProjects\SensorDriver\EthernetScanner\EthernetScanner.dll")
INTERVAL = 200 # in msec (30 FPS)
dash.register_page(__name__, path='/')

layout = html.Div([
    html.H3('Real-time monitor'),
    dbc.Row([
        dbc.Col([
            html.H4('cloud'),
            dcc.Graph(id='cloud'),
        ],
        width=6),
        dbc.Col([
            html.H4('Zoomed cloud'),
            dcc.Graph(id='zoomedCloud'),
        ],
        width=6),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.H4('controls'),
                    html.Br(),
                    html.Button('Connect scanner', id='connect'),
                    html.Br(),
                    html.Button('Start scanning', id='start'),
                    html.Br(),
                    html.Button('Pause scanning', id='pause'),
                    html.Br(),
                    html.Button('Stop scanning', id='stop'),
                ]),
                dbc.Col([
                    html.H4('save/load'),
                    html.Br(),
                    html.Button('Save to file', id='save'),
                    html.Br(),
                    html.Button('Load from RAM', id='load'),
                    html.Br(),
                    html.Button('Load from file', id='loadf'),
                ]),
            ]),
            dbc.Row([
                    html.Output('Log info', id='info'),
                    html.Br(),
                    html.Output('Count info', id='countInfo'),
            ]),
        ]),
        dbc.Col([
            html.H4('3D'),
            dcc.Graph(id='3D'),
        ]),
    ]),
    dcc.Interval('interval', interval=INTERVAL, n_intervals=0, max_intervals=0),
    dcc.Store(id='zoomedRegion')
])


def clearingZeros():
    pass


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

    return arr


@callback(
    Output('info', 'children'),
    Output('cloud', 'figure'),
    Output('zoomedCloud', 'figure'),
    # Output('3D', 'figure'),
    Input('interval', 'n_intervals'),
    Input('zoomedRegion', 'data'),
    prevent_initial_call=True,
)
def update_intervals(n_intervals, data):
    global fig3D, arr
    if ('xaxis.range[0]' in data) and ('yaxis.range[0]' in data) == True:
        xRange0 = data["xaxis.range[0]"]
        xRange1 = data["xaxis.range[1]"]
        yRange0 = data["yaxis.range[0]"]
        yRange1 = data["yaxis.range[1]"]
    else:
        #print(data)
        xRange0 = -60
        xRange1 = 60
        yRange0 = 300
        yRange1 = 0
    #print(f'x0: {data["xaxis.range[0]"]:.2f}, x1: {data["xaxis.range[1]"]:.2f}, y0: {data["yaxis.range[0]"]:.2f}, y1: {data["yaxis.range[1]"]:.2f}')
    #print(f'the countdown is: {n_intervals}')
    dataLength, bufX, bufZ, bufIntensity = getXZIExtended(lib, pointer)
    curArr = transformData(bufX, bufZ, bufIntensity)

    # arr = np.hstack((arr, np.empty(1)))
    # arr[-1] = curArr

    fig1 = makeFig(curArr)
    fig2 = makeFigInten(curArr, xRange0, xRange1, yRange0, yRange1)

    # fig3D = updateFif3D(fig3D, arr, n_intervals)

    # print(f'X: {arr[0, :]}')
    # print(f'Z: {arr[1, :]}')
    # print(f't: {np.full(len(arr[0, :]), n_intervals)}')
    return f'the countdown is: {n_intervals}', fig1, fig2#, fig3D


#connect
@callback(
    Output('info', 'children', allow_duplicate=True),
    Input('connect', 'n_clicks'),
    prevent_initial_call=True,
)
def con(n_intervals):
    # np.savetxt('data.csv', np.zeros((1280*3, 1)), fmt='%.4f') #temp
    # with open('mindata', 'wb') as file:
    #     pickle.dump(np.array([list([0])], dtype=np.object_), file)
    global pointer, status
    pointer, status = connect(lib)
    return 'Trying to connect to the scanner'


#start
@callback(
    Output('interval', 'n_intervals'),
    Output('interval', 'max_intervals'),
    Output('info', 'children', allow_duplicate=True),
    Input('start', 'n_clicks'),
    State('interval', 'n_intervals'),
    prevent_initial_call=True,
)
def start(n_clicks, n_intervals):
    if n_intervals==0:
        print('start')
    else:
        print(f'start from count {n_intervals}')

    return n_intervals, 36000000, f'start from count {n_intervals}'


#pause
@callback(
    Output('interval', 'max_intervals', allow_duplicate=True),
    Output('info', 'children', allow_duplicate=True),
    Input('pause', 'n_clicks'),
    State('interval', 'n_intervals'),
    prevent_initial_call=True,
)
def pause(n_clicks, n_intervals):
    print(f'the countdown has paused on count number: {n_intervals}')
    return 0, f'the countdown has paused on count number: {n_intervals}'


#stop
@callback(
    Output('interval', 'max_intervals', allow_duplicate=True),
    Output('interval', 'n_intervals', allow_duplicate=True),
    Output('info', 'children', allow_duplicate=True),
    Input('stop', 'n_clicks'),
    prevent_initial_call=True,
)
def stop(n_clicks):
    print('the countdown has stopped')
    return 0, 0, 'the countdown has stopped'


#timer output
@callback(
    Output('countInfo', 'children'),
    Input('interval', 'n_intervals'),
)
def countInfo(n_intervals):
    # to do somthing
    return n_intervals


#zoom
@callback(
    Output('info', 'children', allow_duplicate=True),
    Output('zoomedRegion', 'data'),
    Input('cloud', 'relayoutData'),
    prevent_initial_call=True,
)
def zoom(relayoutData):
    # print('first time zoom')
    # print(relayoutData)
    return 'zoomed', relayoutData


#load from RAM
@callback(
    Output('3D', 'figure', allow_duplicate=True),
    Output('info', 'children', allow_duplicate=True),
    Input('3D', 'figure'),
    prevent_initial_call=True,
)
def load(n_intervals):
    global arr
    arr = np.delete(arr, [0, 1])
    print(f'shape of data: {arr.shape}')
    # print(arr.shape)
    # print(arr[2])

    # arr1 = np.genfromtxt('data.csv')
    # arr = arr1.reshape(len(arr1), 3, -1)
    count = 0.0
    for el in arr:
        count += 0.01
        # print(el[0])
        # print(el[1])
        # print(el[2])
        # print('next')
        print(f'length of data: {len(el[0])}')
        fig3D.add_trace(go.Scatter3d(x=el[0],
                                     y=el[1],
                                     z=np.full(len(el[0]), count),
                                     mode='markers',
                                     marker=dict(size=1, color='green')
                                     )
                        )
        # fig3D.add_trace(go.Scatter3d(x=el[0, :],
        #                              y=el[1, :],
        #                              z=np.full(len(el[0, :]), count),
        #                              mode='markers',
        #                              marker=dict(size=1, color='green')
        #                              )
        #                 )
    return fig3D, 'loaded from RAM'


# save to npy
@callback(
    Output('info', 'children', allow_duplicate=True),
    Input('save', 'n_clicks'),
    prevent_initial_call=True,
)
def save(n_intervals):
    global arr
    saveToFile(arr)
    return 'saved to .npy file'


# load from npy
@callback(
    Output('info', 'children', allow_duplicate=True),
    Input('loadf', 'n_clicks'),
    prevent_initial_call=True,
)
def loadf(n_intervals):
    global arr
    loadFromFile()
    return 'loaded from .npy file'
