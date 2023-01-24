import random
import decimal

print("{")
print("'households': {")
for i in range(459):
    print(str(i) + ":{(" + str(float(decimal.Decimal(random.randrange(3600, 3700)/100))) + "," + str(float(decimal.Decimal(random.randrange(-9700, -9600)/100))) + ")},")
print("}, 'schools': {")
for i in range(3):
    print(str(i) + ":{(" + str(float(decimal.Decimal(random.randrange(3600, 3700)/100))) + "," + str(float(decimal.Decimal(random.randrange(-9700, -9600)/100))) + ")},")
print("}, 'workplaces': {")
for i in range(200):
    print(str(i) + ":{(" + str(float(decimal.Decimal(random.randrange(3600, 3700)/100))) + "," + str(float(decimal.Decimal(random.randrange(-9700, -9600)/100))) + ")},")
print("}, 'restaurants': {")
for i in range(10):
    print(str(i) + ":{(" + str(float(decimal.Decimal(random.randrange(3600, 3700)/100))) + "," + str(float(decimal.Decimal(random.randrange(-9700, -9600)/100))) + ")},")
print("}, 'churches': {")
for i in range(5):
    print(str(i) + ":{(" + str(float(decimal.Decimal(random.randrange(3600, 3700)/100))) + "," + str(float(decimal.Decimal(random.randrange(-9700, -9600)/100))) + ")},")
print("}, 'community_centres': {")
for i in range(2):
    print(str(i) + ":{(" + str(float(decimal.Decimal(random.randrange(3600, 3700)/100))) + "," + str(float(decimal.Decimal(random.randrange(-9700, -9600)/100))) + ")},")
print("}, 'supermarkets': {")
for i in range(3):
    print(str(i) + ":{(" + str(float(decimal.Decimal(random.randrange(3600, 3700)/100))) + "," + str(float(decimal.Decimal(random.randrange(-9700, -9600)/100))) + ")},")
print("}, 'stores': {")
for i in range(10):
    print(str(i) + ":{(" + str(float(decimal.Decimal(random.randrange(3600, 3700)/100))) + "," + str(float(decimal.Decimal(random.randrange(-9700, -9600)/100))) + ")},")
print("}, 'hospitals': {")
for i in range(1):
    print(str(i) + ":{(" + str(float(decimal.Decimal(random.randrange(3600, 3700)/100))) + "," + str(float(decimal.Decimal(random.randrange(-9700, -9600)/100))) + ")},")
print("},")
print("}")