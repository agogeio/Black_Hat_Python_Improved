from collections import namedtuple

#* https://www.geeksforgeeks.org/namedtuple-in-python/
#? Performance - https://medium.com/@jacktator/dataclass-vs-namedtuple-vs-object-for-performance-optimization-in-python-691e234253b9
#? Performance - https://news.ycombinator.com/item?id=11054590
#? Working with namedtuples - https://towardsdatascience.com/understand-how-to-use-namedtuple-and-dataclass-in-python-e82e535c3691
#! Updating tuples - That depends on the data type of the tuple attributes,
#! If the attribute is immutable like str, float, int, then we can’t modify the state

# Transaction = collections.namedtuple('Transaction',['sender','receiver','date','amount'])
# record = Transaction(sender="jojo",receiver="xiaoxu",date="2020-06-08",amount=1.0)

Heros = namedtuple('Student', ['name', 'age', 'DOB', 'GPA', 'teams'])
id_0001 = Heros('Tony Stark', '44', '09/22/1978', '4.0', ['Avengers'])
#? id_0001 = Student(name='Tony Stark', age='44', DOB='09/22/1978', GPA='4.0')
#? You can assign based on keys identified in the constructor

print(f'Heros memory location: {id(Heros)}')
print(f'id_0001 memory location: {id(id_0001)}')

# Access using name
print(f'Hero data is: {id_0001.name}, {id_0001.age}, {id_0001.DOB}, {id_0001.GPA}, {id_0001.teams}')
# Access using position
print(f'Hero data is: {id_0001[0]}, {id_0001[1]}, {id_0001[2]}, {id_0001[3]}, {id_0001[4]}')
# Convert to dict
print(id_0001._asdict())

try:
    #! If the attribute is immutable like str, float, int, then we can’t modify the state
    id_0001.name = "Bruce Banner"
except Exception as err:
    print(err)

#! We CAN modify the state of an object if it is mutable like a list
id_0001.teams.append('Solo')
print(f'Hero data is: {id_0001.name}, {id_0001.age}, {id_0001.DOB}, {id_0001.GPA}, {id_0001.teams}')


name = "Steven" 
print(f'Name memory location: {id(name)}') #? NOTE: Memory location 
name = "Lindsay"
print(f'Name memory location: {id(name)}') #? NOTE: Changed Memory location because strings are not mutable

friends = ['Joe', 'John', 'Myles']
print(f'Friends memory location: {id(friends)}')
friends[2] = 'Lindsay' #? This will NOT change the memory location 
print(f'Friends memory location: {id(friends)}')
friends = ['Joe', 'John', 'Myles', 'Lindsay'] #? This WILL change the memory location
print(f'Friends memory location: {id(friends)}')
