import os
import numpy as np
from nibabel.testing import data_path

import nibabel
print("HALLO")

data = np.ones((32, 32, 15, 100), dtype=np.int16)
img = nibabel.Nifti1Image(data, np.eye(4))
nibabel.save(img, os.path.join('','test4d.nii.gz'))