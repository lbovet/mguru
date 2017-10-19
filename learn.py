from vowpalwabbit import pyvw
vw = pyvw.vw(quiet=True)
ex = vw.example('1 | a:1 b:1 c:1')
vw.learn(ex)
ex = vw.example('2 | a:2 b:2 c:2')
vw.learn(ex)
ex = vw.example('2 | a:3 b:2 c:3')
vw.learn(ex)
ex = vw.example('3 | a:2 b:3 c:3')
vw.learn(ex)
t = vw.example('a:2 b:3 c:3')
print vw.predict(ex)