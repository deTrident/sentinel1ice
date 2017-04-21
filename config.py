import os

def get_env():

    env = {}
    env['inputDirectory'] = '/Data/sat/downloads/sentinel1/'
    env['outputDirectory'] = '/Data/sat/downloads/sentinel1/tmp/'
    env['minDate'] = '20170320'
    env['maxDate'] = '20170405'
    env['wildcard'] = 'S1?_EW_GRDM_1SDH_20170[3,4]*.zip'
    env['unzipInput'] = False
    env['development'] = False
    env['textureFeatureNormalizationFilePrefix'] = 'norm01'
    env['myZonesSuffix'] = '_my_zones.png'
    env['supportVectorMachineFile'] = 'svm_ice_water_testver.pickle'
    env['multiLookFactor'] = 1
    env['stepSize'] = 25
    env['subwindowSize'] = 25
    env['grayLevel'] = 64
    env['sigma0_max'] = {'HH':  -1.75, 'HV': -14.75}
    env['sigma0_min'] = {'HH': -24.75, 'HV': -30.25}
    env['numberOfThreads'] = 4
    env['textureFeatureAlgorithm'] = 'averagedGLCM'
    env['skewnessThreshold'] = 0
    env['textureFeatureNormalization'] = 'boxcox'
    env['textureFeatureID'] = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    env['numberOfPrincialComponent'] = 6
    env['numberOfKmeansCluster'] = 15
    env['princialComponentID'] = [0,1,2,3,4,5]
    env['zoneColors'] = [100,250]

    if not os.path.exists(env['inputDirectory']):
            raise IOError('cannot find input directory %s' % env['inputDirectory'])
    
    if not os.path.exists(env['outputDirectory']):
            raise IOError('cannot find output directory %s' % env['outputDirectory'])

    if env['multiLookFactor']%1!=0 or env['multiLookFactor']<=0:
        raise ValueError('"multiLookFactor" must be positive integer.')
    
    if env['stepSize']%1!=0 or env['stepSize']<=0:
        raise ValueError('"stepSize" must be positive integer.')
    
    if env['subwindowSize']%1!=0 or env['subwindowSize']<=0:
        raise ValueError('"subwindowSize" must be positive integer.')
    
    if env['grayLevel']%1!=0 or env['grayLevel']<=0:
        raise ValueError('"grayLevel" must be positive integer.')
    
    if env['numberOfThreads']%1!=0 or env['numberOfThreads']<=0:
        raise ValueError('"numberOfThreads" must be positive integer.')
    
    if env['textureFeatureAlgorithm'] not in ['averagedGLCM','averagedTFs']:
        raise KeyError('"textureFeatureAlgorithm" must be "averagedGLCM" or "averagedTFs".')
    
    if env['textureFeatureNormalization'] not in ['log','boxcox']:
        raise KeyError('"textureFeatureNormalization" must be "log" or "boxcox".')

    if ( sum([ID < 13 for ID in env['textureFeatureID'] ])
         != len(env['textureFeatureID']) ):
        raise KeyError('"textureFeatureID" contains wrong number.')

    if not all([ ID < env['numberOfPrincialComponent']
                 for ID in env['princialComponentID'] ]):
        raise KeyError('"princialComponentID" contains wrong number.')

    return env
