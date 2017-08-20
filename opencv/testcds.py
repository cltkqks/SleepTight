#test cds function
import cds

try:
    while True:
        print(cds.light(4))
except KeyboardInterrupt:
    pass
finally:
    cds.clean()

