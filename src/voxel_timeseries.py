import os


def main():
	os.chdir('../')
	flist = [line.rstrip() for line in open('pipeline.txt', 'r').readlines()]
	for fname in flist:
		if os.path.exists('voxel-timeseries/'+fname[1:10]):
			print('exists:'+fname[1:10])
			break
		os.mkdir(os.path.join('voxel-timeseries/'+fname[1:10]))
		for roi in os.listdir('masks/atlas'):
			os.system('3dmaskdump'+
				' -noijk'+
				' -xyz'+
				' -mask'+
				' '+os.getcwd()+'/masks/atlas/'+roi+
				' '+os.getcwd()+'/pcnp-mni/rest-bold/'+fname+
				' > voxel-timeseries/'+fname[1:10]+'/'+fname[1:10]+
				'-'+roi.replace('.nii', '.csv'))

if __name__ == '__main__':
	main()
