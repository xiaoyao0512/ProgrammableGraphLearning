import torch
from torch.utils.data import Dataset, DataLoader
import sys
import multifractal
sys.path.append('graphs/')
import polybench_gpu_1_0_bicg_bicgKernel1_1
import polybench_gpu_1_0_bicg_bicgKernel1_2
import polybench_gpu_1_0_bicg_bicgKernel1_3
import polybench_gpu_1_0_bicg_bicgKernel1_4
import polybench_gpu_1_0_bicg_bicgKernel1_12
import polybench_gpu_1_0_bicg_bicgKernel1_13
import polybench_gpu_1_0_bicg_bicgKernel1_14
import polybench_gpu_1_0_bicg_bicgKernel1_15
import shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_1
import shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_2
import shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_3
import shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_4
import shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_12
import shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_13
import shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_14
import shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_15
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_1
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_2
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_3
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_4
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_12
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_13
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_14
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_15
import npb_3_3_CG_main_2_1
import npb_3_3_CG_main_2_2
import npb_3_3_CG_main_2_3
import npb_3_3_CG_main_2_4
import npb_3_3_CG_main_2_12
import npb_3_3_CG_main_2_13
import npb_3_3_CG_main_2_14
import npb_3_3_CG_main_2_15
import npb_3_3_CG_makea_2_1
import npb_3_3_CG_makea_2_2
import npb_3_3_CG_makea_2_3
import npb_3_3_CG_makea_2_4
import npb_3_3_CG_makea_2_12
import npb_3_3_CG_makea_2_13
import npb_3_3_CG_makea_2_14
import npb_3_3_CG_makea_2_15
import polybench_gpu_1_0_atax_atax_kernel1_1
import polybench_gpu_1_0_atax_atax_kernel1_2
import polybench_gpu_1_0_atax_atax_kernel1_3
import polybench_gpu_1_0_atax_atax_kernel1_4
import polybench_gpu_1_0_atax_atax_kernel1_12
import polybench_gpu_1_0_atax_atax_kernel1_13
import polybench_gpu_1_0_atax_atax_kernel1_14
import polybench_gpu_1_0_atax_atax_kernel1_15
import npb_3_3_FT_init_ui_1
import npb_3_3_FT_init_ui_2
import npb_3_3_FT_init_ui_3
import npb_3_3_FT_init_ui_4
import npb_3_3_FT_init_ui_12
import npb_3_3_FT_init_ui_13
import npb_3_3_FT_init_ui_14
import npb_3_3_FT_init_ui_15
import amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_1
import amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_2
import amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_3
import amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_4
import amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_12
import amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_13
import amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_14
import amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_15
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_1
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_2
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_3
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_4
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_12
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_13
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_14
import polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_15
import amd_app_sdk_3_0_ScanLargeArrays_blockAddition_1
import amd_app_sdk_3_0_ScanLargeArrays_blockAddition_2
import amd_app_sdk_3_0_ScanLargeArrays_blockAddition_3
import amd_app_sdk_3_0_ScanLargeArrays_blockAddition_4
import amd_app_sdk_3_0_ScanLargeArrays_blockAddition_12
import amd_app_sdk_3_0_ScanLargeArrays_blockAddition_13
import amd_app_sdk_3_0_ScanLargeArrays_blockAddition_14
import amd_app_sdk_3_0_ScanLargeArrays_blockAddition_15
import npb_3_3_CG_main_1_1
import npb_3_3_CG_main_1_2
import npb_3_3_CG_main_1_3
import npb_3_3_CG_main_1_4
import npb_3_3_CG_main_1_12
import npb_3_3_CG_main_1_13
import npb_3_3_CG_main_1_14
import npb_3_3_CG_main_1_15
import rodinia_3_1_cfd_memset_kernel_1
import rodinia_3_1_cfd_memset_kernel_2
import rodinia_3_1_cfd_memset_kernel_3
import rodinia_3_1_cfd_memset_kernel_4
import rodinia_3_1_cfd_memset_kernel_12
import rodinia_3_1_cfd_memset_kernel_13
import rodinia_3_1_cfd_memset_kernel_14
import rodinia_3_1_cfd_memset_kernel_15
import npb_3_3_CG_conj_grad_0_1
import npb_3_3_CG_conj_grad_0_2
import npb_3_3_CG_conj_grad_0_3
import npb_3_3_CG_conj_grad_0_4
import npb_3_3_CG_conj_grad_0_12
import npb_3_3_CG_conj_grad_0_13
import npb_3_3_CG_conj_grad_0_14
import npb_3_3_CG_conj_grad_0_15
import npb_3_3_FT_compute_indexmap_1
import npb_3_3_FT_compute_indexmap_2
import npb_3_3_FT_compute_indexmap_3
import npb_3_3_FT_compute_indexmap_4
import npb_3_3_FT_compute_indexmap_12
import npb_3_3_FT_compute_indexmap_13
import npb_3_3_FT_compute_indexmap_14
import npb_3_3_FT_compute_indexmap_15
import npb_3_3_FT_compute_indexmap2_1
import npb_3_3_FT_compute_indexmap2_2
import npb_3_3_FT_compute_indexmap2_3
import npb_3_3_FT_compute_indexmap2_4
import npb_3_3_FT_compute_indexmap2_12
import npb_3_3_FT_compute_indexmap2_13
import npb_3_3_FT_compute_indexmap2_14
import npb_3_3_FT_compute_indexmap2_15
import npb_3_3_FT_compute_indexmap3_1
import npb_3_3_FT_compute_indexmap3_2
import npb_3_3_FT_compute_indexmap3_3
import npb_3_3_FT_compute_indexmap3_4
import npb_3_3_FT_compute_indexmap3_12
import npb_3_3_FT_compute_indexmap3_13
import npb_3_3_FT_compute_indexmap3_14
import npb_3_3_FT_compute_indexmap3_15
import npb_3_3_FT_evolve_1
import npb_3_3_FT_evolve_2
import npb_3_3_FT_evolve_3
import npb_3_3_FT_evolve_4
import npb_3_3_FT_evolve_12
import npb_3_3_FT_evolve_13
import npb_3_3_FT_evolve_14
import npb_3_3_FT_evolve_15
import npb_3_3_CG_main_0_1
import npb_3_3_CG_main_0_2
import npb_3_3_CG_main_0_3
import npb_3_3_CG_main_0_4
import npb_3_3_CG_main_0_12
import npb_3_3_CG_main_0_13
import npb_3_3_CG_main_0_14
import npb_3_3_CG_main_0_15
import shoc_1_1_5_Spmv_spmv_ellpackr_kernel_1
import shoc_1_1_5_Spmv_spmv_ellpackr_kernel_2
import shoc_1_1_5_Spmv_spmv_ellpackr_kernel_3
import shoc_1_1_5_Spmv_spmv_ellpackr_kernel_4
import shoc_1_1_5_Spmv_spmv_ellpackr_kernel_12
import shoc_1_1_5_Spmv_spmv_ellpackr_kernel_13
import shoc_1_1_5_Spmv_spmv_ellpackr_kernel_14
import shoc_1_1_5_Spmv_spmv_ellpackr_kernel_15
import shoc_1_1_5_Triad_Triad_1
import shoc_1_1_5_Triad_Triad_2
import shoc_1_1_5_Triad_Triad_3
import shoc_1_1_5_Triad_Triad_4
import shoc_1_1_5_Triad_Triad_12
import shoc_1_1_5_Triad_Triad_13
import shoc_1_1_5_Triad_Triad_14
import shoc_1_1_5_Triad_Triad_15
import npb_3_3_CG_init_mem_0_1
import npb_3_3_CG_init_mem_0_2
import npb_3_3_CG_init_mem_0_3
import npb_3_3_CG_init_mem_0_4
import npb_3_3_CG_init_mem_0_12
import npb_3_3_CG_init_mem_0_13
import npb_3_3_CG_init_mem_0_14
import npb_3_3_CG_init_mem_0_15
import rodinia_3_1_particlefilter_sum_kernel_1
import rodinia_3_1_particlefilter_sum_kernel_2
import rodinia_3_1_particlefilter_sum_kernel_3
import rodinia_3_1_particlefilter_sum_kernel_4
import rodinia_3_1_particlefilter_sum_kernel_12
import rodinia_3_1_particlefilter_sum_kernel_13
import rodinia_3_1_particlefilter_sum_kernel_14
import rodinia_3_1_particlefilter_sum_kernel_15
import npb_3_3_CG_init_mem_1_1
import npb_3_3_CG_init_mem_1_2
import npb_3_3_CG_init_mem_1_3
import npb_3_3_CG_init_mem_1_4
import npb_3_3_CG_init_mem_1_12
import npb_3_3_CG_init_mem_1_13
import npb_3_3_CG_init_mem_1_14
import npb_3_3_CG_init_mem_1_15
import polybench_gpu_1_0_covariance_mean_kernel_1
import polybench_gpu_1_0_covariance_mean_kernel_2
import polybench_gpu_1_0_covariance_mean_kernel_3
import polybench_gpu_1_0_covariance_mean_kernel_4
import polybench_gpu_1_0_covariance_mean_kernel_12
import polybench_gpu_1_0_covariance_mean_kernel_13
import polybench_gpu_1_0_covariance_mean_kernel_14
import polybench_gpu_1_0_covariance_mean_kernel_15
import rodinia_3_1_cfd_initialize_variables_1
import rodinia_3_1_cfd_initialize_variables_2
import rodinia_3_1_cfd_initialize_variables_3
import rodinia_3_1_cfd_initialize_variables_4
import rodinia_3_1_cfd_initialize_variables_12
import rodinia_3_1_cfd_initialize_variables_13
import rodinia_3_1_cfd_initialize_variables_14
import rodinia_3_1_cfd_initialize_variables_15
import polybench_gpu_1_0_gesummv_gesummv_kernel_1
import polybench_gpu_1_0_gesummv_gesummv_kernel_2
import polybench_gpu_1_0_gesummv_gesummv_kernel_3
import polybench_gpu_1_0_gesummv_gesummv_kernel_4
import polybench_gpu_1_0_gesummv_gesummv_kernel_12
import polybench_gpu_1_0_gesummv_gesummv_kernel_13
import polybench_gpu_1_0_gesummv_gesummv_kernel_14
import polybench_gpu_1_0_gesummv_gesummv_kernel_15
import npb_3_3_CG_makea_7_1
import npb_3_3_CG_makea_7_2
import npb_3_3_CG_makea_7_3
import npb_3_3_CG_makea_7_4
import npb_3_3_CG_makea_7_12
import npb_3_3_CG_makea_7_13
import npb_3_3_CG_makea_7_14
import npb_3_3_CG_makea_7_15
import polybench_gpu_1_0_mvt_mvt_kernel2_1
import polybench_gpu_1_0_mvt_mvt_kernel2_2
import polybench_gpu_1_0_mvt_mvt_kernel2_3
import polybench_gpu_1_0_mvt_mvt_kernel2_4
import polybench_gpu_1_0_mvt_mvt_kernel2_12
import polybench_gpu_1_0_mvt_mvt_kernel2_13
import polybench_gpu_1_0_mvt_mvt_kernel2_14
import polybench_gpu_1_0_mvt_mvt_kernel2_15
import nvidia_4_2_DotProduct_DotProduct_1
import nvidia_4_2_DotProduct_DotProduct_2
import nvidia_4_2_DotProduct_DotProduct_3
import nvidia_4_2_DotProduct_DotProduct_4
import nvidia_4_2_DotProduct_DotProduct_12
import nvidia_4_2_DotProduct_DotProduct_13
import nvidia_4_2_DotProduct_DotProduct_14
import nvidia_4_2_DotProduct_DotProduct_15
import rodinia_3_1_streamcluster_memset_kernel_1
import rodinia_3_1_streamcluster_memset_kernel_2
import rodinia_3_1_streamcluster_memset_kernel_3
import rodinia_3_1_streamcluster_memset_kernel_4
import rodinia_3_1_streamcluster_memset_kernel_12
import rodinia_3_1_streamcluster_memset_kernel_13
import rodinia_3_1_streamcluster_memset_kernel_14
import rodinia_3_1_streamcluster_memset_kernel_15
import MatVecMul_1
import MatVecMul_2
import MatVecMul_3
import MatVecMul_4
import MatVecMul_12
import MatVecMul_13
import MatVecMul_14
import MatVecMul_15
import nvidia_4_2_VectorAdd_VectorAdd_1
import nvidia_4_2_VectorAdd_VectorAdd_2
import nvidia_4_2_VectorAdd_VectorAdd_3
import nvidia_4_2_VectorAdd_VectorAdd_4
import nvidia_4_2_VectorAdd_VectorAdd_12
import nvidia_4_2_VectorAdd_VectorAdd_13
import nvidia_4_2_VectorAdd_VectorAdd_14
import nvidia_4_2_VectorAdd_VectorAdd_15
import numpy as np

def nodeFeatures(g, types):
    #g = dgl.add_self_loop(g)
    #graph = dgl.DGLGraph.to_networkx(g)
    if (types == "simple"):
        return g.in_degrees()
    elif (types == "weight"):
        return dgl.khop_adj(g, 1) #g.ndata['w']
    elif (types == "multifractal"):
        return multifractal.multifractal(g)

class GraphDataset(Dataset):
	def __init__(self):
		self.graphs = [polybench_gpu_1_0_bicg_bicgKernel1_1.polybench_gpu_1_0_bicg_bicgKernel1_1(), polybench_gpu_1_0_bicg_bicgKernel1_2.polybench_gpu_1_0_bicg_bicgKernel1_2(), polybench_gpu_1_0_bicg_bicgKernel1_3.polybench_gpu_1_0_bicg_bicgKernel1_3(), polybench_gpu_1_0_bicg_bicgKernel1_4.polybench_gpu_1_0_bicg_bicgKernel1_4(), polybench_gpu_1_0_bicg_bicgKernel1_12.polybench_gpu_1_0_bicg_bicgKernel1_12(), polybench_gpu_1_0_bicg_bicgKernel1_13.polybench_gpu_1_0_bicg_bicgKernel1_13(), polybench_gpu_1_0_bicg_bicgKernel1_14.polybench_gpu_1_0_bicg_bicgKernel1_14(), polybench_gpu_1_0_bicg_bicgKernel1_15.polybench_gpu_1_0_bicg_bicgKernel1_15(), shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_1.shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_1(), shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_2.shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_2(), shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_3.shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_3(), shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_4.shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_4(), shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_12.shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_12(), shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_13.shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_13(), shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_14.shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_14(), shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_15.shoc_1_1_5_Spmv_spmv_csr_scalar_kernel_15(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_1.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_1(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_2.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_2(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_3.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_3(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_4.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_4(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_12.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_12(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_13.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_13(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_14.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_14(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_15.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel2_15(), npb_3_3_CG_main_2_1.npb_3_3_CG_main_2_1(), npb_3_3_CG_main_2_2.npb_3_3_CG_main_2_2(), npb_3_3_CG_main_2_3.npb_3_3_CG_main_2_3(), npb_3_3_CG_main_2_4.npb_3_3_CG_main_2_4(), npb_3_3_CG_main_2_12.npb_3_3_CG_main_2_12(), npb_3_3_CG_main_2_13.npb_3_3_CG_main_2_13(), npb_3_3_CG_main_2_14.npb_3_3_CG_main_2_14(), npb_3_3_CG_main_2_15.npb_3_3_CG_main_2_15(), npb_3_3_CG_makea_2_1.npb_3_3_CG_makea_2_1(), npb_3_3_CG_makea_2_2.npb_3_3_CG_makea_2_2(), npb_3_3_CG_makea_2_3.npb_3_3_CG_makea_2_3(), npb_3_3_CG_makea_2_4.npb_3_3_CG_makea_2_4(), npb_3_3_CG_makea_2_12.npb_3_3_CG_makea_2_12(), npb_3_3_CG_makea_2_13.npb_3_3_CG_makea_2_13(), npb_3_3_CG_makea_2_14.npb_3_3_CG_makea_2_14(), npb_3_3_CG_makea_2_15.npb_3_3_CG_makea_2_15(), polybench_gpu_1_0_atax_atax_kernel1_1.polybench_gpu_1_0_atax_atax_kernel1_1(), polybench_gpu_1_0_atax_atax_kernel1_2.polybench_gpu_1_0_atax_atax_kernel1_2(), polybench_gpu_1_0_atax_atax_kernel1_3.polybench_gpu_1_0_atax_atax_kernel1_3(), polybench_gpu_1_0_atax_atax_kernel1_4.polybench_gpu_1_0_atax_atax_kernel1_4(), polybench_gpu_1_0_atax_atax_kernel1_12.polybench_gpu_1_0_atax_atax_kernel1_12(), polybench_gpu_1_0_atax_atax_kernel1_13.polybench_gpu_1_0_atax_atax_kernel1_13(), polybench_gpu_1_0_atax_atax_kernel1_14.polybench_gpu_1_0_atax_atax_kernel1_14(), polybench_gpu_1_0_atax_atax_kernel1_15.polybench_gpu_1_0_atax_atax_kernel1_15(), npb_3_3_FT_init_ui_1.npb_3_3_FT_init_ui_1(), npb_3_3_FT_init_ui_2.npb_3_3_FT_init_ui_2(), npb_3_3_FT_init_ui_3.npb_3_3_FT_init_ui_3(), npb_3_3_FT_init_ui_4.npb_3_3_FT_init_ui_4(), npb_3_3_FT_init_ui_12.npb_3_3_FT_init_ui_12(), npb_3_3_FT_init_ui_13.npb_3_3_FT_init_ui_13(), npb_3_3_FT_init_ui_14.npb_3_3_FT_init_ui_14(), npb_3_3_FT_init_ui_15.npb_3_3_FT_init_ui_15(), amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_1.amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_1(), amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_2.amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_2(), amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_3.amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_3(), amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_4.amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_4(), amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_12.amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_12(), amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_13.amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_13(), amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_14.amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_14(), amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_15.amd_app_sdk_3_0_FastWalshTransform_fastWalshTransform_15(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_1.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_1(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_2.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_2(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_3.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_3(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_4.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_4(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_12.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_12(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_13.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_13(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_14.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_14(), polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_15.polybench_gpu_1_0_gramschmidt_gramschmidt_kernel1_15(), amd_app_sdk_3_0_ScanLargeArrays_blockAddition_1.amd_app_sdk_3_0_ScanLargeArrays_blockAddition_1(), amd_app_sdk_3_0_ScanLargeArrays_blockAddition_2.amd_app_sdk_3_0_ScanLargeArrays_blockAddition_2(), amd_app_sdk_3_0_ScanLargeArrays_blockAddition_3.amd_app_sdk_3_0_ScanLargeArrays_blockAddition_3(), amd_app_sdk_3_0_ScanLargeArrays_blockAddition_4.amd_app_sdk_3_0_ScanLargeArrays_blockAddition_4(), amd_app_sdk_3_0_ScanLargeArrays_blockAddition_12.amd_app_sdk_3_0_ScanLargeArrays_blockAddition_12(), amd_app_sdk_3_0_ScanLargeArrays_blockAddition_13.amd_app_sdk_3_0_ScanLargeArrays_blockAddition_13(), amd_app_sdk_3_0_ScanLargeArrays_blockAddition_14.amd_app_sdk_3_0_ScanLargeArrays_blockAddition_14(), amd_app_sdk_3_0_ScanLargeArrays_blockAddition_15.amd_app_sdk_3_0_ScanLargeArrays_blockAddition_15(), npb_3_3_CG_main_1_1.npb_3_3_CG_main_1_1(), npb_3_3_CG_main_1_2.npb_3_3_CG_main_1_2(), npb_3_3_CG_main_1_3.npb_3_3_CG_main_1_3(), npb_3_3_CG_main_1_4.npb_3_3_CG_main_1_4(), npb_3_3_CG_main_1_12.npb_3_3_CG_main_1_12(), npb_3_3_CG_main_1_13.npb_3_3_CG_main_1_13(), npb_3_3_CG_main_1_14.npb_3_3_CG_main_1_14(), npb_3_3_CG_main_1_15.npb_3_3_CG_main_1_15(), rodinia_3_1_cfd_memset_kernel_1.rodinia_3_1_cfd_memset_kernel_1(), rodinia_3_1_cfd_memset_kernel_2.rodinia_3_1_cfd_memset_kernel_2(), rodinia_3_1_cfd_memset_kernel_3.rodinia_3_1_cfd_memset_kernel_3(), rodinia_3_1_cfd_memset_kernel_4.rodinia_3_1_cfd_memset_kernel_4(), rodinia_3_1_cfd_memset_kernel_12.rodinia_3_1_cfd_memset_kernel_12(), rodinia_3_1_cfd_memset_kernel_13.rodinia_3_1_cfd_memset_kernel_13(), rodinia_3_1_cfd_memset_kernel_14.rodinia_3_1_cfd_memset_kernel_14(), rodinia_3_1_cfd_memset_kernel_15.rodinia_3_1_cfd_memset_kernel_15(), npb_3_3_CG_conj_grad_0_1.npb_3_3_CG_conj_grad_0_1(), npb_3_3_CG_conj_grad_0_2.npb_3_3_CG_conj_grad_0_2(), npb_3_3_CG_conj_grad_0_3.npb_3_3_CG_conj_grad_0_3(), npb_3_3_CG_conj_grad_0_4.npb_3_3_CG_conj_grad_0_4(), npb_3_3_CG_conj_grad_0_12.npb_3_3_CG_conj_grad_0_12(), npb_3_3_CG_conj_grad_0_13.npb_3_3_CG_conj_grad_0_13(), npb_3_3_CG_conj_grad_0_14.npb_3_3_CG_conj_grad_0_14(), npb_3_3_CG_conj_grad_0_15.npb_3_3_CG_conj_grad_0_15(), npb_3_3_FT_compute_indexmap_1.npb_3_3_FT_compute_indexmap_1(), npb_3_3_FT_compute_indexmap_2.npb_3_3_FT_compute_indexmap_2(), npb_3_3_FT_compute_indexmap_3.npb_3_3_FT_compute_indexmap_3(), npb_3_3_FT_compute_indexmap_4.npb_3_3_FT_compute_indexmap_4(), npb_3_3_FT_compute_indexmap_12.npb_3_3_FT_compute_indexmap_12(), npb_3_3_FT_compute_indexmap_13.npb_3_3_FT_compute_indexmap_13(), npb_3_3_FT_compute_indexmap_14.npb_3_3_FT_compute_indexmap_14(), npb_3_3_FT_compute_indexmap_15.npb_3_3_FT_compute_indexmap_15(), npb_3_3_FT_compute_indexmap2_1.npb_3_3_FT_compute_indexmap2_1(), npb_3_3_FT_compute_indexmap2_2.npb_3_3_FT_compute_indexmap2_2(), npb_3_3_FT_compute_indexmap2_3.npb_3_3_FT_compute_indexmap2_3(), npb_3_3_FT_compute_indexmap2_4.npb_3_3_FT_compute_indexmap2_4(), npb_3_3_FT_compute_indexmap2_12.npb_3_3_FT_compute_indexmap2_12(), npb_3_3_FT_compute_indexmap2_13.npb_3_3_FT_compute_indexmap2_13(), npb_3_3_FT_compute_indexmap2_14.npb_3_3_FT_compute_indexmap2_14(), npb_3_3_FT_compute_indexmap2_15.npb_3_3_FT_compute_indexmap2_15(), npb_3_3_FT_compute_indexmap3_1.npb_3_3_FT_compute_indexmap3_1(), npb_3_3_FT_compute_indexmap3_2.npb_3_3_FT_compute_indexmap3_2(), npb_3_3_FT_compute_indexmap3_3.npb_3_3_FT_compute_indexmap3_3(), npb_3_3_FT_compute_indexmap3_4.npb_3_3_FT_compute_indexmap3_4(), npb_3_3_FT_compute_indexmap3_12.npb_3_3_FT_compute_indexmap3_12(), npb_3_3_FT_compute_indexmap3_13.npb_3_3_FT_compute_indexmap3_13(), npb_3_3_FT_compute_indexmap3_14.npb_3_3_FT_compute_indexmap3_14(), npb_3_3_FT_compute_indexmap3_15.npb_3_3_FT_compute_indexmap3_15(), npb_3_3_FT_evolve_1.npb_3_3_FT_evolve_1(), npb_3_3_FT_evolve_2.npb_3_3_FT_evolve_2(), npb_3_3_FT_evolve_3.npb_3_3_FT_evolve_3(), npb_3_3_FT_evolve_4.npb_3_3_FT_evolve_4(), npb_3_3_FT_evolve_12.npb_3_3_FT_evolve_12(), npb_3_3_FT_evolve_13.npb_3_3_FT_evolve_13(), npb_3_3_FT_evolve_14.npb_3_3_FT_evolve_14(), npb_3_3_FT_evolve_15.npb_3_3_FT_evolve_15(), npb_3_3_CG_main_0_1.npb_3_3_CG_main_0_1(), npb_3_3_CG_main_0_2.npb_3_3_CG_main_0_2(), npb_3_3_CG_main_0_3.npb_3_3_CG_main_0_3(), npb_3_3_CG_main_0_4.npb_3_3_CG_main_0_4(), npb_3_3_CG_main_0_12.npb_3_3_CG_main_0_12(), npb_3_3_CG_main_0_13.npb_3_3_CG_main_0_13(), npb_3_3_CG_main_0_14.npb_3_3_CG_main_0_14(), npb_3_3_CG_main_0_15.npb_3_3_CG_main_0_15(), shoc_1_1_5_Spmv_spmv_ellpackr_kernel_1.shoc_1_1_5_Spmv_spmv_ellpackr_kernel_1(), shoc_1_1_5_Spmv_spmv_ellpackr_kernel_2.shoc_1_1_5_Spmv_spmv_ellpackr_kernel_2(), shoc_1_1_5_Spmv_spmv_ellpackr_kernel_3.shoc_1_1_5_Spmv_spmv_ellpackr_kernel_3(), shoc_1_1_5_Spmv_spmv_ellpackr_kernel_4.shoc_1_1_5_Spmv_spmv_ellpackr_kernel_4(), shoc_1_1_5_Spmv_spmv_ellpackr_kernel_12.shoc_1_1_5_Spmv_spmv_ellpackr_kernel_12(), shoc_1_1_5_Spmv_spmv_ellpackr_kernel_13.shoc_1_1_5_Spmv_spmv_ellpackr_kernel_13(), shoc_1_1_5_Spmv_spmv_ellpackr_kernel_14.shoc_1_1_5_Spmv_spmv_ellpackr_kernel_14(), shoc_1_1_5_Spmv_spmv_ellpackr_kernel_15.shoc_1_1_5_Spmv_spmv_ellpackr_kernel_15(), shoc_1_1_5_Triad_Triad_1.shoc_1_1_5_Triad_Triad_1(), shoc_1_1_5_Triad_Triad_2.shoc_1_1_5_Triad_Triad_2(), shoc_1_1_5_Triad_Triad_3.shoc_1_1_5_Triad_Triad_3(), shoc_1_1_5_Triad_Triad_4.shoc_1_1_5_Triad_Triad_4(), shoc_1_1_5_Triad_Triad_12.shoc_1_1_5_Triad_Triad_12(), shoc_1_1_5_Triad_Triad_13.shoc_1_1_5_Triad_Triad_13(), shoc_1_1_5_Triad_Triad_14.shoc_1_1_5_Triad_Triad_14(), shoc_1_1_5_Triad_Triad_15.shoc_1_1_5_Triad_Triad_15(), npb_3_3_CG_init_mem_0_1.npb_3_3_CG_init_mem_0_1(), npb_3_3_CG_init_mem_0_2.npb_3_3_CG_init_mem_0_2(), npb_3_3_CG_init_mem_0_3.npb_3_3_CG_init_mem_0_3(), npb_3_3_CG_init_mem_0_4.npb_3_3_CG_init_mem_0_4(), npb_3_3_CG_init_mem_0_12.npb_3_3_CG_init_mem_0_12(), npb_3_3_CG_init_mem_0_13.npb_3_3_CG_init_mem_0_13(), npb_3_3_CG_init_mem_0_14.npb_3_3_CG_init_mem_0_14(), npb_3_3_CG_init_mem_0_15.npb_3_3_CG_init_mem_0_15(), rodinia_3_1_particlefilter_sum_kernel_1.rodinia_3_1_particlefilter_sum_kernel_1(), rodinia_3_1_particlefilter_sum_kernel_2.rodinia_3_1_particlefilter_sum_kernel_2(), rodinia_3_1_particlefilter_sum_kernel_3.rodinia_3_1_particlefilter_sum_kernel_3(), rodinia_3_1_particlefilter_sum_kernel_4.rodinia_3_1_particlefilter_sum_kernel_4(), rodinia_3_1_particlefilter_sum_kernel_12.rodinia_3_1_particlefilter_sum_kernel_12(), rodinia_3_1_particlefilter_sum_kernel_13.rodinia_3_1_particlefilter_sum_kernel_13(), rodinia_3_1_particlefilter_sum_kernel_14.rodinia_3_1_particlefilter_sum_kernel_14(), rodinia_3_1_particlefilter_sum_kernel_15.rodinia_3_1_particlefilter_sum_kernel_15(), npb_3_3_CG_init_mem_1_1.npb_3_3_CG_init_mem_1_1(), npb_3_3_CG_init_mem_1_2.npb_3_3_CG_init_mem_1_2(), npb_3_3_CG_init_mem_1_3.npb_3_3_CG_init_mem_1_3(), npb_3_3_CG_init_mem_1_4.npb_3_3_CG_init_mem_1_4(), npb_3_3_CG_init_mem_1_12.npb_3_3_CG_init_mem_1_12(), npb_3_3_CG_init_mem_1_13.npb_3_3_CG_init_mem_1_13(), npb_3_3_CG_init_mem_1_14.npb_3_3_CG_init_mem_1_14(), npb_3_3_CG_init_mem_1_15.npb_3_3_CG_init_mem_1_15(), polybench_gpu_1_0_covariance_mean_kernel_1.polybench_gpu_1_0_covariance_mean_kernel_1(), polybench_gpu_1_0_covariance_mean_kernel_2.polybench_gpu_1_0_covariance_mean_kernel_2(), polybench_gpu_1_0_covariance_mean_kernel_3.polybench_gpu_1_0_covariance_mean_kernel_3(), polybench_gpu_1_0_covariance_mean_kernel_4.polybench_gpu_1_0_covariance_mean_kernel_4(), polybench_gpu_1_0_covariance_mean_kernel_12.polybench_gpu_1_0_covariance_mean_kernel_12(), polybench_gpu_1_0_covariance_mean_kernel_13.polybench_gpu_1_0_covariance_mean_kernel_13(), polybench_gpu_1_0_covariance_mean_kernel_14.polybench_gpu_1_0_covariance_mean_kernel_14(), polybench_gpu_1_0_covariance_mean_kernel_15.polybench_gpu_1_0_covariance_mean_kernel_15(), rodinia_3_1_cfd_initialize_variables_1.rodinia_3_1_cfd_initialize_variables_1(), rodinia_3_1_cfd_initialize_variables_2.rodinia_3_1_cfd_initialize_variables_2(), rodinia_3_1_cfd_initialize_variables_3.rodinia_3_1_cfd_initialize_variables_3(), rodinia_3_1_cfd_initialize_variables_4.rodinia_3_1_cfd_initialize_variables_4(), rodinia_3_1_cfd_initialize_variables_12.rodinia_3_1_cfd_initialize_variables_12(), rodinia_3_1_cfd_initialize_variables_13.rodinia_3_1_cfd_initialize_variables_13(), rodinia_3_1_cfd_initialize_variables_14.rodinia_3_1_cfd_initialize_variables_14(), rodinia_3_1_cfd_initialize_variables_15.rodinia_3_1_cfd_initialize_variables_15(), polybench_gpu_1_0_gesummv_gesummv_kernel_1.polybench_gpu_1_0_gesummv_gesummv_kernel_1(), polybench_gpu_1_0_gesummv_gesummv_kernel_2.polybench_gpu_1_0_gesummv_gesummv_kernel_2(), polybench_gpu_1_0_gesummv_gesummv_kernel_3.polybench_gpu_1_0_gesummv_gesummv_kernel_3(), polybench_gpu_1_0_gesummv_gesummv_kernel_4.polybench_gpu_1_0_gesummv_gesummv_kernel_4(), polybench_gpu_1_0_gesummv_gesummv_kernel_12.polybench_gpu_1_0_gesummv_gesummv_kernel_12(), polybench_gpu_1_0_gesummv_gesummv_kernel_13.polybench_gpu_1_0_gesummv_gesummv_kernel_13(), polybench_gpu_1_0_gesummv_gesummv_kernel_14.polybench_gpu_1_0_gesummv_gesummv_kernel_14(), polybench_gpu_1_0_gesummv_gesummv_kernel_15.polybench_gpu_1_0_gesummv_gesummv_kernel_15(), npb_3_3_CG_makea_7_1.npb_3_3_CG_makea_7_1(), npb_3_3_CG_makea_7_2.npb_3_3_CG_makea_7_2(), npb_3_3_CG_makea_7_3.npb_3_3_CG_makea_7_3(), npb_3_3_CG_makea_7_4.npb_3_3_CG_makea_7_4(), npb_3_3_CG_makea_7_12.npb_3_3_CG_makea_7_12(), npb_3_3_CG_makea_7_13.npb_3_3_CG_makea_7_13(), npb_3_3_CG_makea_7_14.npb_3_3_CG_makea_7_14(), npb_3_3_CG_makea_7_15.npb_3_3_CG_makea_7_15(), polybench_gpu_1_0_mvt_mvt_kernel2_1.polybench_gpu_1_0_mvt_mvt_kernel2_1(), polybench_gpu_1_0_mvt_mvt_kernel2_2.polybench_gpu_1_0_mvt_mvt_kernel2_2(), polybench_gpu_1_0_mvt_mvt_kernel2_3.polybench_gpu_1_0_mvt_mvt_kernel2_3(), polybench_gpu_1_0_mvt_mvt_kernel2_4.polybench_gpu_1_0_mvt_mvt_kernel2_4(), polybench_gpu_1_0_mvt_mvt_kernel2_12.polybench_gpu_1_0_mvt_mvt_kernel2_12(), polybench_gpu_1_0_mvt_mvt_kernel2_13.polybench_gpu_1_0_mvt_mvt_kernel2_13(), polybench_gpu_1_0_mvt_mvt_kernel2_14.polybench_gpu_1_0_mvt_mvt_kernel2_14(), polybench_gpu_1_0_mvt_mvt_kernel2_15.polybench_gpu_1_0_mvt_mvt_kernel2_15(), nvidia_4_2_DotProduct_DotProduct_1.nvidia_4_2_DotProduct_DotProduct_1(), nvidia_4_2_DotProduct_DotProduct_2.nvidia_4_2_DotProduct_DotProduct_2(), nvidia_4_2_DotProduct_DotProduct_3.nvidia_4_2_DotProduct_DotProduct_3(), nvidia_4_2_DotProduct_DotProduct_4.nvidia_4_2_DotProduct_DotProduct_4(), nvidia_4_2_DotProduct_DotProduct_12.nvidia_4_2_DotProduct_DotProduct_12(), nvidia_4_2_DotProduct_DotProduct_13.nvidia_4_2_DotProduct_DotProduct_13(), nvidia_4_2_DotProduct_DotProduct_14.nvidia_4_2_DotProduct_DotProduct_14(), nvidia_4_2_DotProduct_DotProduct_15.nvidia_4_2_DotProduct_DotProduct_15(), rodinia_3_1_streamcluster_memset_kernel_1.rodinia_3_1_streamcluster_memset_kernel_1(), rodinia_3_1_streamcluster_memset_kernel_2.rodinia_3_1_streamcluster_memset_kernel_2(), rodinia_3_1_streamcluster_memset_kernel_3.rodinia_3_1_streamcluster_memset_kernel_3(), rodinia_3_1_streamcluster_memset_kernel_4.rodinia_3_1_streamcluster_memset_kernel_4(), rodinia_3_1_streamcluster_memset_kernel_12.rodinia_3_1_streamcluster_memset_kernel_12(), rodinia_3_1_streamcluster_memset_kernel_13.rodinia_3_1_streamcluster_memset_kernel_13(), rodinia_3_1_streamcluster_memset_kernel_14.rodinia_3_1_streamcluster_memset_kernel_14(), rodinia_3_1_streamcluster_memset_kernel_15.rodinia_3_1_streamcluster_memset_kernel_15(), MatVecMul_1.MatVecMul_1(), MatVecMul_2.MatVecMul_2(), MatVecMul_3.MatVecMul_3(), MatVecMul_4.MatVecMul_4(), MatVecMul_12.MatVecMul_12(), MatVecMul_13.MatVecMul_13(), MatVecMul_14.MatVecMul_14(), MatVecMul_15.MatVecMul_15(), nvidia_4_2_VectorAdd_VectorAdd_1.nvidia_4_2_VectorAdd_VectorAdd_1(), nvidia_4_2_VectorAdd_VectorAdd_2.nvidia_4_2_VectorAdd_VectorAdd_2(), nvidia_4_2_VectorAdd_VectorAdd_3.nvidia_4_2_VectorAdd_VectorAdd_3(), nvidia_4_2_VectorAdd_VectorAdd_4.nvidia_4_2_VectorAdd_VectorAdd_4(), nvidia_4_2_VectorAdd_VectorAdd_12.nvidia_4_2_VectorAdd_VectorAdd_12(), nvidia_4_2_VectorAdd_VectorAdd_13.nvidia_4_2_VectorAdd_VectorAdd_13(), nvidia_4_2_VectorAdd_VectorAdd_14.nvidia_4_2_VectorAdd_VectorAdd_14(), nvidia_4_2_VectorAdd_VectorAdd_15.nvidia_4_2_VectorAdd_VectorAdd_15()]
		self.labels = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0] #92.96875
		for g in self.graphs:
			g.ndata['m'] = nodeFeatures(g, "multifractal")
	def __len__(self):
		return len(self.graphs)
	def __getitem__(self, idx):
		return self.graphs[idx], self.labels[idx]
