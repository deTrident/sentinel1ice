import os

def get_env():

    env = {}
    
    env['inputDirectory'] = '/Volumes/MacOS8TB/Archives/Sentinel-1/FramStrait/'
    if not os.path.exists(env['inputDirectory']):
        raise IOError('cannot find input directory %s' % env['inputDirectory'])

    env['outputDirectory'] = '/Volumes/MacOS8TB/Process/sentinel1ice/FramStrait/'
    if not os.path.exists(env['outputDirectory']):
        os.mkdir(env['outputDirectory'])

    env['sourceType'] = 'AARI'
    if env['sourceType'] not in ['AARI', 'CIS', 'manual']:
        raise KeyError('"sourceType" must be "AARI" or "CIS" or "manual".')

    env['iceChartDirectory'] = '/Users/jeopar/Development/Python/sentinel1ice/AARI'
    if env['sourceType']!='manual':
        if not os.path.exists(env['iceChartDirectory']):
            raise IOError('cannot find ice chart directory %s' % env['iceChartDirectory'])

    env['kmeansFilename'] = 'kmeans_FramStrait.pickle'

    env['classifierFilename'] = 'rf_FramStrait.pickle'

    env['minDate'] = None

    env['maxDate'] = None

    env['wildcard'] = '*.zip'

    env['unzipInput'] = False
    if env['unzipInput'] not in [True, False]:
        raise ValueError('"unzipInput" must be a boolean.')

    env['gamma0_max'] = {'HH':  +1.0, 'HV':  -8.0}

    env['gamma0_min'] = {'HH': -31.0, 'HV': -32.0}

    env['stepSize'] = 25
    if env['stepSize']%1!=0 or env['stepSize']<=0:
        raise ValueError('"stepSize" must be positive integer.')

    env['subwindowSize'] = 25
    if env['subwindowSize']%1!=0 or env['subwindowSize']<=0:
        raise ValueError('"subwindowSize" must be positive integer.')

    env['grayLevel'] = 64
    if env['grayLevel']%1!=0 or env['grayLevel']<=0:
        raise ValueError('"grayLevel" must be positive integer.')

    env['textureFeatureAlgorithm'] = 'averagedGLCM'
    if env['textureFeatureAlgorithm'] not in ['averagedGLCM','averagedTFs']:
        raise KeyError('"textureFeatureAlgorithm" must be "averagedGLCM" or "averagedTFs".')

    env['numberOfThreads'] = 2
    if (env['numberOfThreads']<=0) or (env['numberOfThreads']>os.cpu_count()):
        raise ValueError('"numberOfThreads" must be positive integer (max=%d).' % os.cpu_count())

    return env
