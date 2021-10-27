import pyvisa
import numpy
from struct import unpack

def get_pyvisa_scope():
    # Return the pyvisa scope so we can get data and images from it.

    scope_manual_ip = '192.168.1.123'
    rm = pyvisa.ResourceManager()
    scope = rm.open_resource('TCPIP::' + scope_manual_ip + '::INSTR')
    
    return scope

def get_image(scope):
    pass

def get_xy_lists(scope):
    # Given the pyvisa scope, get its x and y plot.
    
    scope.write('DATA:SOURCE CH1')
    scope.write('DATA:WIDTH 1')
    scope.write('DATA:ENC RPB')
    
    ymult = float(scope.query('WFMPRE:YMULT?'))
    yzero = float(scope.query('WFMPRE:YZERO?'))
    yoff = float(scope.query('WFMPRE:YOFF?'))
    xincr = float(scope.query('WFMPRE:XINCR?'))
    xzero = float(scope.query('wfmpre:xzero?'))
    
    scope.write("curve?")
    data = scope.read_raw()
    headerlen = 2 + int(data[1])
    ADC_wave = data[headerlen:-1]
    ADC_wave = numpy.array(unpack('%sB' % len(ADC_wave), ADC_wave))
    y = (ADC_wave - yoff) * ymult + yzero
    x = numpy.arange(0, xincr*len(y), xincr)
    return x, y