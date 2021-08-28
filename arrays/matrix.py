import random
from fractions import Fraction
from math import *
from operator import add,sub, mul
from copy import copy,deepcopy
from tools.exprs import Expr,Es,Eqn, Eqns
from errors.exceptions import *
from errors.wreck import Fizzle
from fundamentals.primary import Num
from misc.gen import whole, com_arrays, com_arr_str, imap
from misc.assist import getter
from misc.tables import D2_ord
from misc.abilities import intable
from misc.vars import alpha
from misc.miscs import simp_var, num, lexpr, fnum
from oblects.abc import MatrixObjectClass, Utilities, StaticStates
try:
    from numpy import array,ndarray
except ImportError:
    class ndarray:
        pass
    
from oblects.states import *


class Matrix(MatrixObjectClass, Utilities.matrix, StaticStates):
    '''
        Calling this class create a Matrix Object.
        The class will initialize a Matrix for you byis just calling Matrix()
        if you want to convert arrays to Matrix Object you use the X parameter
            You convert a list to Matrix Object; this will work fine if the
                first 2 elements gives the order of the matrix

                e.g To convert [1,2,3,4,5,6,7,8], this can be a 1x8, 2x4, 4x2 or 8x1
                    so you indicate the order by adding the order to the begining
                    if the order is 2 x 4
                    Mat_A = Matrix(X = [2,4,1,2,3,4,5,6,7,8]
                    
            You can convert 2D array (in form of list)
                e.g Mat_A = Matrix([[1,2],[3,4],[5,6],[7,8]])

            Also, You convert consistent list or tuple to Matrix Object
                e.g Mat_A = Matrix([1,2],[3,4],[5,6],[7,8])
            

            You can convert numpy arrays as well
                e.g if Y is an numpy.ndarray object, then Mat_A = Matrix(X = Y)

    '''
       
    def __init__(self, X = [], *Y):
        self.name = "Matrix"
        self.state = 'enabled'
        if Y:
            
            cols = len(X)
            x = [1 + len(Y),cols] + X
            for Xs in Y:
                if len(Xs) != cols:
                    raise InconsistencyError(f'These data are not consistent in columns: {str(X) +", " + star(Y)}')
                x += Xs
            try:
                self.Mat = [fnum(items) if c > 1 else items for c, items in enumerate(x)]
            except Fizzle:
                raise UnacceptableToken(f'Unaccepetable entry: {items}, Note that Matrix class only accepts Numbers, you can use Matrix_ instead')
        if isinstance(X,set):
            try:
                self.Mat = [fnum(items) if c > 1 else items for c, items in enumerate(X)]
            except Fizzle:
                raise UnacceptableToken(f'Unaccepetable entry: {items}, Note that Matrix class only accepts Numbers, you can use Matrix_ instead')
            return 
        if isinstance(X,ndarray) or isinstance(X, (list, tuple)):
            _mat = X
            if isinstance(X,ndarray):
                _mat = list(X.shape)
                for rows in X:
                    Mat_ += list(rows)
                _mat = Mat_
            elif X and isinstance(X[0],(list, tuple)):
                _mat = [len(X),len(X[0])]
                for rows in X:
                    if len(rows) != _mat[1]:
                        raise DimensionError('Dimension Inconsistent')
                    _mat += rows
            try:
                self.Mat = [fnum(items) if c > 1 else items for c, items in enumerate(_mat)]
            except Fizzle:
                raise UnacceptableToken(f'Unaccepetable entry: {items}, Note that Matrix class only accepts Numbers, you can use Matrix_ instead')
        elif isinstance(X,Matrix_):
            self.Mat = X.Mat
            return 
        else:
            Mat = []
            try:
                order = input("Matrix Order: ")
                col = int(order.split('x')[1]); row = int(order.split('x')[0])
                Mat.append(row); Mat.append(col); count = 1
                while count <= row:
                    disp = "Enter the"
                    if count == 1:
                        pos = 'First'
                    elif count ==2:
                        pos = 'Second'
                    elif count == row:
                        pos = 'Last'; disp = 'Good, Now the'
                    else: pos = 'Next'; disp = ''
                    element = input(f"{disp} {pos} row: ").split(',')
                    while True:
                        if len(element) == col:
                            for elements in element:
                                try:
                                    Mat.append(fnum(elements))
                                except Fizzle:
                                    raise UnacceptableToken(f'Unaccepetable entry: {elements}, Note that Matrix class only accepts Numbers, you can use Matrix_ instead')
                            break
                        num = "element" if len(element) == 1 else 'elements'
                        print(f"Error, You Entered {len(element)} {num} instead of {col}")
                        element = input("Try Again: ").split(',')
                    count += 1
                            
            except Exception:
                raise ImprobableError('Unknown Error Occurred')
            self.Mat = Mat

        
    def __str__(self,pr_sr = True):
        lines = []
        for integers in range(self.rows):
            line = []
            # Checking if elements are whole number and convert to fractions if not
            for integer in range(self.cols):
                if intable(self[integers + 1,integer + 1]):
                    line.append(int(self[integers + 1,integer + 1]))
                else: 
                    frac = Fraction(self[integers + 1,integer + 1]).limit_denominator()
                    line += [frac.numerator] if frac.denominator == 1 else [f'{frac.numerator}/{frac.denominator}']
            lines.append(line)
        if pr_sr:
            return str(D2_ord(lines))
        else:
            return ''

    __repr__ = __str__
        
    def null(self,order):
        ''' Returns Null Matrix'''
        mat = self.empty
        if isinstance(order, int):
            mat.Mat = [order,order]
            order = order*order
            
        else:
            mat.Mat = [order[0],order[1]]
            order = order[0] * order[1]
            
        mat.Mat += [0 for i in range(order)]
        return mat
    
    def unit(self,order):
        ''' Returns Unit Matrix'''
        if isinstance(order,int):
            order = [order,order]
        Mat = list(order); mat = self.empty
        if Mat[0] != Mat[1]:
            raise DimensionError('Unit Matrix are meant to be Square')
        for integer in range(order[0]):
            for integers in range(order[1]):
                Mat.append(1 if integer == integers else 0)
        mat.Mat = Mat
        return mat
    

    @property
    def cross(self):
        return Matrix_(self.Mat)
        
    
    def __setitem__(self,key,value):
        ''' Set elements in a MatObj
            MatObj[i] = value
                if i is an integer:
                    if i < 0, then backward counting; -1 will select the last row, -2 will select the second to the last row and so on
                    if value i is not a list or tuple, the ith entry of the MatObj will be set to value
                    else if value is a list or tuple:
                        if i is within the number of rows, row i will set to the list or tuple elements
                        else if i is 1 + the number of rows, a new row will be added and its elements will
                        be set to that of the list or tuple
                else if i is a string:
                    it works just as described above but on the columns not rows
            MatObj[i,j] = value
                The element at row i, col j is set to value
                Negative entries are also supported            
        '''

        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if self.isimut:
            raise InvalidOperation('This Matrix is Immutable')
        # row for integer, col for string, i,j for list 
        if isinstance(key,int):
            if key < 0:
                key = self.rows + 1 + key
            if not isinstance(value,(list, tuple)):
                self.Mat[key+1] = fnum(value)
            elif isinstance(value,(list, tuple)):
                if key == self.rows+1:
                    self.add_row(value)
                elif key > 0 and key <= self.rows:
                    self.add_row(value)
                    self.perform('~',rows=[-1, key])
                    del self[-1]
                else:
                    raise UnacceptableToken(f'Invalid Entry: {key}')
        elif isinstance(key,str):
            self.__setitem__(['*',int(key)],value)
        elif len(key) == 2:
            key = list(key)
            if key[0] == '*':
                if key[1] < 0:
                    key = ['*',self.cols + 1 + key[1]]
                if key[1] == self.cols+1:
                    self.add_col(value)
                elif key[1] > 0 and key[1] <= self.cols:
                    self.add_col(value)
                    self.perform('~',cols=[-1, key[1]])
                    del self['-1']
                else:
                    raise UnacceptableToken(f'Invalid Entry: {str(key)}')
                
            elif key[0] > self.rows or key[1] > self.cols:
                raise OutOfRange(f"Entry {key} doesn't exist. This Matrix only has {self.rows} rows and {self.cols} columns")
            else:
                if isinstance(value, (tuple,list)):
                    raise UnacceptableToken(f'Invalid value {value} for entry {key}')
                if key[1] < 0:
                    key[1] += self.cols + 1
                if key[0] < 0:
                    key[0] += self.rows + 1

                self.Mat[(key[0]-1)*self.cols+ key[1]+1] = fnum(value)
    
    def __abs__(self):
        '''abs(A) -> |A|
           returns the determinat of th MatObj
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if self.rows != self.cols: # For Square Matrix certainty
            raise InvalidOperation('Determinats are only supported by Square Matrices')
        mat_init = tuple(self.Mat)
        res = 0
        if self.order == [2,2]:
            return self[1]*self[4] - self[3]*self[2]
        mult = self.pop()
        _mat = tuple(self.Mat)
        for integers in range(self.cols):
            self.Mat = list(_mat)
            del self[f'{integers+1}']
            res += (-1)**integers * mult[integers] * abs(self)
        self.Mat = list(mat_init)
        return res

    def add_row(self, *row):
        '''
            Add rows to the MatObj
            MatObj.add_row([...],[....],[....])
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if self.isimut:
            raise InvalidOperation('This Matrix is Immutable')
        row_ = []; empty = True if len(self.Mat) == 2 else False; l = 0
        for rows in row:
            if empty or len(rows) == self.cols:
                row_ += [fnum(rows_) for rows_ in rows]
            else:
                raise DimensionError(f'{rows} is not consistent with this Matrix which has {self.cols} columns')
            if l and l != len(rows):
                raise DimensionError(f'these entries are not consistent {star(row)}')
            l = len(rows)
        else:
            self.Mat += row_
            self.Mat[0] += len(row)
            if empty:
                self.Mat[1] += l

    def LU(self):
        '''returns the Matrix in lower and upper triangular Matrix'''
        H = self.matrix_.LU()
        return H[0].matrix, H[1].matrix

    def trace(self):
        '''returns the trace of the MatObj'''
        return sum(self.get_diag())    
        
    def perform(self, operation = '',rows = [],A = 1,B = 1, cols = []):
        # Row Operations
        if self.isimut:
            raise InvalidOperation('This Matrix is Immutable')
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        # To translate to Column Operations
        if not rows:
            col_mat = Matrix(self.trn().Mat)
            col_mat.perform(operation = operation,rows = cols,A = A,B = B, cols = [])
            self.Mat = col_mat.trn().Mat
            return None
        # Row multiplication with scalar rows[0],Interchanging Rows, Addition, Subtraction
        if not operation:
            row = self.get_row(rows[1])
            for integer in range(self.cols):
                self[rows[1],integer+1] = row[integer]*rows[0]
        elif operation == '~':
            row1 = self.get_row(rows[0])
            row2 = self.get_row(rows[1])
            for integer in range(self.cols):
                self[rows[0],integer+1] = row2[integer]
                self[rows[1],integer+1] = row1[integer]
        elif operation == '+':
            row1 = self.get_row(rows[0])
            row2 = self.get_row(rows[1])
            for integer in range(self.cols):
                self[rows[0],integer+1] = A*row1[integer] + B*row2[integer]
        elif operation == '-':
            row1 = self.get_row(rows[0])
            row2 = self.get_row(rows[1])
            for integer in range(self.cols):
                self[rows[0],integer+1] = A*row1[integer] - B*row2[integer]
                
    def modal(self):
        '''returns the modal matrix of the MatObj'''
        return self.matrix_.modal().matrix
    
    @property
    def type(self):
        '''returns the type of the Matrix'''
        attr = []
        if self.issq:
            attr.append('Square')
        if self.issing:
            attr.append('Singular')
        if not self:
            attr.append('Null')
        if self.isunit:
            attr.append('Unit')
        if self.isdiag:
            attr.append('Diagonal')
        if self.isscalar:
            attr.append('Scalar')
        if self.issym:
            attr.append('Symmetric')
        if self.isskw_sym:
            attr.append('Skew Symmetric')
        if self.isupper_delta:
            attr.append('Upper Triangular')
        elif self.islower_delta:
            attr.append('Lower Triangular')
        if self.isorth:
            attr.append('Orthogonal')
        if self.isidemp:
            attr.append('Idempotent')
        if self.isperiodic:
            attr.append('Periodic')
        if self.isnilp:
            attr.append('Nilpotent')
        if self.isinv:
            attr.append('Involuntary')
        
        return ', '.join(attr) + ' Matrix'

    
    def quad(self,vec = ''):
        if not vec:
            vec = [1,self.cols]
            for i in range(self.cols):
                vec.append(alpha[i])
        return (Matrix_(vec) * self * Matrix_(vec).trn())[1,1]
    
    def export(self):
        return array([rows for rows in self])

    @property
    def matrix_(self):
        '''convert the MatObj to Matrix_ Obj'''
        return Matrix_(self.Mat)

    def spectral(self):
        '''returns the spectral Matrix of a MatObj'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        
        if not self.issq:
            raise InvalidOperation('Only Square  Matrices can have Spectral Matrix')
        return mat.diag(self.ev())
    
    @property
    def issym(self):
        '''returns True if Symmetric else False'''
        return self == self.trn()

    @property
    def isskw_sym(self):
        '''returns True if Skew Symmetric else False'''
        return self.trn() == -self
        
    @property
    def isidemp(self):
        '''returns True if Idempotent else False'''
        try:
            return self*self == self
        except DimensionError:
            return False

    @property
    def isperiodic(self):
        '''returns True if periodic else False'''
        try:
            self_ = self*self
            for i in range(2):
                if self_ == self:
                    return True
                self_ *= self
            return False
        except DimensionError:
            return False
        except Exception:
            raise ImprobableError


    def __invert__(self):
        '''returns the inverse of the Matrix
           ~MatObj -> MatObj^-1
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        
        # Ensuring Matrix is Square and not singular
        if not self.issq:
            raise InvalidOperation('Inverse Property are only supported by Square')
        if self.issing:
            raise InvalidOperation('Singular Matrix has no Inverse')
        
        self._mat = self.Mat
        self.aug()
        emulated = mat.unit(self.rows);count = 0
        
        for integer in range(emulated.cols): #row
            col = self.get_col(integer+1)
            for integers in range(emulated.rows): #col
                count_ = 0
                if self[integers+1,integer+1] != emulated[integers+1,integer+1]:# To check if the elements corresponds as in Unit Matrix
                    if emulated[integers+1,integer+1] == 1: # To try convert the element to 1
                        try:
                            self.perform(rows = [1/self[integers+1, integer+1],integers+1])
                        except ZeroDivisionError:
                            # Switching elements to a non-zero elements after Multiply the row by the inverse
                            while True:
                                if count_ > count:
                                    if col[count_] != 0:
                                        self.perform('~',[integers+1,count_+1])
                                        self.perform([1/self[integers+1, integer+1]],integers+1)
                                        break
                                count_ += 1
                    else:
                        # Try setting the element to 0
                        while True:
                            try:
                                if integers > integer:
                                    self.perform(rows = [(self[integers+1, integer+1]/self[integer+1,integer+1])**(-1),integers+1])
                                    self.perform('-',[integers+1,integer+1])
                                elif integers < integer:
                                    self.perform(rows = [(self[integers+1, integer+1]/self[integer+1,integer+1]),integer+1])
                                    self.perform('-',[integers+1,integer+1])
                                break
                            except ZeroDivisionError:
                                while True:
                                    if count_ > count:
                                        if col[count_] != 0:
                                            self.perform('~',[integer+1,count_+1])
                                            break
                                    count_ += 1
            count += 1
        for integers in range(self.rows):
            del self['1']
        self.mat = self.Mat
        self.Mat = self.mat
        return Matrix(self.mat)
    

    def crack(self):
        '''splits the MatObj into two'''
        if not self.issq:
            raise InvalidOperation('Only Square Matrices support this operation')
        return .5 * (self + ~self),.5 * (self - ~self)
    
    def nullspace(self):
        '''returns all the nullspace of the MatObj'''
        return self.matrix_.nullspace().matrix    
    
    def ev(self, repeat = False):
        '''returns all the real eigen values of the MatObj'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        return self.matrix_.ev()
    
    def property(self):
        '''Displays the property of the MatObj'''
        print(self)
        try:
            print(self.type)
            try:
                print(f'Determinat is {abs(self)}')
            except InvalidOperation:
                print('Determinant Not Supported')
            print(f'Rank is {self.rank}')
            try:
                self_ = self * self
                if self.isnilp:
                    for i in range(2,6):
                        if not (self_ if  i == 2  else _self):
                            print(f'This Matrix is Nilpotent to the index of {i+1}')
                            break;
                        if i == 2:
                            _self = self_ * self
                        else:
                            _self *= self
            except Exception:
                pass
            try:
                if self.isperiodic:
                    for i in range(3,6):
                        if not (self_ if  i == 3  else _self) | self:
                            print(f'This Matrix has a period of {i-1}')
                            break
                        if i == 3:
                            _self = self_ * self
                        else:
                            _self *= self
            except Exception:
                pass
            
            try:
                for i in range(2,6):
                    if self_.unit:
                        print(f'This Matrix raised to the power of {i-1} gives its inverse\n Hence This Matrix raised to the power of {i} gives a Unit Matrix')
                        break;
                    self_ *= self
            except Exception:
                pass
            print('------Transpose-------')
            print(self.trn())
            print('------Cofactors-------')
            try:
                print(self.cofactors())
            except InvalidOperation:
                print('Not Supported')
            print('------Spectral-------')
            print(self.spectral())
            print('------Modal-------')
            print(self.modal())
            print('------Inverse-------')
            try:
                print(~self)
            except InvalidOperation:
                print('Singular Matrix has no Inverse')
            print('------Echelon Form-------')
            print(self.echelon())
            print('------Reduced Echelon Form-------')
            print(self.canonical())
        except OperationNotAllowed:
            print('This Matrix is Disabled')
        
    def __add__(self,other):
        if self.isdisabled or other.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')

        if self.order != other.order:
            raise DimensionError(f'Incompatible Matrices: {" x ".join(self.order)} and {" x ".join(other.order)}')
        new = self.empty; _new = list(self.order)
        for integer in range(self.rows):
            _new += list(map(add, self.get_row(integer+1), other.get_row(integer+1)))
        new.Mat = _new
        return new
    
    def __sub__(self,other):
        if self.isdisabled or other.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')

        if self.order != other.order:
            raise DimensionError(f'Incompatible Matrices: {" x ".join(self.order)} and {" x ".join(other.order)}')
        new = self.empty; _new = list(self.order)
        for integer in range(self.rows):
            _new += list(map(sub, self.get_row(integer+1), other.get_row(integer+1)))
        new.Mat = _new
        return new
    
    def __mul__(self,other):
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')

        new = self.empty
        if isinstance(other, int) or isinstance(other, float):
            _new = list(self.order)
            for integer in range(self.rows):
                _new += [other*item for item in self.get_row(integer+1)]
        else:
            if self.isdisabled:
                raise OperationNotAllowed('This Matrix is Disabled')

            if not self.cols == other.rows:
                raise DimensionError(f'Incompatible Matrices: {" x ".join(self.order)} and {" x ".join(other.self.order)}')
            _new = [self.rows, other.cols]
            for integer in range(self.rows):
                row = self.get_row(integer+1)
                for integers in range(other.cols):
                    _new.append(sum(list(map(mul,row , other.get_col(integers+1)))))
        new.Mat = _new
        return new
    
    def __truth__(self):
        get = ''
        for integer in range(self.rows):
            for integers in range(self.cols):
                if self[integer+1,integers+1]:
                    return True
        return False


mat = Matrix((1,2))

class Matrix_(MatrixObjectClass, Utilities.matrix, StaticStates):
    '''
        Calling this class create a Matrix Object.
        The class will initialize a Matrix for you by just calling Matrix_()
        if you want to convert arrays to Matrix Object you use the X parameter
            You convert a list to Matrix Object; this will work fine if the
                first 2 elements gives the order of the matrix

                e.g To convert [1,2,3,4,5,6,7,8], this can be a 1x8, 2x4, 4x2 or 8x1
                    so you indicate the order by adding the order to the begining
                    if the order is 2 x 4
                    Mat_A = Matrix(X = [2,4,1,2,3,4,5,6,7,8]
                    
            You can convert 2D array (in form of list)
                e.g Mat_A = Matrix([[1,2],[3,4],[5,6],[7,8]])

            Also, You convert consistent list or tuple to Matrix Object
                e.g Mat_A = Matrix([1,2],[3,4],[5,6],[7,8])

            You can convert numpy arrays as well
                e.g if Y is an numpy.ndarray object, then Mat_A = Matrix(X = Y)

    '''
            
    def __init__(self, X = [], *Y):
        self.name = "Matrix_"
        if Y:
            
            cols = len(X)
            x = [1 + len(Y),cols] + X
            for Xs in Y:
                if len(Xs) != cols:
                    raise InconsistencyError(f'These data are not consistent in columns: {str(X) +", " + star(Y)}')
                x += Xs
            Mat = x
        elif isinstance(X,set):
            self.Mat = X
            self.state = 'enabled'
            return
        elif isinstance(X,ndarray) or X:
            _mat = X
            if isinstance(X,ndarray):
                _mat = list(X.shape)
                for rows in X:
                    Mat_ += list(rows)
                Mat = Mat_
            elif X and isinstance(X[0],(list, tuple)):
                _mat = [len(X),len(X[0])]
                for rows in X:
                    if len(rows) != _mat[1]:
                        raise DimensionError('Dimension Inconsistent')
                    _mat += rows
                Mat = _mat
            elif isinstance(X,(list, tuple)):
                Mat = X
        elif isinstance(X,Matrix_):
            Mat = X.Mat
        else:
            Mat = []
            try:
                order = input("Matrix Order: ")
                col = int(order.split('x')[1]); row = int(order.split('x')[0])
                Mat.append(row); Mat.append(col); count = 1
                while count <= row:
                    disp = "Enter the"
                    if count == 1:
                        pos = 'First'
                    elif count ==2:
                        pos = 'Second'
                    elif count == row:
                        pos = 'Last'; disp = 'Good, Now the'
                    else: pos = 'Next'; disp = ''
                    element = input(f"{disp} {pos} row: ").split(',')
                    while True:
                        if len(element) == col:
                            for elements in element:
                                Mat.append(Expr(elements))
                            break
                        num = "element" if len(element) == 1 else 'elements'
                        print(f"Error, You Entered {len(element)} {num} instead of {col}")
                        element = input("Try Again: ").split(',')
                    count += 1
                            
            except Exception:
                raise ImprobableError(f'Unknown Error Occurred')
        self.Mat = [Expr(items) if c > 1 else items for c, items in enumerate(Mat)]
        self.state = 'enabled'
        
    def __str__(self,pr_sr = True):
        ord_ = []
        for integers in range(self.rows):
            ord_.append([repr(self[integers + 1, integer + 1]) for integer in range(self.cols)])
        return str(D2_ord(ord_))
    
    def null(self,order):
        ''' Returns Null Matrix'''
        mat = self.empty
        if isinstance(order, int):
            mat.Mat = [order,order]
            order = order*order
            
        else:
            mat.Mat = [order[0],order[1]]
            order = order[0] * order[1]
        mat.Mat += [Expr({0: [{'':0}]}) for i in range(order)]
        return mat
    
    def unit(self,order):
        ''' Returns Unit Matrix'''
        if isinstance(order,int):
            order = [order,order]
        Mat = list(order); mat = self.empty
        if Mat[0] != Mat[1]:
            raise DimensionError('Unit Matrix are meant to be Square')
        for integer in range(order[0]):
            for integers in range(order[1]):
                Mat.append(Expr({1: [{'':0}]}) if integer == integers else Expr({0: [{'':0}]}))
        mat.Mat = Mat
        return mat


    def __repr__(self):
        return self.__str__()
            
    
    def __setitem__(self,key,value,force = False):
        ''' Set elements in a MatObj
            MatObj[i] = value
                if i is an integer:
                    if i < 0, then backward counting; -1 will select the last row, -2 will select the second to the last row and so on
                    if value i is not a list or tuple, the ith entry of the MatObj will be set to value
                    else if value is a list or tuple:
                        if i is within the number of rows, row i will set to the list or tuple elements
                        else if i is 1 + the number of rows, a new row will be added and its elements will
                        be set to that of the list or tuple
                else if i is a string:
                    it works just as described above but on the columns not rows
            MatObj[i,j] = value
                The element at row i, col j is set to value
                Negative entries are also supported

            
        '''
        # check if Matrix is active or immutable
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if self.isimut:
            raise InvalidOperation('This Matrix is Immutable')
        # row for integer, col for string, i,j for list 
        if isinstance(key,int):
            if key < 0:
                key = self.rows + 1 + key
            if not isinstance(value,(tuple,list)):
                self.Mat[key+1] = Expr(value) if not force else value
            elif isinstance(value,(list, tuple)):
                if key == self.rows+1:
                    self.add_row(value)
                elif key > 0 and key <= self.rows:
                    self.add_row(value)
                    self.perform('~',rows=[-1, key])
                    del self[-1]
                else:
                    raise UnacceptableToken(f'Invalid Entry: {key}')
        elif isinstance(key,str):
            self.__setitem__(['*',int(key)],value)
        elif len(key) == 2:
            key = list(key)
            if key[0] == '*':
                if key[1] < 0:
                    key = ['*',self.cols + 1 + key[1]]
                if key[1] == self.cols+1:
                    self.add_col(value)
                elif key[1] > 0 and key[1] <= self.cols:
                    self.add_col(value)
                    self.perform('~',cols=[-1, key[1]])
                    del self['-1']
                else:
                    raise UnacceptableToken(f'Invalid Entry: {str(key)}')
            elif key[0] > self.rows or key[1] > self.cols:
                raise OutOfRange(f"Entry {key} doesn't exist. This Matrix only has {self.rows} rows and {self.cols} columns")
            else:
                if isinstance(value, (tuple,list)):
                    raise UnacceptableToken(f'Invalid value {value} for entry {key}')
                if key[1] < 0:
                    key[1] += self.cols + 1
                if key[0] < 0:
                    key[0] += self.rows + 1
                self.Mat[(key[0]-1)*self.cols+ key[1]+1] = Expr(value) if not force else value
                
    def solns(self,equate = 0,repeat = False, **kwargs):
        '''Returns the values of the unknows when the determinat = equate in tuple

                [   3        7       - x]
           A =  [  - 3/2   x - 2     5  ], if |A| = 10, find x
                [x^2 - 6     - 9   x + 2]

            >>> A = Matrix_([3,3,3,7,'-x', -3/2,'x-2',5,'x^2 -6',-9, 'x+2'])
            >>> A.solns(10)
            which gives (-1.5487461869840489, 1.4235819144877857)

                    [   3         7d       - xy - sqrt(a)]
               Z =  [  - 3/2   3log2(a)        - 3c/4    ]
                    [x^2 - 6      - 9      2xy - 5log2(a)]
            
                find x, given that a = 4, c = 5, d = -2, y = -7 and |A| = -5
             >>> Z = Matrix_([3,3,3,'7d','-xy - sqrt(a)', -3/2,'3log2(a)','-3c/4','x^2 -6',-9, '2xy - 5log2(a)'])
             >>> Z.solns(-5, a = 4, c = 5, d = -2, y = -7)
             which is equivalent to
             >>> Z.solns(-5, **{'a': 4, 'c': 5, 'd': -2, 'y' : -7})
             which gives (1.182787466260118, 3.290717213374106, -2.937790393919938)
             
        '''
        self_ = self
        if kwargs:
            self_ = self.cal(kwargs)
        var_list =  self_.vars
        if not var_list:
            raise ActionDuplicationError('This Matrix is already solved')
        elif len(var_list) > 1:
            raise OperationNotAllowed
        return abs(self_).solns(equate, repeat = repeat, **kwargs)
    
    def __abs__(self):
        '''returns the determinat of a Matrix'''
        
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if not self.issq: # For Square Matrix certainty
            raise InvalidOperation('Determinats are only supported by Square Matrices')
        mat_init = tuple(self.Mat)
        res = 0
        if self.order == [2,2]:
            return (self[1]*self[4] - self[3]*self[2]).simp()
        mult = self.pop()
        _mat = tuple(self.Mat)
        for integers in range(self.cols):
            self.Mat = list(_mat)
            del self[f'{integers+1}']
            res += (-1)**integers * mult[integers] * abs(self)
        self.Mat = list(mat_init)
        return res.simp()


    @property
    def vars(self):
        '''Returns all the Variables in the MatObj''' 
        var_list = []
        for index in range(len(self)):
            var_list += self[index+1].vars
        return list(set(var_list))
    
    @property
    def variables(self):
        var_list = []
        for index in range(len(self)):
            var_list += self[index+1].variables
        return list(set(var_list))

    def add_row(self, *row):
        '''
            Add rows to the MatObj
            MatObj.add_row([...],[....],[....])
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if self.isimut:
            raise InvalidOperation('This Matrix is Immutable')
        row_ = []; empty = True if len(self.Mat) == 2 else False; l = 0
        for rows in row:
            if empty or len(rows) == self.cols:
                row_ += [Expr(rows_) for rows_ in rows]
            else:
                raise DimensionError(f'{rows} is not consistent with this Matrix which has {self.cols} columns')
            if l and l != len(rows):
                raise DimensionError(f'these entries are not consistent {star(row)}')
            l = len(rows)
        else:
            self.Mat += row_
            self.Mat[0] += len(row)
            if empty:
                self.Mat[1] += l
            
    
    def trace(self):
        '''returns the trace of the MatObj'''
        return sum(self.get_diag()).simp()

    def __lshift__(self,other):
        '''To Compare two Matrices and solve them

            A = [x + 3   2y + x],    B = [0    - 7]
                [z - 1   4a - 6]         [3    2a ]

            >>> A << B
            now 
            which are the solutions
        '''
        if not isinstance(other, (Matrix_, Matrix)):
            raise InvalidOperation(f'Only Matrices can be compared: Matrix and {type(other)}')
        if self.order != other.order:
            raise DimensionError('Only Matrices of the same order can be compared: {" x ".join(self.order)} and {" x ".join(other.order)}')

        soln = (self - other) >> mat_.null(self.order)
        self.cal(soln)
        other.cal(soln)
        return soln
    
    def __rshift__(self,other):
        '''To Compare two Matrices and find the unknowns

            A = [x + 3   2y + x],    B = [0    - 7]
                [z - 1   4a - 6]         [3    2a ]

            >>> A >> B
            will give [{'x': -3, 'y': -2, 'z': 4, 'a': 3}]
            which are the solutions
        '''
        if not isinstance(other, (Matrix_, Matrix)):
            raise InvalidOperation(f'Only Matrices can be compared: Matrix and {type(other)}')
        if self.order != other.order:
            raise DimensionError('Only Matrices of the same order can be compared: {" x ".join(self.order)} and {" x ".join(other.order)}')

        return  self.toequation(other.elements).solve()
    
    def inv(self):
        for ints_ in range(len(self)):
            if not self[ints_+1].isnum():
                return True
        return False
    
    def LU(self):
        '''Decomposes the MatObj into a Upper and Lower triangular Matrix'''
        if not self.issq:
            raise InvalidOperation('This can only decompose square Matrix and this is not a Square Matrix')
        alpha = simp_var()
        L = mat_.null(self.order)
        U = mat_.unit(self.order)
        for i in range(1,self.rows+1):
            for j in range(1,self.cols+1):
                if j > i:
                    U[i,j] = next(alpha)
                    continue
                L[i,j] =  next(alpha)
        soln = ((L*U) >> self)[0]
        return L.cal(soln), U.cal(soln)
    
    def perform(self, operation = '',rows = [],A = 1,B = 1, cols = []):
        '''
            Row operations perform(operation = '',rows = [],A = 1,B = 1, cols = [])
            For Rows and columns Operation

            To interchange rows, set the operation argument to '~', and the
                    rows argument to a list or tuple of the two rows to be change

                            [    1  - x        cos(2θ)      sin(3α)]
                  Let A =   [ 8x^2ln(xy)    2x - tan(2αβ)   cos2(θ)]
                            [cos(α)sin(β)       1  + x      x^2 - 1]
                   To interchange row 1 and row 3

                   >>> A.perform('~',[1,3])
                   now A is

                            [cos(α)sin(β)       1  + x      x^2 - 1]
                            [ 8x^2ln(xy)    2x - tan(2αβ)   cos2(θ)]
                            [    1  - x        cos(2θ)      sin(3α)]
                    To interchange column 2 and 3
                    >>> A.perform('~',cols = [2,3])
                    A is now 
                            [cos(α)sin(β)   x^2 - 1       1  + x   ]
                            [ 8x^2ln(xy)    cos2(θ)   2x - tan(2αβ)]
                            [    1  - x     sin(3α)      cos(2θ)   ]
            Row, col multiplication:

                    To multiply row 2 by 4
                    >>> A.perform(rows = [4,2]) # or A.perform('',[4,2])
                    A is now
                        [cos(α)sin(β)    x^2 - 1        1  + x   ]
                        [ 32x^2ln(xy)   4cos2(θ)   8x - 4tan(2αβ)]
                        [    1  - x      sin(3α)       cos(2θ)   ]
            Addition and Subtraction of Rows and cols:
                set operation to either + or -, use A, B to set the coefficients
                of the first and second rows (or cols). By default A = B = 1

                    To Add row 2 to row 1
                    >>> A.perform('+',[1,2])

                    A is
                [sin(β)cos(α) + 32x^2ln(xy)   4cos2(θ) + x^2 - 1    - 4tan(2αβ) + 9x +  1 ]
                [        32x^2ln(xy)               4cos2(θ)             8x - 4tan(2αβ)    ]
                [           1  - x                  sin(3α)                cos(2θ)        ]

                To add row 1 to row 2
                >>> A.perform('+',[2,1])
                
                A =
                [sin(β)cos(α) + 32x^2ln(xy)   4cos2(θ) + x^2 - 1     - 4tan(2αβ) + 9x +  1 ]
                [sin(β)cos(α) + 64x^2ln(xy)   8cos2(θ) + x^2 - 1    - 8tan(2αβ) + 17x +  1 ]
                [           1  - x                  sin(3α)                 cos(2θ)        ]

                To multiply row 1 by 2 and add row 2 to it
                >>> A.perform('+',[1,2],2)
                This is equivalent to
                >>> A.perform(rows = (2,1))
                >>> A.perform('+',(1,2))
                A = 
                [3sin(β)cos(α) + 128x^2ln(xy)   16cos2(θ) + 3x^2 - 3     - 16tan(2αβ) + 35x + 3]
                [ sin(β)cos(α) + 64x^2ln(xy)     8cos2(θ) + x^2 - 1     - 8tan(2αβ) + 17x +  1 ]
                [            1  - x                    sin(3α)                  cos(2θ)        ]

                To multiply row 2 by 3 and add it to row 3
                >>> A.perform('+',[3,2],B = 3)
                which is equivalent to
                >>> A.perform('',[3,2])
                >>> A.perform('+',[3,2])

                A =
                [     3sin(β)cos(α) + 128x^2ln(xy)             16cos2(θ) + 3x^2 - 3             - 16tan(2αβ) + 35x + 3   ]
                [      sin(β)cos(α) + 64x^2ln(xy)               8cos2(θ) + x^2 - 1             - 8tan(2αβ) + 17x +  1    ]
                [3sin(β)cos(α) + 192x^2ln(xy) - x +  1    24cos2(θ) + sin(3α) + 3x^2 - 3   cos(2θ) - 24tan(2αβ) + 51x + 3]

                To multiply row 1 by x, then multiply row 3 by y and subtract row 1 from row 3

                >>> A.perform('+',[3,1],'y','x')
                Also equivalent to
                >>> A.perform('',('y',1))
                >>> A.perform(rows = ('x', 3))
                >>> A.perform('-',(3,1))

                A =
            [                      3sin(β)cos(α) + 128x^2ln(xy)                                            16cos2(θ) + 3x^2 - 3                                          - 16tan(2αβ) + 35x + 3                   ]
            [                       sin(β)cos(α) + 64x^2ln(xy)                                              8cos2(θ) + x^2 - 1                                           - 8tan(2αβ) + 17x +  1                   ]
            [3ysin(β)cos(α) + 3xsin(β)cos(α) + 192x^2yln(xy) + 128x^3ln(xy) - xy + y   24ycos2(θ) + 16xcos2(θ) + ysin(3α) + 3x^2y + 3x^3 - 3x - 3y   ycos(2θ) - 24ytan(2αβ) - 16xtan(2αβ) + 51xy + 3x + 3y + 35x^2]


            for col operation just use cols = (...)
        '''
        # Row Operations
        if self.isimut:
            raise InvalidOperation('This Matrix is Immutable')
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        # To translate to Column Operations
        if not rows:
            col_mat = self.trn()
            col_mat.perform(operation = operation,rows = cols,A = A,B = B, cols = [])
            self.Mat = col_mat.trn().Mat
            return
        # Row multiplication with scalar rows[0],Interchanging Rows, Addition, Subtraction
        if not operation:
            row = self.get_row(rows[1])
            for integer in range(self.cols):
                self[rows[1],integer+1] = row[integer]*rows[0]
        elif operation == '~':
            row1 = self.get_row(rows[0])
            row2 = self.get_row(rows[1])
            for integer in range(self.cols):
                self[rows[0],integer+1] = row2[integer]
                self[rows[1],integer+1] = row1[integer]
        elif operation in  ('+','-'):
            row1 = self.get_row(rows[0])
            row2 = self.get_row(rows[1])
            for integer in range(self.cols):
                self[rows[0],integer+1] = (A*row1[integer] + B*row2[integer]).simp() if operation == '+' else (A*row1[integer] - B*row2[integer]).simp()
                
    def modal(self):
        '''returns the modal matrix of the MatObj'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        # Modal Matrix
        if not self.issq:
            raise InvalidOperation(f'Only Square Matrices can have Modal Matrix: {" x ".join(self.order)}')
        mod_mat = self.order
        mod = self.empty
        for evs in self.ev():
            aug_mat = (self - evs * self.unit(mod_mat)).nullspace()
            
            mod.aug((self - evs * self.unit(mod_mat)).nullspace())
        if mod.cols != self.cols:
            raise Fizzle('One or more of the eigenvalues yield eigenvectors that are not linearly independent')
        return mod
    
    def solve(self, equate = 0, **kwargs):
        '''This call the solns method and substitue each solution into the Matrix
           and return is as a generator
        '''
        
        var_list = self.vars
        if len(var_list) != 1:
            raise OperationNotAllowed

        for root in self.solns(equate, **kwargs):
            yield self.cal(root)

    @property       
    def type(self):
        attr = []
        if self.issq:
            attr.append('Square')
        if self.issing:
            attr.append('Singular')
        if not self:
            attr.append('Null')
        if self.isunit:
            attr.append('Unit')
        if self.isdiag:
            attr.append('Diagonal')
        if self.isscalar:
            attr.append('Scalar')
        if self.issym:
            attr.append('Symmetric')
        if self.isskw_sym:
            attr.append('Skew Symmetric')
        if self.isupper_delta:
            attr.append('Upper Triangular')
        elif self.islower_delta:
            attr.append('Lower Triangular')
        if self.isorth:
            attr.append('Orthogonal')
        if self.isunitary:
            attr.append('Unitary')
        if self.isherm:
            attr.append('Hermitian')
        if self.isskw_herm:
            attr.append('Skew Hermitian')
        if self.isidemp:
            attr.append('Idempotent')
        if self.isperiodic:
            attr.append('Periodic')
        if self.isnilp:
            attr.append('Nilpotent')
        if self.isinv:
            attr.append('Involuntary')
        
        return ', '.join(attr) + ' Matrix'

    
    def cal(self,value = '', **values):
        ''' For Substitution
            The values can be parsed as dictionaries or keyword arguments or both
                    [   3          7       - x - sqrt(a)]
                Z = [  - 3/2   3log2(a)        - 3/4    ], if a = 4
                    [x^2 - 6      - 9      2x - 5log2(a)]
            
               Z = Matrix_([3,3,3,7d,'-xy - sqrt(a)', -3/2,'3log2(a)',-3c/4,'x^2 -6',-9, '2xy - 5log2(a)'])
               Zc = Z.cal(a = 4, c = 5, d = -2, y = -7)
               which is equivalent to
               Zc = Z.cal({'a' :4, 'c' : 5, 'd' : -2, 'y' : -7})
               [   3       - 14      7x - 2  ]
               [  - 3/2     6        - 15/4  ]
               [x^2 - 6     - 9    - 14x - 10]
               
               
        '''
        var_list = self.vars
        if value and (isinstance(value,(float,int,str)) or getter(value,'name') == 'Expr') and not values  and len(var_list) != 1 :
            raise Vague('Operation not Understood')
        self_ = self.empty;
        if not value and not values:
            
            value = {}
            for var_ in var_list:
                value[var_] = Expr(input(f'{var_}? '))
        _self = [self[ints+1].cal(value, **values) for ints in range(len(self))]
        self_.Mat = list(self.order) + _self
        return self_
            
    def quad(self,vec = ''):
        if vec:
            if not isinstance(vec,list) and not isinstance(vec,tuple)and not isinstance(vec,dict):
                raise UnacceptableToken('vec must be either list or tuple')
            if len(vec) != self.cols:
                raise UnacceptableToken(f'This Matrix has {self.cols} columns; so, a {self.cols} column vector is expected, not {len(vec)}')
            vec = [1,self.cols] + list(vec)
        if not vec:
            vec = [1,self.cols]
            for i in range(self.cols):
                vec.append(alpha[i])
        return (Matrix_(vec) * self * Matrix_(vec).trn())[1,1]
    
    def export(self):
        return array([rows for rows in self])

    @property
    def isscalar(self):
        '''returns True if Scaler else False'''
        if not self.issq:
            return False
        return List(self.get_diag()).unique
    
    @property
    def issym(self):
        '''returns True if Symmetric else False'''
        return self | self.trn()

    @property
    def isskw_sym(self):
        '''returns True if Skew Symmetric else False'''
        return self.trn() | -self
        
    @property
    def isidemp(self):
        '''returns True if Idempotent else False'''
        try:
            return self*self | self
        except DimensionError:
            return False

    @property
    def isperiodic(self):
        '''returns True if periodic else False'''
        try:
            self_ = self*self
            for i in range(2):
                if self_ | self:
                    return True
                self_ *= self
            return False
        except DimensionError:
            return False
        except Exception:
            raise ImprobableError

    @property
    def isherm(self):
        '''returns True if Hermitian else False'''
        if not self.iscomplex:
            return False
        return self | self.conj().trn()

    @property
    def isunitary(self):
        '''returns True if Unitary else False'''
        if not self.issq or not self.iscomplex:
            return False
        return (self * self.theta()).isunit

    @property
    def iscomplex(self):
        '''returns True if Complex else False'''
        var = self.variables
        if 'î' in var or 'ĵ' in var or 'ǩ' in var or not var:
            return True
        return False

    @property
    def isskw_herm(self):
        '''returns True if Skew-Hermitian else False'''
        if not self.iscomplex:
            return False
        return self | -self.conj().trn()
    
    def __invert__(self):
        '''returns the inverse of the Matrix
           ~MatObj -> MatObj^-1
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        
        # Ensuring Matrix is Square and not singular
        if not self.issq:
            raise InvalidOperation('Inverse Property are only supported by Square')
        if self.issing:
            raise InvalidOperation('Singular Matrix has no Inverse')
        #if self.vars:
         #   raise OperationNotAllowed("This is operation is not allowed on Matrices with expressions")
        emulated = mat_.unit(self.order);count = 0
        self._mat = self.Mat
        self.aug()
        
        for integer in range(emulated.cols): #row
            col = self.get_col(integer+1)
            for integers in range(emulated.rows): #col
                count_ = 0
                if self[integers+1,integer+1] != emulated[integers+1,integer+1]:# To check if the elements corresponds as in Unit Matrix
                    if emulated[integers+1,integer+1] == 1: # To try convert the element to 1
                        try:
                            self.perform(rows = [~self[integers+1, integer+1],integers+1])
                        except ZeroDivisionError:
                            # Switching elements to a non-zero elements after Multiply the row by the inverse
                            while True:
                                if count_ > count:
                                    if col[count_]:
                                        self.perform('~',[integers+1,count_+1])
                                        self.perform([~self[integers+1, integer+1]],integers+1)
                                        break
                                count_ += 1
                    else:
                        # Try setting the element to 0
                        while True:
                            try:
                                if integers > integer:
                                    self.perform(rows = [self[integer+1,integer+1]/self[integers+1, integer+1],integers+1])
                                    self.perform('-',[integers+1,integer+1])
                                elif integers < integer:
                                    self.perform(rows = [(self[integers+1, integer+1]/self[integer+1,integer+1]),integer+1])
                                    self.perform('-',[integers+1,integer+1])
                                break
                            except ZeroDivisionError:
                                while True:
                                    if count_ > count:
                                        if col[count_] != 0:
                                            self.perform('~',[integer+1,count_+1])
                                            break
                                    count_ += 1
            count += 1
        for integers in range(self.rows):
            del self['1']
        self.mat = self.Mat
        self.Mat = self.mat_
        return Matrix_(self.mat)

    @property
    def matrix(self):
        '''converting the MatObj to Matrix Class'''
        return Matrix(self.Mat)
    
    def spectral(self):
        '''returns the spectral Matrix of a MatObj'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        
        if not self.issq:
            raise InvalidOperation('Only Square  Matrices can have Spectral Matrix')
        return mat_.diag(self.ev())
        
    def toequation(self,eq = '', var = ''):
        '''returns set of eqns of the MatObj multiplied with a column vector (variables)
           MatObj.toequation([....], ['x1','x2','x3',.....])
        '''
        cross = self * (Matrix_([len(var),1] + var) if var else 1)
        eqn = Eqns()
        for elements, eqs in imap(cross.elements, eq):
            if not eqs:
                eqs = 0
            eqn.add(Eqn(elements, eqs))
        return eqn
    
    def conj(self):
        '''returns the conjugate of the MatObj'''
        if not self.iscomplex:
            raise InvalidOperation('This must contain a complex identity')
        conjugate = copy(self)
        for i in range(len(self)):
            conjugate[i+1] = self[i+1].conjugate if self[i+1].iscomplex else self[i+1]
                    
        return conjugate
    
    def crack(self):
        '''decomposes the MatObj into two MatObjs'''
        if not self.issq:
            raise InvalidOperation('Only Square Matrices support this operation')
        if self.iscomplex:
            return  .5 * (self + self.theta()), .5 * (self - self.theta())
        return .5 * (self + ~self),.5 * (self - ~self)

    def nullspace(self):
        '''returns all the linearly independent column vectors of the Matrix'''
        if not self.islindep:
            raise Fizzle('This Matrix composed of linearly independent column vectors')
        var = [f'a{i}' for i in range(1, self.cols +1)]
        zeros = [0 for i in range(self.rows)]
        eqn = Eqns(); self_ = copy(self)
        self_.add_col(zeros)
        solns = eqn.solve(matrix = self_, vmat = var, q = ''); vlist = []
        vecs = lexpr(*[vals for var, vals in solns[0].items()])
        space = self.empty
        for vec in vecs:
            vlist += list(vec.vars)
        vlist = list(set(vlist))
        for v in vlist:
            space.add_col(lexpr(*whole([num(var.coeff(v)) for var in vecs])))

        return space
         
    def theta(self):
        '''returns the transpose of the conjugate of the MatObj'''
        return self.conj().trn()
    
    
    def ev(self, repeat = False):
        '''returns all the real eigen values of the MatObj'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        eigen_values = []
        if not self.issq:
            raise InvalidOperation('Determinats are only supported by Square Matrices')
        self_ = copy(self)
        for integers in range(self.rows):
            self_[integers+1,integers+1] = self_[integers+1,integers+1] - 'x'
        
        return self_.solns(repeat = repeat)
    
    def property(self):
        '''Displays the property of the MatObj'''
        print(self)
        try:
            
            print(self.type)
            try:
                print(f'Determinat is {abs(self)}')
            except InvalidOperation:
                print('Determinant Not Supported')
            print(f'Rank is {self.rank}')
            try:
                self_ = self * self
                if self.isnilp:
                    for i in range(2,6):
                        if not (self_ if  i == 2  else _self):
                            print(f'This Matrix is Nilpotent to the index of {i+1}')
                            break;
                        if i == 2:
                            _self = self_ * self
                        else:
                            _self *= self

            except Exception:
                pass
            try:
                if self.isperiodic:
                    for i in range(3,6):
                        if not (self_ if  i == 3  else _self) | self:
                            print(f'This Matrix has a period of {i-1}')
                            break
                        if i == 3:
                            _self = self_ * self
                        else:
                            _self *= self
            except Exception:
                pass
            try:
                for i in range(2,6):
                    if self_.unit:
                        print(f'This Matrix raised to the power of {i-1} gives its inverse\n Hence This Matrix raised to the power of {i} gives a Unit Matrix')
                        break;
                    self_ *= self
            except Exception:
                pass
            print('------Transpose-------')
            print(self.trn())
            print('------Cofactors-------')
            try:
                print(self.cofactors())
            except InvalidOperation:
                print('Not Supported')
            print('------Spectral-------')
            try:
                print(self.spectral())
            except Exception:
                print('Not Supported')
            print('------Modal-------')
            try:
                print(self.modal())
            except InvalidOperation:
                print('Not Supported')
            print('------Inverse-------')
            try:
                print(~self)
            except InvalidOperation:
                print('Singular Matrix has no Inverse')
            print('------Echelon Form-------')
            print(self.echelon())
            print('------Canonical Form-------')
            print(self.canonical())
        except OperationNotAllowed:
            print('This Matrix is Disabled')
        
    def __add__(self,other):
        if self.isdisabled or other.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')

        if self.order != other.order:
            raise DimensionError(f'Incompatible Matrices: {" x ".join(self.order)} and {" x ".join(other.order)}')
        new_ = list(self.order); new = self.empty
        for integer in range(self.rows):
            new_ += list(map(add, self.get_row(integer+1), other.get_row(integer+1)))
        new.Mat = new_
        return new.simp()
    
    def __sub__(self,other):
        if self.isdisabled or other.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')

        if self.order != other.order:
            raise DimensionError(f'Incompatible Matrices: {" x ".join(self.order)} and {" x ".join(other.order)}')
        new_ = list(self.order); new = self.empty
        for integer in range(self.rows):
            new_ += list(map(sub, self.get_row(integer+1), other.get_row(integer+1)))
        new.Mat = new_
        return new.simp()


    def __or__(self, other):
        '''compares two MatObj
           compare entries of the MatObj to the correspondingly for equivalence'''
        if not isinstance(other,Matrix_):
            raise UnacceptableToken(f'Only Matrices can be compared')
        if self.order != other.order:
            return False
        for element1, element2 in imap(self.elements, other.elements):
            if not element1 | element2:
                return False
        return True
    
    def __mul__(self,other):
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        new = self.empty
        if isinstance(other, int) or isinstance(other, float) or isinstance(other,Expr):
            new_ = list(self.order)
            for element in self.elements:
                new_.append(other * element)
        elif not getter(other, 'name') in ('Matrix','Matrix_'):
            raise InvalidOperation(f"Can't  multiply MatObjs with {type(other)}")
        else:
            if self.isdisabled:
                raise OperationNotAllowed('This Matrix is Disabled')

            if not self.cols == other.rows:
                raise DimensionError(f'Incompatible Matrices: {" x ".join(self.order)} and {" x ".join(other.self.order)}')
            new_ = [self.rows, other.cols]
            for integer in range(self.rows):
                row = self.get_row(integer+1)
                for integers in range(other.cols):
                    new_.append(sum(list(map(mul, row, other.get_col(integers+1)))).simp())
        new.Mat = new_
        return new
    
    def lin_diff(self, var = 't', repeat = 1,*args, **kwargs):
        '''different each entries wrt var'''
        diff = self.empty; new = list(self.order)
        diff.Mat = new + [elements.lin_diff(var,
                                            repeat,
                                            *args,
                                            **kwargs) for elements in self.elements]
        return diff
        
    def simp(self):
        '''rewriting all entries in concise form if possible'''
        for i , j in enumerate(self.elements,1):
            self[i] = j.simp()
        return self
    
    def __truth__(self):
        get = ''
        int(b)
        for integer in range(self.rows):
            for integers in range(self.cols):
                if self[integer+1,integers+1]:
                    return True
        return False


InitMat = Matrix_({'!@#$%^&'})
mat_ = Matrix_({'!@#$%^&'})

