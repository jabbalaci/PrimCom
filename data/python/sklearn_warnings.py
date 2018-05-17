# suppress DeprecationWarning in sklearn
import warnings
from sklearn import ...
# first import from sklearn, then add the following line
warnings.filterwarnings("ignore", category=DeprecationWarning)
