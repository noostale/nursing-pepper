from interaction_manager import InteractionManager


im = InteractionManager(None, None)
im.logenable(True)

im.setProfile(['*', '*', 'es', '*'])
im.setDemoPath('../../demo/sample/')
im.init()
im.execute('welcome')
im.execute('animal')

#print im.listConditions('animal')

#im.setPath('../../demo/facultywelcomedaynew/')
#im.execute('welcome')
