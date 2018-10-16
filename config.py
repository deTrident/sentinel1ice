import os

inputDirectory = '/Volumes/MacOS8TB/Archives/Sentinel-1/FramStrait/'

if not os.path.exists(inputDirectory):
    raise IOError('cannot find input directory %s' % inputDirectory)

outputDirectory = '/Volumes/MacOS8TB/Process/sentinel1ice/FramStrait/'
if not os.path.exists(outputDirectory):
    os.mkdir(outputDirectory)

#must be in ['AARI', 'NIC', 'manual']
sourceType = 'AARI'
if sourceType!='manual':
    # minimum ice concentration that SAR can observe the ice signatures
    minCT = 30

iceChartDirectory = '/Volumes/MacOS8TB/Archives/Ice_chart/'
if sourceType != 'manual':
    if not os.path.exists(iceChartDirectory):
        raise IOError('cannot find ice chart directory %s' % iceChartDirectory)

kmeansFilename = 'kmeans_FramStrait.pickle'

classifierFilename = '/Data/sat/downloads/sentinel1/rf_FramStrait_AARI.pickle'

# limit file list for denosing by the following parameters:
minDate = "20161001"
maxDate = "20170531"
wildcard = 'S1*'

sigma0_max = {'HH':  +2.0, 'HV':  -7.0}
sigma0_min = {'HH': -36.0, 'HV': -35.0}

# angular dependency for deformed FYI (Reference; doi: 10.1109/TGRS.2017.2721981)
angularDependency = {'HH':-0.24, 'HV':-0.16}

# must be positive integer
stepSize = 25

# must be positive integer
subwindowSize = 25

# must be positive integer
grayLevel = 64

# must be in ["averagedGLCM", "averagedTFs"]
textureFeatureAlgorithm = 'averagedGLCM'

# must be positive integer
maxNumberOfSamplesToTrain = 1000000

# must be float < 1.0
pcaVarThres = 0.95

# must be 0 (no multiprocessing) or positive integer < os.cpu_count()
numberOfThreads = 3

# boolean, generate quicklook of denoised image?
quicklook = True

# boolean, unzip input files and keep them?
unzipInput = False

# boolean, land masking?
landmask = True

# boolean, force reprocessing?
force = False
