FROM continuumio/miniconda3

RUN conda create -n vowel_plotter -c conda-forge montreal-forced-aligner pandas matplotlib
RUN touch ~/.bashrc
RUN echo "source activate vowel_plotter" > ~/.bashrc
ENV PATH /opt/conda/envs/vowel_plotter/bin:$PATH

SHELL ["/bin/bash", "--login", "-c"]
# SHELL ["conda", "run", "-n", "vowel_plotter", "/bin/bash", "-c"]
# RUN pip install praat-parselmouth

COPY entrypoint.sh ./
RUN ./entrypoint.sh