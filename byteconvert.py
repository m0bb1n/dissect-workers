from fractions import gcd

class ByteConvert (object):
    tempUnit = 'b'
    numbers = None

    def __init__ (self, numbers):
        self.numbers = numbers

    def to_terra(self, number):
        self.tempUnit = 'TB'
        return number/1e+12

    def to_giga(self, number):
        self.tempUnit = 'KB'
        return number/1e+9

    def to_mega(self, number):
        self.tempUnit = 'MB'
        return number/1000000

    def to_kilo(self, number):
        self.tempUnit = 'KB'
        return number/1000


    def getBestUnit(self):
        units = (self.to_terra, self.to_giga, self.to_mega, self.to_kilo)
        data = {'gcd':1,'unit':'b'}
        for unit in units:
            convertedNumbers = []
            for num in self.numbers:
                convertedNumbers.append(unit(num))

            temp = reduce(gcd,convertedNumbers)
            print 'temp for {} {}'.format(str(unit),temp)
            if temp/sum(convertedNumbers)<.10:
                for i in range(0,len(convertedNumbers)):
                    convertedNumbers[i]=int(round(convertedNumbers[i]/25.0)*25.0)
                temp = reduce(gcd,convertedNumbers)
                print 'NON CHANGED GCD = 1'

            if temp>data['gcd']:
                data['gcd']=temp
                data['unit'] =  self.tempUnit
                data['numbers'] = convertedNumbers


        print data['numbers']
        print data['gcd']
        print data['unit']
        return data

    #data = getBestUnit([574761,957936,383174])
#print 'highest gcd is {} and in {} format'.format(data['gcd'],data['unit'])
