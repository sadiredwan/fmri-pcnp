import gc
import os
import re
import shutil
import nibabel as nb
from nilearn import image


def alphanum(dir):
	convert = lambda text: int(text) if text.isdigit() else text.lower()
	alphanum_key = lambda key: [convert(k) for k in re.split('([0-9]+)', key)] 
	return sorted(dir, key=alphanum_key)


if __name__ == '__main__':
	flist = [line.rstrip() for line in open('pipeline.txt', 'r').readlines()]
	for fname in flist:
		img = nb.load('pcnp-ucla/rest-bold/'+fname)
		if os.path.exists('tmp/'):
			shutil.rmtree('tmp/')

		os.mkdir(os.path.join('tmp'))
		for i, timg in enumerate(image.iter_img(img)):
			nb.save(timg, 'tmp/'+str(i)+'.nii.gz')
		
		if os.path.exists('mni-tmp/'):
			shutil.rmtree('mni-tmp/')

		shutil.copytree('tmp/', 'mni-tmp/')
		FSLDIR = '/home/sadi/fsl/'
		INDIR = os.getcwd()+'/tmp/'
		OUTDIR = os.getcwd()+'/mni-tmp/'
		for f in os.listdir(INDIR):
			os.system(FSLDIR+'bin/flirt'+
					' -in '+INDIR+f+
					' -ref '+FSLDIR+'data/standard/MNI152_T1_2mm_brain'+
					' -out '+OUTDIR+f+
					' -bins 256'+
					' -cost corratio'+
					' -dof 9'+
					' -interp trilinear')
		
		mni_reg = []
		for f in alphanum(os.listdir('mni-tmp/')):
			mni_reg.append('mni-tmp/'+f)

		mni_reg = image.concat_imgs(mni_reg)
		nb.save(mni_reg, 'pcnp-mni/rest-bold/'+fname)
		shutil.rmtree('tmp/')
		shutil.rmtree('mni-tmp/')
		
	gc.collect()
