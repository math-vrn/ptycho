/*interface*/
%module ptychofft

%{
#define SWIG_FILE_WITH_INIT
#include "ptychofft.cuh"
%}

%include "numpy.i"

%init %{
import_array();
%}
class ptychofft
{	
public:
	%immutable;
	size_t n;
	size_t ntheta;
	size_t nz;
	size_t nscan;
	size_t detx;
	size_t dety;
	size_t nprb;
	size_t ngpus;

	%mutable;
	ptychofft(size_t ntheta, size_t nz, size_t n, 
		size_t nscan, size_t detx, size_t dety, size_t nprb, size_t ngpus);
	~ptychofft();	
	void fwd(size_t g, size_t f, size_t prb, size_t scan, size_t igpu);
	void adj(size_t f, size_t g, size_t prb, size_t scan, size_t igpu);	
	void adjprb(size_t prb, size_t g, size_t scan, size_t f, size_t igpu);
};


