# Use the official Ensembl VEP Docker image as the base
FROM ensemblorg/ensembl-vep:latest

# Switch to root user for package installation
USER root

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    samtools \
    curl \
    unzip \
    make \
    gcc \
    libpng-dev \
    libssl-dev \
    libmysqlclient-dev \
    libsqlite3-dev \
    cpanminus \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install UCSC Kent utilities (BigWig tools) using curl
WORKDIR /usr/local/bin
RUN curl -O -L http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/wigToBigWig && \
    curl -O -L http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/bigWigToBedGraph && \
    curl -O -L http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/bigWigSummary && \
    chmod +x wigToBigWig bigWigToBedGraph bigWigSummary

# Download and unpack Kent source v335 (needed for Bio::DB::BigFile)
WORKDIR /opt
RUN curl -O -L https://github.com/ucscGenomeBrowser/kent/archive/v335_base.tar.gz && \
    tar xzf v335_base.tar.gz && \
    rm v335_base.tar.gz

# Set up environment variables manually
ENV KENT_SRC=/opt/kent-335_base/src \
    MACHTYPE=x86_64 \
    CFLAGS="-fPIC"

# Set up MySQL-related variables in a separate RUN command
RUN export MYSQLINC=$(mysql_config --include | sed -e 's/^-I//g') && \
    export MYSQLLIBS=$(mysql_config --libs) && \
    echo "export MYSQLINC=$MYSQLINC" >> /etc/environment && \
    echo "export MYSQLLIBS=$MYSQLLIBS" >> /etc/environment

# Modify Kent build parameters and compile
WORKDIR $KENT_SRC/lib
RUN echo 'CFLAGS="-fPIC"' > ../inc/localEnvironment.mk && \
    make clean && make

WORKDIR $KENT_SRC/jkOwnLib
RUN make clean && make

# Ensure compiled files are in the correct location
RUN ln -s $KENT_SRC/lib/x86_64/* $KENT_SRC/lib/

# Install Perl modules (Bio::DB::BigFile and DBD::SQLite)
WORKDIR /opt
RUN mkdir -p $HOME/cpanm && \
    export PERL5LIB=$PERL5LIB:$HOME/cpanm/lib/perl5 && \
    cpanm -l $HOME/cpanm Bio::DB::BigFile && \
    cpanm -l $HOME/cpanm DBD::SQLite

# Ensure the ensembl user exists (if needed)
RUN if ! id "ensembl" &>/dev/null; then useradd -m -s /bin/bash ensembl; fi

# Switch back to the default user if it exists
USER ensembl

# Set working directory
WORKDIR /data

# Default command
CMD ["/bin/bash"]

USER root
