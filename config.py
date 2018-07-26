import os

inputDirectory = '/Volumes/MacOS8TB/Archives/Sentinel-1/FramStrait/'
inputDirectory = '/files/sentinel1a/'

if not os.path.exists(inputDirectory):
    raise IOError('cannot find input directory %s' % inputDirectory)

outputDirectory = '/Volumes/MacOS8TB/Process/sentinel1ice/FramStrait/'
outputDirectory = '/files/sentinel1a/denoised/'
if not os.path.exists(outputDirectory):
    os.mkdir(outputDirectory)

#must be in ['AARI', 'CIS', 'manual']
sourceType = 'AARI'

iceChartDirectory = '/Volumes/MacOS8TB/Archives/Ice_chart/AARI'
iceChartDirectory = '/files/sentinel1a/denoised/'
if sourceType != 'manual':
    if not os.path.exists(iceChartDirectory):
        raise IOError('cannot find ice chart directory %s' % iceChartDirectory)

kmeansFilename = 'kmeans_FramStrait.pickle'

classifierFilename = '/Data/sat/downloads/sentinel1/rf_FramStrait_AARI.pickle'

# limit file list for denosing by the following parameters:
minDate = None
maxDate = None
wildcard = 'S1A*'

# boolean, generate quicklook of denoised image?
quicklook = False

# boolean, unzip input files and keep them?
unzipInput = False

gamma0_max = {'HH':  +1.0, 'HV':  -8.0}
gamma0_min = {'HH': -31.0, 'HV': -32.0}

# must be positive integer
stepSize = 25

# must be positive integer
subwindowSize = 25

# must be positive integer
grayLevel = 64

# must be in ["averagedGLCM", "averagedTFs"]
textureFeatureAlgorithm = 'averagedGLCM'

# must be o (no multiprocessing) or positive integer < os.cpu_count()
numberOfThreads = 6

# boolean, force processing?
force = True
