from misc.gen import getter
from misc.utilities import iter2, iter1, mat_iter, element, mat_iter_col
from abc import ABCMeta, abstractmethod
from copy import copy, deepcopy
from fundamentals.primary import Num
from misc.miscs import num
from misc.assist import deepcopy
from errors.exceptions import *
from errors.wreck import Fizzle


class BaseClass(object):

    """Parent Class for all engpy Objects"""
    
    @classmethod
    def form(cls):
        return cls

    @property
    def recreate(self):
        if getter(self,'form'):
            return self.form()
        return NotImplemented

    def __instancecheck__(self, ins):
        return self.form() is ins


class ExpressionObjectClass(BaseClass):

    @property
    def struct(self):
        if getter(self,'__iter2__'):
            return self.__iter2__(self)

        return NotImplemented

    def __iter__(self):
        return iter1(self)


class MatrixObjectClass(BaseClass):
    @property
    def elements(self):
        if getter(self,'__iter3__'):
            return self.__iter3__(self)

        return NotImplemented

    def __iter__(self):
        return mat_iter(self)

    @property
    def columns(self):
        if getter(self,'__iter5__'):
            return self.__iter5__(self)

        return NotImplemented

    def echelon(self, unique_diag = True):
        '''return the echelon form of the MatObj
           if unique_diag is set to False, the diagonal will not be unique
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        ech = copy(self)
        c, r = self.cols, self.rows
        
        while self[1,1] != 1:
            col = self.get_col()
            if 1 in col:
                ech.perform('~', rows = [1,col.index(1)+1])
            elif self[1,1] == 0:
                col.reverse()
                index = 0
                for item in col:
                    if item:
                        break
                    index += 1
                else:
                    break
                ech.perform('~', rows = [1,len(col)-index])
            break
        for integers in range(c):
            for integer in range(r):
                col = ech.get_col(integers+1)
                if integer > integers and ech[integer+1,integers+1]:
                    try:
                        lcm = Num(num(ech[integers+1, integers+1]),num(ech[integer+1,integers+1])).LCM()
                    except Exception:
                        lcm = ech[integers+1, integers+1]*ech[integer+1,integers+1]
                    A = lcm/ech[integer+1,integers+1]
                    B = lcm/ech[integers+1,integers+1]
                    ech.perform('-',[integer +1,integers+1], A, B )
                elif integer == integers and not ech[integer+1,integers+1]:
                    index = 0
                    for item in col:
                        if index > integer and item:
                            ech.perform('~', rows = [integer+1,index +1])
                            break
                        index += 1
        if unique_diag:
            for i in range(c):
                rows = self.get_col(i +1)
                if i == r:
                    break
                if rows[i]:
                    ech.perform(rows = [~rows[i], i + 1])
        return ech

    def reduce(self,to = 'c'):
        '''return the MatObj in its reduced form
           to can be set to '', c, u, l for row, column, upper triangular,lower
           trigangular reductions respectively. by default to is set to c
        '''
        self_ = copy(self)
        index = 0
        # To ensure the first element is zero
        if self_[1,1] != 1:
            col = self_.get_col()
            if 1 in col:
                index = col.index(1) + 1
                self_.perform('~',[1,index])
            else:
                col = self_.get_row()
                if 1 in col:
                    index = col.index(1) + 1
                    self_.perform('~',cols = [1,index])
                else:
                    col = self_.get_col()
                    for items in col:
                        if items:
                            index = col.index(items) + 1
                            self_.perform('~',[1,index])
                            break
                    if not index:
                        col = self_.get_row()
                        for items in col:
                            if items:
                                index = col.index(items) + 1
                                self_.perform('~',cols = [1,index])
                                break
        if self_[1,1] != 1:
            self_.perform(rows = [~self_[1,1],1])
        for ints in range(min(self_.order)):
            if not self_[ints+1,ints+1]:
                for count, rows in enumerate(self):
                    if count-1 < ints:
                        continue
                    if rows[ints]:
                        self_.perform('~',[count+1,ints+1])
            if not self_[ints+1,ints+1]:
                for count, cols in enumerate(self.trn()):
                    if count-1 < ints:
                        continue
                    if cols[ints]:
                        self_.perform('~',cols = [count+1,ints+1])
            if self_[ints+1,ints+1]  != 1:
                try:
                    if round(self_[ints+1,ints+1],10) == 0:
                        break
                    self_.perform(rows = [~self_[ints+1,ints+1],ints+1])
                except ZeroDivisionError:
                    break
            if to == 'c' or to == 'u':
                for i in range(1,self_.rows+1):
                    if i -2 < ints:
                        continue
                    c_row = self_.get_row(i)
                    if c_row[ints]:
                        self_.perform('+',[i,ints+1], B = -c_row[ints])
            if to == 'c' or to == 'l':
                for i in range(1,self_.cols+1):
                    if i -2 < ints:
                        continue
                    c_row = self_.get_col(i)
                    if c_row[ints]:
                        self_.perform('+',cols = [i,ints+1], B = -c_row[ints])

        return self_

    def trn(self):
        '''returns the transpose of the MatObj'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        rows = self.empty; row = [self.cols, self.rows]
        for col in self.columns:
            row += col
        rows.Mat = row
        return rows
    
    def new(self,new_mat):
        self.Mat = new_mat
        return self
        
    def minor(self,row = 1, col = 1):
        '''returns the minor, A.minor(i, j) => Aij
           by default it returns A11
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        
        minor_ = copy(self)
        del minor_[row, col]
        return minor_
    
    def cofactor(self,row = 1, col = 1):
        '''returns the cofactor, A.cofactor(i, j) => Cij
           by default it returns C11
        '''
        if self.order == [2,2]:
            raise InvalidOperation("2x2 Matrices don't have cofactors")
        return abs(self.minor(row,col))*(-1)**(row+col)

    def cofactors(self):
        '''returns all the Cofactors of the MatObj'''
        cofactor = self.empty
        for integer in range(self.rows):
            cofactor.add_row([cofactor.append(self.cofactor(integer+1,integers+1)) for integers in range(self.cols)])
        return cofactor

    def canonical(self):
        '''returns the reduce MatObj in its Canonical form'''
        return self.reduce()

    def __truediv__(self,other):
        if isinstance(other, int) or isinstance(other, float):
            return self * (1/other)
        return self * ~other

    def __rtruediv__(self,other):
        return other * ~A

    def __round__(self,other):
        '''Approximate each values'''
        self_ = self.empty; _self = list(self.order)
        for rows in self:
            self_ += [round(row, other) for row in rows]
        self_.Mat = _self
        return self_

    def __rmul__(self,other):
        return self.__mul__(other)
    
    def __pow__(self,other):
        if isinstance(other, int):
            for integer in range(abs(other)-1):
                if not integer:
                    obj = self * self
                else:
                    obj *= self
            if other < 0:
                return ~obj
        return obj

    def __le__(self,other):
        '''return Rank of MatObj <= x; where x is number'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if isinstance(other,Matrix):
            other = other.rank
        if not isinstance(other, int):
            raise UnacceptableToken(f'integer or Matrix Object is required: Matrix <= {type(other)}')
        return self.rank <= other
    
    def __gt__(self,other):
        '''return Rank of MatObj > x; where x is number'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if isinstance(other,Matrix):
            other = other.rank
        if not isinstance(other, int):
            raise UnacceptableToken(f'integer or Matrix Object is required: Matrix > {type(other)}')
        return self.rank > other
    
    def __ge__(self,other):
        '''return Rank of MatObj >= x; where x is number'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if isinstance(other,Matrix):
            other = other.rank()
        if not isinstance(other, int):
            raise UnacceptableToken(f'integer or Matrix Object is required: Matrix >= {type(other)}')
        return self.rank >= other

    @property
    def rank(self):
        '''return the rank of the MatObj'''
        rank_ = 0
        for rows in self.echelon():
            rank_ += 1 if rows.count(0) - len(rows) else 0
        return rank_
    
    def __copy__(self):
        mat = self.empty
        mat.Mat = deepcopy(self.Mat)
        return mat
            
    def adj(self):
        '''returns the Adjoint Matrix of the MatObj'''
        return self.cofactors().trn()

    def scalar(self,x,order):
        '''returns a diagonal Matrix with scaler x of order order
           mat_.scalar(4, 3) will return
            [4   0   0]
            [0   4   0]
            [0   0   4]
        '''   
        return self.diag([x for i in range(order)])

    def __ne__(self,other):
        '''Returns False if the MatObj != Another Matrix'''
        if getter(other, 'name') !=  'Matrix_':
            raise InvalidOperation(f'A Matrix can only be compared to Another Matrix Objects, not {type(other)}')
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        return self.Mat != other.Mat
    
    def __lt__(self,x):
        '''return Rank of MatObj < x; where x is number'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if isinstance(x,Matrix):
            x = x.rank()
        if not isinstance(x, int):
            raise UnacceptableToken(f'integer or Matrix Object is required: Matrix < {type(x)}')
        return self.rank < x

    def __contains__(self,item):
        '''return True if item is in the MatObj, else False'''
        other = Expr(item)
        for elements in self.elements:
            if elements == other:
                return True
        return False

    def __neg__(self):
        return -1 * self

    def __eq__(self,other):
        '''Returns True if the MatObj = Another Matrix'''
        if not isinstance(other, Matrix_):
            raise InvalidOperation(f'A Matrix can only be compared to Another Matrix Objects, not {type(other)}')
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        return self.Mat == other.Mat

    def pop(self,key=1):
        '''Deletes the entry and returns the value'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if self.isimut:
            raise InvalidOperation('This Matrix is Immutable')

        # if key is an integer rows is returned else if key is a string column is returned
        if isinstance(key, int):
            if key < 0:
                key = self.rows + 1 + key
            get = self.get_row(key)
            del self[key]
        elif isinstance(key,str):
            if int(key[1]) < 0:
                key = self.cols + 1 + int(key)
            get = self.get_col(int(key))
            del self[str(key)]
        elif isinstance(key,(tuple, list)) and len(key) == 2:
            get = (self.get_row(int(key[0])), self.get_col(int(key[1])))
            del self[int(key[0])]
            del self[str(key[1])]
        return get

    def __delitem__(self,key):
        '''
            You delete rows, columns.
            del MatObj[i]
                if i is an integer, row i will be deleted
                else if i is a string, column i will be deleted
            del MatObj[i,j] will delete row i, and column j

            Negative entries are supported
        '''
        # check if Matrix is active or immutable
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if self.isimut:
            raise InvalidOperation('This Matrix is Immutable')
        # if key is an integer rows is deleted else if key is a string column is deleted
        if isinstance(key,int):
            if key > self.rows:
                raise OutOfRange(f"This Matrix only has {self.rows} rows, Hence Can't get to row {key}")
            if key < 0:
                key = self.rows + 1 + key
            for integer in range(self.cols):
                del self.Mat[(key-1)*self.cols+2]
            self.Mat[0] -= 1
        elif isinstance(key,str):
            if int(key) > self.cols:
                raise OutOfRange(f"This Matrix only has {self.cols} columns, Hence Can't get to column {key}")
            if int(key) < 0:
                key = self.cols + 1 + int(key)
            for integer in range(self.rows):
                del self.Mat[integer*self.cols+2+int(key)-(integer+1)]
            self.Mat[1] -= 1
        elif len(key) == 2:
            del self[int(key[0])]
            del self[str(key[1])]

    def __getitem__(self,other):
        '''Returns the element at i, j
           Use as MatObj[i,j] this will return the element located at row i column j
           if only i i.e MatObj[i] will return the ith element of the Matrix
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')

        if isinstance(other,int): # To get elements element-wise
            return self.Mat[other+1]
        elif len(other) == 2:# To get element located i,j
            if other[1] > self.cols or other[0] > self.rows:
                raise OutOfRange(f"This Matrix only has {self.rows} rows and {self.cols} columns")
            return self.get_row(other[0])[other[1]-1]
        
    def get_row(self,row = 1):
        '''return all the elements at a row in list
           MatObj.row() returns the first row
           Negative entries are also suppported 
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if row > self.rows:
            raise OutOfRange(f"Can't get to column {row}, This Matrix only has {self.rows} columns")
        if row < 0: # To support negative keys
            row = self.rows + 1 + row
        return [self.Mat[(row-1)*self.cols+integer+2] for integer in range(self.cols)]

    def get_col(self, col = 1):
        '''return all the elements at a column in list
            MatObj.col() returns the first column
           Negative entries are also suppported 
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if col > self.cols:
            raise OutOfRange(f"Can't get to column {col}, This Matrix only has {self.cols} columns")
        if col < 0:
            col = self.cols + 1 + col
        return [self.Mat[(col-1)+self.Mat[1]*intger+2] for intger in range(self.rows)]
    def get_diag(self, diag = ''):
        '''return all the elements along the diagonals in list
            MatObj.get_diag() returns the principal diagonal, or give
            diag argument any value
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        Diag = []
        if not self.issq:
            raise DimensionError('Can only get Diagonal of Square Matrix')
        if not diag:
            for rows in self:
                Diag.append(rows[len(Diag)])
        else:
            for rows in self:
                Diag.append(rows[self.rows-(len(Diag)+1)])
        return Diag

    def add_col(self, *col):
        '''
            Add cols to the MatObj
            MatObj.add_col([...],[....],[....])
        '''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if self.isimut:
            raise InvalidOperation('This Matrix is Immutable')
        row_ = []; empty = True if len(self.Mat) == 2 else False
        for rows in col:
            if not empty and len(rows) != self.rows:
                raise DimensionError(f'{rows} is not consistent with this Matrix which has {self.rows} rows')
        addded_mat = self.trn()
        addded_mat.add_row(*col)
        self.Mat = addded_mat.trn().Mat

    @property
    def geomul(self):
        '''returns the geometric multiplicity of each eigenvalues in a dictionary'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        # Modal Matrix
        if not self.issq:
            raise InvalidOperation(f'Only Square Matrices can have Modal Matrix: {" x ".join(self.order)}')
        mod_mat = self.order; mul_ = {}
        for evs in self.ev():
            try:
                mul_[evs] = (self - evs * self.unit(mod_mat)).nullspace().cols
            except Fizzle:
                mul_[evs] = 0
                
        return mul_

    @property
    def algmul(self):
        '''returns the algebraic multiplicity of each eigenvalues in a dictionary'''
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        # Modal Matrix
        if not self.issq:
            raise InvalidOperation(f'Only Square Matrices can have Modal Matrix: {" x ".join(self.order)}')
        mod_mat = self.order; mul_ = {}
        for evs in self.ev(True):
            if evs in mul_:
                mul_[evs] += 1
            else:
                mul_[evs] = 1
                
        return mul_

    def random(self,order, boundary = (-50,50)):
        '''mat_.random(order, boundary) -> returns a MatObj with random element within the boundaries
           e.g mat_.random((3,4),(-2, 10)) -> returns 3 x 4 Matrix with elements within -2 and 10 at random
           by default the boundary is set to -50,50
        '''
        S = self.null(order)
        for i in range(len(S)):
            S[i] = random.randint(boundary[0],boundary[1])
        return S

    def unify(self):
        return [elements if count < 2 else str(elements) for count, elements in enumerate(self.Mat)]

    def reverse(self):
        '''reverse the elements in the MatObj'''
        order = self.order
        mat = self.Mat; del mat[0];del mat[0];mat.reverse()
        self.Mat = list(order) + mat

    def reversed(self):
        ''' return the MatObj with its element reversed'''
        order = self.order; emp = self.empty
        mat = self.Mat; del mat[0];del mat[0];mat.reverse()
        emp.Mat = list(order) + mat
        return emp
    
    def __string__(self):
        return self.__str__(False)

    def aug(self,aug_mat = ''):
        '''Concatenate two MatObj
           MatObj.aug(aug_mat) -> concatenate MatObj with aug_mat
           MatObj.aug() -> concatenate MatObj with Unit Matrix of the same order
        '''
        
        if self.isdisabled:
            raise OperationNotAllowed('This Matrix is Disabled')
        if self.isimut:
            raise InvalidOperation('This Matrix is Immutable')

        if not aug_mat:
            aug_mat = self.unit(self.order)
        else:
            if not self.isempty and self.rows != aug_mat.rows:
                raise DimensionError(f"Can't concatenate Matrices with different number of rows: {self.rows} and {aug_mat.rows}")
        aug_mat = aug_mat.trn()
        _mat_ = self.trn()
        for rows in aug_mat:
            _mat_[_mat_.rows+1] = rows
        self.Mat = _mat_.trn().Mat

    def diag(self,values):
        '''return a diagonal Matrix of values where values is iterable
            mat_..diag([....])
        '''
        
        mat = self.null(len(values))
        for i in range(len(values)):
            mat[i+1,i+1] = values[i]
        return mat

class BaseClassABC(metaclass=ABCMeta):

    @abstractmethod
    def __str__(self):
        return
    
    @abstractmethod
    def __repr__(self):
        return

class BaseOperatorsClassABC(BaseClassABC):
    
    @abstractmethod
    def __add__(self, other):
        return NotImplemented

    @abstractmethod
    def __sub__(self, other):
        return NotImplemented

    @abstractmethod
    def __mul__(self, other):
        return NotImplemented

    @abstractmethod
    def __radd__(self, other):
        return NotImplemented

    @abstractmethod
    def __rsub__(self, other):
        return NotImplemented

    @abstractmethod
    def __rmul__(self, other):
        return NotImplemented

    @abstractmethod
    def __truediv__(self, other):
        return NotImplemented

    @abstractmethod
    def __rtruediv__(self, other):
        return NotImplemented

class StateOperatorClassABC(BaseClassABC):
    
    @abstractmethod
    def __eq__(self, other):
        return NotImplemented

    @abstractmethod
    def __ne__(self, other):
        return NotImplemented

    @abstractmethod
    def __bool__(self, other):
        return NotImplemented

    
class BasicOperatorsClassABC(BaseOperatorsClassABC, StateOperatorClassABC):
    pass

class Utilities(BaseClass):
    class expr:
        def __iter1__(self, cls):
            return iter1(cls)
    class matrix:
        def __iter3__(self, cls):
                return element(cls)
        def __iter5__(self,cls):
            return mat_iter_col(cls)

        def __bool__(self):
            '''returns True if not null Matrix else False'''
            if self != self.null(self.order):
                return True
            
            return False

        @property
        def empty(self):
            return self.recreate([0,0])

        @property
        def issing(self):
            '''returns True if Singular else False'''
            if not self.issq:
                return False
            return not bool(abs(self))
        
        @property
        def isnull(self):
            '''returns True if null else False'''
            return not bool(self)
        
        @property
        def isunit(self,strict):
            '''returns True if Unit else False'''
            if not self.issq or self[1,1] != 1:
                return False
            return self  == mat_.unit(self.order)
        
        @property
        def isdiag(self):
            '''returns True if diagonal else False'''
            if self.isnull:
                return False
            for i in range(self.rows):
                for j in range(self.cols):
                    if j != i and self[i+1,j+1]:
                        return False
            return True
        
        @property
        def isscalar(self):
            '''returns True if Scalar else False'''
            if not self.issq:
                return False
            diag = []
            for i in range(self.rows):
                for j in range(self.cols):
                    if j != i and self[i+1,j+1]:
                        return False
                    else:
                        diag.append(self[i+1,j+1])
            return List(diag).unique
        
        @property
        def islower_delta(self):
            '''returns True if lower triangular else False'''
            for i in range(self.rows):
                for j in range(self.cols):
                    if j > i and self[i+1,j+1]:
                        return False
            return True
        
        @property
        def isupper_delta(self):
            '''returns True if upper triangular else False'''
            for i in range(self.rows):
                for j in range(self.cols):
                    if j < i and self[i+1,j+1]:
                        return False
            return True

        @property
        def isdelta(self):
            '''returns True if triangular else False'''
            if self.isupper_delta or self.islower_delta:
                return True
            return False

        @property
        def isorth(self):
            '''returns True if orthogonal else False'''
            try:
                return (self*self.trn()).isunit
            except DimensionError:
                return False

        @property
        def issq(self):
            '''returns True if sqaure else False'''
            return self.rows == self.cols

        @property
        def islindep(self):
            '''returns True if the vecors are linearly dependent  else False'''
            return self.rank != self.rows

        @property
        def isempty(self):
            '''returns True if empty else False'''
            return True if self.Mat == [0,0] else False

        @property
        def isimut(self):
            '''returns True if Immutable else False'''
            return self.state == 'shield'

        @property
        def isdisabled(self):
            '''returns True if disabled else False'''
            return self.state == 'disabled'

        @property
        def isenabled(self):
            '''returns True if enabled else False'''
            return self.state == 'enabled'
        
        def __len__(self):
            return self.Mat[0]*self.Mat[1]
        
        @property
        def isnilp(self):
            '''returns True if Nilpotent else False'''
            try:
                self_ = self*self
                for i in range(2):
                    if self_ == mat_.null(self.order):
                        return True
                    self_ *= self
                return False
            except DimensionError:
                return False

        @property
        def isinv(self):
            '''returns True if Involuntary else False'''
            if not self[1,1]:
                return False
            try:
                return (self * self).isunit
            except DimensionError:
                return False
            except ImportError:
                raise ImprobableError

        @property
        def cols(self):
            '''returns the number of columns'''
            return self.order[1]

        @property
        def rows(self):
            '''returns the number of rows'''
            return self.order[0]

        @property
        def order(self):
            '''returns the order of the MatObj'''
            return [self.Mat[0],self.Mat[1]]
        
class UtilityClass(BaseClass):
    def __iter2__(self, cls):
        return iter2(cls)
        
class StaticStates:
    def __shield__(self):
        self.state = 'shield'
        
    def __ishield__(self):
        self.state = 'active'
        
    def __disable__(self):
        self.state = 'disabled'
        
    def __enable__(self):
        self.state = 'enabled'
