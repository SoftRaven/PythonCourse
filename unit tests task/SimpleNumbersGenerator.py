class SimpleNumbersGenerator:
    def __init__(self):
        pass

    def generate(self, ceil):
        if ceil < 0:
            raise ValueError("Ceil must be more or equal than zero.")
        primes = []
        a = 2
        while a <= ceil:
            counter = 0
            for i in primes:
                if a % i == 0:
                    counter += 1

            if counter == 0:
                primes.append(a)

            a = a + 1
        return primes