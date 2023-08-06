<pre style="line-height: 1.2;">

                               ██╗██╗
                               ╚═╝╚═╝
    ██████╗ ███████╗██╗    ██╗ █████╗ ██╗  ██╗███████╗███████╗
    ██╔══██╗██╔════╝██║    ██║██╔══██╗██║ ██╔╝██╔════╝██╔════╝
    ██║  ██║█████╗  ██║ █╗ ██║███████║█████╔╝ ███████╗███████╗
    ██║  ██║██╔══╝  ██║███╗██║██╔══██║██╔═██╗ ╚════██║╚════██║
    ██████╔╝███████╗╚███╔███╔╝██║  ██║██║  ██╗███████║███████║
    ╚═════╝ ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝

</pre>
Denoising Expression data with a Weighted Affinity Kernel and Self-Supervision
================================================================================================

## Summary
Single cell sequencing produces gene expression data which has many individual observations, but each individual cell is noisy and sparsely sampled. Existing denoising and imputation methods are of varying complexity, and it is difficult to determine if an output is optimally denoised. There are often no general criteria by which to choose model hyperparameters and users may need to supply unknown parameters such as noise distributions. Neighbor graphs are common in single cell expression analysis pipelines and are frequently used in denoising applications. Data is averaged within a connected neighborhood of the k-nearest neighbors for each observation to reduce noise. Denoising without a clear objective criteria can result in data with too much averaging and where biological information is lost. Many existing methods lack such an objective criteria and tend to overly smooth data. We have developed and evaluated an objective function that can be reliably minimized for optimally denoising single cell data on a graph, DEWÄKSS. The DEWÄKSS objective function is derived from self supervised learning principles and requires optimization over only a few parameters. DEWÄKSS performs robustly compared to more complex algorithms and state of the art graph denoising methods.

<p align="center"><img src="img/fig_repo/dewakss_procedure_v2.svg" width="80%" /></p>

Install latest version through pip
```
pip install dewakss
```
For best results DEWAKSS require the MKL from intel which should be default in any conda install. 
If DEWAKSS complains please check how to get MKL from [intel](https://software.intel.com/content/www/us/en/develop/tools/math-kernel-library.html) or [anaconda](https://docs.anaconda.com/mkl-optimizations/).

Install the bleeding edge version by cloning this repository
```
git clone https://gitlab.com/Xparx/dewakss.git
cd dewakss
```
and then in the dewakss directory:
```
pip install .
```

or alternatively
```
pip install -e .
```
if one wish to keep track of new updates in the git repository.

## MKL support
For faster execution times DEWAKSS currently relies on the math kernel library ([MKL](https://software.intel.com/en-us/mkl/choose-download)) from intel through the package [sparse-dot-mkl](https://pypi.org/project/sparse-dot-mkl/). The most reliable ways to get support from MKL is to get the latest version  of `python anaconda`, else the latest version of MKL needs to be installed and the location to the shared object files needs to be added to `LD_LIBRARY_PATH`.


## Usage

The simplest way to use DEWAKSS is to simply run the following

    import dewakss.denoise as dewakss
    
    denoiseer = dewakss.DEWAKSS(adata)
    denoiseer.fit(adata)
    denoiseer.transform(adata, copy=False)

where `adata` is either an expression matrix or an [AnnData](https://scanpy.readthedocs.io/en/stable/) object with genes as columns and cells/samples as rows.

To explore the results one can use

    denoiseer.plot_global_performance()


A more refined optimization can be computed as e.g.
```
neighbors = np.flip([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100])
npcss = [50, 100, 150, 200]
denoiseer = dewakss.DEWAKSS(adata, n_pcs=npcss , n_neighbors=neighbors, use_global_err=False, modest='max', n_batches=1)
denoiseer.fit(adata)
denoiseer.transform(adata, copy=False)
```
In this case we use the local optima for each cell to estimate the number of neighbours out of the one we iterate over. 
A modest adjustment is done when we denoise in the transform step (below). The neighbors and PCs to compute is chosen explicitly to cover a more fine grained distribution of hyper parameters (recommended).

To evaluate the local error run:

    denoiseer.plot_local_performance()

Local denosing unlocks some extra features such as a graph output stored in the returned object as well a clustering estimate using the Leiden algorithm using that graph.

The data can be split into batches along the column (gene) dimension.
Splitting the computation into batches may increase compute time but can spare memory usage.

## Citation
```
@article{Tjarnberg2021,
    author = {Tj{\"a}rnberg, Andreas AND Mahmood, Omar AND Jackson, Christopher A. AND Saldi, Giuseppe-Antonio AND Cho, Kyunghyun AND Christiaen, Lionel A. AND Bonneau, Richard A.},
    journal = {PLOS Computational Biology},
    publisher = {Public Library of Science},
    title = {Optimal tuning of weighted kNN- and diffusion-based methods for denoising single cell genomics data},
    year = {2021},
    month = {01},
    volume = {17},
    url = {https://doi.org/10.1371/journal.pcbi.1008569},
    pages = {1-22},
    number = {1},
    doi = {10.1371/journal.pcbi.1008569}
}
```

## Manuscript results
To reproduce the results from [Tjarnberg2020](https://doi.org/10.1371/journal.pcbi.1008569) run the command
```
pip install DEWAKSS==0.99rc2020
```
The appropriate notebooks to follow can be found in the tag
[Tjarnberg2020](https://gitlab.com/Xparx/dewakss/-/tree/Tjarnberg2020)
