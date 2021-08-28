"""This module implements and provides Vector Operation to engpy"""
import math
from operator import mul, add
from errors.exceptions import *
from errors.warnings import warn
from arrays import Matrix_
from interface import Var
from interface import _complex, zero
from interface import arccos
from misc.assist import getter
from misc.gen import check_rest
from oblects.abc import BaseClass

_complex()

from interface import i, j, k, _i, _j, _k
component = [_i, _j, _k]


class Vector(BaseClass):
    def __init__(self, cexp):
        """Vector Objects (VectObjs) can be created by calling the Vector Class
           if R = xî + yĵ + zǩ
           To represent R as VectObj, then
           This can be either
               1. parsing the coefficients the i, j, k planes respectively:
                   >>> R = Vector(['x','y','z']
                   xî + yĵ + zǩ
    
                2. Taking the vector of an ExprObj
                    >>> from engpy.tools.exprs import Expr
                    >>> from engpy.arrays import Vector
                    >>> r = Expr('x.i + y.j +z.k')
                    >>> R = Vector(r)
                3. parsing as a string
                    >>> R = Vector('xi + yj +zk')
        """
        self.name = 'Vector'
        if not cexp:
            self.vec = Var(cexp)
            return
        if isinstance(cexp,(list, tuple)):
            if len(cexp) > 3:
                raise Vague(f'{cexp} has more than 3 elements')
            v = (i, j , k)
            cxep = Var(*cexp)
            while len(cexp) < 3:
                cexp.append(zero)
            self.vec = sum(list(map(mul,cexp,v)))
        elif getter(cexp, 'name') == 'Expr':
            if not cexp.iscomplex:
                raise UnacceptableToken(f'No Vector component is present: {cexp}')
            self.vec = cexp.simp()
        elif isinstance(cexp, Vector):
            self.vec = cexp.vec
        else:
            cexp = cexp.replace('.i',
                                     _i).replace('.j',
                                                     _j).replace('.k',
                                                                 _k)
            self.vec = Var(cexp.replace('i',
                                         _i).replace('j',
                                                     _j).replace('k',
                                                                 _k)).simp()

    def __str__(self):
        add = []; k = self.i, self.j, self.k
        if i:
            term = f'({i}){_i} ' if len(i) > 1 else  format(i) + _i if  format(i) != ' 1 ' else _i
            add.append(term)
        if j:
            
            term = f'({j}){_j} ' if len(j) > 1 else  format(j)+ _j if  format(j) != ' 1 ' else _j
            if  term.replace(' ','')[0] != '-':
                term = ' + ' + term
            add.append(term)
        if self.k:
            term = f'({k}){_k} '  if len(k) > 1 else  format(k) + _k if  format(k) != ' 1 ' else _k
            if  term.replace(' ','')[0] != '-':
                term = ' + ' + term
            add.append(term)
        if not add:
            return '0'
        return ''.join(add)
    
    def __setitem__(self,other,value):
        """To change the coefficient of the planes, use 1,2,3 for the planes respectively or
           the plane itself
           R = xî + yĵ + zǩ
           to change i component to 2x^2 - y and k component to z^2 + 2x
           >>> R = Vector('xi + yj +zk')
           >>> R[1] = '2x^2 - y'  # or R['i'] = '2x^2 - y'
           >>> R[k] = 'z^2 + 2x'
        """
        if other in ('i', _i, 1, i):
            self.vec = (self.vec - i * self.i + i * Var(value)).simp()
        elif other in ('j', _j, 2, j):
            self.vec = (self.vec - j * self.j + j * Var(value)).simp()
        elif other in ('k', _k, 3, k):
            self.vec = (self.vec - k * self.k + k *Var(value)).simp()

    def __getitem__(self,other):
        """VectObj[x] -> x can be either 1, 2 ,3 or the planes (i,j,k)"""
        return self.i if other in (1,_i, i, 'i') else self.j if other in (2,_j,j,'j') else self.k if other in (3,_k, k,'k') else None
    
    @property
    def vars(self):
        """returns all the variables in the VectObj"""
        var_list = self.vec.vars
        if _i in var_list:
            var_list.remove(_i)
        if _i in var_list:
            var_list.remove(_j)
        if _i in var_list:
            var_list.remove(_k)
        return var_list

    @property
    def i(self):
        """returns the i component of the VectObj"""
        return self.vec.coeff(_i)

    @property
    def j(self):
        '''returns the j component of the VectObj'''
        return self.vec.coeff(_j)

    @property
    def k(self):
        '''returns the k component of the VectObj'''
        return self.vec.coeff(_k)

    def __abs__(self):
        '''returns the modulus of the VectObj'''
        return ((self.i**2 + self.j**2 + self.k**2).simp())**0.5
    
    def ray(self):
        '''returns the VectObj component in a list'''
        return [self.i,self.j,self.k]

    def __sub__(self,other):
        if not isinstance(other,Vector):
            raise InvalidOperation('Subtraction only take btwn Vaectors Only')
        return Vector((self.vec - other.vec).simp())
    
    def __add__(self,other):
        if not isinstance(other,Vector):
            raise InvalidOperation('Addition is btwn Vectors Only')
        return Vector((self.vec + other.vec).simp())

    def __repr__(self):
        add = []; i, j, k = self.i, self.j, self.k
        if i:
            term = f'({repr(i.inroots)}){_i} ' if len(self.i) > 1 else  repr(i.inroots) + _i if  repr(i.inroots) != ' 1 ' else _i
            add.append(term)
        if j:
            
            term = f'({repr(j.inroots)}){_j} ' if len(self.j) > 1 else  repr(j.inroots)+ _j if  repr(j.inroots) != ' 1 ' else _j
            if  term.replace(' ','')[0] != '-':
                term = ' + ' + term
            add.append(term)
        if k:
            term = f'({repr(i.inroots)}){_k} '  if len(self.k) > 1 else  repr(k.inroots) + _k if  repr(k.inroots) != ' 1 ' else _k
            if  term.replace(' ','')[0] != '-':
                term = ' + ' + term
            add.append(term)
        if not add:
            return '0'
        return ''.join(add)

    @property
    def theta_x(self):
        '''returns the directional cosine in x direction'''
        return self.i/abs(self)

    @property
    def theta_y(self):
        '''returns the directional cosine in y direction'''
        return self.j/abs(self)

    @property
    def theta_z(self):
        '''returns the directional cosine in z direction'''
        return self.k/abs(self)

    def theta(self, other):
        '''returns the angle between tow VectObjs'''
        return arccos(self & other)
    
    def lin_diff(self,var = 't'):
        '''Differentiate a VectObj wrt to var
           by default, var = 't'
        '''
        return Vector(self.vec.lin_diff(var))
    
    def integrate(self,var = 't'):
        '''Integrate a VectObj wrt to var
           by default, var = 't'
        '''
        return Vector(self.vec.integrate(var))

    @property
    def isscalar(self):
        '''returns True if the VectObj is a scalar'''
        if check_rest(component, str(self)):
            return True
        return False
    
    def unit(self):
        '''returns the VectObj in unit form/notation'''
        return self/abs(self)
    
    def tangent(self,**var):
        """returns the tangent of the VectObj

           Determine the tangent vector at point (2,4,7) for the curve with
           parametric equation
                           x = 2u; y = u^2 + 3; z = 2u^2 + 5
           >>> x, y , z = Var('2u', 'u^2 + 3', '2u^2 + 5')
           >>> r = Vector((x,y,z))
           >>> r.tangent(u = 1)
           2î + 2ĵ + 4ǩ


           Determine the unit tangent vector at point (2,0,π) for the curve with
           parametric equation
                           x = 3t, y = 2t^2, z = 2t^2 + 2
           >>> x, y , z = Var('3t', '2t^2', '2t^2 + 2')
           >>> r = Vector((x,y,z))
           >>> r.tangent(t = 2).unit()
           59299/231359î + 306942/449083ĵ + 306942/449083ǩ


           A particle moves in space so that at time t its position is stated as
           x = 2t + 3, y = t^2 + 3t, z = t^3 + 2t^2. Find the component of velocity
        """
        return self.lin_diff(list(var)[0]).simp(**var)
    
    def _simp(self, **values):
        if not values:
            var_list = self.vars
            for var_ in var_list:
                if not var_ in component:
                    values[var_] = Var(input(f'{var_}? '))
        if 'i' in values or 'j' in values  or 'k' in values:
            warn('values for i,j,k will be neglected')
        for ints in range(3):
            self[ints+1] = self[ints+1].cal(**values)
        return self
    
    def simp(self,**values):
        """Evaluating and substituting values into the VectObj
           e.g VectObj.simp(x =4)
        """
        return self._simp(**values) if values else self
    
    def grad(self,scalar,*func, **pts):
        """returns the grad of a scalar
           the scalar can be a string or ExprObj, by default func is
           x : i, y:j , z: k pair
           
           if φ = 3x^2y - y^3z^2; find gard φ at the point (1,-2,-1)

           >>> vec.grad('3x^2y - y^3z^2', x = 1, y = -2, z = -1)
           - 12î - 9ĵ - 16ǩ
        """
            
        if getter(scalar, 'name') != 'Expr':
            scalar = Var(scalar)
        if func:
            if len(func) == 1 and isinstance(func[0], dict):
                func = func[0]
            elif len(func) != 3:
                raise UnacceptableToken
            else:
                func = dict(zip(('x','y','z'),func))
        else:   
            func = {'x':i,'y':j,'z':k} 
        if scalar.iscomplex:
            raise UnacceptableToken(f'{scalar} is not a scalar')
        
        return Vector(scalar.diffs(func)).simp(**pts)
    
    def direc(self,scalar,*func, **pts):
        '''Similar to grad, however, must be carried out on the vector with the direction


           Find the directonal derivative of x^2y^2z^2 at the point (1,1,-1) in the direction
           of the tangent of the curve x = e^t, y = sin(2t) + 1, z = 1 - cos(t) at t = 0

           >>> phi = Var('x^2y^2z^2')
           >>> curve = Vector(('.e^t', 'sin(2t)+1','1-cos(t)'))
           >>> tan_curve = curve.tangent(t = 0)
           >>> tan_curve.direc(phi, x = 1, y = 1, z = -1)
           832040/310083
        '''
        if func:
            if len(func) != 3:
                raise UnacceptableToken
            func = dict(zip(('x','y','z'),func))
        else:   
            func = {'x':i,'y':j,'z':k} 
        return self.unit() & self.grad(scalar,*[func],**pts)
    
    def normal(self,scalar,*func, **pts):
        '''

            Find the rate of change of φ = xyz in the direction normal to the surface
                                x^2y + y^2x + yz^2 = 3 at the point (1,1,1)
            >>> normal = vec.normal('x^2y + y^2x + yz^2 - 3', x = 1, y =1, z =1)
            >>> normal.grad('xyz', x = 1, y = 1, z = 1)
            1587401/949824


            Find the constants m and n such that the surface mx^2 - 2nyz = (m + 4)x will
            be orthogonal to the surface 4x^2y + z^3 = 4 at the point (1, -1, 2)

            >>> phi_1 = Var('mx^2 - 2nyz - (m + 4)x')
            >>> points = {'x': 1, 'y': -1, 'z': 2}
            >>> n = phi_1.solved(**points)
            >>> phi_2 = Var('4x^2y + z^3 - 4')
            >>> normal_phi_1 = vec.normal(phi_1,n = n, **points)
            >>> normal_phi_2 = vec.normal(phi_2,**points)
            >>> m = (normal_phi_1 & normal_phi_2).solved()  # both normals are said to be orthogonal
            >>> m,n
            (5, 1)
            
            
        '''
        if func:
            if len(func) != 3:
                raise UnacceptableToken
            func = dict(zip(('x','y','z'),func))
        else:   
            func = {'x':i,'y':j,'z':k} 
        return self.grad(scalar,*[func], **pts)
    
    @property
    def issolenoidal(self):
        '''return True if solenoidal else False'''
        return not(self.div())

    @property
    def isrotational(self):
        '''return False if irrotational else True'''
        return bool(self.curl())

    def isorth(self,other):
        '''return True if vectObj and the other VecObj are orthogonal else False'''
        if not isinstance(other, Vector):
            raise InvalidOperation
        return not self & other
    
    def div(self,planes = ('x','y','z'), **pts):
        """ returns the divergence of a VectObj on planes
            By default the planes are x, y, z

            if u =  x^2 + y^2 + z^2, and r = xî + yĵ + zǩ, then find div(ur)

            >>> u = Var('x^2 + y^2 + z^2')
            >>> r = Vector('xî + yĵ + zǩ')
            >>> (u * r).div()
            5x^2 + 5y^2 + 5z^2
        """
        return (self.i.lin_diff(planes[0]) +
                self.j.lin_diff(planes[1]) +
                self.k.lin_diff(planes[2])
                )._cal(**pts)
                
    def curl(self, planes = ('x','y','z'), **pts):
        '''returns the curl of a VectObj on planes

           Find the divergence and curl of v = (xyz)î + (3x^2y)ĵ + (xz^2 - y^2z)ǩ
                   at  (2, -1, 1)

           >>> v = Vector('(xyz)i + (3x^2y)j + (xz^2 - y^2z)k')
           >>> div_v = v.div(x = 2, y = -1, z = 1)
           >>> curl_v = v.curl(x = 2, y = -1, z = 1)
           >>> div_v, curl_v
           (14, 2î - 3ĵ - 14ǩ)
        '''
        return Vector(abs(Matrix_([3,3] +
                                  component +
                                  _del(planes)+
                                  self.ray()
                                  )
                          )
                      ).simp(**pts)
    
    def __xor__(self,other):
        '''returns the angle between two VectObj in cosines'''
        if not isinstance(other, Vector):
            raise InvalidOperation(f'Can only find angle btwn VectObjs: {type(other)}')
        return (self.theta_x * other.theta_x +
               self.theta_y * other.theta_y +
               self.theta_z * other.theta_z
               ).simp()
    
    @property
    def empty(self):
        '''return Null VectObj'''
        return Vector('')
    
    def __mul__(self,other):
        if not isinstance(other,(int,float, Vector))  and getter(other, 'name') != 'Expr':
            raise InvalidOperation('Multiplication only take btwn Vectors Only or scalars')
        if isinstance(other,(int,float)) or getter(other, 'name') == 'Expr':
            if not isinstance(other,(int,float)) and other.vectorized:
                other = Vector(other)
            else:
                vec = self.empty
                vec.vec = other * self.vec
                return vec
        return Vector(abs(Matrix_([3,3]+component+self.ray()+other.ray())))
    
    def __truediv__(self,other):
        return self * other** -1

    def __and__(self,other):
        '''returns the dot product of two VectObj'''
        if not isinstance(other, Vector):
            raise InvalidOperation(f"can't take dot product of Vector and {type(other)}")

        return sum(list(map(mul,self.ray(),other.ray()))).simp()
    
    def s_trip(self,v1,v2):
        '''returns the scalar product of 3 VectObjs'''
        if not isinstance(v1, Vector) or not isinstance(v1, Vector):
            raise InvalidOperation('Scalar product only take place btw vectors')
        return abs(Matrix_([3,3]+self.ray()+v1.ray()+v2.ray()))
    
    def v_trip(self,v1,v2):
        '''returns the vector product of 3 VectObjs'''
        if not isinstance(v1, Vector) or not isinstance(v1, Vector):
            raise InvalidOperation('Vector product only take place btw vectors')
        return self * (v1 * v2)

    def __or__(self,other):
        for planes in component:
            if not self[planes] | other[planes]:
                return False
        return True
    
    def __bool__(self):
        return bool(self.vec)
    
    def __eq__(self,other):
        if not isinstance(other, Vector):
            return False
        return self.vec == other.vec
    
    def __ne__(self,other):
        return not self.vec == other.vec
    
    def __rmul__(self,other):
        return self * other
    
    def __neg__(self):
        return -1 * self
    
    def coplanar(self,other,_other):
        '''returns True  if the 3 VectObjs re coplanar else False'''
        return True if not self.s_trip(other,_other) else False


def _del(var = ('x','y','z')):
    return [f'.F{var_}' for var_ in var]


vec = Vector('')
