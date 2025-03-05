from dataclasses import dataclass
#Creates 3D list based on prompted inputs. 1st list is a list of restaurant brand. 
# Each restaurant brand has a list of restaurant buildings (2). 
# Each restaurant building has a list of employees (3).
# 
# FUNCTIONS
def stripAll(oldList:list):
    newList = []
    for i in oldList:
        i.strip()
        newList.append(i)
    return newList

def buildListClassesOnlyNames(classInput: type):
    #first gather all the name attributes from the user. Initialize other values to fill in later
    namesInput = input(f"please type all of the names of the {classInput} you want inputted seperated by commas")
    names = namesInput.split(',')
    #get rid of whitespace
    names = stripAll(names)
    #Create instances with names and store in a list
    instances = []
    if classInput != Employee:
        for name in names:
            instances.append(classInput(name, 0, Finance(), [], -1))
    else:
        for name in names:
            instances.append(classInput(name, 0, -1))

    return instances

#init 3d list for restaurant
D1 = 0
D2 = 0
D3 = 0
restaurantEmployees = [[[None for x in range(D1)] for y in range(D2)] for z in range(D3)]

#CLASSES that will be used in the list
#Finance (shared class attribute for brand and building)
@dataclass
class Finance:
    profit = -1
    laborExpenses = -1
    otherExpenses = -1
    expenses = laborExpenses + otherExpenses
    net = profit - expenses

# brands
@dataclass
class Brand:
    name: str
    address: str
    financial: Finance
    buildings: list
    id: int

# buildings
@dataclass
class Building:
    name: str
    address: str
    financial: Finance
    employees: list
    id: int

# employees
@dataclass
class Employee:
    name: str
    pay: int
    id: int

#Building brands
Brands = buildListClassesOnlyNames(Brand)
#Building buildings for each brand and employees for each building
for i in Brands:
    print(f"Now input the names of the buldings owned by {i.name}")
    i.buildings = buildListClassesOnlyNames(Building)
    for j in i.buildings:
        print(f"Now input all of the employees who work at {j.name}")
        j.employees = buildListClassesOnlyNames(Employee)

#build big list of employees organized by brands and then by buildings
for z, zBrand in enumerate(Brands):
    # set index equal to id attribute
    zBrand.id = z
    restaurantEmployees.append([])
    for y, yBuilding in enumerate(zBrand.buildings):
        yBuilding.id = y
        restaurantEmployees[z].append([])
        for x, xEmployee in enumerate(yBuilding.employees):
            xEmployee.id = x
            restaurantEmployees[z][y].append(xEmployee.name) 

print(restaurantEmployees)