import os
import warnings
import numpy as np
import pandas as pd
import nibabel as nb
from tqdm import tqdm
from nilearn import datasets
from nilearn.maskers import NiftiMapsMasker


if __name__ == '__main__':
	warnings.filterwarnings('ignore')
	directory = '../pcnp-mni/rest-bold/'
	atlas = datasets.fetch_atlas_harvard_oxford('cort-prob-2mm')
	masker = NiftiMapsMasker(maps_img=atlas.maps, memory='nilearn-cache')
	atlas.labels.remove('Background')
	for fname in tqdm(os.listdir(directory)):
		df = pd.DataFrame(columns=atlas.labels)
		time_series = masker.fit_transform(nb.load(directory+fname))
		for i, ts in enumerate(time_series.T):
			df[df.columns[i]] = ts
		df.to_csv('../timeseries/rest/'+fname[:9]+'.csv', index=False)
