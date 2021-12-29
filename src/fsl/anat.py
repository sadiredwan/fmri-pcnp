import gc
import os


if __name__ == '__main__':
	os.chdir('../')
	flist = [line.rstrip() for line in open('pipeline.txt', 'r').readlines()]
	for fname in flist:
		FSLDIR = '/home/sadi/fsl/'
		INDIR = os.path.join('/pcnp-ucla/anat/')
		OUTDIR = os.path.join('/pcnp-mni/anat/')
		os.system(FSLDIR+'bin/bet'+
				' '+INDIR+fname+
				' '+OUTDIR+fname+
				' -f 0.5 -g 0')
		
		os.system(FSLDIR+'bin/flirt'+
				' -in '+OUTDIR+fname+
				' -ref '+FSLDIR+'data/standard/MNI152_T1_2mm_brain'+
				' -out '+OUTDIR+fname+
				' -bins 256'+
				' -cost corratio'+
				' -dof 12'+
				' -interp trilinear')
	gc.collect()
