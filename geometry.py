# coding: utf-8

"""
Classes geométricas.
"""
__author__  = 'Humberto Lino'
__version__ = '1.0'

class Circle:
    """
    Representa um Círculo.
    """
    def __init__(self, pos, radius):
        """
        @type  pos: Point
        @param pos: Posição (x,y)
        @type  radius: number
        @param radius: Raio
        @rtype: Circle
        @return: Instâncida de Círculo.
        """
        self.pos = pos
        self.radius = radius

    def tuple(self):
        """
        Tupla.

        @rtype: tuple
        @return: Tupla com (x,y,raio).
        """
        return (self.pos.x, self.pos.y, self.radius)

    def __repr__(self):
        """
        Representa Círculo em String.

        @rtype: string
        @return: Circle(x,y,raio).
        """
        return "Circle(%s, %s, %s)" % self.tuple()


class Rectangle:
    """
    Representa um Retângulo.
    """
    def __init__(self, pos, width, height):
        """
        Construtor.

        @type  pos: Point
        @param pos: Posição (x,y)
        @type  width: number
        @param width: Largura
        @type  height: number
        @param height: Altura
        @rtype: Rectangle
        @return: Instâncida do Retângulo.
        """
        self.pos = pos
        self.width = width
        self.height = height

    def tuple(self):
        """
        Tupla.

        @rtype: tuple
        @return: Tupla com (x,y,largura,altura).
        """
        return (self.pos.x, self.pos.y, self.width, self.height)

    def __repr__(self):
        """
        String.

        @rtype: string
        @return: Rectangle(x,y,largura,altura).
        """
        return "Rectangle(%s, %s, %s, %s)" % self.tuple()

class Line:
    """
    Representa uma Linha.
    """
    def __init__(self, p1, p2):
        """
        Construtor.

        @type  p1: Point
        @param p1: Ponto 1
        @type  p2: Point
        @param p2: Ponto 2
        @rtype: Line
        @return: Instância de Line.
        """
        self.p1 = p1
        self.p2 = p2

    def tuple(self):
        """
        Representa um Círculo.

        @rtype: tuple
        @return: tuple(p1,p2).
        """
        return (self.p1, self.p2)

    def __repr__(self):
        """
        String.

        @rtype: string
        @return: (p1,p2).
        """
        return "(%s, %s)" % self.tuple()

class Point:
    """
    Representa um Ponto 2D.
    """
    def __init__(self, x, y):
        """
        Construtor.
        @type  x: number
        @param x: Coordenada X do eixo das abscissas
        @type  y: number
        @param y: Coordenada Y do eixo das coordenas
        @rtype: Point
        @return: Instância de Point.
        """
        self.x = x
        self.y = y

    def tuple(self):
        """
        Tupla.
        @rtype: string
        @return: tuple(x,y).
        """
        return (self.x, self.y)

    def __repr__(self):
        """
        String.
        @rtype: string
        @return: (x,y)
        """
        return "(%.2f, %.2f)" % self.tuple()