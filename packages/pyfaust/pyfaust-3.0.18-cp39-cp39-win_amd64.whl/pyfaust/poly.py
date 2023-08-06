# experimental block start
# ##########################################################################################
# Copyright (c) 2021, INRIA                                                              #
# All rights reserved.                                                                   #
#                                                                                        #
# BSD License 2.0                                                                        #
#                                                                                        #
# Redistribution and use in source and binary forms, with or without                     #
# modification, are permitted provided that the following conditions are met:            #
# * Redistributions of source code must retain the above copyright notice,               #
# this list of conditions and the following disclaimer.                                  #
# * Redistributions in binary form must reproduce the above copyright notice,            #
# this list of conditions and the following disclaimer in the documentation              #
# and/or other materials provided with the distribution.                                 #
# * Neither the name of the <copyright holder> nor the names of its contributors         #
# may be used to endorse or promote products derived from this software without          #
# specific prior written permission.                                                     #
#                                                                                        #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND        #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED          #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.     #
# IN NO EVENT SHALL INRIA BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,       #
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF     #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) #
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,  #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS  #
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                           #
#                                                                                        #
# Contacts:                                                                              #
# 	Remi Gribonval  : remi.gribonval@inria.fr                                        #
# 	Hakim Hadj-dji. : hakim.hadj-djilani@inria.fr                                    #
#                                                                                        #
# Authors:                                                                               #
# 	Software Engineers:                                                              #
# 		Nicolas Bellot                                                           #
# 		Thomas Gautrais,                                                         #
# 		Hakim Hadj-Djilani,                                                      #
# 		Adrien Leman,                                                            #
#                                                                                        #
# 	Researchers:                                                                     #
# 		Luc Le Magoarou,                                                         #
# 		Remi Gribonval                                                           #
#                                                                                        #
# 	INRIA Rennes, FRANCE                                                             #
# 	http://www.inria.fr/                                                             #
##########################################################################################


## @package pyfaust.poly @brief The pyfaust module for polynomial basis as Faust objects.

import _FaustCorePy
import scipy.sparse as sp
import numpy as np
import _FaustCorePy
from scipy.sparse import csr_matrix
from pyfaust import (Faust, isFaust, eye as feye, vstack as fvstack, hstack as
                     fhstack)
from scipy.sparse.linalg import eigsh
import threading


def Chebyshev(L, K, dev='cpu', T0=None, impl='native'):
    """
    Builds the Faust of the Chebyshev polynomial basis defined on the sparse matrix L.

    Args:
        L: the sparse scipy square matrix in CSR format (scipy.sparse.csr_matrix).
           L can aslo be a Faust if impl is "py".
        K: the degree of the last polynomial, i.e. the K+1 first polynomials are built.
        dev (optional): the device to instantiate the returned Faust ('cpu' or 'gpu').
        'gpu' is not available yet for impl='native'.
        T0 (optional): to define the 0-degree polynomial as something else than the identity.
        impl (optional): 'native' (by default) for the C++ impl., "py" for the Python impl.

    Returns:
        The Faust of the K+1 Chebyshev polynomials.

    See pyfaust.poly.basis which is pretty the same (e.g.: calling
    Chebyshev(L, K) is equivalent to basis(L, K, 'chebyshev')
    """
    if not isinstance(L, csr_matrix) and not isFaust(L):
        L = csr_matrix(L)
    if L.shape[0] != L.shape[1]:
        raise ValueError('L must be a square matrix.')
    if impl == "py":
        twoL = 2*L
        d = L.shape[0]
        # Id = sp.eye(d, format="csr")
        Id = _eyes_like(L, d)
        if isinstance(T0, type(None)):
            T0 = Id
        T1 = _vstack((Id, L))
        rR = _hstack((-1*Id, twoL))
        if isFaust(L):
            if isFaust(T0):
                T0 = T0.factors(0)
            G = FaustPoly(T0, T1=T1, rR=rR, L=L, dev=dev, impl='py')
            for i in range(0, K):
                next(G)
            return next(G)
        else:
            return _chebyshev(L, K, T0, T1, rR, dev)
    elif impl == 'native':
        F = FaustPoly(core_obj=_FaustCorePy.FaustCore.polyBasis(L, K, T0),
                      impl='native')
        return F
    else:
        raise ValueError(impl+" is an unknown implementation.")



def basis(L, K, basis_name, dev='cpu', T0=None, impl='native'):
    """
    Builds the Faust of the polynomial basis defined on the sparse matrix L.

    Args:
        L: the sparse scipy square matrix in CSR format (scipy.sparse.csr_matrix).
           L can aslo be a Faust if impl is "py".
        K: the degree of the last polynomial, i.e. the K+1 first polynomials are built.
        basis_name: 'chebyshev', and others yet to come.
        dev (optional): the device to instantiate the returned Faust ('cpu' or 'gpu').
        'gpu' is not available yet for impl='native'.
        T0 (optional): a sparse matrix to replace the identity as a 0-degree polynomial of the basis.
        impl (optional): 'native' (by default) for the C++ impl., "py" for the Python impl.

    Returns:
        The Faust G of the basis composed of the K+1 orthogonal polynomials.
        Note that the Faust returned is also a generator: calling next(G) will return the basis of dimension K+1.

    Example:
        >>> from pyfaust.poly import basis
        >>> from scipy.sparse import random
        >>> L = random(50, 50, .02, format='csr')
        >>> L = L@L.T
        >>> K = 3
        >>> F = basis(L, K, 'chebyshev')
        >>> F
        Faust size 200x50, density 0.0687, nnz_sum 687, 4 factor(s): 
            - FACTOR 0 (real) SPARSE, size 200x150, density 0.0093, nnz 279
            - FACTOR 1 (real) SPARSE, size 150x100, density 0.0152667, nnz 229
            - FACTOR 2 (real) SPARSE, size 100x50, density 0.0258, nnz 129
            - FACTOR 3 (real) SPARSE, size 50x50, density 0.02, nnz 50

        Generate the next basis (the one with one additional dimension,
        whose the polynomial greatest degree is K+1 = 4)

        >>> G = next(F)
        >>> G
        Faust size 250x50, density 0.08128, nnz_sum 1016, 5 factor(s): 
            - FACTOR 0 (real) SPARSE, size 250x200, density 0.00658, nnz 329
            - FACTOR 1 (real) SPARSE, size 200x150, density 0.0093, nnz 279
            - FACTOR 2 (real) SPARSE, size 150x100, density 0.0152667, nnz 229
            - FACTOR 3 (real) SPARSE, size 100x50, density 0.0258, nnz 129
            - FACTOR 4 (real) SPARSE, size 50x50, density 0.02, nnz 50

        The factors 0 to 3 of G are views of the same factors of F.
        They are not duplicated in memory (iff impl==native).

        By default, the 0-degree polynomial is the identity.
        However it is possible to replace the corresponding matrix by
        any csr sparse matrix T0 of your choice (with the only constraint that
        T0.shape[0] == L.shape[0]. In that purpose, do as follows:

        >>> F2 = basis(L, K, 'chebyshev', T0=random(50,2, .3, format='csr'))
        >>> F2
        Faust size 200x2, density 1.7125, nnz_sum 685, 4 factor(s): 
            - FACTOR 0 (real) SPARSE, size 200x150, density 0.0095, nnz 285
            - FACTOR 1 (real) SPARSE, size 150x100, density 0.0156667, nnz 235
            - FACTOR 2 (real) SPARSE, size 100x50, density 0.027, nnz 135
            - FACTOR 3 (real) SPARSE, size 50x2, density 0.3, nnz 30



    """
    if basis_name.lower() == 'chebyshev':
        return Chebyshev(L, K, dev=dev, T0=T0, impl=impl)
    else:
        raise ValueError(basis_name+" is not a valid basis name")


def poly(coeffs, basis='chebyshev', L=None, dev='cpu', impl='native'):
    """
        Computes the linear combination of the polynomials defined by basis.

        Args:
            coeffs: the linear combination coefficients (vector as a numpy.ndarray).
            basis: either the name of the polynomial basis to build on L or the
            basis if already built externally (as a FaustPoly or an equivalent
            np.ndarray).
            L: the sparse scipy square matrix in CSR format
            (scipy.sparse.csr_matrix) on which the polynomial basis is built if basis is not already a Faust or a numpy.ndarray.
            L can aslo be a Faust if impl is "py". It can't be None if basis is not a FaustPoly or a numpy.ndarray.
            dev: the device to instantiate the returned Faust ('cpu' or 'gpu').
            'gpu' is not available yet for impl='native'.
            impl: 'native' (by default) for the C++ impl., "py" for the Python impl.

        Returns:
            The linear combination Faust or np.ndarray depending on if basis is itself a Faust or a np.ndarray.

        Example:
            >>> import numpy as np
            >>> from pyfaust.poly import basis, poly
            >>> from scipy.sparse import random
            >>> L = random(50, 50, .02, format='csr')
            >>> L = L@L.T
            >>> coeffs = np.array([.5, 1, 2, 3])
            >>> G = poly(coeffs, 'chebyshev', L)
            >>> G
            Faust size 50x50, density 0.3608, nnz_sum 902, 5 factor(s):
            - FACTOR 0 (real) SPARSE, size 50x200, density 0.02, nnz 200
            - FACTOR 1 (real) SPARSE, size 200x150, density 0.00946667, nnz 284
            - FACTOR 2 (real) SPARSE, size 150x100, density 0.0156, nnz 234
            - FACTOR 3 (real) SPARSE, size 100x50, density 0.0268, nnz 134
            - FACTOR 4 (real) SPARSE, size 50x50, density 0.02, nnz 50

            Which is equivalent to do as below (in two times):

            >>> K = 3
            >>> F = basis(L, K, 'chebyshev')
            >>> coeffs = np.array([.5, 1, 2, 3])
            >>> G = poly(coeffs, F)
            >>> G
            Faust size 50x50, density 0.3608, nnz_sum 902, 5 factor(s):
            - FACTOR 0 (real) SPARSE, size 50x200, density 0.02, nnz 200
            - FACTOR 1 (real) SPARSE, size 200x150, density 0.00946667, nnz 284
            - FACTOR 2 (real) SPARSE, size 150x100, density 0.0156, nnz 234
            - FACTOR 3 (real) SPARSE, size 100x50, density 0.0268, nnz 134
            - FACTOR 4 (real) SPARSE, size 50x50, density 0.02, nnz 50

            Above G is a Faust because F is too.
            Below the full array of the Faust F is passed, so an array is returned into GA.
            >>> GA = poly(coeffs, F.toarray())
            >>> type(GA)
            numpy.ndarray

            But of course they are equal:

            >>> np.allclose(GA, G.toarray())
            True

    """
    K = coeffs.size-1
    if isinstance(basis, str):
        if L is None:
            raise ValueError('The L matrix must be set to build the'
                             ' polynomials.')
        from pyfaust.poly import basis as _basis
        basis = F = _basis(L, K, basis, dev=dev, impl=impl)

    if isFaust(basis):
        F = basis
    elif not isinstance(basis, np.ndarray):
        raise TypeError('basis is neither a str neither a Faust nor'
                        ' a numpy.ndarray')
    else:
        F = basis
    if L == None:
        d = F.shape[0]//(K+1)
    else:
        d = L.shape[0]
    if impl == 'py':
        if isFaust(F):
            Id = sp.eye(d, format="csr")
            scoeffs = sp.hstack(tuple(Id*coeffs[i] for i in range(0, K+1)),
                                format="csr")
            Fc = Faust(scoeffs, dev=dev) @ F
            return Fc
        else:
           # F is a np.ndarray
           return _poly_arr_py(coeffs, F, d, dev=dev)
    elif impl == 'native':
        if isFaust(F):
            Fc = _poly_Faust_cpp(coeffs, F)
            if F.device != dev:
                Fc = Fc.clone(dev=dev)
            return Fc
        else:
            return _poly_arr_cpp(coeffs, F, d, dev='cpu')
    else:
        raise ValueError(impl+" is an unknown implementation.")


def _poly_arr_py(coeffs, basisX, d, dev='cpu'):
    """
    """
    mt = True # multithreading
    n = basisX.shape[1]
    K_plus_1 = int(basisX.shape[0]/d)
    Y = np.empty((d, n))
    if n == 1:
        Y[:, 0] = basisX[:, 0].reshape(d, K_plus_1, order='F') @ coeffs
    elif mt:
        nthreads = 4
        threads = []
        def apply_coeffs(i, n):
            for i in range(i,n,nthreads):
                Y[:, i] = basisX[:, i].reshape(d, K_plus_1, order='F') @ coeffs
        for i in range(0,nthreads):
            t = threading.Thread(target=apply_coeffs, args=([i,n]))
            threads.append(t)
            t.start()
        for i in range(0,nthreads):
           threads[i].join()
    else:
         for i in range(n):
                Y[:, i] = basisX[:, i].reshape(d, K_plus_1, order='F') @ coeffs
# other way:
#    Y = coeffs[0] * basisX[0:d,:]
#    for i in range(1,K_plus_1):
#        Y += (basisX[d*i:(i+1)*d, :] * coeffs[i])
    return Y

def _poly_arr_cpp(coeffs, basisX, d, dev='cpu'):
    Y = _FaustCorePy.polyCoeffs(d, basisX, coeffs)
    return Y

def _poly_Faust_cpp(coeffs, basisFaust, dev='cpu'):
    Y = Faust(core_obj=basisFaust.m_faust.polyCoeffs(coeffs))
    return Y


def _chebyshev(L, K, T0, T1, rR, dev='cpu'):
    d = L.shape[0]
    factors = [T0]
    if(K > 0):
        factors.insert(0, T1)
        for i in range(2, K + 1):
            Ti = _chebyshev_Ti_matrix(rR, L, i)
            factors.insert(0, Ti)
    kwargs = {'T1': T1, 'rR': rR, 'L': L, 'impl':'py'}
    T = FaustPoly(factors, dev=dev, **kwargs)
    return T  # K-th poly is T[K*L.shape[0]:,:]


def _chebyshev_Ti_matrix(rR, L, i):
    d = L.shape[0]
    if i <= 2:
        R = rR
    else:
        #zero = csr_matrix((d, (i-2)*d), dtype=float)
        zero = _zeros_like(L, shape=(d, (i-2)*d))
        R = _hstack((zero, rR))
    di = d*i
    Ti = _vstack((_eyes_like(L, shape=di), R))
    return Ti


def _zeros_like(M, shape=None):
    """
    Returns a zero of the same type of M: csr_matrix, pyfaust.Faust.
    """
    if isinstance(shape, type(None)):
        shape = M.shape
    if isFaust(M):
        zero = csr_matrix(([0], ([0], [0])), shape=shape)
        return Faust(zero)
    elif isinstance(M, csr_matrix):
        zero = csr_matrix(shape, dtype=M.dtype)
        return zero
    else:
        raise TypeError('M must be a Faust or a scipy.sparse.csr_matrix.')


def _eyes_like(M, shape=None):
    """
    Returns an identity of the same type of M: csr_matrix, pyfaust.Faust.
    """
    if isinstance(shape, type(None)):
        shape = M.shape[1]
    if isFaust(M):
        return feye(shape)
    elif isinstance(M, csr_matrix):
        return sp.eye(shape, format='csr')
    else:
        raise TypeError('M must be a Faust or a scipy.sparse.csr_matrix.')


def _vstack(arrays):
    _arrays = _build_consistent_tuple(arrays)
    if isFaust(arrays[0]):
        # all arrays are of type Faust
        return fvstack(arrays)
    else:
        # all arrays are of type csr_matrix
        return sp.vstack(arrays, format='csr')


def _hstack(arrays):
    _arrays = _build_consistent_tuple(arrays)
    if isFaust(arrays[0]):
        # all arrays are of type Faust
        return fhstack(arrays)
    else:
        # all arrays are of type csr_matrix
        return sp.hstack(arrays, format='csr')


def _build_consistent_tuple(arrays):
    contains_a_Faust = False
    for a in arrays:
        if isFaust(a):
            contains_a_Faust = True
            break
    if contains_a_Faust:
        _arrays = []
        for a in arrays:
            if not isFaust(a):
                a = Faust(a)
            _arrays.append(a)
        return tuple(_arrays)
    else:
        return arrays

class FaustPoly(Faust):
    """
    Subclass of Faust specialized for orthogonal polynomial basis.

    This class is used only for the native implementation of the poly functions.

    NOTE: it is not advisable to use this class directly.

    """
    def __init__(self, *args, **kwargs):
        super(FaustPoly, self).__init__(*args, **kwargs)
        if 'impl' in kwargs:
            if kwargs['impl'] == 'native':
                self.gen = self._native_gen()
            elif kwargs['impl'] == 'py':
                L = kwargs['L']
                T1 = kwargs['T1']
                rR = kwargs['rR']
                if 'dev' in kwargs:
                    dev = kwargs['dev']
                else:
                    dev = 'cpu'
                self.gen = self._py_gen(L, T1, rR, dev)
        else:
            raise ValueError('FaustPoly ctor must have receive impl'
                             ' argument')

    def _native_gen(self):
        F = self
        while True:
            F_next = FaustPoly(core_obj=F.m_faust.polyNext(), impl='native')
            F = F_next
            yield F

    def _py_gen(self, L, T1, rR, dev='cpu'):
        kwargs = {'T1': T1, 'rR': rR, 'L': L, 'impl':'py'}
        T = self
        if isFaust(L):
            i = T.shape[0] // L.shape[0]
        else:
            i = T.numfactors()
        # i is at least 1
#        if i == 0:
#            if isFaust(T0):
#                T = T0
#            else:
#                T = Faust(T0)
#            yield T
#            i += 1 # i == 1
        # TODO: optimize to avoid factor copies
        # TODO: override __matmul__ (only if impl is py!)
        # by calling parent __matmul__, using the FaustCore object to create
        # a new FaustPoly with a proper generator
        if i == 1:
            if isFaust(T1):
                T = FaustPoly([T1.factors(i) for i in range(T1.numfactors())] + [T.factors(i) for i in
                                                                                 range(T.numfactors())], **kwargs)
            else:
                T = FaustPoly([T1] + [T.factors(i) for i in
                                      range(T.numfactors())], **kwargs)
            yield T
            i += 1 # i == 2
        while True:
            Ti = _chebyshev_Ti_matrix(rR, L, i)
            if isFaust(Ti):
                T = FaustPoly([Ti.factors(i) for i in range(Ti.numfactors())] + [T.factors(i) for i in
                                      range(T.numfactors())], **kwargs)
            else:
                T = FaustPoly([Ti] + [T.factors(i) for i in
                                      range(T.numfactors())], **kwargs)
            yield T
            i += 1

    def __next__(self):
        return next(self.gen)

# experimental block end
