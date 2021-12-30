library(matlabr)
library(spm12r)
library(neurobase)


if(!have_matlab()){
	stop('404:matlab')
}

add_spm_dir('../utils/spm12')

f <- file('../pipeline.txt', open='r')
fnames <-readLines(f)

for(fname in fnames){
	file.copy(paste('../pcnp-ucla/rest-bold/', substr(fname, 0, 9), '_task-rest_bold.nii', sep=''), '../tmp')
	file.copy(paste('../pcnp-ucla/anat/', substr(fname, 0, 9), '_T1w.nii', sep=''), '../tmp')
	functional = paste('../tmp/', substr(fname, 0, 9), '_task-rest_bold.nii', sep='')
	anatomical = paste('../tmp/', substr(fname, 0, 9), '_T1w.nii', sep='')
	files = c(anatomical = anatomical, functional = functional)

	#realign
	realign_batch = build_spm12_realign( 
		filename = functional, 
		register_to = 'mean',
		reslice = 'mean'
	)

	realigned = spm12_realign( 
		filename = functional, 
		register_to = 'mean',
		reslice = 'mean',
		clean = FALSE
	)

	#slicetime
	tr = 2
	nslices = 34
	n_time_points = 152
	ta = tr-(tr/nslices)
	slice_order = c(seq(2, nslices, 2), seq(1, nslices, 2))
	ref_slice = slice_order[median(seq(nslices))]

	st_batch = build_spm12_slice_timing(
		filename = functional,
		time_points = seq(n_time_points),
		nslices = nslices,
		tr = tr,
		ref_slice = ref_slice,
		prefix = 'a'
	)

	st_corrected = spm12_slice_timing(
		filename = realigned[['outfiles']],
		time_points = seq(n_time_points),
		nslices = nslices,
		tr = tr, 
		slice_order = slice_order,
		ta = ta, 
		ref_slice = ref_slice,
		prefix = 'a', 
		clean = FALSE, 
		retimg = FALSE
	)

	#coregister
	aimg = st_corrected$outfile
	mean_img = realigned[['mean']]
	mean_nifti = readnii(mean_img)

	acpc_reorient(
		infiles = c(mean_img, aimg),
		modality = 'T1'
	)

	anatomical = files['anatomical']
	anat_img = checknii(anatomical)

	acpc_reorient(
		infiles = anat_img,
		modality = 'T1'
	)

	coreg = spm12_coregister(
		fixed = mean_img,
		moving = anat_img,
		prefix = 'r'
	)

	coreg_anat = coreg$outfile
	coreg_img = readnii(coreg_anat)

	#segment
	seg_res = spm12_segment(
		filename = coreg_anat,
		affine = 'mni',
		set_origin = FALSE,
		retimg = FALSE,
		clean = FALSE
	)

	#normalize
	bbox = matrix(
		c(-90, -126, -72,
			90, 90, 108),
		nrow = 2, byrow = TRUE
	)

	norm_res = spm12_normalize_write(
		deformation = seg_res$deformation,
		other.files = c(coreg_anat, mean_img, aimg),
		bounding_box = bbox,
		retimg = FALSE
	)
	
	norm_data = norm_res$outfiles
	names(norm_data) = c('anat', 'mean', 'fmri')
	norm_fmri = readnii(norm_data['fmri'])
	norm_fmri@sform_code <- 4
	norm_fmri@qform_code <- 4
	write_nifti(norm_fmri, paste('../pcnp-mni/rest-bold/w', substr(fname, 0, 9), '_task-rest_bold.nii', sep=''))
}

for(tmp in list.files(path = '../tmp')){
	file.remove(paste('../tmp/', tmp, sep=''))
}

close(f)
