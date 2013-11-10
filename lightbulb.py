weight_high = 4
weight_med = 2
weight_low = 1
pop_size = 250
adopters_of_cfl = 0.6
cfl_lamps_for_adopters = 0.2
halogen_prob = 0.2
change_socket_prob = 0.15
lum_distribution = [
    dict(socket='E27', shape='Pear', value=70),
    dict(socket='E14', shape='Pear', value=7),
    dict(socket='GU10', shape='Reflector', value=15),
    dict(socket='G53', shape='Reflector', value=5),
    dict(socket='R7S', shape='Tubular', value=3),
    dict(socket='G24d2', shape='Reflector', value=0),
    ]        
import random

class Person:
    def __init__(self):
        self.friends = []
        self.weight = dict(
            price = weight_high * random.uniform(0.5, 1.5),
            efficiency = weight_med * random.uniform(0.5, 1.5),
            lifetime =  weight_low * random.uniform(0.5, 1.5),
            friends =  weight_med * random.uniform(0.5, 1.5),
            cri =  weight_med * random.uniform(0.5, 1.5),
            output =  weight_low * random.uniform(0.5, 1.5),
            color =  weight_med * random.uniform(0.5, 1.5),
            percept_type =  weight_med * random.uniform(0.5, 1.5),
            percept_brand =  weight_low * random.uniform(0.5, 1.5),
            percept_model =  weight_low * random.uniform(0.5, 1.5),
            )
        self.opinions = dict(
            type = dict(),
            brand = dict(),
            model = dict(),
            )
        self.luminaires = []
        self.init_luminaires()
   
    def init_luminaires(self):
        # TODO: fix this distribution to (Bartlett 1993)
        
        
        is_cfl = random.random() < adopters_of_cfl
        
        count = int(random.uniform(5, 65))
        
        while len(self.luminaires)<count:
            if random.random()< halogen_prob:
                type = 'Halogen'
            else:    
                type = 'Incandescent'
                if is_cfl:
                    if random.random() < cfl_lamps_for_adopters:
                        type = 'CFL'
                        
            if type == 'Incandescent' or type=='CFL':
                options = []
                for lum in lum_distribution:
                    if lum['shape']=='Pear':
                        for i in range(lum['value']):
                            options.append(lum)
                option = random.choice(options)
            elif type == 'Halogen':
                options = []
                for lum in lum_distribution:
                    for i in range(lum['value']):
                        options.append(lum)
                option = random.choice(options)


                        
            
            lamp = lamps.pick(type, option['socket'], option['shape'])
            
            if lamp is not None:
                mine = dict()
                mine.update(lamp)
                u = lamp['lifetime_uncertainty']
                lamp['lifetime'] = lamp['lifetime']*random.uniform(1.0-u, 1.0+u)
                lamp['lifetime'] = lamp['lifetime']*random.uniform(0, 1)
               
                self.luminaires.append(lamp)
            
            
            
    def update_opinions(self):
        pass   # how to update opinions?
        # pos: +=0.1 if x>0 else 0.2
        # neg: -=0.3
        
class People:
    def __init__(self, size):
        self.people = [Person() for i in range(size)]
        self.make_friends()
        
    def make_friends(self):
        edges = 0
        minf = 0
        while minf < 15:
            for j, new in enumerate(self.people):
                for person in self.people[:j]:
                    num = len(person.friends)
                    denom = edges
                    p = float(num)/denom if denom > 0 else 1
                    
                    if random.random()<p:
                        new.friends.append(person)
                        person.friends.append(new)
                        edges += 1
            minf = min([len(p.friends) for p in self.people])            
        #print 'min:', minf, 'edges', edges
        #print [len(p.friends) for p in self.people]
        # TODO: is this legit?  Is this what they meant?
    
    def step(self, dt):
        for lamp in self.luminaires[:]:
            lamp['lifetime'] -= dt
            if lamp['lifetime'] < 0:
                self.replace(lamp)
    
    def replace(self, lamp):    
        self.luminaires.remove(lamp)
        socket = lamp['socket']
        shape = lamp['shape']
        
        change_socket = random.random()<change_socket_prob
        
        for lamp in lamps.lamps:
            if change_socket or (lamp['socket']==socket and lamp['shape']==shape):
                utility = self.compute_utility(lamp)
        
        
    def compute_utility(self, lamp):
        pass
        
                
class Lamps:
    def __init__(self):
        self.lamps = []
        for line in open('lamps.csv').readlines():
            line = line.strip().split(',')
            lamp = dict(
                type = line[0],
                label = line[1],
                lifetime = float(line[2]),
                lifetime_uncertainty = float(line[3]),
                output = float(line[4]),
                power = float(line[5]),
                cri = float(line[6]),
                color_temp = float(line[7]),
                shape = line[8],
                socket = line[9],
                price = float(line[10]),
                year = int(line[11]),
                )
            self.lamps.append(lamp)    
    def pick(self, type, socket, shape):
        lamp_list = list(self.lamps)
        random.shuffle(lamp_list)
        for lamp in lamp_list:
            if lamp['shape']==shape and lamp['socket']==socket and lamp['type']==type:
                return lamp
        return None        
                
        
lamps = Lamps()
    
people = People(pop_size)            