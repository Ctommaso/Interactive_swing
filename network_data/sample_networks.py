# Some sample networks, that can be used for tests

buses1 = [(0, {'name':"Load 0", 'coord': [0.00, 0.00], 'sm': False, 'power':-0.5, 'damping':0.5}),
          (1, {'name': "Gen 1", 'coord': [0.10, 0.10], 'sm': True,  'power': 1.0, 'inertia':1, 'damping':0.5}),
          (2, {'name': "Gen 2", 'coord': [0.15, 0.00], 'sm': True,  'power':-0.5, 'inertia':1, 'damping':0.5}),
          (3, {'name':"Load 3", 'coord': [0.10, -0.1], 'sm': False, 'power':-1.0, 'damping':1}),
          (4, {'name':"Load 4", 'coord': [0.20, -0.1], 'sm': False, 'power': 1.0, 'damping':0.75}),
          (5, {'name':"Load 5", 'coord': [0.10, 0.30], 'sm': False, 'power':-2.0, 'damping':1}),
          (6, {'name': "Gen 6", 'coord': [0.30, 0.00], 'sm': True,  'power': 1.0, 'inertia':0.6, 'damping':0.75}),
          (7, {'name':"Load 7", 'coord': [-0.05,0.07], 'sm': False, 'power':-0.5, 'damping':1}),
          (8, {'name':"Load 8", 'coord': [0.00, 0.20], 'sm': False, 'power':-0.5, 'damping':0.75}),
          (9, {'name': "Gen 9", 'coord': [0.00, 0.30], 'sm': True,  'power': 2.5, 'inertia':0.7, 'damping':0.5}),
          (10,{'name':"Load 10",'coord': [0.00, 0.35], 'sm': False, 'power':-0.5, 'damping':0.6})]
	         

# Same as buses but all nodes are synchrnous machines
buses2 = [(0, {'name': "SM 0", 'coord': [0.00, 0.00], 'sm': True, 'power':-0.5, 'inertia':1.0, 'damping':0.5}),
          (1, {'name': "SM 1", 'coord': [0.10, 0.10], 'sm': True, 'power': 1.0, 'inertia':0.8, 'damping':0.5}),
          (2, {'name': "SM 2", 'coord': [0.15, 0.00], 'sm': True, 'power':-0.5, 'inertia':1.0, 'damping':0.5}),
          (3, {'name': "SM 3", 'coord': [0.10, -0.1], 'sm': True, 'power':-1.0, 'inertia':0.5, 'damping':1}),
          (4, {'name': "SM 4", 'coord': [0.20, -0.1], 'sm': True, 'power': 1.0, 'inertia':1.0, 'damping':0.75}),
          (5, {'name': "SM 5", 'coord': [0.10, 0.30], 'sm': True, 'power':-2.0, 'inertia':1.0, 'damping':1}),
          (6, {'name': "SM 6", 'coord': [0.30, 0.00], 'sm': True, 'power': 1.0, 'inertia':0.6, 'damping':0.75}),
          (7, {'name': "SM 7", 'coord': [-0.05,0.07], 'sm': True, 'power':-0.5, 'inertia':1.0, 'damping':1}),
          (8, {'name': "SM 8", 'coord': [0.00, 0.20], 'sm': True, 'power':-0.5, 'inertia':1.0, 'damping':0.75}),
          (9, {'name': "SM 9", 'coord': [0.00, 0.30], 'sm': True, 'power': 2.5, 'inertia':0.7, 'damping':0.5}),
          (10,{'name': "SM 10",'coord': [0.00, 0.35], 'sm': True, 'power':-0.5, 'inertia':1.0, 'damping':0.6})]
         

# works also with buses2
lines1 =[(0,1,{'susceptance':2.0, 'status':True}),(0,2,{'susceptance':1.0, 'status':True}),(0,3,{'susceptance':7.0, 'status':True}),
         (1,2,{'susceptance':3.0, 'status':True}),(2,3,{'susceptance':4.0, 'status':True}),(3,4,{'susceptance':3.0, 'status':True}),
         (1,5,{'susceptance':3.5, 'status':True}),(2,6,{'susceptance':4.0, 'status':True}),(5,6,{'susceptance':2.0,'status':True}),
         (0,7,{'susceptance':4.3, 'status':True}),(7,8,{'susceptance':3.0, 'status':True}),(1,8,{'susceptance':2.0, 'status':True}),
         (8,9,{'susceptance':4.0, 'status':True}),(9,10,{'susceptance':3.0, 'status':True})]


# Radial network example
buses_r = [(0, {'name': "Gen 0", 'coord': [0.00,  0.00], 'sm': True, 'power': 5.5, 'inertia':1, 'damping':0.5}),
          (1, {'name': "Gen 1", 'coord': [-0.30, 0.00], 'sm': True, 'power': 0.5, 'inertia':1, 'damping':0.5}),
          (2, {'name':"Load 2", 'coord': [-0.10, 0.00], 'sm': False,'power':-2.0, 'damping':0.5}),
          (3, {'name':"Load 3", 'coord': [-0.20, 0.00], 'sm': False,'power':-1.0, 'damping':1}),
          (4, {'name':"Load 4", 'coord': [0.10, -0.10], 'sm': False,'power':-1.0, 'damping':0.75}),
          (5, {'name':"Load 5", 'coord': [0.10, 0.10], 'sm': False, 'power':-1.5, 'damping':1}),
          (6, {'name':"Load 6", 'coord': [0.20, 0.20], 'sm': False, 'power':-0.5, 'damping':0.75})]

lines_r =[(0,2,{'susceptance':3.0, 'status':True}),(0,4,{'susceptance':3.0, 'status':True}),(0,5,{'susceptance':3.0, 'status':True}),
          (3,2,{'susceptance':3.0, 'status':True}),(1,3,{'susceptance':3.0, 'status':True}),(5,6,{'susceptance':3.0, 'status':True})]


# Simple four node Complete graph
buses_c = [(0, {'name':"Gen 0",  'coord': [-0.10, 0.00], 'sm': True, 'power': 1.0,'inertia':1, 'damping':0.5}),
          (1, {'name': "Gen 1",  'coord': [ 0.10, 0.00], 'sm': True, 'power': 0.5, 'inertia':1, 'damping':0.5}),
          (2, {'name': "Load 2", 'coord': [-0.20, 0.10], 'sm': True, 'power':-1.2, 'inertia':1, 'damping':0.5}),
          (3, {'name': "Load 3", 'coord': [ 0.20, 0.10], 'sm': True, 'power':-0.3, 'inertia':1, 'damping':0.5}),
          (4, {'name': "Load 4", 'coord': [-0.10, 0.20], 'sm': True, 'power':-0.5, 'inertia':1, 'damping':0.5}),
          (5, {'name': "Gen 5",  'coord': [ 0.10, 0.20], 'sm': True, 'power': 0.5, 'inertia':1, 'damping':0.5})]

lines_c =[(0,1,{'susceptance':1.0, 'status':True}),(0,2,{'susceptance':1.0, 'status':True}),(0,3,{'susceptance':1.0, 'status':True}),
          (0,4,{'susceptance':1.0, 'status':True}),(0,5,{'susceptance':1.0, 'status':True}),(1,2,{'susceptance':1.0, 'status':True}),
          (1,3,{'susceptance':1.0, 'status':True}),(1,4,{'susceptance':1.0, 'status':True}),(1,5,{'susceptance':1.0, 'status':True}),
          (2,3,{'susceptance':1.0, 'status':True}),(2,4,{'susceptance':1.0, 'status':True}),(2,5,{'susceptance':1.0, 'status':True}),
          (3,4,{'susceptance':1.0, 'status':True}),(3,5,{'susceptance':1.0, 'status':True}),(4,5,{'susceptance':1.0, 'status':True})]


# Devil network 
buses_d = [(0, {'name':"Load 0",  'coord': [-0.10, 0.00], 'sm': True, 'power': -1.25,'inertia':1,  'damping':0.5}),
           (1, {'name': "Gen 1",  'coord': [ 0.00, 0.20], 'sm': True, 'power':  2.50, 'inertia':1, 'damping':0.5}),
           (2, {'name': "Load 2", 'coord': [ 0.10, 0.00], 'sm': True, 'power': -1.25, 'inertia':1, 'damping':0.5})]
          

lines_d =[(0,1,{'susceptance':3.0, 'status':True}),(1,2,{'susceptance':3.0, 'status':True})]
          

















