from collections import namedtuple

from typesystem import *
from typesystem.numpy import toNumpySchema

longint = Number(True, False, 8)
double = Number(False, False, 8)
string = String("bytes", None)

assert longint.isinstance(4)
assert not longint.isinstance(3.14)

assert double.isinstance(3.14)
assert double.isinstance(4)

assert double.issubtype(double)
assert longint.issubtype(longint)
assert double.issubtype(longint)
assert not longint.issubtype(double)

assert double.issubtype(Number(False, False, 4))
assert not Number(False, False, 4).issubtype(double)

assert Number(False, True, 8).issubtype(Number(False, True, 8))
assert not double.issubtype(Number(False, True, 8))
assert not Number(False, True, 8).issubtype(double)

assert String("bytes", None).isinstance(b"hello")
assert not String("bytes", None).isinstance(u"hello")
assert String("utf-8", None).isinstance(u"hello")
assert not String("utf-8", None).isinstance(b"hello")

assert String("bytes", 5).isinstance(b"hello")
assert not String("bytes", 4).isinstance(b"hello")
assert String("utf-8", 5).isinstance(u"hello")
assert not String("utf-8", 4).isinstance(u"hello")

assert String("bytes", None).issubtype(String("bytes", None))
assert String("bytes", None).issubtype(String("bytes", 5))
assert String("utf-8", None).issubtype(String("utf-8", None))
assert String("utf-8", None).issubtype(String("utf-8", 5))

assert not String("bytes", None).issubtype(String("utf-8", None))
assert not String("bytes", 5).issubtype(String("bytes", None))
assert not String("utf-8", None).issubtype(String("bytes", None))
assert not String("utf-8", 5).issubtype(String("utf-8", None))

assert Tensor(double, 5).isinstance([1, 2, 3, 4, 5])
assert not Tensor(double, 5).isinstance([1, 2, 3, 4])
assert Tensor(double, 2, 3).isinstance([[1, 2, 3], [4, 5, 6]])
assert not Tensor(double, 2, 3).isinstance([[1, 2, 3]])
assert not Tensor(double, 2, 3).isinstance([[1, 2, 3], [4, 5]])
assert Tensor(String("bytes", None), 3).isinstance([b"one", b"two", b"three"])
assert not Tensor(double, 3).isinstance([b"one", b"two", b"three"])

assert Tensor(double, 5).issubtype(Tensor(double, 5))
assert not Tensor(double, 5).issubtype(Tensor(double, 4))
assert not Tensor(double, 4).issubtype(Tensor(double, 5))

assert Tensor(double, 5).issubtype(Tensor(longint, 5))
assert not Tensor(longint, 5).issubtype(Tensor(double, 5))

assert Collection(double, False, None).isinstance([1, 2, 3])
assert Collection(double, True, None).isinstance([1, 2, 3])
assert not Collection(double, False, 3).isinstance([1, 2, 3, 4, 5])
assert Collection(longint, False, None).isinstance([1, 2, 3])
assert not Collection(longint, False, None).isinstance([1.1, 2.2, 3.3])
assert Collection(double, False, None).isinstance([1.1, 2.2, 3.3])

assert Collection(double, False, None).issubtype(Collection(double, False, None))
assert Collection(double, False, None).issubtype(Collection(longint, False, None))
assert not Collection(longint, False, None).issubtype(Collection(double, False, None))

assert Collection(double, True, None).issubtype(Collection(double, True, None))
assert Collection(double, False, None).issubtype(Collection(double, True, None))
assert not Collection(double, True, None).issubtype(Collection(double, False, None))

assert Collection(double, False, None).issubtype(Collection(double, False, 3))
assert not Collection(double, False, 3).issubtype(Collection(double, False, None))
assert Collection(double, False, 5).issubtype(Collection(double, False, 3))
assert not Collection(double, False, 3).issubtype(Collection(double, False, 5))

assert Mapping(string, double).isinstance({b"one": 1.1, b"two": 2.2, b"three": 3.3})
assert not Mapping(string, longint).isinstance({b"one": 1.1, b"two": 2.2, b"three": 3.3})
assert not Mapping(string, double).isinstance({u"one": 1.1, u"two": 2.2, u"three": 3.3})

assert Mapping(string, double).issubtype(Mapping(string, double))
assert Mapping(string, double).issubtype(Mapping(string, longint))
assert not Mapping(string, longint).issubtype(Mapping(string, double))
assert not Mapping(string, double).issubtype(Mapping(String("utf-8", None), double))

assert Record(one=longint, two=double, three=string).isinstance(namedtuple("tmp", ["one", "two", "three"])(1, 2.2, b"three"))
assert not Record(one=longint, two=double, three=string).isinstance(namedtuple("tmp", ["one", "two", "three"])(1, 2.2, u"three"))
assert not Record(one=longint, two=double, three=string).isinstance(namedtuple("tmp", ["one", "two"])(1, 2.2))
assert Record(one=longint, two=double, three=string).isinstance(namedtuple("tmp", ["one", "two", "three", "four"])(1, 2.2, b"three", b"four"))

assert Record(one=longint, two=double, three=string).issubtype(Record(one=longint, two=double, three=string))
assert not Record(one=longint, two=double, three=string).issubtype(Record(one=longint, two=double, three=String("utf-8", None)))
assert not Record(one=longint, two=double, three=string).issubtype(Record(one=longint, two=double))
assert Record(one=longint, two=double, three=string).issubtype(Record(one=longint, two=double, three=string, four=string))

assert Union(double, string).isinstance(3.14)
assert Union(double, string).isinstance(b"hello")
assert Union(longint, double, string).isinstance(3.14)

assert Union(double, string).issubtype(double)
assert Union(double, string).issubtype(string)
assert Union(double, string).issubtype(longint)
assert Union(double, string).issubtype(Union(double))
assert double.issubtype(Union(double))
assert Union(double).issubtype(double)
assert not Union(double, string).issubtype(Union(double, String("utf-8", None)))

assert Union(double, longint).issubtype(double)
assert double.issubtype(Union(double, longint))
assert Union(double, longint, string).issubtype(Union(double, longint))
assert not Union(double, longint).issubtype(Union(double, longint, string))

top = Record(table=Collection(string, True, None), pointer=Reference("table"))
assert top.fields["pointer"].schema(top) == string
assert top.fields["pointer"].schema(top) != String("utf-8", None)

top = Record(table=Collection(string, True, 5), pointer=Reference("table"))
assert top.fields["pointer"].schema(top) == string
assert top.fields["pointer"].schema(top) != String("utf-8", None)

top = Record(table=Collection(string, False, None), pointer=Reference("table"))
try:
    top.fields["pointer"].schema(top) == string
except TypeError:
    pass
else:
    raise AssertionError

top = Record(table=Collection(Collection(string, True, None), True, None), pointer=Reference("table", 5))
assert top.fields["pointer"].schema(top) == string
assert top.fields["pointer"].schema(top) != String("utf-8", None)

top = Record(table=Tensor(string, 5, 5), pointer=Reference("table", 3))
assert top.fields["pointer"].schema(top) == string
assert top.fields["pointer"].schema(top) != String("utf-8", None)

top = Record(table=Tensor(string, 5, 5, 5), pointer=Reference("table", 3, 3))
assert top.fields["pointer"].schema(top) == string
assert top.fields["pointer"].schema(top) != String("utf-8", None)

top = Record(table=Tensor(string, 5, 5), pointer=Reference("table", 6))
try:
    top.fields["pointer"].schema(top) == string
except TypeError:
    pass
else:
    raise AssertionError

top = Record(table=Mapping(string, Collection(string, True, None)), pointer=Reference("table", ""))
assert top.fields["pointer"].schema(top) == string
assert top.fields["pointer"].schema(top) != String("utf-8", None)

top = Record(outer=Record(inner=Collection(string, True, None)), pointer=Reference("outer", "inner"))
assert top.fields["pointer"].schema(top) == string
assert top.fields["pointer"].schema(top) != String("utf-8", None)

print(pretty(Anything()))
print(pretty(Nothing()))
print(pretty(Null()))
print(pretty(Boolean()))
print(pretty(Number(True, True, 8)))
print(pretty(Number(False, True, 8)))
print(pretty(Number(False, False, 8)))
print(pretty(Number(True, True, 1)))
print(pretty(Number(False, True, 1)))
print(pretty(String("bytes", None)))
print(pretty(String("utf-8", None)))
print(pretty(String("utf-32le", None)))
print(pretty(Tensor(Number(True, True, 8), 1, 2, 3)))
print(pretty(Collection(Number(True, True, 8), False, None)))
print(pretty(Mapping(String("bytes", None), Number(True, True, 8))))
print(pretty(Record(one=Boolean(), two=Number(True, True, 8), three=String("bytes", None))))
print(pretty(Union(Boolean(), Number(True, True, 8), String("bytes", None))))
print(pretty(Union(Null(), Number(True, True, 8))))
print(pretty(Union(String("bytes", None))))
print(pretty(Record(table=Collection(Number(True, True, 8), True, None), pointer=Reference("table")))) 
print(pretty(Record(table=Tensor(Number(True, True, 8), 4, 4), pointer=Reference("table", 2)))) 

print("Unsupported by Numpy:")
print(unsupported(toNumpySchema(Anything())))
print(unsupported(toNumpySchema(Nothing())))
print(unsupported(toNumpySchema(Null())))
print(unsupported(toNumpySchema(Boolean())))
print(unsupported(toNumpySchema(Number(True, True, 8))))
print(unsupported(toNumpySchema(Number(False, True, 8))))
print(unsupported(toNumpySchema(Number(False, False, 8))))
print(unsupported(toNumpySchema(Number(True, True, 1))))
print(unsupported(toNumpySchema(Number(False, True, 1))))
print(unsupported(toNumpySchema(String("bytes", None))))
print(unsupported(toNumpySchema(String("utf-8", None))))
print(unsupported(toNumpySchema(String("utf-32le", None))))
print(unsupported(toNumpySchema(Tensor(Number(True, True, 8), 1, 2, 3))))
print(unsupported(toNumpySchema(Collection(Number(True, True, 8), False, None))))
print(unsupported(toNumpySchema(Mapping(String("bytes", None), Number(True, True, 8)))))
print(unsupported(toNumpySchema(Record(one=Boolean(), two=Number(True, True, 8), three=String("bytes", None)))))
print(unsupported(toNumpySchema(Union(Boolean(), Number(True, True, 8), String("bytes", None)))))
print(unsupported(toNumpySchema(Union(Null(), Number(True, True, 8)))))
print(unsupported(toNumpySchema(Union(String("bytes", None)))))
print(unsupported(toNumpySchema(Record(table=Collection(Number(True, True, 8), True, None), pointer=Reference("table"))))) 
print(unsupported(toNumpySchema(Record(table=Tensor(Number(True, True, 8), 4, 4), pointer=Reference("table", 2))))) 

assert not toNumpySchema(Anything()).supported()
assert not toNumpySchema(Nothing()).supported()
assert not toNumpySchema(Null()).supported()
assert toNumpySchema(Boolean()).supported()
assert toNumpySchema(Number(True, True, 8)).supported()
assert toNumpySchema(Number(False, True, 8)).supported()
assert not toNumpySchema(Number(False, False, 8)).supported()
assert toNumpySchema(Number(True, True, 1)).supported()
assert not toNumpySchema(Number(False, True, 1)).supported()
assert toNumpySchema(String("bytes", None)).supported()
assert not toNumpySchema(String("utf-8", None)).supported()
assert toNumpySchema(String("utf-32le", None)).supported()
assert toNumpySchema(Tensor(Number(True, True, 8), 1, 2, 3)).supported()
assert toNumpySchema(Collection(Number(True, True, 8), False, None)).supported()
assert not toNumpySchema(Mapping(String("bytes", None), Number(True, True, 8))).supported()
assert toNumpySchema(Record(one=Boolean(), two=Number(True, True, 8), three=String("bytes", None))).supported()
assert not toNumpySchema(Union(Boolean(), Number(True, True, 8), String("bytes", None))).supported()
assert toNumpySchema(Union(Null(), Number(True, True, 8))).supported()
assert toNumpySchema(Union(String("bytes", None))).supported()
assert not toNumpySchema(Record(table=Collection(Number(True, True, 8), True, None), pointer=Reference("table"))).supported()
assert not toNumpySchema(Record(table=Tensor(Number(True, True, 8), 4, 4), pointer=Reference("table", 2))).supported()

