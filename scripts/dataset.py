from torch.utils.data import Dataset, DataLoader
import torch
import sys
sys.path.append('graphs/')
import npb_3_3_CG_makea_6
import npb_3_3_SP_initialize4
import npb_3_3_MG_kernel_comm3_2
import npb_3_3_SP_compute_rhs6
import amd_app_sdk_3_0_SimpleConvolution_simpleNonSeparableConvolution
import polybench_gpu_1_0_bicg_bicgKernel1
import amd_app_sdk_3_0_ScanLargeArrays_blockAddition
import npb_3_3_MG_kernel_zero3
import amd_app_sdk_3_0_SobelFilter_sobel_filter
import npb_3_3_BT_compute_rhs2
import shoc_1_1_5_Scan_top_scan
import npb_3_3_SP_exact_rhs1
import shoc_1_1_5_Spmv_spmv_csr_scalar_kernel
import npb_3_3_BT_initialize5
import npb_3_3_LU_setbv1
import polybench_gpu_1_0_atax_atax_kernel2
import rodinia_3_1_bfs_BFS_1
import npb_3_3_BT_initialize4
import amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform
import amd_app_sdk_3_0_BinomialOption_binomial_options
import npb_3_3_SP_add
import npb_3_3_SP_ninvr
import npb_3_3_MG_kernel_comm3_3
import npb_3_3_BT_y_solve2
import npb_3_3_SP_initialize5
import npb_3_3_CG_makea_7
import amd_app_sdk_3_0_Reduction_reduce
import polybench_gpu_1_0_correlation_mean_kernel
import npb_3_3_CG_makea_5
import polybench_gpu_1_0_syr2k_syr2k_kernel
import npb_3_3_MG_kernel_comm3_1
import rodinia_3_1_cfd_initialize_variables
import parboil_0_2_stencil_naive_kernel
import rodinia_3_1_lud_lud_internal
import polybench_gpu_1_0_correlation_corr_kernel
import polybench_gpu_1_0_bicg_bicgKernel2
import rodinia_3_1_kmeans_kmeans_swap
import npb_3_3_LU_ssor2
import npb_3_3_FT_compute_indexmap
import npb_3_3_BT_compute_rhs1
import shoc_1_1_5_Triad_Triad
import rodinia_3_1_particlefilter_normalize_weights_kernel
import npb_3_3_LU_setbv2
import polybench_gpu_1_0_atax_atax_kernel1
import rodinia_3_1_bfs_BFS_2
import rodinia_3_1_backprop_bpnn_adjust_weights_ocl
import npb_3_3_MG_kernel_zran3_3
import rodinia_3_1_cfd_compute_step_factor
import amd_app_sdk_3_0_ScanLargeArrays_ScanLargeArrays
import polybench_gpu_1_0_gemm_gemm
import npb_3_3_BT_exact_rhs1
import npb_3_3_BT_x_solve2
import amd_app_sdk_3_0_ScanLargeArrays_prefixSum
import npb_3_3_LU_ssor3
import shoc_1_1_5_Spmv_spmv_ellpackr_kernel
import nvidia_4_2_VectorAdd_VectorAdd
import polybench_gpu_1_0_2DConvolution_Convolution2D_kernel
import shoc_1_1_5_Sort_top_scan
import npb_3_3_CG_makea_4
import nvidia_4_2_MatVecMul_MatVecMulCoalesced2
import nvidia_4_2_MatVecMul_MatVecMulUncoalesced0
import nvidia_4_2_MersenneTwister_BoxMuller
import npb_3_3_BT_exact_rhs5
import npb_3_3_FT_cffts2
import amd_app_sdk_3_0_BitonicSort_bitonicSort
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1
import npb_3_3_CG_main_1
import npb_3_3_BT_initialize3
import rodinia_3_1_gaussian_Fan2
import polybench_gpu_1_0_correlation_std_kernel
import polybench_gpu_1_0_2mm_mm2_kernel1
import polybench_gpu_1_0_correlation_reduce_kernel
import polybench_gpu_1_0_covariance_mean_kernel
import npb_3_3_FT_evolve
import npb_3_3_CG_main_0
import amd_app_sdk_3_0_FloydWarshall_floydWarshallPass
import rodinia_3_1_nn_NearestNeighbor
import npb_3_3_FT_cffts3
import parboil_0_2_spmv_A
import nvidia_4_2_MatVecMul_MatVecMulUncoalesced1
import polybench_gpu_1_0_mvt_mvt_kernel1
import amd_app_sdk_3_0_SimpleConvolution_simpleSeparableConvolutionPass1
import npb_3_3_CG_conj_grad_0
import polybench_gpu_1_0_3mm_mm3_kernel1
import npb_3_3_SP_initialize3
import rodinia_3_1_particlefilter_find_index_kernel
import npb_3_3_SP_initialize1
import shoc_1_1_5_FFT_chk1D_512
import nvidia_4_2_DotProduct_DotProduct
import polybench_gpu_1_0_3mm_mm3_kernel3
import amd_app_sdk_3_0_PrefixSum_group_prefixSum
import npb_3_3_BT_z_solve2
import shoc_1_1_5_BFS_BFS_kernel_warp
import nvidia_4_2_MatVecMul_MatVecMulCoalesced1
import rodinia_3_1_cfd_time_step
import npb_3_3_CG_init_mem_1
import polybench_gpu_1_0_covariance_covar_kernel
import npb_3_3_FT_cffts1
import polybench_gpu_1_0_gesummv_gesummv_kernel
import rodinia_3_1_cfd_memset_kernel
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2
import npb_3_3_BT_add
import npb_3_3_CG_main_2
import rodinia_3_1_gaussian_Fan1
import polybench_gpu_1_0_2mm_mm2_kernel2
import amd_app_sdk_3_0_MatrixTranspose_matrixTranspose
import npb_3_3_BT_initialize1
import shoc_1_1_5_Scan_reduce
import npb_3_3_SP_exact_rhs5
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel3
import polybench_gpu_1_0_syrk_syrk_kernel
import npb_3_3_BT_compute_rhs6
import rodinia_3_1_streamcluster_memset_kernel
import npb_3_3_CG_init_mem_0
import shoc_1_1_5_Reduction_reduce
import rodinia_3_1_kmeans_kmeans_kernel_c
import nvidia_4_2_MatVecMul_MatVecMulCoalesced0
import npb_3_3_FT_checksum
import npb_3_3_SP_compute_rhs2
import npb_3_3_FT_init_ui
import polybench_gpu_1_0_covariance_reduce_kernel
import polybench_gpu_1_0_mvt_mvt_kernel2
import rodinia_3_1_particlefilter_sum_kernel
import amd_app_sdk_3_0_SimpleConvolution_simpleSeparableConvolutionPass2
import polybench_gpu_1_0_3mm_mm3_kernel2
import npb_3_3_SP_pinvr
import npb_3_3_CG_makea_2
import numpy as np
import multifractal
def nodeFeatures(g, types):
	if (types == 'simple'):
		return g.in_degrees()
	elif (types == 'weight'):
		return dgl.khop_adj(g, 1)
	elif (types == 'multifractal'):
		return multifractal.multifractal(g)
class GraphDataset(Dataset):
	def __init__(self):
		self.graphs = [npb_3_3_CG_makea_6.npb_3_3_CG_makea_6(), npb_3_3_SP_initialize4.npb_3_3_SP_initialize4(), npb_3_3_MG_kernel_comm3_2.npb_3_3_MG_kernel_comm3_2(), npb_3_3_SP_compute_rhs6.npb_3_3_SP_compute_rhs6(), amd_app_sdk_3_0_SimpleConvolution_simpleNonSeparableConvolution.amd_app_sdk_3_0_SimpleConvolution_simpleNonSeparableConvolution(), polybench_gpu_1_0_bicg_bicgKernel1.polybench_gpu_1_0_bicg_bicgKernel1(), amd_app_sdk_3_0_ScanLargeArrays_blockAddition.amd_app_sdk_3_0_ScanLargeArrays_blockAddition(), npb_3_3_MG_kernel_zero3.npb_3_3_MG_kernel_zero3(), amd_app_sdk_3_0_SobelFilter_sobel_filter.amd_app_sdk_3_0_SobelFilter_sobel_filter(), npb_3_3_BT_compute_rhs2.npb_3_3_BT_compute_rhs2(), shoc_1_1_5_Scan_top_scan.shoc_1_1_5_Scan_top_scan(), npb_3_3_SP_exact_rhs1.npb_3_3_SP_exact_rhs1(), shoc_1_1_5_Spmv_spmv_csr_scalar_kernel.shoc_1_1_5_Spmv_spmv_csr_scalar_kernel(), npb_3_3_BT_initialize5.npb_3_3_BT_initialize5(), npb_3_3_LU_setbv1.npb_3_3_LU_setbv1(), polybench_gpu_1_0_atax_atax_kernel2.polybench_gpu_1_0_atax_atax_kernel2(), rodinia_3_1_bfs_BFS_1.rodinia_3_1_bfs_BFS_1(), npb_3_3_BT_initialize4.npb_3_3_BT_initialize4(), amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform.amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform(), amd_app_sdk_3_0_BinomialOption_binomial_options.amd_app_sdk_3_0_BinomialOption_binomial_options(), npb_3_3_SP_add.npb_3_3_SP_add(), npb_3_3_SP_ninvr.npb_3_3_SP_ninvr(), npb_3_3_MG_kernel_comm3_3.npb_3_3_MG_kernel_comm3_3(), npb_3_3_BT_y_solve2.npb_3_3_BT_y_solve2(), npb_3_3_SP_initialize5.npb_3_3_SP_initialize5(), npb_3_3_CG_makea_7.npb_3_3_CG_makea_7(), amd_app_sdk_3_0_Reduction_reduce.amd_app_sdk_3_0_Reduction_reduce(), polybench_gpu_1_0_correlation_mean_kernel.polybench_gpu_1_0_correlation_mean_kernel(), npb_3_3_CG_makea_5.npb_3_3_CG_makea_5(), polybench_gpu_1_0_syr2k_syr2k_kernel.polybench_gpu_1_0_syr2k_syr2k_kernel(), npb_3_3_MG_kernel_comm3_1.npb_3_3_MG_kernel_comm3_1(), rodinia_3_1_cfd_initialize_variables.rodinia_3_1_cfd_initialize_variables(), parboil_0_2_stencil_naive_kernel.parboil_0_2_stencil_naive_kernel(), rodinia_3_1_lud_lud_internal.rodinia_3_1_lud_lud_internal(), polybench_gpu_1_0_correlation_corr_kernel.polybench_gpu_1_0_correlation_corr_kernel(), polybench_gpu_1_0_bicg_bicgKernel2.polybench_gpu_1_0_bicg_bicgKernel2(), rodinia_3_1_kmeans_kmeans_swap.rodinia_3_1_kmeans_kmeans_swap(), npb_3_3_LU_ssor2.npb_3_3_LU_ssor2(), npb_3_3_FT_compute_indexmap.npb_3_3_FT_compute_indexmap(), npb_3_3_BT_compute_rhs1.npb_3_3_BT_compute_rhs1(), shoc_1_1_5_Triad_Triad.shoc_1_1_5_Triad_Triad(), rodinia_3_1_particlefilter_normalize_weights_kernel.rodinia_3_1_particlefilter_normalize_weights_kernel(), npb_3_3_LU_setbv2.npb_3_3_LU_setbv2(), polybench_gpu_1_0_atax_atax_kernel1.polybench_gpu_1_0_atax_atax_kernel1(), rodinia_3_1_bfs_BFS_2.rodinia_3_1_bfs_BFS_2(), rodinia_3_1_backprop_bpnn_adjust_weights_ocl.rodinia_3_1_backprop_bpnn_adjust_weights_ocl(), npb_3_3_MG_kernel_zran3_3.npb_3_3_MG_kernel_zran3_3(), rodinia_3_1_cfd_compute_step_factor.rodinia_3_1_cfd_compute_step_factor(), amd_app_sdk_3_0_ScanLargeArrays_ScanLargeArrays.amd_app_sdk_3_0_ScanLargeArrays_ScanLargeArrays(), polybench_gpu_1_0_gemm_gemm.polybench_gpu_1_0_gemm_gemm(), npb_3_3_BT_exact_rhs1.npb_3_3_BT_exact_rhs1(), npb_3_3_BT_x_solve2.npb_3_3_BT_x_solve2(), amd_app_sdk_3_0_ScanLargeArrays_prefixSum.amd_app_sdk_3_0_ScanLargeArrays_prefixSum(), npb_3_3_LU_ssor3.npb_3_3_LU_ssor3(), shoc_1_1_5_Spmv_spmv_ellpackr_kernel.shoc_1_1_5_Spmv_spmv_ellpackr_kernel(), nvidia_4_2_VectorAdd_VectorAdd.nvidia_4_2_VectorAdd_VectorAdd(), polybench_gpu_1_0_2DConvolution_Convolution2D_kernel.polybench_gpu_1_0_2DConvolution_Convolution2D_kernel(), shoc_1_1_5_Sort_top_scan.shoc_1_1_5_Sort_top_scan(), npb_3_3_CG_makea_4.npb_3_3_CG_makea_4(), nvidia_4_2_MatVecMul_MatVecMulCoalesced2.nvidia_4_2_MatVecMul_MatVecMulCoalesced2(), nvidia_4_2_MatVecMul_MatVecMulUncoalesced0.nvidia_4_2_MatVecMul_MatVecMulUncoalesced0(), nvidia_4_2_MersenneTwister_BoxMuller.nvidia_4_2_MersenneTwister_BoxMuller(), npb_3_3_BT_exact_rhs5.npb_3_3_BT_exact_rhs5(), npb_3_3_FT_cffts2.npb_3_3_FT_cffts2(), amd_app_sdk_3_0_BitonicSort_bitonicSort.amd_app_sdk_3_0_BitonicSort_bitonicSort(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1(), npb_3_3_CG_main_1.npb_3_3_CG_main_1(), npb_3_3_BT_initialize3.npb_3_3_BT_initialize3(), rodinia_3_1_gaussian_Fan2.rodinia_3_1_gaussian_Fan2(), polybench_gpu_1_0_correlation_std_kernel.polybench_gpu_1_0_correlation_std_kernel(), polybench_gpu_1_0_2mm_mm2_kernel1.polybench_gpu_1_0_2mm_mm2_kernel1(), polybench_gpu_1_0_correlation_reduce_kernel.polybench_gpu_1_0_correlation_reduce_kernel(), polybench_gpu_1_0_covariance_mean_kernel.polybench_gpu_1_0_covariance_mean_kernel(), npb_3_3_FT_evolve.npb_3_3_FT_evolve(), npb_3_3_CG_main_0.npb_3_3_CG_main_0(), amd_app_sdk_3_0_FloydWarshall_floydWarshallPass.amd_app_sdk_3_0_FloydWarshall_floydWarshallPass(), rodinia_3_1_nn_NearestNeighbor.rodinia_3_1_nn_NearestNeighbor(), npb_3_3_FT_cffts3.npb_3_3_FT_cffts3(), parboil_0_2_spmv_A.parboil_0_2_spmv_A(), nvidia_4_2_MatVecMul_MatVecMulUncoalesced1.nvidia_4_2_MatVecMul_MatVecMulUncoalesced1(), polybench_gpu_1_0_mvt_mvt_kernel1.polybench_gpu_1_0_mvt_mvt_kernel1(), amd_app_sdk_3_0_SimpleConvolution_simpleSeparableConvolutionPass1.amd_app_sdk_3_0_SimpleConvolution_simpleSeparableConvolutionPass1(), npb_3_3_CG_conj_grad_0.npb_3_3_CG_conj_grad_0(), polybench_gpu_1_0_3mm_mm3_kernel1.polybench_gpu_1_0_3mm_mm3_kernel1(), npb_3_3_SP_initialize3.npb_3_3_SP_initialize3(), rodinia_3_1_particlefilter_find_index_kernel.rodinia_3_1_particlefilter_find_index_kernel(), npb_3_3_SP_initialize1.npb_3_3_SP_initialize1(), shoc_1_1_5_FFT_chk1D_512.shoc_1_1_5_FFT_chk1D_512(), nvidia_4_2_DotProduct_DotProduct.nvidia_4_2_DotProduct_DotProduct(), polybench_gpu_1_0_3mm_mm3_kernel3.polybench_gpu_1_0_3mm_mm3_kernel3(), amd_app_sdk_3_0_PrefixSum_group_prefixSum.amd_app_sdk_3_0_PrefixSum_group_prefixSum(), npb_3_3_BT_z_solve2.npb_3_3_BT_z_solve2(), shoc_1_1_5_BFS_BFS_kernel_warp.shoc_1_1_5_BFS_BFS_kernel_warp(), nvidia_4_2_MatVecMul_MatVecMulCoalesced1.nvidia_4_2_MatVecMul_MatVecMulCoalesced1(), rodinia_3_1_cfd_time_step.rodinia_3_1_cfd_time_step(), npb_3_3_CG_init_mem_1.npb_3_3_CG_init_mem_1(), polybench_gpu_1_0_covariance_covar_kernel.polybench_gpu_1_0_covariance_covar_kernel(), npb_3_3_FT_cffts1.npb_3_3_FT_cffts1(), polybench_gpu_1_0_gesummv_gesummv_kernel.polybench_gpu_1_0_gesummv_gesummv_kernel(), rodinia_3_1_cfd_memset_kernel.rodinia_3_1_cfd_memset_kernel(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2(), npb_3_3_BT_add.npb_3_3_BT_add(), npb_3_3_CG_main_2.npb_3_3_CG_main_2(), rodinia_3_1_gaussian_Fan1.rodinia_3_1_gaussian_Fan1(), polybench_gpu_1_0_2mm_mm2_kernel2.polybench_gpu_1_0_2mm_mm2_kernel2(), amd_app_sdk_3_0_MatrixTranspose_matrixTranspose.amd_app_sdk_3_0_MatrixTranspose_matrixTranspose(), npb_3_3_BT_initialize1.npb_3_3_BT_initialize1(), shoc_1_1_5_Scan_reduce.shoc_1_1_5_Scan_reduce(), npb_3_3_SP_exact_rhs5.npb_3_3_SP_exact_rhs5(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel3.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel3(), polybench_gpu_1_0_syrk_syrk_kernel.polybench_gpu_1_0_syrk_syrk_kernel(), npb_3_3_BT_compute_rhs6.npb_3_3_BT_compute_rhs6(), rodinia_3_1_streamcluster_memset_kernel.rodinia_3_1_streamcluster_memset_kernel(), npb_3_3_CG_init_mem_0.npb_3_3_CG_init_mem_0(), shoc_1_1_5_Reduction_reduce.shoc_1_1_5_Reduction_reduce(), rodinia_3_1_kmeans_kmeans_kernel_c.rodinia_3_1_kmeans_kmeans_kernel_c(), nvidia_4_2_MatVecMul_MatVecMulCoalesced0.nvidia_4_2_MatVecMul_MatVecMulCoalesced0(), npb_3_3_FT_checksum.npb_3_3_FT_checksum(), npb_3_3_SP_compute_rhs2.npb_3_3_SP_compute_rhs2(), npb_3_3_FT_init_ui.npb_3_3_FT_init_ui(), polybench_gpu_1_0_covariance_reduce_kernel.polybench_gpu_1_0_covariance_reduce_kernel(), polybench_gpu_1_0_mvt_mvt_kernel2.polybench_gpu_1_0_mvt_mvt_kernel2(), rodinia_3_1_particlefilter_sum_kernel.rodinia_3_1_particlefilter_sum_kernel(), amd_app_sdk_3_0_SimpleConvolution_simpleSeparableConvolutionPass2.amd_app_sdk_3_0_SimpleConvolution_simpleSeparableConvolutionPass2(), polybench_gpu_1_0_3mm_mm3_kernel2.polybench_gpu_1_0_3mm_mm3_kernel2(), npb_3_3_SP_pinvr.npb_3_3_SP_pinvr(), npb_3_3_CG_makea_2.npb_3_3_CG_makea_2()]
		self.labels = [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1]
		for g in self.graphs:
			g.ndata['m'] = nodeFeatures(g, 'multifractal')
	def __len__(self):
		return len(self.graphs)
	def __getitem__(self, idx):
		return self.graphs[idx], self.labels[idx]
