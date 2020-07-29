
from direct.showbase.ShowBase import ShowBase
import simplepbr
from panda3d.core import DirectionalLight, AmbientLight

ShowBase()

pipeline = simplepbr.init()




lightSun = DirectionalLight('light_sun')
lightSun.setColorTemperature(5300)
lightSun.setShadowCaster(True, 2048, 2048)
lightSunNP = render.attachNewNode(lightSun)
lightSunNP.setPos(2, 2, 2)
lightSunNP.lookAt(0, 0, 0)
render.setLight(lightSunNP)

lightAmb = AmbientLight('light_ambient')
lightAmb.setColor((0.1, 0.1, 0.1, 1))
lightAmbNP = render.attachNewNode(lightAmb)
render.setLight(lightAmbNP)

model = base.loader.loadModel("./warrior.bam")
#model.setPos(0, 3, -0.5)
model.setScale(50)
model.reparentTo(render)

run()
