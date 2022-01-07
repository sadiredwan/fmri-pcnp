import os
import sys


def main():
	os.chdir('../')
	datamod = sys.argv[1]
	flist = [line.rstrip() for line in open('pipeline.txt', 'r').readlines()]
	for fname in flist:
		if os.path.exists('voxel-timeseries/'+datamod+'/'+fname[:9]):
			print('exists:'+fname[:9])
			break
		os.mkdir(os.path.join('voxel-timeseries/'+datamod+'/'+fname[:9]))
		for roi in os.listdir('masks/atlas'):
			os.system('3dmaskdump'+
				' -noijk'+
				' -xyz'+
				' -mask'+
				' '+os.getcwd()+'/masks/atlas/'+roi+
				' '+os.getcwd()+'/pcnp-mni/'+datamod+'-bold/'+fname+
				' > voxel-timeseries/'+datamod+'/'+fname[:9]+'/'+fname[:9]+
				'-'+roi.replace('.nii', '.csv'))

if __name__ == '__main__':
	main()
